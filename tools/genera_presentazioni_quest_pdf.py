#!/usr/bin/env python3
"""Genera un PDF "da presentare ai giocatori" per ciascuna quest in wiki/quest/,
estraendo SOLO la sezione "## Presentazione ai giocatori" di ogni pagina — mai
il resto della quest, che contiene segreti, struttura delle scene e la trama
completa pensati per il GM. Aggiunge anche un piccolo "cast" di ritratti (PG
coinvolti + PNG già noti, dal frontmatter) e, se presenti, un paio di
illustrazioni rappresentative della quest.

La sezione sorgente va scritta apposta per essere spoiler-free e in terza
persona: un aggancio narrativo che incuriosisce, non un riassunto della trama
né un indirizzo diretto al giocatore. Vedi CLAUDE.md, schema di
wiki/quest/*.md, per la convenzione.

Uso: python3 tools/genera_presentazioni_quest_pdf.py
Richiede: pacchetto Python 'markdown' (pip3 install markdown), Google Chrome.
"""
import re
import subprocess
from pathlib import Path

import markdown

from pdf_common import BASE_CSS, ROOT, WIKILINK_RE, load_body, render_pdf, split_sections

QUEST_DIR = ROOT / "wiki" / "quest"
ASSETS_DIR = ROOT / "raw" / "assets"
OUT_DIR = ROOT / "export" / "presentazioni-quest"
SCRATCH = Path("/private/tmp/claude-501/-Users-francescovaleriolorenzo-Vaults-LLM-Wiki-LLM-Wiki/369dfdf9-c795-44f7-bfee-2d3679a90ffb/scratchpad/presentazioni-html")
THUMBS_DIR = SCRATCH / "thumbs"

OUT_DIR.mkdir(parents=True, exist_ok=True)
SCRATCH.mkdir(parents=True, exist_ok=True)
THUMBS_DIR.mkdir(parents=True, exist_ok=True)


def resized_copy(src: Path, max_dim: int) -> Path:
    """Ridimensiona (via 'sips', macOS) una copia cache dell'immagine, per non
    incorporare nel PDF asset a piena risoluzione (1024x1536) mostrati a
    pochi centimetri: gonfierebbe il file da poche centinaia di KB a decine
    di MB senza alcun beneficio visivo."""
    dest = THUMBS_DIR / f"{src.stem}-{max_dim}{src.suffix}"
    if not dest.exists() or dest.stat().st_mtime < src.stat().st_mtime:
        subprocess.run(
            ["sips", "--resampleHeightWidthMax", str(max_dim), str(src), "--out", str(dest)],
            check=True,
            capture_output=True,
        )
    return dest

QUESTS = [
    "il-filo-spezzato",
    "conti-in-sospeso",
]

SECTION_TITLE = "Presentazione ai giocatori"

EXTRA_CSS = """
body { font-size: 11.3pt; line-height: 1.5; }
.sheet { padding: 6px 6px; }
h1 { font-size: 23pt; padding: 14px 26px 10px 26px; margin-bottom: 14px; }
.gallery {
  display: flex;
  gap: 8px;
  margin: 0 0 16px 0;
}
.gallery img {
  width: 50%;
  height: 145px;
  object-fit: cover;
  border-radius: 4px;
  border: 2px solid var(--navy2);
}
.gallery.single img { width: 100%; }
p.tagline {
  font-style: italic;
  color: var(--accent);
  font-size: 13.5pt;
  text-align: center;
  margin: 0 0 16px 0;
}
.pitch p { margin: 0 0 11px 0; }
.logistics {
  margin-top: 16px;
  padding: 10px 18px;
  border-left: 4px solid var(--accent);
  background: #f4f1ec;
  font-size: 10.3pt;
}
.logistics strong { color: var(--navy); }
.cast { margin-top: 18px; }
.cast h3 {
  font-size: 9.2pt;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--navy2);
  border-bottom: 1px solid #ccc;
  padding-bottom: 3px;
  margin: 0 0 8px 0;
}
.cast-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 12px;
}
.cast-item { width: 70px; text-align: center; }
.cast-item img {
  width: 64px;
  height: 64px;
  object-fit: cover;
  border-radius: 50%;
  border: 2px solid var(--navy2);
  display: block;
  margin: 0 auto 3px auto;
}
.cast-item span {
  font-size: 7.5pt;
  color: #333;
  line-height: 1.15;
  display: block;
}
.footer-note {
  margin-top: 16px;
}
"""


def frontmatter_field(md_path: Path, field: str) -> str:
    text = md_path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return ""
    fm_match = re.search(rf"^{field}:\s*(.+)$", m.group(1), re.M)
    return fm_match.group(1).strip() if fm_match else ""


def parse_wikilink_cast(raw_value: str):
    """Estrae (slug, nome_visualizzato) da un campo frontmatter come
    pg_coinvolti/png_noti, es. '["[[pg/vela-9|Vela-9]]", ...]'."""
    entries = []
    for target, alias in WIKILINK_RE.findall(raw_value):
        slug = target.split("/")[-1]
        name = alias or slug
        entries.append((slug, name))
    return entries


def cast_grid_html(slug: str, entries: list) -> str:
    items = []
    for pg_slug, name in entries:
        portrait = ASSETS_DIR / "ritratti" / f"{pg_slug}-ritratto.png"
        if not portrait.exists():
            print(f"  [nota] nessun ritratto per '{pg_slug}' ({portrait}), saltato")
            continue
        thumb = resized_copy(portrait, 240)
        items.append(
            f'<div class="cast-item"><img src="{thumb.as_uri()}"><span>{name}</span></div>'
        )
    return "".join(items)


def build_cast_html(md_path: Path, slug: str) -> str:
    pg_entries = parse_wikilink_cast(frontmatter_field(md_path, "pg_coinvolti"))
    png_entries = parse_wikilink_cast(frontmatter_field(md_path, "png_noti"))

    blocks = []
    pg_html = cast_grid_html(slug, pg_entries)
    if pg_html:
        blocks.append(f'<h3>Il gruppo</h3><div class="cast-grid">{pg_html}</div>')
    png_html = cast_grid_html(slug, png_entries)
    if png_html:
        blocks.append(f'<h3>Un volto già noto</h3><div class="cast-grid">{png_html}</div>')

    if not blocks:
        return ""
    return f'<div class="cast">{"".join(blocks)}</div>'


def build_gallery_html(slug: str) -> str:
    paths = [ASSETS_DIR / "presentazioni-quest" / f"{slug}-presentazione-{i}.png" for i in (1, 2)]
    existing = [p for p in paths if p.exists()]
    if not existing:
        return ""
    css_class = "gallery single" if len(existing) == 1 else "gallery"
    imgs = "".join(f'<img src="{resized_copy(p, 900).as_uri()}">' for p in existing)
    return f'<div class="{css_class}">{imgs}</div>'


def extract_pitch_html(md_path: Path) -> str:
    body_md = load_body(md_path)
    body_html = markdown.markdown(body_md, extensions=["tables", "sane_lists"])
    sections = split_sections(body_html)
    for title, html in sections:
        if title == SECTION_TITLE:
            html = re.sub(r"<h2[^>]*>.*?</h2>", "", html, count=1, flags=re.S)
            html = re.sub(r"<p><em>(.*?)</em></p>", r'<p class="tagline">\1</p>', html, count=1)
            html = re.sub(
                r"<p>(<strong>Cosa aspettarsi:</strong>.*?)</p>",
                r'<div class="logistics">\1</div>',
                html,
                flags=re.S,
            )
            return html
    raise ValueError(
        f"Sezione '## {SECTION_TITLE}' non trovata in {md_path} — "
        "vedi CLAUDE.md per la convenzione, va aggiunta prima di generare il PDF."
    )


def build_html(slug: str) -> Path:
    md_path = QUEST_DIR / f"{slug}.md"
    nome = frontmatter_field(md_path, "nome") or slug
    pitch_html = extract_pitch_html(md_path)
    gallery_html = build_gallery_html(slug)
    cast_html = build_cast_html(md_path, slug)

    full_html = f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<title>{nome}</title>
<style>{BASE_CSS}{EXTRA_CSS}</style>
</head>
<body>
<div class="sheet">
<h1 data-subtitle="PRESENTAZIONE AI GIOCATORI">{nome}</h1>
{gallery_html}
<div class="pitch">
{pitch_html}
</div>
{cast_html}
<div class="footer-note">Presentazione generata da wiki/quest/{slug}.md — LLM-Wiki di campagna Starfinder.</div>
</div>
</body>
</html>"""
    out_path = SCRATCH / f"{slug}.html"
    out_path.write_text(full_html, encoding="utf-8")
    return out_path


def main():
    for slug in QUESTS:
        print(f"{slug}:")
        html_path = build_html(slug)
        pdf_path = OUT_DIR / f"{slug}-presentazione.pdf"
        render_pdf(html_path, pdf_path)
        print(f"  {pdf_path} ({pdf_path.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
