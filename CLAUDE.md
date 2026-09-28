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

index.md               catalogo di tutte le pagine del wiki, organizzato per categoria
log.md                 log cronologico append-only di tutto ciò che è successo (in gioco) e di ogni manutenzione del wiki

tools/                  script di supporto (non contenuto di campagna) — genera_schede_pdf.py, genera_legenda_gm_pdf.py, genera_rosa_pdf.py, pdf_common.py (stile condiviso)
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
- **Vocabolari controllati**: i campi `categoria` di `wiki/nemici/`, `wiki/oggetti/`, `wiki/incontri/`, `wiki/luoghi/` e `wiki/fazioni/` usano il set chiuso di valori indicato nel commento del rispettivo schema frontmatter (sotto) — non inventare nuove categorie senza aggiornare prima lo schema qui in CLAUDE.md. Il campo `ruolo` di `wiki/png/` resta invece testo libero descrittivo (es. "Liaison Operativa, Solmark Ricerche"): serve alla lettura umana, non a classificare il nodo — la relazione con fazione/luogo passa dai campi `fazione`/`luogo`, già wikilink, e la relazione col party dal campo `relazione_con_party`. *(Nota di riconciliazione: una sessione precedente aveva invece proposto di chiudere anche `ruolo` a un vocabolario fisso — scelta scartata qui perché nessuna delle 4 pagine PNG esistenti vi si conformava senza perdita di informazione; correggimi se preferisci l'altra strada.)*
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

### `wiki/png/*.md` — Personaggi non giocanti
```yaml
---
tipo: png
nome: 
ruolo: 
fazione: "[[...]]"
luogo: "[[...]]"
relazione_con_party: 
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
data_reale: 
data_in_gioco: 
pg_presenti: []
luoghi_visitati: []
tags: [sessione]
---
```

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

Se l'utente manda invece appunti sciolti in chat o una trascrizione (senza passare dal template), salvali comunque in `raw/sessioni/` prima di procedere, poi segui gli stessi passi 2-7.

### Aggiornamenti manuali dell'utente
L'utente potrebbe modificare file direttamente (fuori da questa chat). Quando riprendi il lavoro, se hai dubbi sullo stato attuale di una pagina, rileggila invece di fidarti della cronologia della conversazione. Guarda anche le ultime righe di `log.md` per capire cosa è successo di recente.

### Creazione di una nuova entità su richiesta
Quando l'utente chiede di creare un PNG, nemico, oggetto, nave, luogo, ecc. fuori da un recap di sessione: **prima di creare la pagina**, applica il controllo duplicati (vedi Convenzioni generali). Se un'entità simile esiste già, anche come stub minimo generato da un wikilink non ancora risolto altrove, aggiorna quella pagina invece di crearne una nuova. Solo se non esiste, crea la pagina con lo schema corretto, collega le entità correlate con wikilink, aggiorna `index.md` e aggiungi una entry a `log.md` (tipo `creazione`).

### Query
Quando l'utente fa una domanda sulla campagna (es. "cosa sappiamo di questa fazione", "riassumi la relazione tra questi due PNG", "quali quest sono ancora aperte"), leggi prima `index.md` per orientarti, poi le pagine pertinenti in `wiki/`, e rispondi con citazioni/link alle pagine. Se la risposta è sostanziosa (es. un riassunto della trama, un confronto), valuta se salvarla come pagina in `wiki/storia/` invece di lasciarla solo in chat.

### Lint (su richiesta o periodicamente)
Controlla: contraddizioni tra pagine, stati non aggiornati (PNG morti ancora segnati "vivo", quest completate ancora "attiva"), pagine orfane senza link in entrata, entità menzionate ripetutamente ma senza una pagina propria, wikilink rotti. Riporta i problemi trovati e proponi correzioni prima di applicarle.

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
