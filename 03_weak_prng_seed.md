# 📖 Scheda Operativa: 03_weak_prng_seed

## 1. QUANDO USARE QUESTO SCRIPT (30 Secondi)
* **Scenario:** Il codice sorgente fornito o l'analisi dell'applicazione mostrano l'uso del modulo `random` di Python inizializzato con `time.time()` o `int(time.time())`.
* **Criterio:** Il generatore pseudo-casuale non è crittograficamente sicuro (Mersenne Twister MT19937) e lo spazio delle chiavi è ridotto all'intervallo temporale di esecuzione del server.
* **Input Noto:** Un timestamp approssimativo dell'evento (es. orario della richiesta, intestazione HTTP `Date`) e il prefisso della flag (es. `flag{`).

---

## 2. VARIABILI DA MODIFICARE IN SEDE D'ESAME
1. `HEX_CIPHERTEXT = "..."`: Incolla la stringa cifrata in esadecimale fornita dalla traccia.
2. `APPROX_TIMESTAMP = 1700000000`: Impostare il timestamp UNIX approssimativo (in secondi) relativo all'ora di generazione della flag.
3. `WINDOW_SECONDS = 86400`: Ampiezza della finestra di ricerca attorno al timestamp (es. 86400 secondi = $\pm 24$ ore).
4. `KNOWN_PREFIX = "flag{"`: Modificare se il prefisso della flag è diverso (es. `CTF{`, `UNIPD{`).

---

## 3. WRITE-UP TEORICO MODELLO (Da personalizzare)

### 1. Vulnerabilità e Modello Teorico
Il sistema di cifratura impiega il modulo standard `random` di Python, basato sull'algoritmo Mersenne Twister (MT19937). 

La procedura presenta due gravi debolezze architetturali:
1. **Inidoneità Crittografica del PRNG:** MT19937 è un generatore di numeri pseudo-casuali (PRNG) deterministico privo di proprietà crittografiche. L'intera sequenza estratta dipende in modo univo dal valore iniziale (*seed*).
2. **Crollo dell'Entropia (Time-Based Seeding):** L'inizializzazione del generatore tramite `int(time.time())` riduce drasticamente lo spazio delle chiavi dal dominio teorico ad un insieme finito di $N$ secondi attorno all'istante di esecuzione.

La complessità dell'inversione passa da una ricerca esaustiva esponenziale ad una ricerca lineare deterministica $\mathcal{O}(N)$ nel dominio del tempo, consentendo un attacco di re-seeding ad altissima efficienza.

### 2. Approccio e Payload/Script
Per la risoluzione è stato eseguito lo script di prontuario `03_weak_prng_seed.py`.

Procedura operativa applicata:
1. Impostato il timestamp centrale stimato $t$ e definita una finestra temporale di ricerca $\Delta t$.
2. Eseguita l'iterazione per ogni candidato valore di seed $s \in [t - \Delta t, t + \Delta t]$.
3. Per ciascun candidato, è stato re-inizializzato il generatore con `random.seed(s)`, rigenerato il flusso di byte e applicata l'operazione XOR con il ciphertext.
4. Convalidata la corretta decifrazione mediante corrispondenza del prefisso noto `flag{`.

### 3. Remediation / Hardening
Per eliminare la vulnerabilità legata al PRNG temporale:
- Sostituire il modulo `random` con un generatore di numeri pseudo-casuali crittograficamente sicuro (CSPRNG), come il modulo `secrets` di Python o la chiamata di sistema `os.urandom()`.
- Per cifrare dati mediante operazioni XOR o cifrari a flusso, generare chiavi ed Initialization Vector (IV) attingendo da sorgenti di entropia hardware o di sistema incondizionate.
