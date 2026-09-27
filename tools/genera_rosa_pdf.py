#!/usr/bin/env python3
"""Genera il PDF della rosa dei personaggi giocanti da wiki/pg/rosa-personaggi.md,
con la stessa impaginazione delle schede PG (vedi tools/pdf_common.py).

Uso: python3 tools/genera_rosa_pdf.py
Richiede: pacchetto Python 'markdown' (pip3 install markdown), Google Chrome.
"""
import re
from pathlib import Path

import markdown

from pdf_common import BASE_CSS, ROOT, assemble_sections, load_body, render_pdf, rewrite_image_paths

SRC = ROOT / "wiki" / "pg" / "rosa-personaggi.md"
OUT_DIR = ROOT / "export"
SCRATCH = Path("/private/tmp/claude-501/-Users-francescovaleriolorenzo-Vaults-LLM-Wiki-LLM-Wiki/75dde73c-b7aa-45bb-b10b-571af94f94d1/scratchpad/schede-html")

OUT_DIR.mkdir(parents=True, exist_ok=True)
SCRATCH.mkdir(parents=True, exist_ok=True)

EXTRA_CSS = """
img.portrait { width: 110px; }
h2 { page-break-before: always; }
h2:first-of-type { page-break-before: avoid; }
hr { display: none; }
"""


def build_html() -> Path:
    body_md = load_body(SRC)
    body_html = markdown.markdown(body_md, extensions=["tables", "sane_lists"])
    body_html = rewrite_image_paths(body_html, SRC.parent)
    body_html = re.sub(r"<img ", '<img class="portrait" ', body_html)
    body_html = body_html.replace("<h1>", '<h1 data-subtitle="ROSA DEI PERSONAGGI">', 1)
    body_html = assemble_sections(body_html, skip_titles={"Note per il GM"})

    full_html = f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<title>Rosa dei Personaggi</title>
<style>{BASE_CSS}{EXTRA_CSS}</style>
</head>
<body>
<div class="sheet">
{body_html}
</div>
</body>
</html>"""
    out_path = SCRATCH / "rosa-personaggi.html"
    out_path.write_text(full_html, encoding="utf-8")
    return out_path


def main():
    html_path = build_html()
    pdf_path = OUT_DIR / "rosa-personaggi.pdf"
    render_pdf(html_path, pdf_path)
    print(f"rosa-personaggi: {pdf_path} ({pdf_path.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
