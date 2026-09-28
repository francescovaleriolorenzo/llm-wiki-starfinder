# Schema del Grafo Temporale (Neo4j)

Questo documento progetta lo schema del grafo Neo4j derivato dal wiki di campagna. **Non è codice**: è la base da rivedere e correggere insieme prima di scrivere `tools/estrai_grafo.py` (Passo 2).

Principio guida (vedi anche `CLAUDE.md`): il markdown resta l'unica fonte di verità. Il grafo è ricostruibile da zero a partire da frontmatter + sezioni `## Storico` + wikilink nel corpo. Se wiki e grafo divergono, si ricostruisce il grafo.

## 1. Etichette dei nodi

Una per categoria di `CLAUDE.md`, più una singola entità sintetica `Party` per rappresentare il gruppo dei PG collettivamente (necessaria per modellare `relazione_con_party` e `rapporto_col_party`, che nel wiki sono testo/enum riferiti "al party" senza un nodo esplicito).

| Etichetta | Cartella sorgente | Proprietà principali |
|---|---|---|
| `PG` | `wiki/pg/` | `slug`, `nome`, `razza`, `classe`, `livello`, `stato`, `stato_da`, `pagina_origine` |
| `PNG` | `wiki/png/` | `slug`, `nome`, `ruolo`, `stato`, `stato_da`, `pagina_origine` |
| `Nemico` | `wiki/nemici/` | `slug`, `nome`, `categoria`, `cr`, `stato`, `stato_da`, `pagina_origine` |
| `Oggetto` | `wiki/oggetti/` | `slug`, `nome`, `categoria`, `rarita`, `pagina_origine` |
| `Nave` | `wiki/navi/` | `slug`, `nome`, `classe`, `stato`, `stato_da`, `pagina_origine` |
| `Quest` | `wiki/quest/` | `slug`, `nome`, `categoria`, `stato`, `stato_da`, `pagina_origine` |
| `Luogo` | `wiki/luoghi/` | `slug`, `nome`, `categoria`, `pagina_origine` |
| `Fazione` | `wiki/fazioni/` | `slug`, `nome`, `categoria`, `pagina_origine` |
| `Party` | — (sintetico, un solo nodo) | `nome: "Party"` |

**Deliberatamente escluse dalla v1**: `Storia`, `Sessione`, `Incontro`, `Loot`. `Sessione` non diventa un nodo — resta un numero intero nelle proprietà temporali delle relazioni (vedi sotto), più semplice da interrogare per gli use case attuali ("stato a sessione N"). `Storia`/`Incontro`/`Loot` non hanno ancora campi relazionali strutturati abbastanza ricchi da giustificare un'etichetta propria: le pagine di `wiki/storia/` restano fuori dal grafo per ora (sono sintesi narrative, non entità), e se in futuro serve, si aggiungono senza rompere lo schema esistente. Dimmi se preferisci includerle già da subito.

`slug` è la chiave di identità (il nome file senza estensione, es. `ilsa-draak`) — univoco per etichetta, usato per `MERGE` idempotente.

## 2. Vocabolario chiuso delle relazioni

| Tipo | Direzione | Dedotta da (campo frontmatter) | Significato |
|---|---|---|---|
| `APPARTIENE_A` | `(Entità)→(Fazione)` | `fazione` | l'entità è membro/affiliata alla fazione |
| `SI_TROVA_IN` | `(Entità)→(Luogo)` | `luogo`, `luogo_attuale`, `luogo_associato` | posizione attuale/associata dell'entità |
| `PARTE_DI` | `(Luogo)→(Luogo)` | `luogo_padre` | gerarchia di contenimento tra luoghi |
| `CONTROLLATO_DA` | `(Luogo)→(Fazione)` | `fazione_controllante` | chi controlla il luogo |
| `POSSIEDE` | `(Entità)→(Oggetto\|Nave)` | `proprietario` (invertito: il proprietario possiede l'oggetto) | proprietà |
| `MANDANTE_DI` | `(PNG)→(Party)` | `relazione_con_party` contiene "mandante" | chi assegna la quest |
| `ALLEATO_DI` | `(Entità)→(Party)` | `relazione_con_party`/`rapporto_col_party` contiene "alleat" | alleanza |
| `OSTILE_A` | `(Entità)→(Party)` | `relazione_con_party`/`rapporto_col_party` contiene "ostile" | ostilità dichiarata |
| `RIVALE_DI` | `(Entità)→(Party)` | `relazione_con_party` contiene "rivale" | rivalità non ancora ostile/negoziabile |
| `AMBIGUO_CON` | `(Entità)→(Party)` | `rapporto_col_party` = "ambigua" | rapporto non ancora definito |
| `NEMICO_DI` | `(Nemico)→(Party)` | implicita per ogni nodo `Nemico` | ostilità di default per tutto ciò che è catalogato come nemico |
| `CONNESSO_A` | `(A)→(B)` | wikilink nel corpo non coperto da un campo sopra; fallback per `relazione_con_party` senza parola chiave riconosciuta | connessione generica, con `descrizione` come proprietà testuale quando disponibile |
| `HA_STATO` | `(Entità)→(Entità)` (auto-relazione) | `stato` + `stato_da` + righe `## Storico` sullo stato | valore di stato nel tempo — vedi sezione 3 |

**Nota sulla mappatura testo libero → tipo chiuso**: `relazione_con_party` (PNG) è oggi testo libero (es. "fonte chiave, da trovare e proteggere"). L'estrazione deterministica cerca le parole chiave sopra (case-insensitive, substring match) in ordine; se nessuna corrisponde, usa `CONNESSO_A` col testo originale in `descrizione`. È una perdita di informazione accettabile per la v1 — se il testo non si presta, meglio un arco generico che nessun arco. Rivedi tu se le parole chiave ti sembrano giuste prima che scriva l'estrazione.

## 3. Proprietà delle relazioni (validità temporale)

Ogni relazione (incluse le auto-relazioni `HA_STATO`) ha:

| Proprietà | Tipo | Significato |
|---|---|---|
| `valido_da_sessione` | Integer | `0` = valido dalla creazione (prima di qualunque sessione), altrimenti il numero della sessione che ha stabilito/cambiato il fatto |
| `valido_a_sessione` | Integer, nullable | `null` = ancora valido ora; altrimenti la sessione in cui il fatto è cessato di essere vero (es. quando un nuovo valore lo sostituisce) |
| `fonte` | String | come è stata estratta: `frontmatter:<campo>` \| `storico` \| `wikilink-corpo` |
| `pagina_origine` | String | path del file `.md` da cui è stata estratta, es. `wiki/png/ilsa-draak.md` |

**Perché `HA_STATO` è un'auto-relazione invece di una proprietà semplice sul nodo**: una proprietà nodo cattura solo il valore *attuale*. Modellare anche lo stato come relazione (che punta all'entità stessa) permette a `stato_a_sessione` di usare lo stesso identico pattern Cypher sia per lo stato sia per le altre relazioni — un solo filtro `WHERE r.valido_da_sessione <= $n AND (r.valido_a_sessione IS NULL OR r.valido_a_sessione > $n)` funziona per entrambi. Il nodo mantiene comunque `stato`/`stato_da` come proprietà dirette per le query "stato attuale" più comuni, che non hanno bisogno di filtrare nel tempo.

Quando una sessione futura cambia uno stato o una relazione, l'estrazione deterministica (leggendo `## Storico`) deve: (a) chiudere la relazione/HA_STATO precedente impostando `valido_a_sessione` alla sessione del cambiamento, (b) crearne una nuova con `valido_da_sessione` alla stessa sessione. Questo succederà al Passo 2.

## 4. Vincoli Cypher (`CREATE CONSTRAINT`)

```cypher
CREATE CONSTRAINT pg_slug IF NOT EXISTS FOR (n:PG) REQUIRE n.slug IS UNIQUE;
CREATE CONSTRAINT png_slug IF NOT EXISTS FOR (n:PNG) REQUIRE n.slug IS UNIQUE;
CREATE CONSTRAINT nemico_slug IF NOT EXISTS FOR (n:Nemico) REQUIRE n.slug IS UNIQUE;
CREATE CONSTRAINT oggetto_slug IF NOT EXISTS FOR (n:Oggetto) REQUIRE n.slug IS UNIQUE;
CREATE CONSTRAINT nave_slug IF NOT EXISTS FOR (n:Nave) REQUIRE n.slug IS UNIQUE;
CREATE CONSTRAINT quest_slug IF NOT EXISTS FOR (n:Quest) REQUIRE n.slug IS UNIQUE;
CREATE CONSTRAINT luogo_slug IF NOT EXISTS FOR (n:Luogo) REQUIRE n.slug IS UNIQUE;
CREATE CONSTRAINT fazione_slug IF NOT EXISTS FOR (n:Fazione) REQUIRE n.slug IS UNIQUE;
CREATE CONSTRAINT party_nome IF NOT EXISTS FOR (n:Party) REQUIRE n.nome IS UNIQUE;
```

## 5. Esempi `CREATE` (dati reali della campagna)

Nodi:

```cypher
MERGE (party:Party {nome: "Party"});

MERGE (ilsa:PNG {slug: "ilsa-draak"})
SET ilsa.nome = "Ilsa Draak",
    ilsa.ruolo = "Capitana mercenaria, Kestrel Recovery",
    ilsa.stato = "vivo",
    ilsa.stato_da = "creazione",
    ilsa.pagina_origine = "wiki/png/ilsa-draak.md";

MERGE (kestrel:Fazione {slug: "kestrel-recovery"})
SET kestrel.nome = "Kestrel Recovery",
    kestrel.categoria = "criminale",
    kestrel.pagina_origine = "wiki/fazioni/kestrel-recovery.md";

MERGE (solmark:Fazione {slug: "solmark-ricerche"})
SET solmark.nome = "Solmark Ricerche",
    solmark.categoria = "corporazione",
    solmark.pagina_origine = "wiki/fazioni/solmark-ricerche.md";
```

Relazioni (con provenienza temporale):

```cypher
MATCH (ilsa:PNG {slug: "ilsa-draak"}), (kestrel:Fazione {slug: "kestrel-recovery"})
MERGE (ilsa)-[r:APPARTIENE_A]->(kestrel)
SET r.valido_da_sessione = 0,
    r.valido_a_sessione = null,
    r.fonte = "frontmatter:fazione",
    r.pagina_origine = "wiki/png/ilsa-draak.md";

MATCH (ilsa:PNG {slug: "ilsa-draak"}), (party:Party {nome: "Party"})
MERGE (ilsa)-[r:RIVALE_DI]->(party)
SET r.valido_da_sessione = 0,
    r.valido_a_sessione = null,
    r.fonte = "frontmatter:relazione_con_party",
    r.pagina_origine = "wiki/png/ilsa-draak.md";

// Auto-relazione di stato
MATCH (ilsa:PNG {slug: "ilsa-draak"})
MERGE (ilsa)-[r:HA_STATO {valido_da_sessione: 0}]->(ilsa)
SET r.valore = "vivo",
    r.valido_a_sessione = null,
    r.fonte = "frontmatter:stato",
    r.pagina_origine = "wiki/png/ilsa-draak.md";
```

## 6. Query pronte per Neo4j Browser (visualizzazione)

**Sottografo attorno a una fazione** (es. Kestrel Recovery, entro 2 salti):
```cypher
MATCH p = (f:Fazione {slug: "kestrel-recovery"})-[*1..2]-(altro)
RETURN p;
```

**Tutte le relazioni attive a una certa sessione** (es. sessione 3 — sostituisci `$n`):
```cypher
:param n => 3;
MATCH (a)-[r]->(b)
WHERE r.valido_da_sessione <= $n AND (r.valido_a_sessione IS NULL OR r.valido_a_sessione > $n)
RETURN a, r, b;
```

**Tutto il grafo attuale** (utile per un primo colpo d'occhio dopo l'estrazione):
```cypher
MATCH (n) RETURN n LIMIT 300;
```

**Cammino più breve tra due entità** (es. Kestrel Recovery → Solmark Ricerche, agganci non ovvi):
```cypher
MATCH (a {slug: "kestrel-recovery"}), (b {slug: "solmark-ricerche"}), p = shortestPath((a)-[*..15]-(b))
RETURN p;
```

## 7. Decisioni prese (rivedibili dopo la prima estrazione)

Le domande aperte della prima stesura sono state chiuse con scelte di default ragionevoli, correggibili dopo aver visto l'output della prima estrazione reale (Passo 2):

1. **`Party` come nodo sintetico**: confermato, resta com'è.
2. **Parole chiave per `relazione_con_party`**: resta la lista mandante/alleat/ostile/rivale. Lo script di estrazione logga ogni PNG il cui `relazione_con_party` non matcha nessuna parola chiave (fallback `CONNESSO_A`), così dopo la prima run si vede subito se la lista va allargata.
3. **`Storia`/`Sessione`/`Incontro`/`Loot` esclusi dalla v1**: confermato. `Sessione` resta un numero intero nelle proprietà temporali, non un nodo.
4. **`CONNESSO_A` come fallback generico**: confermato per la v1, tipo unico indifferenziato per i wikilink nel corpo non coperti da un campo frontmatter.

Passo al Passo 2 (`tools/estrai_grafo.py`).
