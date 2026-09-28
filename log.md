# Log — Campagna Starfinder

Log cronologico append-only. Formato: `## [YYYY-MM-DD] tipo | Titolo`. Vedi [CLAUDE.md](CLAUDE.md) per i dettagli.

## [2026-09-22] creazione | Impostazione iniziale del wiki di campagna

Creata la struttura di cartelle (`raw/`, `wiki/`), lo schema in `CLAUDE.md`, `index.md` e questo log. Nessuna sessione ancora registrata.

## [2026-09-22] aggiornamento | Fonti regole Starfinder in italiano

Nessun manuale ufficiale completo acquistato: il "Manuale di Gioco" italiano di Giochi Uniti è un prodotto commerciale a pagamento, nessuna copia gratuita legittima trovata online. Scaricato invece il modulo introduttivo ufficiale gratuito "Primo Contatto" in `raw/regole/starfinder-primo-contatto.pdf`. Individuato anche il wiki OGL italiano (starfinder.altervista.org) come riferimento regole completo e gratuito, da consultare on-demand. Dettagli in `raw/regole/fonti-regole.md`.

## [2026-09-22] ingest | Mirror completo del wiki OGL italiano (5207 pagine)

Su richiesta dell'utente, scaricato l'intero wiki starfinder.altervista.org via API MediaWiki (export wikitext, 105 batch da 50 pagine) in `raw/regole/wiki-completo/` — 5207 pagine, 28 MB, sorgente immutabile. Categorizzate via tag `{{:Menù ...}}` di MediaWiki e organizzate in cataloghi di navigazione in `wiki/regole/`: equipaggiamento (2679), alieni/razze e creature (843), magia (320), talenti (228), astronavi (223), razze (97), veicoli (89), per iniziare (89), classi (62), game master (48), mech (33), regole generali (26), abilità (21), più 449 pagine di ambientazione/lore Paizo non taggate come regola meccanica. Indice principale: `wiki/regole/indice-regolamento.md`. Aggiornati `index.md` e `CLAUDE.md` (nuova sezione "Il regolamento" con workflow d'uso).

## [2026-09-22] aggiornamento | Fix struttura file mirror regolamento

Corretto un bug: il 59% dei titoli del wiki (3096/5207, es. "Equipaggiamento/Pistola X") contiene "/", inizialmente appiattito in nomi file con underscore (`Equipaggiamento_Pistola X.md`), il che rompeva i wikilink `[[Equipaggiamento/Pistola X]]` usati negli indici. Migrati tutti i file in `raw/regole/wiki-completo/` a una struttura a sottocartelle reale che rispecchia i titoli originali (es. `raw/regole/wiki-completo/Equipaggiamento/Pistola X.md`), poi rigenerati i cataloghi in `wiki/regole/` con wikilink ora funzionanti.

## [2026-09-22] creazione | PG: Vela-9 (Androide, Meccanico livello 8)

Creato il primo PG del gruppo su richiesta dell'utente: `wiki/pg/vela-9.md`. Androide femmina, Meccanico (specializzazione Drone) livello 8, tema Erudito (Scienza Fisica). Classe scelta dall'agente per coerenza col lore razziale (affinità androidi-macchine esplicitamente citata in [[Androide]]). Scheda completa: caratteristiche, PF/PS/PR, CA, talenti, privilegi di classe, drone da combattimento "Unità-Falco" con statistiche proprie, equipaggiamento (armatura e arma reperite dal regolamento locale), personalità coerente coi tratti razziali (emozioni sopite, diffidenza verso l'autorità, legame più forte con la tecnologia che con gli organici). Aggiornato `index.md`. Da definire: nome giocatore, background dettagliato, luogo attuale, fazioni.

## [2026-09-22] aggiornamento | Riformattazione scheda PG secondo lo stile ufficiale

L'utente ha fornito il manuale ufficiale "Starfinder Core Rulebook" (inglese, PDF) in `raw/regole/Starfinder - Core Rulebook.pdf`, da usare solo come riferimento di impaginazione (non come fonte di regole aggiuntive). Installato `poppler` (brew) per visualizzare le pagine del PDF. Individuata la scheda personaggio ufficiale (pag. stampata 524-525) e ripreso lo stile: sezioni con tabelle di scomposizione dei bonus (Totale = Base + Modificatore + Varie) per Iniziativa, Salute e Risolutezza, Classe Armatura, Tiri Salvezza, Bonus di Attacco, Armi, Abilità. Riformattata `wiki/pg/vela-9.md` di conseguenza. Aggiunta convenzione di formattazione per le pagine PG in `CLAUDE.md`, con Vela-9 come modello di riferimento.

## [2026-09-22] creazione | Quest: Il Filo Spezzato (prima quest della campagna)

Costruita su richiesta dell'utente la prima quest della campagna: investigativa/esplorativa, 5-6 PG livello 8, ~5 ore, ambientata nel nuovo [[luoghi/sistema-di-ordessa|Sistema di Ordessa]] (originale, non legato alla lore Paizo). Filo tematico unificante: motivo della tessitura/filo (stazione Elice-7, artefatto "il Telaio", entità antagonista "l'Ordito", PNG corrotti "Tessuti", nave "Filo di Arianna").

Pagine create:
- Luoghi: `luoghi/sistema-di-ordessa.md`, `luoghi/stazione-elice-7.md`
- Fazioni: `fazioni/solmark-ricerche.md`
- PNG: `png/imara-voss.md` (mandante), `png/renn-kade.md`, `png/toby-ferra.md`, `png/ilsa-draak.md` (rivale con statistiche di combattimento)
- Nemici: `nemici/tessuto-corrotto.md` (GS5, Battaglia 1), `nemici/mercenari-kestrel.md` (GS5+leader GS8, Battaglia 2), `nemici/ordito.md` (GS11, boss)
- Navi: `navi/filo-di-arianna.md` (Tier 4, assegnata al party)
- Quest: `quest/il-filo-spezzato.md` — struttura in 8 scene con timing stimato, 3 eventi minori (Tempesta di Schegge, Registro Criptato, Il Guasto), ordine esplorazione flessibile, note su risoluzione non violenta della Battaglia 2

Aggiornato `index.md`. CR/statistiche dei nemici pensate per essere giocabili subito, senza validazione matematica esaustiva (per filosofia generale vedi `CLAUDE.md`). Gancio aperto per la trama principale: identità del creatore dell'Ordito e del committente di Ilsa Draak, entrambi non ancora rivelati.

## [2026-09-22] creazione | Resto del party (4 PG)

Completato il party di 5 PG livello 8 su richiesta dell'utente, con classi e razze scelte per coprire ruoli complementari a [[pg/vela-9|Vela-9]] (Meccanico androide):

- `pg/kesh-vantor.md` — [[pg/kesh-vantor|Kesh Vantor]], Vesk Soldato (stile Guerriero Provetto), tank/danno in mischia, doshko avanzato.
- `pg/naeva-thess.md` — [[pg/naeva-thess|Naeva Thess]], Lashunta Damaya Mistico (connessione Guaritore), supporto/cura — prima fonte di guarigione del party.
- `pg/whix-chitterclaw.md` — [[pg/whix-chitterclaw|Whix Chitterclaw]], Ysoki Operativo (specializzazione Detective), skill-monster/investigatrice, iniziativa altissima (+11).
- `pg/callan-reyes.md` — [[pg/callan-reyes|Callan Reyes]], Umano Emissario, volto sociale/negoziatore del party.

Tutte le schede seguono lo standard di formattazione stabilito con Vela-9 (tabelle di scomposizione dei bonus, ispirate alla scheda ufficiale Starfinder). Equipaggiamento e statistiche derivati dal regolamento locale in `raw/regole/wiki-completo/`. Alcuni elementi lasciati aperti per scelta del giocatore al tavolo: trucchi dell'operativo di Whix (oltre a Scorgere la Verità), improvvisazioni/doti perfezionate di Callan Reyes, lista incantesimi completa di Naeva, talento bonus umano di Callan Reyes. Aggiornati `index.md` e `pg_coinvolti` in `quest/il-filo-spezzato.md`.

## [2026-09-23] aggiornamento | Ritratti e illustrazioni generati esternamente (OpenAI)

L'utente ha generato 14 immagini (ritratti dei 5 PG, di 5 PNG/nemici, 2 illustrazioni di luoghi, 1 concept art dell'Ordito) tramite OpenAI e le ha aggiunte al wiki, con embed markdown nelle pagine corrispondenti. Verificate: tutti file PNG validi, contenuto coerente con le descrizioni testuali (es. Vela-9 con braccio cibernetico e tuta da meccanico, Kesh Vantor corazzato in stile Vesk, concept dell'Ordito come telaio bio-meccanico luminescente).

Le immagini erano finite in `wiki/assets/`, cartella non prevista dallo schema (che assegna le immagini a `raw/assets/`, sorgenti immutabili). Su richiesta dell'utente, spostate in `raw/assets/` e aggiornati i riferimenti nelle 14 pagine (`../assets/` → `../../raw/assets/`). Nessun contenuto testuale modificato.

## [2026-09-23] aggiornamento | Generate le 2 immagini mancanti (drone e nave)

Su richiesta dell'utente, generate le immagini mancanti per completare la copertura visiva della quest: `raw/assets/unita-falco-ritratto.png` (il drone da combattimento di [[pg/vela-9|Vela-9]]) e `raw/assets/filo-di-arianna-illustrazione.png` (la nave [[navi/filo-di-arianna|Filo di Arianna]] presso Kaldenor). Generate con chiamata diretta all'API immagini di OpenAI (`gpt-image-1`) via curl, usando la API key già presente nell'ambiente dell'utente (`~/.zshrc`) — nessun server MCP di terze parti installato, su scelta esplicita dell'utente per evitare di eseguire codice non verificato. Aggiunti i riferimenti immagine in `wiki/pg/vela-9.md` (sezione Unità-Falco) e `wiki/navi/filo-di-arianna.md`.

## [2026-09-23] lint | Verifica giocabilità de Il Filo Spezzato e correzioni

Su richiesta dell'utente, verificata la quest [[quest/il-filo-spezzato|Il Filo Spezzato]] per interesse narrativo, completezza e giocabilità, incrociando le statistiche dei nemici (create prima del party) con le CA/attacchi reali dei 5 PG. Esito:

- **Narrativa**: promossa senza riserve (gancio, twist, antagonista non manicheo, scelta combattere/negoziare in Scena 6).
- **Completezza**: trovato un buco — il drone Unità-Falco di [[pg/vela-9|Vela-9]] aveva 2 Montature per Arma ma nessuna arma assegnata. Corretto: 2× [[Equipaggiamento/Modulatore d'Onda III|Modulatore d'Onda III]] installati, che gli danno anche una seconda fonte di danno sonico contro l'Ordito.
- **Giocabilità**: la Battaglia Boss contro [[nemici/ordito|l'Ordito]] risultava sovra-tarata — attacco +19 (3d10+12) ×2 colpiva Callan Reyes (CAC19) quasi sempre, ~54 danni/round su 108 PF totali (morte in 2 round senza reale contromisura), e la RD 10/– penalizzava pesantemente ogni danneggiatore non sonico allungando il combattimento a 9-10 round. Su indicazione dell'utente, l'Ordito è stato reso più resistente ma meno letale: GS 11→9, PF 210→260, RD 10→5, tentacoli +19 (3d10+12)→+15 (2d8+8), aggiunta una **Scarica di Filamenti a Distanza** (attacco a 18 m) per evitare che il kiting a distanza annulli l'incontro senza snaturare il vincolo "radicato alla camera". Aggiornati i riferimenti a GS 11 in `index.md` e `quest/il-filo-spezzato.md`.

## [2026-09-23] creazione | Schede PDF stampabili per i 5 PG

Su richiesta dell'utente, creato `tools/genera_schede_pdf.py`: converte ciascuna `wiki/pg/*.md` in un PDF con impaginazione ispirata alla scheda personaggio ufficiale del Core Rulebook (banner blu scuro, accento arancione, tabelle con scomposizione dei bonus — riferimento di solo stile, nessun contenuto riprodotto), usando `markdown` (Python, installato via pip) per la conversione e Google Chrome headless per la stampa in PDF. Ogni scheda termina con una pagina di legenda condivisa che spiega le sigle usate nel wiki (PF, PS, PR, CAE, CAC, BAB, TS, CD, GS, RD, tipi di danno Fu/Fr/So/P/T/C, tag (Str)/(Sop)/(Mag), simboli ☑/†, Modale, Cariche, Ingombro).

Generati in `export/schede-pg/`: `vela-9-scheda.pdf`, `kesh-vantor-scheda.pdf`, `naeva-thess-scheda.pdf`, `whix-chitterclaw-scheda.pdf`, `callan-reyes-scheda.pdf` (5-6 pagine ciascuno). Verifica visiva su Vela-9 e Kesh Vantor: buona resa, ritratti posizionati correttamente, tabelle leggibili. Documentata la nuova cartella `export/` (output compilato, da rigenerare non modificare a mano) e il workflow di rigenerazione in `CLAUDE.md`. Aggiunti link ai PDF in `index.md`.

## [2026-09-23] creazione | FAQ per il GM (wiki + PDF)

Su richiesta dell'utente, creata `wiki/regole/domande-frequenti-gm.md`: guida rapida a domande comuni al tavolo, in tre parti — meccaniche generali (azioni/turni, PS/PF, stabilizzarsi, copertura, afferrare), domande specifiche di [[quest/il-filo-spezzato|Il Filo Spezzato]] (esplorazione libera, negoziare con Ilsa Draak, vulnerabilità sonora dell'Ordito, ecc.), e domande sulle capacità di ciascuno dei 5 PG (una sotto-sezione a testa). Chiude con una nota di filosofia del tavolo coerente con l'approccio "non pedante" già stabilito in `CLAUDE.md`.

Refactoring: estratto lo stile CSS condiviso dei PDF in `tools/pdf_common.py` (usato sia da `genera_schede_pdf.py` sia dal nuovo `tools/genera_legenda_gm_pdf.py`), corretto un difetto di impaginazione nel banner del titolo quando il testo è lungo (il sottotitolo ora va a capo invece di sovrapporsi). Generato `export/domande-frequenti-gm.pdf` (3 pagine, stesso stile delle schede PG). Aggiornati `CLAUDE.md` (nuova sezione, nota su come far crescere la FAQ nel tempo) e `index.md`.

## [2026-09-23] aggiornamento | Rinominato il PG Umano Emissario in "Callan Reyes"

Su richiesta esplicita dell'utente, rinominato il PG Umano Emissario (nome precedente non più in uso da nessuna parte nel wiki, comprese le voci storiche di questo log, ripulite su ulteriore richiesta dell'utente). Nuovo file `wiki/pg/callan-reyes.md`, ritratto rinominato `raw/assets/callan-reyes-ritratto.png`, aggiornati tutti i riferimenti in `index.md`, `wiki/quest/il-filo-spezzato.md` (pg_coinvolti), `wiki/regole/domande-frequenti-gm.md` e `tools/genera_schede_pdf.py`. Rimossa anche la vecchia `export/schede-pg/*.pdf` (rigenerata con il nuovo nome) e una cartella `output/imagegen/` trovata fuori dalla struttura documentata — duplicati esatti (stesso hash) delle immagini già in `raw/assets/`, lasciata lì dallo strumento esterno di generazione.

## [2026-09-23] aggiornamento | Abilità complete e ottimizzazione layout PDF

Su richiesta dell'utente, due migliorie alle schede PG:

1. **Tabella Abilità completa**: tutte le 20 abilità di Starfinder ora elencate per ciascun PG (prima era mostrata solo una selezione delle abilità addestrate), comprese quelle non addestrate con il relativo bonus (solo modificatore di caratteristica, nessun bonus di classe senza almeno 1 grado). Completate anche alcune assegnazioni lasciate aperte in precedenza (es. gradi aggiuntivi di Naeva Thess e Whix Chitterclaw non ancora assegnati a un'abilità specifica) e corretto un errore aritmetico nel totale di Cultura di Naeva Thess (era +17, corretto a +15; il secondo bonus Studioso ora assegnato esplicitamente a Misticismo, portandolo a +17).
2. **Layout PDF ottimizzato**: aggiunta logica in `tools/pdf_common.py` (`assemble_sections`, `split_table_two_cols`, `PAIR_RULES`) che affianca in colonne le sezioni brevi (Iniziativa+Salute e Risolutezza, Classe Armatura+Tiri Salvezza, Bonus di Attacco+Lingue, Talenti e Competenze+Equipaggiamento) e spezza la tabella Abilità (ora lunga 20 righe) in due colonne affiancate. Ridotti margini/padding per una resa più compatta. Pagine totali ridotte per 4 PG su 5 (es. Kesh Vantor 5→4, Naeva Thess 6→5).

Rigenerate tutte le 5 schede PDF in `export/schede-pg/`. Verifica visiva su Vela-9 (layout completo, tabella abilità spezzata) e Callan Reyes (rinomina corretta).

## [2026-09-23] aggiornamento | Personaggi completati per la one-shot + rimossa "Note per il GM" dal PDF

Su richiesta dell'utente, completati tutti gli elementi "da definire"/"da assegnare" ancora aperti nelle 5 schede PG, trattandosi di una one-shot (nessun bisogno di background esteso, ma la scheda dev'essere pronta all'uso):

- **Mondo natale** per tutti e 5: Vela-9 (Fonderia Halvenn), Kesh Vantor (Vesk-12), Naeva Thess (Aelara — sostituito il riferimento a Castrovel, mondo ufficiale Paizo, con uno originale per coerenza con la politica di non mescolare lore ufficiale e ambientazione della campagna), Whix Chitterclaw (Stazione Rottame), Callan Reyes (Aurelia Nova).
- **Divinità** di Naeva Thess: Vaelith (dea della guarigione, originale, patrona della connessione Guaritore).
- **`luogo_attuale`** per tutti e 5: Stazione Varrow (avamposto franco condiviso, prima dell'incarico di Imara Voss).
- **Crediti** per tutti e 5: importi plausibili di liquidità residua (200-900 a seconda della personalità), con nota che il grosso della ricchezza iniziale è già nell'equipaggiamento elencato.
- **Lista incantesimi completa di Naeva Thess**: tutti gli incantesimi conosciuti per livello (0°-3°), nomi reali presi da `Lista del Mistico` nel regolamento locale. Corretta anche la descrizione dell'incantesimo della connessione Guaritore: non è "Cura Mistica a livello variabile" come scritto in precedenza, ma una progressione di incantesimi diversi (Rimuovi Condizione Inferiore → Rimuovi Condizione → Rimuovi Afflizione), attualmente al 3° livello.
- **4 trucchi dell'Operativo di Whix Chitterclaw**: Notare Trappole, Senza Traccia, Hacker Veloce, Mira Rapida (nomi reali da `Operativo/Trucchi`).
- **Talento bonus umano, 5 improvvisazioni e 2 doti perfezionate di Callan Reyes**: Allerta Costante; Scherno Demoralizzante, Incoraggiamento Ispiratore, Attacco Astuto, Orazione Ispiratrice, Cogliere il Vantaggio; Bugiardo Convincente, Diplomatico Universale (nomi reali da `Emissario/Improvvisazioni` e `Emissario/Doti`).

Campo lasciato volutamente aperto in tutti e 5: `giocatore` — non è un elemento narrativo completabile dall'agente, dipende da chi si siederà al tavolo.

Inoltre, su richiesta dell'utente, la sezione "Note per il GM" non viene più stampata nei PDF (resta nel markdown sorgente in `wiki/pg/`, è contenuto per l'agente/GM, non per il giocatore): aggiunto il parametro `skip_titles` a `assemble_sections` in `tools/pdf_common.py`. Rigenerate tutte le 5 schede PDF; verifica visiva su Naeva Thess (lista incantesimi, divinità) e Callan Reyes (privilegi di classe completi, nessuna sezione GM).

## [2026-09-23] creazione | 2 nuovi PG (Keskodai, Jehir Voloteo) + rosa dei personaggi per la scelta dei giocatori

Su richiesta dell'utente, creati 2 PG aggiuntivi come alternative di scelta per i giocatori, portando il roster totale a 7. Scelte razza/classe per coprire ruoli non ancora rappresentati nel party (le uniche due classi "core" di Starfinder ancora mancanti):

- `pg/keskodai.md` — [[pg/keskodai|Keskodai]], Shirren Tecnomante livello 8, tema Erudito. Cannone magico offensivo/controllo, ruolo assente nel resto del party (Naeva Thess è orientata alla cura, non all'attacco). Incantesimi e hackeraggi magici reali da `Lista del Tecnomante` e `Tecnomante/Hackeraggi`.
- `pg/jehir-voloteo.md` — [[pg/jehir-voloteo|Jehir Voloteo]], Kasatha Solarian livello 8, tema Icona. Duellante in mischia con Manifestazione Solare (arma di energia stellare) e Modalità Stellare (sottosistema di risorse a turni, gravitonica/fotonica) — distinto sia da Kesh Vantor (soldato "always-on") sia dal resto del party. Rivelazioni Stellari bilanciate 3 fotoniche/3 gravitoniche da `Solarian/Rivelazioni`.

Entrambe le schede seguono lo stesso standard delle altre 5 (tabella abilità completa a 20 voci, tutti gli elementi "da definire" già completati fin dall'inizio, formattazione PDF ottimizzata, nessuna sezione GM nel PDF). Generati ritratti via API OpenAI (stesso metodo delle altre immagini) e salvati in `raw/assets/`.

Creata `wiki/pg/rosa-personaggi.md`: per ciascuno dei 7 PG un paragrafo di concept, "Come si gioca" (in linguaggio semplice, orientato al giocatore non al regolamento) e "Momento forte", più una tabella di riepilogo ruoli — pensata per permettere ai giocatori di scegliere senza leggere le schede complete. Creato `tools/genera_rosa_pdf.py` (riusa lo stile condiviso di `pdf_common.py`, una pagina per personaggio) e generato `export/rosa-personaggi.pdf` (8 pagine). Aggiornati `index.md` (inclusi i 2 nuovi PG e il link alla rosa) e `CLAUDE.md` (documentata la nuova convenzione, nota su come mantenere la rosa aggiornata quando si aggiungono nuovi PG).

## [2026-09-23] aggiornamento | Rosa dei personaggi: ruolo, statistiche chiave e punti di forza/debolezza

Su richiesta dell'utente, arricchita ogni pagina di `wiki/pg/rosa-personaggi.md` (una pagina per personaggio, con spazio libero da riempire) con tre elementi per chiarire il ruolo a colpo d'occhio: un tag **Ruolo** subito sotto il titolo (es. "TANK / DANNO IN MISCHIA", "GUARITRICE / SUPPORTO"), una tabella con le statistiche chiave (PS/PF, CAE/CAC, attacco principale con danno) trascritte dalle rispettive schede, e una tabella Punti di forza/Punti deboli con 2-3 voci per lato. Numeri verificati da ogni scheda PG prima della trascrizione, nessun valore ricordato a memoria. Rigenerato `export/rosa-personaggi.pdf`, ancora 8 pagine ma con impaginazione più equilibrata.

## [2026-09-23] creazione | Template note di sessione + workflow di aggiornamento in due fasi

Su richiesta dell'utente, creato `raw/sessioni/template-note-sessione.md`: template pensato per essere compilato dal vivo durante la sessione (appunti telegrafici, non prosa), con sezioni per info rapide, timeline, PNG, nemici/combattimenti, loot, quest, decisioni impreviste, momenti memorabili, prossima sessione, e una sezione esplicita "Domande per l'agente" dove l'utente segna i propri dubbi durante il gioco.

Aggiornato il workflow "Nuova sessione" in `CLAUDE.md` per riflettere il processo in due fasi: (1) l'utente compila da solo `raw/sessioni/sessione-NN-note.md` copiando il template; (2) in un secondo momento, l'agente legge il file per intero (comprese le domande segnate), fa domande mirate per colmare lacune o ambiguità prima di procedere, e solo dopo esegue l'aggiornamento completo (recap in `wiki/sessioni/`, tutte le pagine toccate, `index.md`, `log.md`). Documentato anche il caso di appunti sciolti mandati in chat senza passare dal template.

## [2026-09-23] creazione | Bottino per Il Filo Spezzato

Su richiesta dell'utente, preparato il bottino della quest in anticipo, prevedendo che i giocatori perquisiscano corpi, esplorino ambienti e possibilmente tentino di derubare i PNG.

Creati 3 oggetti unici in `wiki/oggetti/`:
- `campione-di-filo-corrotto.md` — bottino dai Tessuti Corrotti/Braccio A; percorso alternativo per scoprire la vulnerabilità sonora dell'Ordito prima della Battaglia Boss.
- `datapad-criptato-kestrel.md` — bottino dai mercenari; indizio parziale ("Meridian Holdings") sul committente di Ilsa Draak, deliberatamente incompleto per non chiudere il gancio aperto della trama principale.
- `frammento-del-telaio.md` — trovato nella Camera del Telaio dopo il boss; materiale di ricerca senza effetto meccanico, gancio narrativo per sviluppi futuri.

Aggiunta sezione "Bottino" a `nemici/tessuto-corrotto.md`, `nemici/mercenari-kestrel.md` e `png/ilsa-draak.md` (quest'ultima con bottino disponibile solo se K.O. e perquisita, più conseguenza narrativa esplicita — preclude alleanza/defezione futura). Aggiunta sezione "Cosa si può trovare esplorando" a `luoghi/stazione-elice-7.md`, area per area, coerente con la struttura già esistente.

Aggiunta sezione "Bottino e furti — domande frequenti" a `wiki/regole/domande-frequenti-gm.md`: cosa succede se i giocatori tentano di derubare [[png/toby-ferra|Toby Ferra]] (smette di collaborare), [[png/renn-kade|Renn Kade]] (dati incompleti, lei si richiude, possibile segnalazione a Imara) o [[png/imara-voss|Imara Voss]] (relazione con Solmark chiusa, da comunicare chiaramente ai giocatori prima di applicarla, non a sorpresa). Rigenerato `export/domande-frequenti-gm.pdf`.

Aggiunto un riepilogo "Bottino" a `wiki/quest/il-filo-spezzato.md` con tabella di riferimento rapido per il tavolo. Aggiornato `index.md` con i 3 nuovi oggetti.

## [2026-09-23] creazione | Gancio per una sessione futura: L'Eco nel Filo + prima pagina di wiki/storia/

Su richiesta dell'utente, aggiunto un gancio concreto (non solo domande aperte) per continuare la campagna oltre il one-shot. Ampliato `wiki/oggetti/frammento-del-telaio.md`: esaminando il frammento con successo di 5+ oltre la CD base (o con strumentazione adeguata, es. il laboratorio della [[navi/filo-di-arianna|Filo di Arianna]]), emerge **L'Eco nel Filo** — una risonanza residua che si decodifica in coordinate stellari verso un secondo sito non catalogato: il Telaio di Tessitrice non era unico. Destinazione deliberatamente non sviluppata nei dettagli, da inventare quando servirà davvero.

Creata la prima pagina di `wiki/storia/`: `la-rete-dei-telai.md`, sintesi "cosa sappiamo / cosa sospettiamo / fili aperti" della trama principale (l'Ordito, il sospetto leak interno di Imara Voss, Meridian Holdings, L'Eco nel Filo) — pensata per essere aggiornata dopo ogni sessione, non riscritta da zero. Collegata da `wiki/quest/il-filo-spezzato.md` (gancio aperto) e `wiki/nemici/ordito.md` (note sulla dissoluzione). Aggiornato `index.md` con la nuova pagina in Storia.

## [2026-09-23] aggiornamento | Ritratto di Naeva Thess

Generato un ritratto originale per [[pg/naeva-thess|Naeva Thess]] e salvato in `wiki/assets/naeva-thess-ritratto.png`. Inserito nella scheda PG; l'immagine la raffigura come lashunta Damaya mistica guaritrice.

## [2026-09-23] aggiornamento | Ritratti del resto del party

Generati ritratti originali per [[pg/vela-9|Vela-9]], [[pg/kesh-vantor|Kesh Vantor]], [[pg/whix-chitterclaw|Whix Chitterclaw]] e [[pg/callan-reyes|Callan Reyes]]. Salvati in `wiki/assets/` e inseriti nelle rispettive schede PG.

## [2026-09-23] aggiornamento | Immagini di PNG, minacce e luoghi

Create immagini per i quattro PNG, le tre minacce (inclusa la figura rappresentativa del Mercenario Kestrel) e i due luoghi descritti nella wiki: [[Sistema di Ordessa]] e [[Stazione Elice-7]]. Inserite nelle pagine corrispondenti e salvate in `wiki/assets/`.

## [2026-09-23] lint | Prima passata completa sulla wiki di campagna

Controllo sistematico di wikilink, pagine orfane e coerenza frontmatter sulle 24 pagine campagna (esclusi i cataloghi di `wiki/regole/`). Trovati e corretti: 9 wikilink che usavano il nome visualizzato invece dello slug del file reale (`[[Solmark Ricerche]]`, `[[Imara Voss]]`) — uno di questi aveva già causato la creazione automatica di uno stub vuoto `Solmark Ricerche.md` in root da parte di Obsidian, rimosso; 1 link rotto verso una voce di regolamento inesistente in [[pg/naeva-thess|Naeva Thess]] (corretto verso `Salute e Risolutezza`); 1 link fuorviante in [[oggetti/frammento-del-telaio|Frammento del Telaio]] che mostrava "Meridian Holdings" ma puntava alla pagina del Datapad. Creata [[fazioni/kestrel-recovery|Kestrel Recovery]] come pagina minima di fazione (menzionata ripetutamente in 7 pagine ma priva di pagina propria) e aggiornati i relativi wikilink/frontmatter in [[png/ilsa-draak|Ilsa Draak]], [[nemici/mercenari-kestrel|Mercenario Kestrel]], [[oggetti/datapad-criptato-kestrel|Datapad Criptato Kestrel]], [[storia/la-rete-dei-telai|La Rete dei Telai]], [[luoghi/sistema-di-ordessa|Sistema di Ordessa]], [[quest/il-filo-spezzato|Il Filo Spezzato]]. Aggiornato `pg_coinvolti` della quest per includere [[pg/keskodai|Keskodai]] e [[pg/jehir-voloteo|Jehir Voloteo]] (mancanti dalla lista originale). Aggiunte le sezioni FAQ mancanti per Keskodai e Jehir Voloteo in `wiki/regole/domande-frequenti-gm.md` e rigenerato `export/domande-frequenti-gm.pdf`. Ripuliti due campi frontmatter con placeholder `[[...]]` mai compilati ([[luoghi/sistema-di-ordessa|Sistema di Ordessa]], [[png/imara-voss|Imara Voss]]). Nessuna pagina orfana trovata, nessuna incoerenza negli stati (`stato`/`vivo`/`attivo`/`attiva`) rilevata. Aggiornato `index.md` con la nuova pagina fazione.

## [2026-09-28] aggiornamento | Schema: stato_da, Storico, vocabolari controllati, controllo duplicati

Materializzato in `CLAUDE.md` uno schema di provenienza temporale in vista dell'estrazione di un grafo Neo4j: campo `stato_da` accanto a ogni campo `stato` (pg, png, nemico, nave, quest, storia), convenzione `## Storico` per registrare i cambiamenti di stato/relazioni nel formato grep-abile `- Sessione N: ...`, vocabolari controllati per i campi `categoria` (nemici, oggetti, incontri, luoghi, fazioni), e un passo di controllo duplicati prima di creare nuove entità. Applicato retroattivamente `stato_da: creazione` alle 17 pagine reali con campo `stato` (nessuna ha ancora `## Storico`, corretto: nessuna sessione è stata ancora giocata). Normalizzato il campo `categoria` di [[nemici/mercenari-kestrel|Mercenario Kestrel]] e [[nemici/tessuto-corrotto|Tessuto Corrotto]] al valore controllato `minaccia minore` (prima contenevano dettagli extra tra parentesi, già presenti nel corpo della pagina).

## [2026-09-28] aggiornamento | Riconciliazione con modifiche parallele su `origin/main`

Scoperto, dopo il lavoro sopra, che una sessione Claude Code precedente aveva già applicato uno schema equivalente (`stato_da`, `## Storico`, vocabolari controllati, controllo duplicati) direttamente su `origin/main` (commit `360fa8e`), mai recuperato in locale prima d'ora — da qui la falsa impressione che l'edit fosse "andato perso". `git stash` delle modifiche locali non committate, `git pull --ff-only` per allineare al remoto, poi `git stash pop` per riapplicarle: conflitto solo in `CLAUDE.md` (8 blocchi), tutti gli altri 18 file uniti senza problemi. Risolti a mano privilegiando la versione più adatta all'estrazione deterministica del grafo (formato `## Storico` con campo/vecchio-valore/nuovo-valore esplicito, `stato_da` come wikilink invece di stringa libera) e unendo il vocabolario `categoria` dei nemici da entrambe le versioni (`minaccia minore | minaccia maggiore | boss | mostro | gregario`). Punto di disaccordo esplicito lasciato in nota in `CLAUDE.md`: il campo `ruolo` dei PNG resta testo libero (la sessione remota lo aveva invece chiuso a vocabolario) perché nessuna pagina PNG esistente vi si conformava senza perdita di informazione — da confermare con l'utente.

## [2026-09-28] creazione | Grafo temporale Neo4j — schema, estrazione, query, integrazione nel workflow

Progettato e implementato un grafo Neo4j derivato dal wiki (ricostruibile da zero, mai una seconda fonte di verità): `schema-grafo.md` (8 etichette nodo + Party sintetico, 13 tipi di relazione chiusi dedotti dai campi frontmatter, proprietà temporali `valido_da_sessione`/`valido_a_sessione`/`fonte`/`pagina_origine`, vincoli e query Cypher), `tools/estrai_grafo.py` (estrazione deterministica senza LLM da frontmatter + wikilink nel corpo + `## Storico`), `tools/interroga_grafo.py` (`stato_a_sessione`, `connessi_a`, `path_tra`). Estratto e verificato contro il wiki reale (23 entità): trovati e corretti tre bug tramite verifica puntuale, non solo sui conteggi — pagina indice senza `tipo:` trattata come entità, matching delle parole chiave per posizione anziché priorità fissa, valore di `rapporto_col_party` con testo extra che non generava nessun arco. Testato con una sessione fittizia in `test-grafo/` (scollegata, poi rimossa insieme al database Neo4j dedicato `grafotest`): emerso e corretto un bug più profondo, lo stato/relazione "di creazione" va ricostruito dal primo `valore_vecchio` in `## Storico` quando presente, non dal frontmatter corrente (che riflette sempre l'ultimo valore). Integrato nel workflow reale di `CLAUDE.md`: nuova sezione "Grafo temporale", passo di rigenerazione dopo l'aggiornamento di una sessione, consultazione consigliata prima di creare nuove entità collegate e per domande sulla timeline della campagna.

## [2026-09-28] lint | Controllo grafo-assistito sulla campagna reale — due correzioni

Su richiesta dell'utente, usato il grafo appena popolato per un controllo di coerenza oltre il lint testuale: query dirette su grado dei nodi, relazioni ridondanti tra stessa coppia di entità, copertura di `proprietario`/`luogo`, valori fuori dai vocabolari controllati. Trovati due problemi reali. (1) `pg_coinvolti` di [[quest/il-filo-spezzato|Il Filo Spezzato]] non generava nessuna relazione nel grafo — campo mai gestito da `tools/estrai_grafo.py`; aggiunto il tipo `PARTECIPA_A` (PG→Quest) allo schema e allo script. (2) "Stazione Varrow", menzionata identicamente nel `luogo_attuale` di tutti e 7 i PG ma priva di pagina propria (nessun SI_TROVA_IN nel grafo per nessun PG) — creata [[luoghi/stazione-varrow|Stazione Varrow]] come vera location (avamposto franco, base operativa ricorrente della campagna, non solo stub), collegata a [[png/imara-voss|Imara Voss]], [[fazioni/solmark-ricerche|Solmark Ricerche]], [[navi/filo-di-arianna|Filo di Arianna]] e alla Scena 1 di [[quest/il-filo-spezzato|Il Filo Spezzato]]; aggiornati i `luogo_attuale` dei 7 PG a wikilink reali. Ri-estratto il grafo: tutti i PG ora hanno grado ≥3 (prima 1-3 con due quasi isolati), nessuna relazione ridondante o contraddittoria residua.

## [2026-09-28] creazione | Prima side-story: promossa "Conti in Sospeso" da materiale di prova a quest reale

Su richiesta dell'utente, la quest e i personaggi creati come test del sistema (`quest-prova/`, vedi entry precedenti) sono stati integrati nella campagna vera come side-story indipendente: [[quest/conti-in-sospeso|Conti in Sospeso]] (categoria secondaria), [[pg/vey-ashkora|Vey Ashkora]] (nuovo PG attivo, Verthani Operativo livello 1), [[png/doss-kellum|Doss Kellum]] e [[png/nix-calder|Nix Calder]] (PNG), [[nemici/ressa-doon|Ressa Doon]] (nemico, categoria corretta a "minaccia minore"), [[oggetti/chiave-di-memoria|Chiave di Memoria]], [[luoghi/avamposto-tregua|Avamposto Tregua]] (nuova location). Immagini spostate da `quest-prova/assets/` a `raw/assets/`; cartella `quest-prova/` rimossa. Deliberatamente non collegata alla trama principale, ma senza escluderlo in futuro (nota esplicita in `Conti in Sospeso`). Rigenerata anche la scheda PDF di Vey Ashkora.

Correzione al sistema richiesta dall'utente, propedeutica alla migrazione: il grafo aveva un solo nodo `Party` globale, che avrebbe reso Ressa Doon (e gli altri PNG della side-story) automaticamente nemici/alleati del party principale solo per condividere il grafo. Aggiunto un campo opzionale `party` a `wiki/png/`, `wiki/nemici/`, `wiki/fazioni/` (default `principale`, retrocompatibile) e un campo `party` a `wiki/sessioni/` (numerazione delle sessioni resta un contatore globale cronologico unico, condiviso da tutti i party — non riparte da 1 per storyline). `tools/estrai_grafo.py` ora crea un nodo `:Party` per ogni valore distinto trovato. Durante la verifica, scoperto e corretto un bug più sottile: alcune query dello script facevano `MATCH` per `slug` senza specificare l'etichetta — innocuo finché gli slug erano unici nell'intero grafo, ma "conti-in-sospeso" è sia lo slug della side-story sia quello del nuovo party, e questo aveva generato un self-loop `HA_STATO` spurio sul nodo Party. Corretto specificando sempre l'etichetta nei `MATCH` per slug; documentato in `schema-grafo.md` come regola generale. Verificato: [[nemici/ressa-doon|Ressa Doon]] risulta ostile solo al party `conti-in-sospeso`, il party `principale` resta invariato (24 entità, stessi archi di prima).

## [2026-09-28] lint | Lint completo (testuale + grafo-assistito) sull'intera campagna

Combinato un controllo testuale (wikilink rotti, path immagini rotti, pagine orfane, campo `stato_da` mancante, valori fuori dai vocabolari controllati su tutte le 33 pagine campagna) con query dirette sul grafo (grado dei nodi, coppie con più di un tipo di relazione tra loro, coerenza dell'assegnazione `party`). Trovati e corretti due problemi.

(1) `wiki/pg/vey-ashkora.md` aveva `stato` ma non `stato_da` — dimenticato durante la migrazione della sessione precedente. Aggiunto `stato_da: creazione`.

(2) Più significativo: il controllo di ridondanza sul grafo ha rivelato che **41 relazioni `CONNESSO_A`** in tutto il grafo (non solo nella side-story appena migrata) duplicavano una relazione già tipizzata tra la stessa coppia di entità — es. Doss Kellum→Chiave di Memoria aveva sia `POSSIEDE` che `CONNESSO_A`. Causa: il controllo anti-duplicati in `tools/estrai_grafo.py` era locale a ogni pagina, ma alcune relazioni tipizzate nascono dalla pagina "dall'altra parte" (`POSSIEDE` nasce processando l'Oggetto, non il proprietario; `PARTECIPA_A` nasce processando la Quest, non il PG) — quindi la pagina che poi linkava lo stesso bersaglio nel corpo non se ne accorgeva. Riscritta l'estrazione in tre passate separate (relazioni tipizzate su tutte le entità → connessioni generiche da wikilink con controllo globale → replay di `## Storico`) invece di una sola passata per pagina. Verificato: zero coppie con relazioni ridondanti dopo il fix (`CONNESSO_A` sceso da 125 a 84 relazioni).
