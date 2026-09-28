#!/usr/bin/env python3
"""Interroga il grafo temporale Neo4j estratto dal wiki di campagna (vedi
schema-grafo.md e tools/estrai_grafo.py). Tre modalità:

  stato_a_sessione  stato e relazioni di un'entità valide a una certa sessione
  connessi_a        entità collegate entro N salti (utile per agganci di trama)
  path_tra          cammino più breve tra due entità (nodo per nodo)

Uso:
  python3 tools/interroga_grafo.py stato_a_sessione ilsa-draak 3
  python3 tools/interroga_grafo.py connessi_a kestrel-recovery --salti 2
  python3 tools/interroga_grafo.py path_tra kestrel-recovery solmark-ricerche

Richiede: pacchetti Python 'neo4j', 'python-dotenv' (pip3 install ...).
Legge le credenziali di connessione da .env nella radice del repo.
"""
import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from neo4j import GraphDatabase

ROOT = Path(__file__).resolve().parent.parent


def connetti():
    load_dotenv(ROOT / ".env")
    return GraphDatabase.driver(
        os.environ["NEO4J_URI"],
        auth=(os.environ["NEO4J_USER"], os.environ["NEO4J_PASSWORD"]),
    )


def stato_a_sessione(session, slug, numero):
    righe = list(session.run(
        "MATCH (n {slug: $slug}) RETURN labels(n)[0] AS tipo, n.nome AS nome",
        slug=slug,
    ))
    if not righe:
        print(f"Nessuna entità con slug {slug!r}.")
        return
    print(f"--- {righe[0]['nome']} ({righe[0]['tipo']}) a sessione {numero} ---\n")

    stato = list(session.run(
        "MATCH (n {slug: $slug})-[r:HA_STATO]->(n) "
        "WHERE r.valido_da_sessione <= $n AND (r.valido_a_sessione IS NULL OR r.valido_a_sessione > $n) "
        "RETURN r.valore AS valore, r.valido_da_sessione AS da, r.fonte AS fonte",
        slug=slug, n=numero,
    ))
    if stato:
        r = stato[0]
        print(f"Stato: {r['valore']} (valido dalla sessione {r['da']}, fonte: {r['fonte']})")
    else:
        print("Stato: nessun valore valido a questa sessione (l'entità non esisteva ancora).")

    print("\nRelazioni uscenti valide a questa sessione:")
    for r in session.run(
        "MATCH (n {slug: $slug})-[r]->(altro) WHERE type(r) <> 'HA_STATO' "
        "AND r.valido_da_sessione <= $n AND (r.valido_a_sessione IS NULL OR r.valido_a_sessione > $n) "
        "RETURN type(r) AS tipo, altro.nome AS verso, r.fonte AS fonte "
        "ORDER BY tipo",
        slug=slug, n=numero,
    ):
        print(f"  -[{r['tipo']}]-> {r['verso']}  ({r['fonte']})")

    print("\nRelazioni entranti valide a questa sessione:")
    for r in session.run(
        "MATCH (altro)-[r]->(n {slug: $slug}) WHERE type(r) <> 'HA_STATO' "
        "AND r.valido_da_sessione <= $n AND (r.valido_a_sessione IS NULL OR r.valido_a_sessione > $n) "
        "RETURN type(r) AS tipo, altro.nome AS da_chi, r.fonte AS fonte "
        "ORDER BY tipo",
        slug=slug, n=numero,
    ):
        print(f"  {r['da_chi']} -[{r['tipo']}]->  ({r['fonte']})")


def connessi_a(session, slug, salti):
    righe = list(session.run(
        "MATCH (n {slug: $slug}) RETURN labels(n)[0] AS tipo, n.nome AS nome", slug=slug,
    ))
    if not righe:
        print(f"Nessuna entità con slug {slug!r}.")
        return
    print(f"--- Entità connesse a {righe[0]['nome']} ({righe[0]['tipo']}) entro {salti} salti ---\n")

    query = (
        f"MATCH (n {{slug: $slug}})-[*1..{int(salti)}]-(altro) "
        "WHERE altro <> n "
        "RETURN DISTINCT labels(altro)[0] AS tipo, altro.nome AS nome, altro.slug AS slug "
        "ORDER BY tipo, nome"
    )
    risultati = list(session.run(query, slug=slug))
    if not risultati:
        print("Nessuna entità raggiungibile entro questo numero di salti.")
        return
    for r in risultati:
        print(f"  [{r['tipo']}] {r['nome']}  ({r['slug']})")


def path_tra(session, slug_a, slug_b):
    risultato = session.run(
        "MATCH (a {slug: $a}), (b {slug: $b}), p = shortestPath((a)-[*..15]-(b)) "
        "RETURN nodes(p) AS nodi, relationships(p) AS relazioni",
        a=slug_a, b=slug_b,
    ).single()
    if not risultato:
        print(f"Nessun cammino trovato tra {slug_a!r} e {slug_b!r} (o una delle due entità non esiste).")
        return
    nodi = risultato["nodi"]
    relazioni = risultato["relazioni"]
    print(f"--- Cammino più breve: {nodi[0]['nome']} → {nodi[-1]['nome']} ({len(relazioni)} passi) ---\n")
    for i, rel in enumerate(relazioni):
        verso_avanti = rel.start_node["slug"] == nodi[i]["slug"]
        freccia = f"-[{rel.type}]->" if verso_avanti else f"<-[{rel.type}]-"
        print(f"  {nodi[i]['nome']} {freccia} {nodi[i + 1]['nome']}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sotto = parser.add_subparsers(dest="comando", required=True)

    p1 = sotto.add_parser("stato_a_sessione")
    p1.add_argument("slug")
    p1.add_argument("numero_sessione", type=int)

    p2 = sotto.add_parser("connessi_a")
    p2.add_argument("slug")
    p2.add_argument("--salti", type=int, default=2)

    p3 = sotto.add_parser("path_tra")
    p3.add_argument("slug_a")
    p3.add_argument("slug_b")

    args = parser.parse_args()
    driver = connetti()
    try:
        with driver.session() as session:
            if args.comando == "stato_a_sessione":
                stato_a_sessione(session, args.slug, args.numero_sessione)
            elif args.comando == "connessi_a":
                connessi_a(session, args.slug, args.salti)
            elif args.comando == "path_tra":
                path_tra(session, args.slug_a, args.slug_b)
    finally:
        driver.close()


if __name__ == "__main__":
    main()
