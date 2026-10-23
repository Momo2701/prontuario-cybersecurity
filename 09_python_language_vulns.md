Modulo 09: Python Language Vulnerabilities (eval() & Format String)
​Parole chiave e indizi espliciti nella traccia:
​Riferimenti a servizi di calcolo matematico online, "calcolatrici", parser di formule o motori di template personalizzati.
​Menzioni esplicite di stringhe di formattazione dinamiche o input valutati in tempo reale dall'interprete.
​Anomalie strutturali o nel codice sorgente:
​Presenza nel codice del server di funzioni critiche come eval(), exec() o dell'utilizzo del metodo .format() associato a oggetti di contesto (self, config) su input non sanificati.
​Motivo logico di applicazione:
​Si sceglie questo pattern quando la traccia mostra uno script in cui l'input dell'utente viene passato direttamente a funzioni di valutazione del linguaggio o a template string, consentendo l'esecuzione di codice o l'introspezione dello spazio di memoria.


3. GUIDA ALL'ADATTAMENTO (COSA MODIFICARE)
​Durante le esercitazioni di laboratorio o l'esame, modifica esclusivamente il blocco di configurazione iniziale:
​TARGET_URL: Imposta l'URL esatto della pagina o dell'API di test (es. [http://127.0.0.1:5000/api/evaluate](http://127.0.0.1:5000/api/evaluate)).
​PARAM_NAME: Inserisci il nome del campo di input del form o del parametro URL (es. formula, template, q).
​METHOD: Imposta "POST" se l'input viene inviato tramite modulo HTML con metodo POST, oppure "GET" se passato nella query string dell'URL.
​4. WRITE-UP TEORICO CONCISO & REMEDIATION
​Vulnerabilità & Meccanismo: L'applicazione è affetta da esecuzione impropria di codice dovuta all'uso della funzione eval() per l'elaborazione di espressioni dell'utente (o all'uso di stringhe di formato non parametriche). Ciò consente di eseguire codice Python all'interno del processo del server o di accedere alle variabili di stato dell'applicazione tramite introspezione degli oggetti (__globals__).
​Identificazione & Metodo: La vulnerabilità è stata confermata inviando un'espressione deterministica (7*7) e verificando che la risposta del server contenesse il risultato calcolato (49), dimostrando la presenza di interpretazione dinamica del payload.
​Remediation & Hardening: Sostituire l'uso di eval() con il modulo standard ast.literal_eval() per la sola valutazione sicura di strutture dati e letterali matematici. Per la formattazione di stringhe, separare la maschera di formato dall'input utente mediante formattazione parametrizzata rigida o template statici fissi.
