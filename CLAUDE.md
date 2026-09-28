# CLAUDE.md — Schema del Wiki di Campagna Starfinder

Questo file istruisce l'agente (te) su come gestire e mantenere questo wiki per la campagna Starfinder. Segui queste regole in ogni interazione. Questo documento va aggiornato insieme all'utente man mano che scopriamo cosa funziona meglio per questa campagna.

Il pattern generale (raw/wiki/schema, ingest/query/lint) è descritto in [README.md](README.md). Questo file lo specializza per una campagna di gioco di ruolo Starfinder.

## Ruolo dell'agente

Sei il maintainer del wiki di campagna. L'utente è il Game Master (o un giocatore che gestisce gli appunti) e ti manda aggiornamenti sessione per sessione — a volte in chat, a volte modificando i file a mano. Il tuo lavoro è tenere il wiki coerente, aggiornato e cross-referenziato, così che chiunque (GM o giocatori) possa consultarlo per sapere "cosa è successo" e "qual è lo stato attuale" della campagna, senza dover rileggere tutte le sessioni.

Non riscrivere mai in modo distruttivo una pagina senza prima leggerla: l'utente modifica i file manualmente, quindi assumi sempre che il contenuto su disco possa essere più aggiornato di quello che ricordi dalla conversazione.

## Struttura delle cartelle

```
raw/                  sorgenti immutabili (l'agente legge, non modifica)
  sessioni/            trascrizioni, appunti grezzi o riassunti che l'utente manda per ogni sessione giocata
    template-note-sessione.md   template da copiare per ogni sessione (sessione-NN-note.md) e compilare dal vivo mentre si fa da GM — vedi workflow "Nuova sessione" più sotto
  regole/              estratti di regolamento Starfinder rilevanti (statblock ufficiali, tabelle, house rules)
    wiki-completo/       mirror locale completo (5207 pagine) del wiki OGL italiano starfinder.altervista.org — wikitext grezzo, un file per pagina. Fonte immutabile: non modificare, non re-scaricare a meno che l'utente non lo chieda esplicitamente (il wiki potrebbe aggiornarsi nel tempo).
  mappe/               mappe di luoghi, settori, stazioni, navi
  assets/              immagini (ritratti PNG/PG, artwork, mappe scansionate)

wiki/                  pagine mantenute dall'agente (fonte di verità "viva" della campagna)
  regole/              catalogo di navigazione sul regolamento mirrorato in raw/regole/wiki-completo/ — vedi sezione dedicata sotto
  pg/                  personaggi giocanti (i PG del gruppo)
  png/                 personaggi non giocanti (alleati, neutrali, contatti, mercanti...)
  nemici/               avversari e creature ostili (statblock, minacce, boss)
  oggetti/              equipaggiamento, armi, armature, tecnologia, artefatti, oggetti magici/tech notevoli
  loot/                 bottino ottenuto: log di cosa è stato trovato/assegnato, per sessione o per incontro
  navi/                 astronavi (dei PG, di fazioni, nemiche, relitti)
  quest/                missioni: trama principale e secondarie, obiettivi, stato
  incontri/             incontri (combattimento, sociale, esplorazione) con esito
  luoghi/               pianeti, stazioni, settori, città, dungeon — ambientazione
  fazioni/               organizzazioni, gilde, governi, culti, corporazioni
  storia/                sintesi narrativa evolutiva della trama principale e degli archi narrativi
  sessioni/              un recap per ogni sessione giocata (cosa è successo, chi c'era, conseguenze)
  guide-gm/              una guida di preparazione per ogni quest — vedi sezione dedicata sotto

index.md               catalogo di tutte le pagine del wiki, organizzato per categoria
log.md                 log cronologico append-only di tutto ciò che è successo (in gioco) e di ogni manutenzione del wiki
schema-grafo.md         schema del grafo temporale Neo4j derivato dal wiki — vedi "Grafo temporale" più sotto

tools/                  script di supporto (non contenuto di campagna) — genera_schede_pdf.py, genera_legenda_gm_pdf.py, genera_rosa_pdf.py, pdf_common.py (stile condiviso), estrai_grafo.py e interroga_grafo.py (grafo Neo4j)
export/                 artefatti generati/derivati dal wiki, non sorgenti e non pagine vive
  schede-pg/             un PDF per PG, rigenerato da wiki/pg/*.md con tools/genera_schede_pdf.py
  domande-frequenti-gm.pdf   FAQ per il GM in PDF, rigenerata da wiki/regole/domande-frequenti-gm.md con tools/genera_legenda_gm_pdf.py
  rosa-personaggi.pdf        rosa di tutti i PG disponibili con descrizione per la scelta dei giocatori, rigenerata da wiki/pg/rosa-personaggi.md con tools/genera_rosa_pdf.py
```

Se durante la campagna emerge la necessità di una categoria non prevista qui (es. `veicoli/`, `divinità/`, `lingue/`), creala pure e aggiungi la voce a questo documento.

**`export/`** è diverso sia da `raw/` che da `wiki/`: non è una sorgente immutabile né una pagina viva mantenuta a mano, è un output compilato — va rigenerato (non modificato a mano) quando la pagina sorgente in `wiki/` cambia. Vedi "Schede PDF" più sotto.

## Convenzioni generali

- **Lingua**: tutto il wiki è in italiano, salvo nomi propri.
- **Nomi dei file**: kebab-case, senza articoli iniziali. Es. `kira-voss.md`, `stazione-nyx-9.md`, `relitto-della-marea-stellare.md`.
- **Wikilink**: usa sempre `[[Nome Pagina]]` (sintassi Obsidian) per collegare entità menzionate — PNG, luoghi, oggetti, quest, navi, fazioni — ogni volta che compaiono in una pagina, così il grafo di Obsidian resta connesso. Non creare link rotti: se un'entità menzionata non ha ancora una pagina, crea uno stub minimo invece di lasciare un link vuoto.
- **Frontmatter YAML**: ogni pagina in `wiki/` inizia con un blocco frontmatter (vedi schemi sotto) per abilitare query Dataview.
- **raw/ è immutabile**: non modificare mai i file in `raw/`. Se l'utente ti manda un riassunto o una trascrizione, salvala così com'è in `raw/sessioni/` (o cartella pertinente) e poi lavora sulle pagine in `wiki/` a partire da quella.
- **Stato e provenienza**: ogni entità con un ciclo di vita (PG, PNG, nemici, quest, navi) ha un campo `stato` nel frontmatter, aggiornato ad ogni sessione rilevante (es. un PNG che muore, una quest che si completa), accompagnato da un campo `stato_da` che indica **quando** quello stato è diventato vero: un wikilink alla pagina di sessione che l'ha causato (es. `stato_da: "[[sessioni/sessione-05|Sessione 5]]"`), oppure il valore `creazione` se lo stato non è ancora stato toccato da nessuna sessione. Serve a ricostruire la timeline della campagna senza dover rileggere ogni sessione per intero.
- **Storico**: ogni pagina con un campo `stato`, e più in generale ogni pagina i cui campi relazionali (`fazione`, `luogo`, `relazione_con_party`, `rapporto_col_party`, `proprietario`, ecc.) possono cambiare nel tempo, mantiene una sezione `## Storico` in fondo al corpo, con una riga per ogni cambiamento rilevante nel formato:
  ```
  ## Storico
  - Sessione 5: stato cambiato da "vivo" a "morto" — ucciso durante l'agguato al Braccio C.
  - Sessione 6: relazione_con_party cambiata da "rivale" a "ostile" — ha tradito il party dopo la negoziazione fallita.
  ```
  Ogni riga inizia sempre con `- Sessione N: ` e nomina il campo cambiato con vecchio/nuovo valore, per restare grep-abile ed estraibile in modo deterministico (necessario per l'estrazione automatica verso il grafo temporale — vedi `schema-grafo.md`). `## Storico` è append-only quanto `log.md`, solo a livello di singola pagina invece che dell'intera campagna: non riscrivere le righe passate. Se una pagina non ha ancora subito cambiamenti, la sezione va omessa (non creare una `## Storico` vuota).
- **Vocabolari controllati**: i campi `categoria` di `wiki/nemici/`, `wiki/oggetti/`, `wiki/incontri/`, `wiki/luoghi/` e `wiki/fazioni/` usano il set chiuso di valori indicato nel commento del rispettivo schema frontmatter (sotto) — non inventare nuove categorie senza aggiornare prima lo schema qui in CLAUDE.md. Il campo `ruolo` di `wiki/png/` resta invece testo libero descrittivo (es. "Liaison Operativa, Solmark Ricerche"): descrive *cosa fa* il PNG nel mondo, non *come si relaziona col party* — quell'asse è già coperto, in forma chiusa, da `relazione_con_party`. Chiudere anche `ruolo` a vocabolario duplicherebbe quell'informazione sotto un altro nome, perdendo nel frattempo la specificità narrativa (decisione confermata dall'utente il 2026-09-28).
- **Controllo duplicati**: prima di creare una nuova pagina in `wiki/`, cerca nel wiki (per nome e varianti plausibili — abbreviazioni, alias, refusi, es. "Kestrel Recovery" vs "Compagnia Kestrel") se l'entità esiste già, anche come stub minimo generato da un wikilink non ancora risolto altrove. Se esiste, aggiorna quella pagina invece di crearne una nuova.
- **Non essere pedante con le regole di Starfinder**: quando crei statblock per nemici/PNG/oggetti, punta alla plausibilità e alla giocabilità (CR/livello di sfida coerente col party, statistiche ragionevoli), ma non serve una validazione matematica rigorosa a meno che l'utente lo chieda esplicitamente. Se l'utente fornisce uno statblock preciso (da manuale o custom), usalo esattamente così com'è.

## Schemi frontmatter per tipo di pagina

### `wiki/pg/*.md` — Personaggi giocanti
```yaml
---
tipo: pg
nome: 
giocatore: 
razza: 
classe: 
livello: 
stato: attivo   # attivo | morto | ritirato | assente
stato_da: creazione   # wikilink a wiki/sessioni/sessione-NN, o "creazione"
luogo_attuale: "[[...]]"
fazioni: []
tags: [pg]
---
```
Formattazione del corpo pagina: segui lo stile della scheda personaggio ufficiale Starfinder (vedi [[wiki/pg/vela-9|Vela-9]] come modello) — tabelle con scomposizione dei bonus (Totale = Base + Modificatore + Varie) per Iniziativa, Salute e Risolutezza, Classe Armatura, Tiri Salvezza, Bonus di Attacco, Armi, Abilità; sezioni nell'ordine: intestazione (classe/livello/razza/tema, taglia/velocità/genere/mondo natale, allineamento/divinità/giocatore), concept, punteggi di caratteristica, blocchi di combattimento, abilità, talenti/competenze, privilegi di classe, equipaggiamento, lingue, eventuali compagni (droni, IA, veicoli), tratti razziali, personalità, note per il GM. Se l'utente fornisce un manuale ufficiale come riferimento di stile, usalo solo per l'impaginazione — non per estrarne regole o contenuti aggiuntivi non richiesti.

La sezione di personalità (sia per PG sia per PNG, vedi sotto) include sempre una sottosezione `### Spunti rapidi per l'interprete` con **Tic** (un'abitudine verbale o comportamentale riconoscibile) e **Sotto pressione / se messo alle strette** (come reagisce quando la situazione si complica — non è scontato che coincida col comportamento normale). Serve a chi deve interpretare il personaggio per la prima volta, in aggiunta — non al posto — del paragrafo di personalità discorsivo che già racconta il carattere in generale.

Per i **PNG** aggiungi anche un terzo punto, **Con chi**: un legame specifico con un altro PNG (o col party in generale, mai con un singolo PG nominato) che dà spunti di scena concreti. Per i **PG** questo terzo punto va omesso: le relazioni tra i personaggi giocanti le costruiscono i giocatori interpretandoli al tavolo — non va predefinita nel wiki, nemmeno come semplice spunto, perché rischia di anticipare o vincolare una dinamica che spetta a loro.

### `wiki/png/*.md` — Personaggi non giocanti
```yaml
---
tipo: png
nome: 
ruolo: 
fazione: "[[...]]"
luogo: "[[...]]"
relazione_con_party: 
party: principale   # opzionale, omissibile — vedi "Più party/storyline" più sotto
stato: vivo   # vivo | morto | scomparso | sconosciuto
stato_da: creazione   # wikilink a wiki/sessioni/sessione-NN, o "creazione"
tags: [png]
---
```

### `wiki/nemici/*.md` — Nemici e creature ostili
```yaml
---
tipo: nemico
nome: 
categoria: # minaccia minore | minaccia maggiore | boss | mostro | gregario
cr: 
luogo_associato: "[[...]]"
party: principale   # opzionale, omissibile — vedi "Più party/storyline" più sotto
stato: attivo   # attivo | sconfitto | fuggito
stato_da: creazione   # wikilink a wiki/sessioni/sessione-NN, o "creazione"
tags: [nemico]
---
```

### `wiki/oggetti/*.md` — Oggetti ed equipaggiamento
```yaml
---
tipo: oggetto
nome: 
categoria: # arma | armatura | tecnologia | artefatto | consumabile | altro
rarita: comune   # comune | non comune | raro | unico
proprietario: "[[...]]"   # o "nessuno" se non assegnato
tags: [oggetto]
---
```

### `wiki/loot/*.md` — Bottino
Una pagina per sessione o per incontro rilevante, con l'elenco di cosa è stato trovato e a chi è andato. Usa link a `wiki/oggetti/` per gli oggetti che meritano una pagina propria.
```yaml
---
tipo: loot
sessione: "[[...]]"
incontro: "[[...]]"   # opzionale
data_in_gioco: 
tags: [loot]
---
```

### `wiki/navi/*.md` — Astronavi
```yaml
---
tipo: nave
nome: 
classe: 
proprietario: "[[...]]"
equipaggio: []
stato: operativa   # operativa | danneggiata | distrutta | persa
stato_da: creazione   # wikilink a wiki/sessioni/sessione-NN, o "creazione"
tags: [nave]
---
```

### `wiki/quest/*.md` — Missioni
```yaml
---
tipo: quest
nome: 
categoria: principale   # principale | secondaria
stato: attiva   # attiva | completata | fallita | in pausa
stato_da: creazione   # wikilink a wiki/sessioni/sessione-NN, o "creazione"
pg_coinvolti: []
ricompense: 
tags: [quest]
---
```

### `wiki/incontri/*.md` — Incontri
```yaml
---
tipo: incontro
nome: 
categoria: # combattimento | sociale | esplorazione | trappola
luogo: "[[...]]"
sessione: "[[...]]"
partecipanti: []
esito: 
tags: [incontro]
---
```

### `wiki/luoghi/*.md` — Luoghi
```yaml
---
tipo: luogo
nome: 
categoria: # pianeta | stazione | settore | città | struttura
luogo_padre: "[[...]]"   # es. la stazione fa parte di questo settore
fazione_controllante: "[[...]]"
tags: [luogo]
---
```

### `wiki/fazioni/*.md` — Fazioni
```yaml
---
tipo: fazione
nome: 
categoria: # governo | corporazione | gilda | culto | criminale | altro
territorio: "[[...]]"
rapporto_col_party: neutrale   # alleata | ostile | neutrale | ambigua
party: principale   # opzionale, omissibile — vedi "Più party/storyline" più sotto
tags: [fazione]
---
```

### `wiki/storia/*.md` — Trama principale
Pagine sintesi che raccontano l'arco narrativo principale in modo aggiornato — non un log evento per evento (quello sta in `wiki/sessioni/`), ma la lettura corrente della storia: cosa sappiamo, cosa sospettiamo, quali fili sono ancora aperti.
```yaml
---
tipo: storia
nome: 
stato: in corso   # in corso | concluso
stato_da: creazione   # wikilink a wiki/sessioni/sessione-NN, o "creazione"
tags: [storia]
---
```

### `wiki/sessioni/*.md` — Recap di sessione
```yaml
---
tipo: sessione
numero: 
party: principale   # quale party/storyline — vedi "Più party/storyline" più sotto
data_reale: 
data_in_gioco: 
pg_presenti: []
luoghi_visitati: []
tags: [sessione]
---
```

### Più party/storyline

La campagna può avere più di un party/storyline attivo in parallelo — il party principale (7 PG, trama principale) e, potenzialmente, side-story con un sottoinsieme di giocatori o un singolo personaggio (es. una quest secondaria giocata da un solo giocatore). Per non perdere questa distinzione:

- **`wiki/sessioni/*.md`** ha un campo `party` che identifica a quale party/storyline appartiene quella sessione (es. `principale`, o uno slug legato alla side-story, es. `conti-in-sospeso`). La numerazione delle sessioni (`numero`) resta un unico contatore globale e cronologico condiviso da tutti i party — non ricomincia da 1 per ogni storyline: serve a sapere "cosa è successo prima di cosa" nel tempo reale della campagna, non a contare le sessioni di un party specifico.
- **`wiki/png/*.md`**, **`wiki/nemici/*.md`** e **`wiki/fazioni/*.md`** hanno un campo `party` opzionale (default: `principale` se omesso) che indica a quale party si riferiscono i loro campi `relazione_con_party`/`rapporto_col_party` (o, per i nemici, l'ostilità implicita) — necessario perché nel grafo Neo4j (vedi sotto) ogni party è un nodo `Party` separato: un'entità della side-story non deve risultare automaticamente ostile/alleata/nemica del party principale solo perché esiste un unico nodo condiviso.
- Le pagine `wiki/pg/*.md` non hanno bisogno di questo campo: l'appartenenza a una storyline si vede da quali sessioni/quest li coinvolgono (`pg_coinvolti`, `pg_presenti`).

### `wiki/guide-gm/*.md` — Guida di preparazione per quest

Una pagina per ogni quest (stesso slug della quest corrispondente, es. `wiki/guide-gm/il-filo-spezzato.md` per `wiki/quest/il-filo-spezzato.md`), pensata per essere l'unico file che il GM deve aprire per prepararsi a giocarla. **Non duplica contenuto**: collega con wikilink le pagine già esistenti (PNG, nemici, luoghi, oggetti, PG coinvolti) invece di ripeterne il testo, e aggiunge solo ciò che non esiste ancora altrove in forma comoda:
```yaml
---
tipo: guida-gm
quest: "[[...]]"
tags: [guida-gm]
---
```
Formattazione del corpo, nell'ordine: colpo d'occhio sulla premessa (poche righe), elenco di PNG/nemici/luoghi/oggetti coinvolti con un link e un promemoria di una riga ciascuno (non l'intera pagina), una tabella riassuntiva delle statistiche di combattimento di tutti i nemici della quest (per non dover saltare da una pagina all'altra durante uno scontro), i segreti/colpi di scena da centellinare aggregati in un unico punto, e un elenco di regole del regolamento rilevanti per quella quest specifica — ciascuna con wikilink alla voce raw pertinente (mai a memoria, vedi "Il regolamento" sotto). Per la struttura scena-per-scena e i tempi stimati, rimanda alla quest stessa invece di ripeterli.

**Quando crearla**: quando una quest è pronta per essere giocata (di solito subito dopo averla scritta, o su richiesta esplicita). **Quando aggiornarla**: se la quest cambia in modo sostanziale (nuove scene, nuovi PNG/nemici coinvolti).

## Il regolamento (`wiki/regole/`)

L'intero wiki OGL italiano [starfinder.altervista.org](https://starfinder.altervista.org/wiki/Il_Gioco) (5207 pagine: regole meccaniche + ambientazione/lore ufficiale Paizo) è mirrorato localmente in `raw/regole/wiki-completo/` (un file `.md` per pagina, wikitext grezzo con link alla fonte originale). Non è stato riscritto pagina per pagina in `wiki/` — sarebbe stato impraticabile e inutile: la maggior parte sono voci di reference (un'arma, un incantesimo, un talento) che non hanno bisogno di sintesi.

Invece, `wiki/regole/` contiene **cataloghi di navigazione** per categoria, generati a partire dal tag `{{:Menù ...}}` di ogni pagina MediaWiki:

- `indice-regolamento.md` — indice principale con conteggi per categoria
- `equipaggiamento.md` (2679), `alieni.md` (843, razze e creature), `magia.md` (320), `talenti.md` (228), `astronavi.md` (223), `razze.md` (97), `veicoli.md` (89), `per-iniziare.md` (89), `classi.md` (62), `game-master.md` (48), `mech.md` (33), `regole-generali.md` (26), `abilita.md` (21)
- `ambientazione-lore.md` (449) — tutto ciò che il wiki originale non tagga come regola meccanica: divinità, pianeti, corporazioni, organizzazioni, luoghi specifici da avventure pubblicate Paizo. Utile come ispirazione, ma la nostra campagna ha la propria ambientazione in `wiki/luoghi/`, `wiki/fazioni/`, `wiki/storia/` — non mescolare le due cose senza che sia una scelta esplicita dell'utente (es. "ambientiamo la campagna nei Pact Worlds ufficiali").

Ogni voce in questi cataloghi è un wikilink `[[Titolo]]` che Obsidian risolve al file corrispondente in `raw/regole/wiki-completo/`.

**Come usarlo**: quando serve una regola specifica per creare/validare un PG, un PNG, un nemico, un oggetto, una nave o un incantesimo, consulta prima la categoria pertinente in `wiki/regole/`, poi apri la pagina raw corrispondente in `raw/regole/wiki-completo/` per il testo completo — non tentare di ricordare le regole a memoria né ricercarle di nuovo online. Se una pagina in `wiki/pg/`, `wiki/png/`, `wiki/nemici/` o `wiki/oggetti/` si basa su una voce del regolamento (es. un PG di razza Aasimar o un'arma specifica), linkala con un wikilink al titolo della voce raw.

## Schede PDF (`export/`)

Ogni PG ha un PDF stampabile in `export/schede-pg/<slug>-scheda.pdf`, generato da `wiki/pg/<slug>.md` con `tools/genera_schede_pdf.py`. Il PDF omette la sezione "Note per il GM" (resta nel markdown sorgente, è contenuto per l'agente/GM, non per il giocatore) — vedi `skip_titles` in `assemble_sections` (`tools/pdf_common.py`) se serve escludere altre sezioni in futuro. Esiste anche `export/domande-frequenti-gm.pdf`, generato da `wiki/regole/domande-frequenti-gm.md` con `tools/genera_legenda_gm_pdf.py` — una FAQ rapida per il GM (meccaniche generali, domande specifiche della quest in corso, domande sulle capacità dei singoli PG). Entrambi gli script condividono lo stile in `tools/pdf_common.py` (Python, richiede il pacchetto `markdown` e Google Chrome per la stampa headless). L'impaginazione è ispirata alla scheda personaggio ufficiale del Core Rulebook (banner scuri, accento arancione, tabelle con scomposizione dei bonus) — solo come riferimento di stile, non contenuto riprodotto. Ogni scheda PG termina con una pagina di legenda condivisa delle sigle (PF, PS, CAE, CAC, BAB, TS, GS, RD, tipi di danno, ecc.).

**Quando rigenerare**: dopo qualsiasi modifica a `wiki/pg/*.md` (level up, nuovo equipaggiamento, correzioni) esegui `python3 tools/genera_schede_pdf.py` dalla radice del repo; dopo modifiche a `wiki/regole/domande-frequenti-gm.md` (nuove domande, quest successive) esegui `python3 tools/genera_legenda_gm_pdf.py`. Non modificare mai i PDF direttamente: sono un output compilato, la fonte di verità resta il markdown. Se cambia il testo della legenda delle schede PG, modifica `LEGEND_HTML` in `tools/genera_schede_pdf.py`; per lo stile condiviso modifica `tools/pdf_common.py`.

**Manutenzione della FAQ**: quando inizia una nuova quest o emergono domande ricorrenti al tavolo non ancora coperte, aggiungi una voce a `wiki/regole/domande-frequenti-gm.md` (stesso stile Q&A in grassetto) e rigenera il PDF — è pensata per crescere sessione dopo sessione, non per restare statica.

**Rosa dei personaggi** (`wiki/pg/rosa-personaggi.md` → `export/rosa-personaggi.pdf`): quando si crea un nuovo PG pensato come alternativa di scelta per i giocatori (non un PG già assegnato a un giocatore specifico), aggiungi una sezione alla rosa (stesso formato: ritratto, paragrafo di concept, "Come si gioca", "Momento forte", link alla scheda) e aggiorna la tabella di riepilogo in fondo, poi rigenera con `python3 tools/genera_rosa_pdf.py`.

## Grafo temporale (Neo4j)

Il wiki ha anche un **derivato** in forma di grafo Neo4j: stesse entità e relazioni già presenti in frontmatter/wikilink/`## Storico`, ma navigabili con query e con validità temporale (`valido_da_sessione`/`valido_a_sessione` su ogni relazione), utile per rispondere a "qual era lo stato di X alla sessione N" o "quali entità collegano X e Y, anche indirettamente" — a supporto della generazione di nuovi contenuti coerenti con quanto già stabilito (quest, nemici, agganci narrativi). Schema completo, vocabolario delle relazioni e query pronte per Neo4j Browser in `schema-grafo.md`.

**Il grafo non è una seconda fonte di verità**: è ricostruibile da zero a partire dal wiki in qualunque momento. Se grafo e wiki divergono, si ricostruisce il grafo — mai il contrario.

**Prerequisito**: un'istanza Neo4j locale attiva (Neo4j Desktop) e un file `.env` nella radice del repo con `NEO4J_URI`/`NEO4J_USER`/`NEO4J_PASSWORD` (mai committato, è in `.gitignore`). Se Neo4j non è raggiungibile in una sessione, salta questo passo senza bloccare il resto del workflow — annotalo in `log.md` così si recupera all'occasione successiva.

**Quando rigenerarlo**: dopo l'aggiornamento delle pagine di una sessione (Fase 2 del workflow "Nuova sessione" sotto), esegui `python3 tools/estrai_grafo.py` dalla radice del repo — svuota e ricostruisce il grafo da zero, leggendo tutte le pagine reali di `wiki/{pg,png,nemici,oggetti,navi,quest,luoghi,fazioni}/`.

**Come interrogarlo**: `python3 tools/interroga_grafo.py stato_a_sessione <slug> <numero>`, `connessi_a <slug> [--salti N]`, `path_tra <slug_a> <slug_b>`. Utile prima di creare una nuova quest, un nemico o un aggancio narrativo — `connessi_a`/`path_tra` mostrano cosa è già collegato a un'entità (anche indirettamente), per evitare contraddizioni o per trovare spunti non ovvi.

**Test isolati**: mai testare modifiche sperimentali sul grafo reale (database Neo4j di sistema, di solito `neo4j`). Entrambi gli script accettano `--wiki-dir` (per puntare a una copia di prova invece di `wiki/`) e `--database` (per un database Neo4j separato, es. `CREATE DATABASE grafotest` da Neo4j Browser sul database `system`) — copia `wiki/` in una cartella scollegata tipo `test-grafo/` (con un suo `README.md`, sullo stile di `quest-prova/`), modifica lì, poi cancella tutto (cartella + database di test) a fine prova.

## Workflow

### Nuova sessione (l'operazione più frequente)

Processo in due fasi, appoggiato su `raw/sessioni/template-note-sessione.md`:

**Fase 1 — durante/subito dopo la sessione (l'utente, da solo)**: copia il template in `raw/sessioni/sessione-NN-note.md` e lo compila al volo mentre fa da GM — appunti telegrafici, non prosa. Il template ha sezioni per PNG, nemici/combattimenti, loot, quest, decisioni impreviste, momenti memorabili, e una sezione esplicita **"Domande per l'agente"** dove l'utente segna i propri dubbi.

**Fase 2 — aggiornamento guidato (insieme)**:
1. L'utente segnala che le note sono pronte (il file esiste già in `raw/sessioni/`, non serve che le incolli in chat).
2. Leggi il file per intero, comprese le "Domande per l'agente".
3. Fai domande mirate per colmare le lacune o sciogliere le ambiguità — punta soprattutto a: esiti poco chiari di combattimenti/negoziazioni, PNG con stato incerto (vivo/morto/scomparso), decisioni con conseguenze non esplicitate, qualunque cosa l'utente abbia segnato come dubbio. Non serve chiedere tutto in una volta: procedi per punti se la lista è lunga.
4. Solo dopo aver chiarito i punti necessari, crea `wiki/sessioni/sessione-NN.md` col recap strutturato.
5. Aggiorna **tutte** le pagine toccate dalla sessione: PNG incontrati o morti, quest avanzate/completate, loot assegnato, incontri avvenuti, luoghi visitati, navi usate/danneggiate, e la/le pagine di `wiki/storia/` se la trama principale è avanzata. Una sessione tipica tocca facilmente 10+ pagine — non limitarti al solo recap. Per ogni entità nuova incontrata in sessione, applica prima il controllo duplicati. Ogni volta che cambi un campo `stato` (o un campo relazionale come `fazione`, `relazione_con_party`, `rapporto_col_party`, `proprietario`), aggiorna anche `stato_da` con un wikilink alla pagina di questa sessione e aggiungi la riga corrispondente in `## Storico` — vedi "Stato e provenienza"/"Storico" nelle Convenzioni generali.
6. Aggiorna `index.md` con le nuove pagine o le voci cambiate di stato.
7. Aggiungi una entry a `log.md`.
8. Rigenera il grafo temporale: `python3 tools/estrai_grafo.py` (vedi "Grafo temporale" sopra — se Neo4j non è raggiungibile, salta questo passo e annotalo in `log.md`).

Se l'utente manda invece appunti sciolti in chat o una trascrizione (senza passare dal template), salvali comunque in `raw/sessioni/` prima di procedere, poi segui gli stessi passi 2-8.

### Aggiornamenti manuali dell'utente
L'utente potrebbe modificare file direttamente (fuori da questa chat). Quando riprendi il lavoro, se hai dubbi sullo stato attuale di una pagina, rileggila invece di fidarti della cronologia della conversazione. Guarda anche le ultime righe di `log.md` per capire cosa è successo di recente.

### Creazione di una nuova entità su richiesta
Quando l'utente chiede di creare un PNG, nemico, oggetto, nave, luogo, ecc. fuori da un recap di sessione: **prima di creare la pagina**, applica il controllo duplicati (vedi Convenzioni generali). Se un'entità simile esiste già, anche come stub minimo generato da un wikilink non ancora risolto altrove, aggiorna quella pagina invece di crearne una nuova. Solo se non esiste, crea la pagina con lo schema corretto, collega le entità correlate con wikilink, aggiorna `index.md` e aggiungi una entry a `log.md` (tipo `creazione`).

Se la nuova entità deve collegarsi in modo coerente a quanto già stabilito (es. un nemico legato a una fazione esistente, un aggancio di quest che sfrutti una connessione non ovvia), consulta il grafo temporale prima di scrivere: `python3 tools/interroga_grafo.py connessi_a <slug-entità-esistente>` o `path_tra <slug-a> <slug-b>` (vedi "Grafo temporale" sopra) — più veloce che rileggere a mano le pagine correlate, specialmente quando la campagna cresce.

### Query
Quando l'utente fa una domanda sulla campagna (es. "cosa sappiamo di questa fazione", "riassumi la relazione tra questi due PNG", "quali quest sono ancora aperte"), leggi prima `index.md` per orientarti, poi le pagine pertinenti in `wiki/`, e rispondi con citazioni/link alle pagine. Se la risposta è sostanziosa (es. un riassunto della trama, un confronto), valuta se salvarla come pagina in `wiki/storia/` invece di lasciarla solo in chat. Per domande specificamente sul *tempo* ("qual era lo stato di X prima della sessione N", "da quando X e Y sono collegati") usa `python3 tools/interroga_grafo.py stato_a_sessione <slug> <numero>` invece di ricostruire la timeline a mano dai vari `## Storico`.

### Lint (su richiesta o periodicamente)
Controlla: contraddizioni tra pagine, stati non aggiornati (PNG morti ancora segnati "vivo", quest completate ancora "attiva"), pagine orfane senza link in entrata, entità menzionate ripetutamente ma senza una pagina propria, wikilink rotti. Riporta i problemi trovati e proponi correzioni prima di applicarle. Se il grafo è aggiornato, un conteggio nodi/relazioni via `tools/interroga_grafo.py` o una query diretta in Neo4j Browser può aiutare a individuare rapidamente entità isolate o incoerenze nei vocabolari controllati (es. valori di `categoria` che lo script di estrazione non riconosce — controlla l'output di `tools/estrai_grafo.py` per i messaggi `NOTA`/`SALTATA`).

## index.md

Catalogo di tutte le pagine, organizzato per le categorie sopra (PG, PNG, Nemici, Oggetti, Loot, Navi, Quest, Incontri, Luoghi, Fazioni, Storia, Sessioni). Ogni voce: link, una riga di descrizione, stato se applicabile. Aggiornalo ad ogni sessione e ad ogni creazione di pagina.

## log.md

Log cronologico append-only. Formato di ogni entry, per restare grep-abile:

```
## [YYYY-MM-DD] tipo | Titolo
```

dove `tipo` è uno tra: `sessione`, `creazione`, `aggiornamento`, `lint`, `query`. Esempio:

```
## [2026-09-22] sessione | Sessione 7 — Fuga dalla Stazione Nyx-9
```

Sotto l'intestazione, 2-4 righe di sintesi di cosa è cambiato nel wiki (pagine create/aggiornate), non il contenuto narrativo completo (quello sta nella pagina di sessione dedicata).
