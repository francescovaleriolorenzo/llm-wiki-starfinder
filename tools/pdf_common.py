"""Utilità condivise per generare PDF dal wiki con impaginazione ispirata alla
scheda personaggio ufficiale di Starfinder (banner scuri, accento arancione).
Usato da genera_schede_pdf.py e genera_legenda_gm_pdf.py.
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

BASE_CSS = """
@page { size: A4; margin: 14mm 12mm; }
:root {
  --navy: #0d1f33;
  --navy2: #17324f;
  --accent: #e8742c;
  --accent2: #2f7fa8;
  --paper: #fdfdfb;
}
* { box-sizing: border-box; }
body {
  font-family: 'Helvetica Neue', Arial, sans-serif;
  color: #1a1a1a;
  background: var(--paper);
  margin: 0;
  font-size: 10.3pt;
  line-height: 1.35;
}
.sheet { padding: 0; }
h1 {
  background: linear-gradient(90deg, var(--navy) 0%, var(--navy2) 85%, transparent 100%);
  color: #fff;
  font-size: 20pt;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  padding: 10px 22px 8px 22px;
  margin: 0 0 14px 0;
  clip-path: polygon(0 0, 100% 0, 96% 100%, 0% 100%);
  font-weight: 800;
  line-height: 1.15;
}
h1::after {
  content: attr(data-subtitle);
  display: block;
  text-align: right;
  font-size: 8.5pt;
  font-weight: 400;
  letter-spacing: 2px;
  opacity: 0.75;
  margin-top: 4px;
}
h2 {
  background: var(--navy2);
  color: #fff;
  font-size: 10.5pt;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 4px 12px;
  margin: 11px 0 6px 0;
  clip-path: polygon(0 0, 100% 0, 98% 100%, 0% 100%);
  border-left: 4px solid var(--accent);
  page-break-after: avoid;
}
h2:first-of-type { margin-top: 0; }
p { margin: 3px 0 6px 0; }
img.portrait {
  float: right;
  width: 140px;
  border: 3px solid var(--navy2);
  margin: 0 0 8px 12px;
  border-radius: 3px;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin: 3px 0 8px 0;
  font-size: 9pt;
  page-break-inside: avoid;
}
th {
  background: var(--navy);
  color: #fff;
  padding: 3px 6px;
  text-align: left;
  font-weight: 600;
  border: 1px solid var(--navy);
}
td {
  padding: 2.5px 6px;
  border: 1px solid #cfd6dc;
  vertical-align: top;
}
tr:nth-child(even) td { background: #eef2f5; }
strong { color: var(--navy); }
em { color: #555; }
hr { border: none; border-top: 1px solid #ccc; margin: 8px 0; }
ul, ol { margin: 3px 0 7px 20px; padding: 0; }
li { margin-bottom: 1.5px; }
a { color: var(--accent2); text-decoration: none; }
.legend-page { page-break-before: always; }
.legend-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0 22px;
}
.legend-grid table { font-size: 8.8pt; }
.footer-note {
  margin-top: 16px;
  font-size: 8pt;
  color: #888;
  border-top: 1px solid #ddd;
  padding-top: 6px;
}
.row2 {
  display: flex;
  gap: 0 18px;
  align-items: flex-start;
  page-break-inside: avoid;
}
.row2 > .col2 {
  flex: 1 1 0;
  min-width: 0;
}
.row2 > .col2 table { font-size: 8.7pt; }
"""

WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")


def strip_wikilinks(text: str) -> str:
    return WIKILINK_RE.sub(lambda m: m.group(2) or m.group(1).split("/")[-1], text)


def load_body(md_path: Path) -> str:
    text = md_path.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        text = parts[2] if len(parts) >= 3 else text
    return strip_wikilinks(text)


def rewrite_image_paths(html: str, md_dir: Path) -> str:
    def repl(m):
        src = m.group(1)
        if src.startswith("http"):
            return m.group(0)
        abs_path = (md_dir / src).resolve()
        return m.group(0).replace(src, abs_path.as_uri())

    return re.sub(r'src="([^"]+)"', repl, html)


# Coppie di sezioni (per titolo H2) da affiancare in colonne quando entrambe
# sono presenti nel documento, per ottimizzare lo spazio verticale.
PAIR_RULES = [
    ("Iniziativa", "Salute e Risolutezza"),
    ("Classe Armatura", "Tiri Salvezza"),
    ("Bonus di Attacco", "Lingue"),
    ("Talenti e Competenze", "Equipaggiamento"),
]

# Sezioni la cui tabella, se lunga, va spezzata in due colonne affiancate
# (stessa intestazione ripetuta su entrambe le metà).
SPLIT_TABLE_SECTIONS = {"Abilità"}
SPLIT_TABLE_MIN_ROWS = 10

H2_RE = re.compile(r"<h2[^>]*>.*?</h2>", re.S)
TAG_RE = re.compile(r"<[^<]+?>")
TABLE_RE = re.compile(r"<table>(.*?)</table>", re.S)
TR_RE = re.compile(r"<tr>.*?</tr>", re.S)


def split_sections(body_html: str):
    """Divide l'HTML del corpo pagina in blocchi (titolo, html) per ogni H2.
    Il contenuto prima del primo H2 (immagine + tabelle d'intestazione) è
    restituito come blocco con titolo None."""
    tags = H2_RE.findall(body_html)
    texts = H2_RE.split(body_html)
    sections = []
    if texts[0].strip():
        sections.append((None, texts[0]))
    for tag, content in zip(tags, texts[1:]):
        title = TAG_RE.sub("", tag).strip()
        sections.append((title, tag + content))
    return sections


def split_table_two_cols(section_html: str) -> str:
    """Spezza l'unica tabella dati di una sezione in due tabelle affiancate
    (stessa intestazione), se ha abbastanza righe da trarne vantaggio."""
    m = TABLE_RE.search(section_html)
    if not m:
        return section_html
    rows = TR_RE.findall(m.group(1))
    if len(rows) < SPLIT_TABLE_MIN_ROWS + 1:  # +1 per l'intestazione
        return section_html
    header, data_rows = rows[0], rows[1:]
    half = (len(data_rows) + 1) // 2
    left = "<table>" + header + "".join(data_rows[:half]) + "</table>"
    right = "<table>" + header + "".join(data_rows[half:]) + "</table>"
    two_col = f'<div class="row2"><div class="col2">{left}</div><div class="col2">{right}</div></div>'
    return section_html[: m.start()] + two_col + section_html[m.end() :]


def assemble_sections(body_html: str, skip_titles=frozenset()) -> str:
    """Ricompone le sezioni applicando SPLIT_TABLE_SECTIONS e PAIR_RULES per
    un'impaginazione più compatta (tabelle corte affiancate a coppie).
    Le sezioni il cui titolo compare in skip_titles vengono omesse (usato per
    non stampare "Note per il GM" nel PDF, pur restando nel markdown sorgente)."""
    sections = split_sections(body_html)
    by_title = {t: h for t, h in sections if t}
    consumed = set(skip_titles)
    out = []
    for title, html in sections:
        if title in consumed:
            continue
        if title in SPLIT_TABLE_SECTIONS:
            html = split_table_two_cols(html)
        partner_title = None
        for a, b in PAIR_RULES:
            if title == a and b in by_title and b not in consumed:
                partner_title = b
                break
        if partner_title:
            partner_html = by_title[partner_title]
            if partner_title in SPLIT_TABLE_SECTIONS:
                partner_html = split_table_two_cols(partner_html)
            out.append(
                f'<div class="row2"><div class="col2">{html}</div>'
                f'<div class="col2">{partner_html}</div></div>'
            )
            consumed.add(partner_title)
        else:
            out.append(html)
    return "\n".join(out)


def render_pdf(html_path: Path, pdf_path: Path):
    subprocess.run(
        [
            CHROME,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            "--print-to-pdf-no-header",
            f"--print-to-pdf={pdf_path}",
            html_path.as_uri(),
        ],
        check=True,
        capture_output=True,
    )
