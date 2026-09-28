#!/usr/bin/env python3
"""Genera un PDF per ciascuna scheda PG in wiki/pg/, con impaginazione ispirata
alla scheda personaggio ufficiale di Starfinder (banner scuri, tabelle pulite),
seguita da una pagina condivisa di legenda delle abbreviazioni.

Uso: python3 tools/genera_schede_pdf.py
Richiede: pacchetto Python 'markdown' (pip3 install markdown), Google Chrome.
"""
from pathlib import Path

import markdown

from pdf_common import (
    BASE_CSS,
    ROOT,
    assemble_sections,
    load_body,
    render_pdf,
    rewrite_image_paths,
)

PG_DIR = ROOT / "wiki" / "pg"
OUT_DIR = ROOT / "export" / "schede-pg"
SCRATCH = Path("/private/tmp/claude-501/-Users-francescovaleriolorenzo-Vaults-LLM-Wiki-LLM-Wiki/75dde73c-b7aa-45bb-b10b-571af94f94d1/scratchpad/schede-html")

OUT_DIR.mkdir(parents=True, exist_ok=True)
SCRATCH.mkdir(parents=True, exist_ok=True)

CHARACTERS = [
    "vela-9",
    "kesh-vantor",
    "naeva-thess",
    "whix-chitterclaw",
    "callan-reyes",
    "keskodai",
    "jehir-voloteo",
    "vey-ashkora",
]

LEGEND_HTML = """
<div class="legend-page">
<h1 data-subtitle="GUIDA ALLE ABBREVIAZIONI">Legenda</h1>
<p>Glossario delle sigle e abbreviazioni usate in questa scheda e nel resto del wiki di campagna. Per le regole complete vedi <em>wiki/regole/</em> nel vault.</p>

<h2>Punteggi vitali</h2>
<div class="legend-grid">
<table>
<tr><th>Sigla</th><th>Significato</th></tr>
<tr><td><strong>PF</strong></td><td>Punti Ferita — danno reale che puoi incassare restando cosciente. A 0 PF sei privo di sensi e morente.</td></tr>
<tr><td><strong>PS</strong></td><td>Punti Stamina — riserva di energia che assorbe i danni per prima. Si rigenera con un breve riposo.</td></tr>
<tr><td><strong>PR</strong></td><td>Punti Risolutezza — riserva di forza di volontà, si spende per attivare privilegi di classe o stabilizzarsi in punto di morte.</td></tr>
</table>
<table>
<tr><th>Sigla</th><th>Significato</th></tr>
<tr><td><strong>CAE</strong></td><td>Classe Armatura Energia — difesa contro attacchi a energia e la maggior parte degli attacchi a distanza.</td></tr>
<tr><td><strong>CAC</strong></td><td>Classe Armatura Cinetica — difesa contro attacchi fisici/da mischia e manovre di combattimento.</td></tr>
<tr><td><strong>BAB</strong></td><td>Bonus Attacco Base — bonus ai tiri per colpire derivato dal livello di classe, prima dei modificatori.</td></tr>
</table>
</div>

<h2>Tiri e prove</h2>
<div class="legend-grid">
<table>
<tr><th>Sigla</th><th>Significato</th></tr>
<tr><td><strong>TS</strong></td><td>Tiro Salvezza — Tempra (Costituzione), Riflessi (Destrezza) o Volontà (Saggezza), per resistere a un effetto.</td></tr>
<tr><td><strong>CD</strong></td><td>Classe Difficoltà — il numero da eguagliare o superare in un tiro per riuscire in una prova o resistere a un effetto.</td></tr>
</table>
<table>
<tr><th>Sigla</th><th>Significato</th></tr>
<tr><td><strong>GS</strong></td><td>Grado di Sfida — indica quanto è pericoloso un nemico rispetto al livello del party (usato nelle schede dei nemici, non dei PG).</td></tr>
<tr><td><strong>RD</strong></td><td>Riduzione del Danno — sottrae un numero fisso da ogni colpo subito, es. "RD 5/–" ignora i primi 5 punti di ogni danno.</td></tr>
</table>
</div>

<h2>Tipi di danno (nelle tabelle Armi)</h2>
<div class="legend-grid">
<table>
<tr><th>Sigla</th><th>Significato</th></tr>
<tr><td><strong>Fu</strong></td><td>Fuoco</td></tr>
<tr><td><strong>Fr</strong></td><td>Freddo</td></tr>
<tr><td><strong>So</strong></td><td>Sonico</td></tr>
</table>
<table>
<tr><th>Sigla</th><th>Significato</th></tr>
<tr><td><strong>P</strong></td><td>Perforante</td></tr>
<tr><td><strong>T</strong></td><td>Tagliente</td></tr>
<tr><td><strong>C</strong></td><td>Contundente</td></tr>
</table>
</div>

<h2>Altre convenzioni</h2>
<table>
<tr><th>Simbolo/Sigla</th><th>Significato</th></tr>
<tr><td><strong>(Str)</strong></td><td>Capacità <em>Straordinaria</em> — non è magia, funziona sempre, anche in aree dove la magia è soppressa.</td></tr>
<tr><td><strong>(Sop)</strong></td><td>Capacità <em>Soprannaturale</em> — origine magica innata ma non è un incantesimo; non funziona in aree che sopprimono la magia.</td></tr>
<tr><td><strong>(Mag)</strong></td><td>Capacità <em>Magica</em> — funziona come lanciare un incantesimo, può subire dissolvimento e simili.</td></tr>
<tr><td><strong>☑</strong></td><td>Abilità di Classe — se hai gradi in essa, ottieni un bonus fisso di classe (+3) oltre ai gradi.</td></tr>
<tr><td><strong>†</strong></td><td>Solo Addestrate — puoi tentare una prova in questa abilità solo se hai almeno 1 grado.</td></tr>
<tr><td><strong>Modale</strong></td><td>L'arma può cambiare tipo di danno (es. fuoco o sonico) a scelta prima dell'attacco.</td></tr>
<tr><td><strong>Cariche</strong></td><td>La "batteria" di un'arma a energia; ogni colpo ne consuma un certo numero (indicato come "Uso").</td></tr>
<tr><td><strong>Ingombro</strong></td><td>Quanto è ingombrante un oggetto ai fini del limite di carico del personaggio ("L" = ingombro leggero, trascurabile).</td></tr>
</table>

<div class="footer-note">Generato automaticamente da wiki/pg/ — LLM-Wiki di campagna Starfinder. Impaginazione ispirata alla scheda personaggio ufficiale del Core Rulebook, usata solo come riferimento di stile.</div>
</div>
"""


def build_html(slug: str) -> Path:
    md_path = PG_DIR / f"{slug}.md"
    body_md = load_body(md_path)
    body_html = markdown.markdown(body_md, extensions=["tables", "sane_lists"])
    body_html = rewrite_image_paths(body_html, PG_DIR)
    body_html = body_html.replace("<img ", '<img class="portrait" ', 1)
    body_html = body_html.replace("<h1>", '<h1 data-subtitle="SCHEDA PERSONAGGIO">', 1)
    body_html = assemble_sections(body_html, skip_titles={"Note per il GM"})

    full_html = f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<title>Scheda {slug}</title>
<style>{BASE_CSS}</style>
</head>
<body>
<div class="sheet">
{body_html}
</div>
{LEGEND_HTML}
</body>
</html>"""
    out_path = SCRATCH / f"{slug}.html"
    out_path.write_text(full_html, encoding="utf-8")
    return out_path


def main():
    for slug in CHARACTERS:
        html_path = build_html(slug)
        pdf_path = OUT_DIR / f"{slug}-scheda.pdf"
        render_pdf(html_path, pdf_path)
        print(f"{slug}: {pdf_path} ({pdf_path.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
