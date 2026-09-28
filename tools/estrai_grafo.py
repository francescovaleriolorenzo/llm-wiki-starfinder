#!/usr/bin/env python3
"""Estrae un grafo temporale Neo4j dal wiki di campagna, in modo deterministico
(nessun LLM): legge frontmatter YAML + wikilink nel corpo + sezioni ## Storico
delle pagine in wiki/pg, wiki/png, wiki/nemici, wiki/oggetti, wiki/navi,
wiki/quest, wiki/luoghi, wiki/fazioni — secondo lo schema in schema-grafo.md.

Il markdown resta l'unica fonte di verità: lo script svuota il grafo esistente
e lo ricostruisce da zero a ogni esecuzione, rigiocando in ordine ogni riga di
## Storico a partire dallo stato "di creazione" (sessione 0). Rieseguibile in
sicurezza in qualunque momento.

Uso: python3 tools/estrai_grafo.py
Richiede: pacchetti Python 'neo4j', 'python-dotenv', 'pyyaml' (pip3 install ...).
Legge le credenziali di connessione da .env nella radice del repo.
"""
import os
import re
from pathlib import Path

import yaml
from dotenv import load_dotenv
from neo4j import GraphDatabase

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"

CATEGORIE = {
    "pg": "PG",
    "png": "PNG",
    "nemici": "Nemico",
    "oggetti": "Oggetto",
    "navi": "Nave",
    "quest": "Quest",
    "luoghi": "Luogo",
    "fazioni": "Fazione",
}

TIPO_ATTESO = {
    "pg": "pg",
    "png": "png",
    "nemici": "nemico",
    "oggetti": "oggetto",
    "navi": "nave",
    "quest": "quest",
    "luoghi": "luogo",
    "fazioni": "fazione",
}

CAMPI_STATO = {"PG", "PNG", "Nemico", "Nave", "Quest"}

PROPRIETA_SCALARI = {
    "PG": ("razza", "classe", "livello", "giocatore"),
    "PNG": ("ruolo",),
    "Nemico": ("categoria", "cr"),
    "Oggetto": ("categoria", "rarita"),
    "Nave": ("classe",),
    "Quest": ("categoria", "ricompense"),
    "Luogo": ("categoria",),
    "Fazione": ("categoria",),
}

CAMPI_RELAZIONALI_SEMPLICI = {
    "fazione": "APPARTIENE_A",
    "luogo": "SI_TROVA_IN",
    "luogo_attuale": "SI_TROVA_IN",
    "luogo_associato": "SI_TROVA_IN",
    "luogo_padre": "PARTE_DI",
    "fazione_controllante": "CONTROLLATO_DA",
}

RAPPORTO_PARTY = {
    "alleata": "ALLEATO_DI",
    "alleato": "ALLEATO_DI",
    "ostile": "OSTILE_A",
    "ambigua": "AMBIGUO_CON",
    "neutrale": None,
}

PAROLE_CHIAVE_RELAZIONE_PARTY = [
    ("mandante", "MANDANTE_DI"),
    ("alleat", "ALLEATO_DI"),
    ("ostile", "OSTILE_A"),
    ("rivale", "RIVALE_DI"),
]

TIPI_RELAZIONE_PARTY = ["MANDANTE_DI", "ALLEATO_DI", "OSTILE_A", "RIVALE_DI", "AMBIGUO_CON", "CONNESSO_A"]

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
SESSIONE_RE = re.compile(r"sessione-(\d+)", re.IGNORECASE)
STORICO_RIGA_RE = re.compile(r"^- Sessione (\d+):\s*(.+)$")
STORICO_CAMPO_RE = re.compile(r'^(\w+)\s+cambiat[ao]\s+da\s+"([^"]*)"\s+a\s+"([^"]*)"')


def normalizza_target(testo_interno):
    testo_interno = testo_interno.replace("\\|", "|")
    target = testo_interno.split("|")[0].split("#")[0].strip()
    if not target or target == "...":
        return None
    return target.split("/")[-1]


def slug_da_wikilink(valore_frontmatter):
    if not isinstance(valore_frontmatter, str):
        return None
    match = WIKILINK_RE.search(valore_frontmatter)
    if not match:
        return None
    return normalizza_target(match.group(1))


def pulisci_testo(valore):
    if not isinstance(valore, str):
        return valore
    match = WIKILINK_RE.search(valore)
    if not match:
        return valore
    contenuto = match.group(1).replace("\\|", "|")
    parti = contenuto.split("|")
    alias = parti[1] if len(parti) > 1 else parti[0]
    return alias.split("#")[0].strip()


def parola_chiave_relazione_party(testo):
    testo_minuscolo = testo.lower()
    trovate = [
        (testo_minuscolo.find(parola), tipo)
        for parola, tipo in PAROLE_CHIAVE_RELAZIONE_PARTY
        if parola in testo_minuscolo
    ]
    if not trovate:
        return None
    return min(trovate, key=lambda coppia: coppia[0])[1]


def tipo_da_rapporto_col_party(testo):
    testo_minuscolo = testo.strip().lower()
    for valore, tipo in RAPPORTO_PARTY.items():
        if testo_minuscolo.startswith(valore):
            return tipo
    return None


def sessione_da_stato_da(valore):
    if not valore or valore == "creazione":
        return 0
    match = SESSIONE_RE.search(valore)
    if match:
        return int(match.group(1))
    print(f"  ATTENZIONE: stato_da non riconosciuto ({valore!r}), uso 0")
    return 0


def leggi_pagina(path):
    testo = path.read_text(encoding="utf-8")
    if not testo.startswith("---"):
        return {}, testo
    fine = testo.index("\n---", 3)
    frontmatter = yaml.safe_load(testo[3:fine]) or {}
    corpo = testo[fine + 4:]
    return frontmatter, corpo


def estrai_storico(corpo):
    righe = []
    dentro = False
    for linea in corpo.splitlines():
        if linea.strip() == "## Storico":
            dentro = True
            continue
        if dentro:
            if linea.startswith("## "):
                break
            match = STORICO_RIGA_RE.match(linea.strip())
            if match:
                righe.append((int(match.group(1)), match.group(2)))
    return sorted(righe, key=lambda coppia: coppia[0])


def scopri_entita(wiki_dir=WIKI):
    entita = {}
    for cartella, label in CATEGORIE.items():
        for path in sorted((wiki_dir / cartella).glob("*.md")):
            frontmatter, corpo = leggi_pagina(path)
            if frontmatter.get("tipo") != TIPO_ATTESO[cartella]:
                print(f"  SALTATA (non è una pagina entità, manca 'tipo: {TIPO_ATTESO[cartella]}'): "
                      f"{path.relative_to(ROOT)}")
                continue
            slug = path.stem
            entita[slug] = {
                "label": label,
                "path": path.relative_to(ROOT).as_posix(),
                "frontmatter": frontmatter,
                "corpo": corpo,
            }
    return entita


def svuota_grafo(tx):
    tx.run("MATCH (n) DETACH DELETE n")


def crea_vincoli(tx):
    for label in list(CATEGORIE.values()) + ["Party"]:
        campo = "nome" if label == "Party" else "slug"
        tx.run(f"CREATE CONSTRAINT IF NOT EXISTS FOR (n:{label}) REQUIRE n.{campo} IS UNIQUE")


def crea_party(tx):
    tx.run("MERGE (p:Party {nome: 'Party'}) SET p.slug = 'party'")


def crea_nodo(tx, slug, info):
    fm = info["frontmatter"]
    label = info["label"]
    proprieta = {
        "slug": slug,
        "nome": fm.get("nome") or slug,
        "pagina_origine": info["path"],
    }
    for campo in PROPRIETA_SCALARI.get(label, ()):
        valore = fm.get(campo)
        if valore not in (None, ""):
            proprieta[campo] = pulisci_testo(valore)
    if label in CAMPI_STATO:
        proprieta["stato"] = fm.get("stato")
        proprieta["stato_da"] = fm.get("stato_da") or "creazione"
    tx.run(f"MERGE (n:{label} {{slug: $slug}}) SET n += $proprieta", slug=slug, proprieta=proprieta)


def crea_arco(tx, source_slug, source_label, tipo, target_slug, target_label,
              valido_da, fonte, pagina, extra=None):
    proprieta = {
        "valido_da_sessione": valido_da,
        "valido_a_sessione": None,
        "fonte": fonte,
        "pagina_origine": pagina,
    }
    if extra:
        proprieta.update(extra)
    query = (
        f"MATCH (a:{source_label} {{slug: $source_slug}}), (b:{target_label} {{slug: $target_slug}}) "
        f"MERGE (a)-[r:{tipo}]->(b) SET r += $proprieta"
    )
    tx.run(query, source_slug=source_slug, target_slug=target_slug, proprieta=proprieta)


def primo_cambio_per_campo(storico):
    """{campo: (sessione_del_cambio, valore_prima_del_cambio)} per il PRIMO cambio di ogni campo.

    Necessario perché il frontmatter contiene sempre il valore *corrente*: se un campo è
    già stato cambiato da una sessione, il frontmatter non rappresenta più il valore "di
    creazione" e l'arco/stato iniziale va ricostruito dal primo valore_vecchio in ## Storico,
    non dal frontmatter.
    """
    primi = {}
    for numero, testo in storico:
        match = STORICO_CAMPO_RE.match(testo)
        if match and match.group(1) not in primi:
            primi[match.group(1)] = (numero, match.group(2))
    return primi


def crea_relazioni_entita(tx, slug, info, tutte_entita):
    fm = info["frontmatter"]
    label = info["label"]
    path = info["path"]
    collegati = set()
    sessione_iniziale = sessione_da_stato_da(fm.get("stato_da")) if label in CAMPI_STATO else 0

    storico = estrai_storico(info["corpo"])
    primi_cambi = primo_cambio_per_campo(storico)

    if label in CAMPI_STATO and fm.get("stato"):
        if "stato" in primi_cambi:
            n_cambio, valore_iniziale = primi_cambi["stato"]
            tx.run(
                "MATCH (n {slug: $slug}) MERGE (n)-[r:HA_STATO {valido_da_sessione: $vds}]->(n) "
                "SET r.valore = $valore, r.valido_a_sessione = $fine, "
                "r.fonte = 'storico', r.pagina_origine = $pagina",
                slug=slug, vds=sessione_iniziale, valore=valore_iniziale, fine=n_cambio, pagina=path,
            )
        else:
            tx.run(
                "MATCH (n {slug: $slug}) MERGE (n)-[r:HA_STATO {valido_da_sessione: $vds}]->(n) "
                "SET r.valore = $valore, r.valido_a_sessione = null, "
                "r.fonte = 'frontmatter:stato', r.pagina_origine = $pagina",
                slug=slug, vds=sessione_iniziale, valore=fm.get("stato"), pagina=path,
            )

    if label == "Nemico":
        crea_arco(tx, slug, label, "NEMICO_DI", "party", "Party",
                   0, "implicito:categoria-nemico", path)
        collegati.add("party")

    for campo, tipo in CAMPI_RELAZIONALI_SEMPLICI.items():
        if campo in primi_cambi:
            print(f"  NOTA: {campo!r} di {slug!r} ha uno storico ma il target non viene "
                  f"ricostruito retroattivamente in v1 (limite noto) — verrà comunque "
                  f"aggiornato correttamente dalla sessione del cambio in poi.")
        target_slug = slug_da_wikilink(fm.get(campo))
        if not target_slug or target_slug not in tutte_entita:
            continue
        crea_arco(tx, slug, label, tipo, target_slug, tutte_entita[target_slug]["label"],
                   sessione_iniziale, f"frontmatter:{campo}", path)
        collegati.add(target_slug)

    for valore in fm.get("fazioni") or []:
        target_slug = slug_da_wikilink(valore)
        if not target_slug or target_slug not in tutte_entita:
            continue
        crea_arco(tx, slug, label, "APPARTIENE_A", target_slug, tutte_entita[target_slug]["label"],
                   sessione_iniziale, "frontmatter:fazioni", path)
        collegati.add(target_slug)

    valore_proprietario = fm.get("proprietario")
    if isinstance(valore_proprietario, str) and valore_proprietario.strip().lower() != "nessuno":
        target_slug = slug_da_wikilink(valore_proprietario)
        if target_slug and target_slug in tutte_entita:
            crea_arco(tx, target_slug, tutte_entita[target_slug]["label"], "POSSIEDE",
                       slug, label, sessione_iniziale, "frontmatter:proprietario", path)
            collegati.add(target_slug)

    if "rapporto_col_party" in primi_cambi:
        n_cambio, valore_iniziale = primi_cambi["rapporto_col_party"]
        tipo = tipo_da_rapporto_col_party(valore_iniziale)
        if tipo:
            crea_arco(tx, slug, label, tipo, "party", "Party", sessione_iniziale,
                       "storico", path, extra={"valido_a_sessione": n_cambio})
        collegati.add("party")
    else:
        valore_rapporto = fm.get("rapporto_col_party")
        if isinstance(valore_rapporto, str):
            tipo = tipo_da_rapporto_col_party(valore_rapporto)
            if tipo:
                crea_arco(tx, slug, label, tipo, "party", "Party",
                           sessione_iniziale, "frontmatter:rapporto_col_party", path)
                collegati.add("party")

    if "relazione_con_party" in primi_cambi:
        n_cambio, valore_iniziale = primi_cambi["relazione_con_party"]
        tipo = parola_chiave_relazione_party(valore_iniziale) or "CONNESSO_A"
        extra = {"valido_a_sessione": n_cambio}
        if tipo == "CONNESSO_A":
            extra["descrizione"] = valore_iniziale
        crea_arco(tx, slug, label, tipo, "party", "Party", sessione_iniziale, "storico", path, extra=extra)
        collegati.add("party")
    else:
        valore_relazione = fm.get("relazione_con_party")
        if isinstance(valore_relazione, str) and valore_relazione.strip():
            tipo = parola_chiave_relazione_party(valore_relazione)
            if tipo:
                crea_arco(tx, slug, label, tipo, "party", "Party",
                           sessione_iniziale, "frontmatter:relazione_con_party", path)
            else:
                crea_arco(tx, slug, label, "CONNESSO_A", "party", "Party",
                           sessione_iniziale, "frontmatter:relazione_con_party", path,
                           extra={"descrizione": valore_relazione})
                print(f"  NOTA: relazione_con_party di {slug!r} senza parola chiave riconosciuta: {valore_relazione!r}")
            collegati.add("party")

    for testo_interno in WIKILINK_RE.findall(info["corpo"]):
        target_slug = normalizza_target(testo_interno)
        if not target_slug or target_slug == slug or target_slug not in tutte_entita:
            continue
        if target_slug in collegati:
            continue
        crea_arco(tx, slug, label, "CONNESSO_A", target_slug, tutte_entita[target_slug]["label"],
                   sessione_iniziale, "wikilink-corpo", path)
        collegati.add(target_slug)

    for numero_sessione, testo in storico:
        applica_storico(tx, slug, label, numero_sessione, testo, path, tutte_entita)


def applica_storico(tx, slug, label, numero_sessione, testo, pagina, tutte_entita):
    match = STORICO_CAMPO_RE.match(testo)
    if not match:
        print(f"  NOTA: riga di Storico non strutturata per {slug!r} (sessione {numero_sessione}): {testo!r}")
        return
    campo, _valore_vecchio, valore_nuovo = match.groups()

    if campo == "stato":
        tx.run(
            "MATCH (n {slug: $slug})-[r:HA_STATO]->(n) WHERE r.valido_a_sessione IS NULL "
            "SET r.valido_a_sessione = $n",
            slug=slug, n=numero_sessione,
        )
        tx.run(
            "MATCH (n {slug: $slug}) "
            "MERGE (n)-[r:HA_STATO {valido_da_sessione: $n}]->(n) "
            "SET r.valore = $valore, r.valido_a_sessione = null, "
            "r.fonte = 'storico', r.pagina_origine = $pagina",
            slug=slug, n=numero_sessione, valore=valore_nuovo, pagina=pagina,
        )
        return

    if campo in ("relazione_con_party", "rapporto_col_party"):
        if campo == "rapporto_col_party":
            tipo_nuovo = tipo_da_rapporto_col_party(valore_nuovo)
        else:
            tipo_nuovo = parola_chiave_relazione_party(valore_nuovo)
        tipo_nuovo = tipo_nuovo or "CONNESSO_A"
        for tipo in TIPI_RELAZIONE_PARTY:
            tx.run(
                f"MATCH (n {{slug: $slug}})-[r:{tipo}]->(:Party) WHERE r.valido_a_sessione IS NULL "
                f"SET r.valido_a_sessione = $n",
                slug=slug, n=numero_sessione,
            )
        crea_arco(tx, slug, label, tipo_nuovo, "party", "Party", numero_sessione, "storico", pagina)
        return

    tipo = CAMPI_RELAZIONALI_SEMPLICI.get(campo)
    target_slug = next(
        (s for s, i in tutte_entita.items() if i["frontmatter"].get("nome") == valore_nuovo), None
    )
    if not tipo or not target_slug:
        print(f"  NOTA: impossibile risolvere il target per {slug!r} campo {campo!r} -> "
              f"{valore_nuovo!r} (sessione {numero_sessione})")
        return
    tx.run(
        f"MATCH (n {{slug: $slug}})-[r:{tipo}]->() WHERE r.valido_a_sessione IS NULL "
        f"SET r.valido_a_sessione = $n",
        slug=slug, n=numero_sessione,
    )
    crea_arco(tx, slug, label, tipo, target_slug, tutte_entita[target_slug]["label"],
               numero_sessione, "storico", pagina)


def stampa_riepilogo(session):
    print("\n--- Riepilogo ---")
    risultato = session.run(
        "MATCH (n) RETURN labels(n)[0] AS label, count(*) AS totale ORDER BY label"
    )
    for record in risultato:
        print(f"  {record['label']}: {record['totale']} nodi")
    risultato = session.run(
        "MATCH ()-[r]->() RETURN type(r) AS tipo, count(*) AS totale ORDER BY tipo"
    )
    for record in risultato:
        print(f"  {record['tipo']}: {record['totale']} relazioni")


def main():
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--wiki-dir", default=str(WIKI),
        help="Cartella wiki/ da cui estrarre (default: wiki/ reale). Usare per puntare a una copia di test.",
    )
    parser.add_argument(
        "--database", default=None,
        help="Nome del database Neo4j di destinazione (default: quello di sistema, es. 'neo4j').",
    )
    args = parser.parse_args()

    load_dotenv(ROOT / ".env")
    driver = GraphDatabase.driver(
        os.environ["NEO4J_URI"],
        auth=(os.environ["NEO4J_USER"], os.environ["NEO4J_PASSWORD"]),
    )
    wiki_dir = Path(args.wiki_dir).resolve()
    entita = scopri_entita(wiki_dir)
    print(f"Trovate {len(entita)} entità in {wiki_dir}/{{{','.join(CATEGORIE)}}}/.")

    with driver.session(database=args.database) as session:
        session.execute_write(svuota_grafo)
        session.execute_write(crea_vincoli)
        session.execute_write(crea_party)

        for slug, info in entita.items():
            session.execute_write(crea_nodo, slug, info)

        for slug, info in entita.items():
            session.execute_write(crea_relazioni_entita, slug, info, entita)

        stampa_riepilogo(session)

    driver.close()
    print("\nEstrazione completata.")


if __name__ == "__main__":
    main()
