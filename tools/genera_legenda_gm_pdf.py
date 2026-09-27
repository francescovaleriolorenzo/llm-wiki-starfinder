#!/usr/bin/env python3
"""Genera il PDF della FAQ per il GM da wiki/regole/domande-frequenti-gm.md,
con la stessa impaginazione delle schede PG (vedi tools/pdf_common.py).

Uso: python3 tools/genera_legenda_gm_pdf.py
Richiede: pacchetto Python 'markdown' (pip3 install markdown), Google Chrome.
"""
from pathlib import Path

import markdown

from pdf_common import BASE_CSS, ROOT, load_body, render_pdf, rewrite_image_paths

SRC = ROOT / "wiki" / "regole" / "domande-frequenti-gm.md"
OUT_DIR = ROOT / "export"
SCRATCH = Path("/private/tmp/claude-501/-Users-francescovaleriolorenzo-Vaults-LLM-Wiki-LLM-Wiki/75dde73c-b7aa-45bb-b10b-571af94f94d1/scratchpad/schede-html")

OUT_DIR.mkdir(parents=True, exist_ok=True)
SCRATCH.mkdir(parents=True, exist_ok=True)

EXTRA_CSS = """
h1 { clip-path: polygon(0 0, 100% 0, 98% 100%, 0% 100%); }
"""


def build_html() -> Path:
    body_md = load_body(SRC)
    body_html = markdown.markdown(body_md, extensions=["tables", "sane_lists"])
    body_html = rewrite_image_paths(body_html, SRC.parent)
    body_html = body_html.replace("<h1>", '<h1 data-subtitle="GUIDA RAPIDA AL TAVOLO">', 1)

    full_html = f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<title>Domande Frequenti per il GM</title>
<style>{BASE_CSS}{EXTRA_CSS}</style>
</head>
<body>
<div class="sheet">
{body_html}
</div>
</body>
</html>"""
    out_path = SCRATCH / "domande-frequenti-gm.html"
    out_path.write_text(full_html, encoding="utf-8")
    return out_path


def main():
    html_path = build_html()
    pdf_path = OUT_DIR / "domande-frequenti-gm.pdf"
    render_pdf(html_path, pdf_path)
    print(f"domande-frequenti-gm: {pdf_path} ({pdf_path.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
