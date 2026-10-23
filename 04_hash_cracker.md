# 📖 Scheda Operativa: 04_hash_cracker

## 1. QUANDO USARE QUESTO SCRIPT (30 Secondi)
* **Scenario:** Challenge che fornisce un digest esadecimale (MD5, SHA-1, SHA-256) derivato da una stringa priva di salt.
* **Criterio:** Si conosce la struttura o maschera fissa del plaintext (es. `flag{XXXX}` con $X \in [0-9]$ o caratteri alfanumerici brevi).
* **Input Noto:** L'hash target e il formato della stringa da ricostruire.

---

## 2. VARIABILI DA MODIFICARE IN SEDE D'ESAME
1. `TARGET_HASH = "..."`: Incolla l'hash esadecimale estratto dalla traccia o dal database.
2. `HASH_TYPE = "md5"`: Impostare `"md5"`, `"sha1"` o `"sha256"` in base all'algoritmo impiegato.
3. `PREFIX = "flag{"` e `SUFFIX = "}"`: Definire le parti fisse della stringa in chiaro.
4. `CHARSET = string.digits`: Selezionare l'alfabeto di ricerca (`string.digits`, `string.ascii_lowercase`, o una stringa personalizzata).
5. `PATTERN_LENGTH = 4`: Specificare il numero di caratteri sconosciuti da generare.

---

## 3. WRITE-UP TEORICO MODELLO (Da personalizzare)

### 1. Vulnerabilità e Modello Teorico
L'applicazione memorizza o autentica segreti tramite una funzione di hashing non salata (Unsalted Hash).

La procedura soffre di due vulnerabilità strutturali critiche:
1. **Assenza di Salt:** L'assenza di un valore casuale univoco concatenato all'input rende la trasformazione $H(m)$ deterministica, consentendo attacchi basati su ricerca combinatoria o tabelle precalcolate (Rainbow Tables).
2. **Compromissione della Resistenza alla Preimmagine via Pattern Truncation:** La proprietà matematico-crittografica di Resistenza alla Preimmagine (impossibilità di ricavare $m$ dato $H(m)$) viene invalidata dalla conoscenza della struttura del plaintext. La maschera `flag{XXXX}` con $k$ caratteri incogniti riduce lo spazio delle chiavi ad un insieme finito di $|C|^k$ combinazioni (es. $10^4 = 10.000$ per 4 cifre numeriche).

La complessità per l'inversione passa da un dominio esponenziale inaffrontabile ad una ricerca esaustiva istantanea di complessità $\mathcal{O}(|C|^k)$.

### 2. Approccio e Payload/Script
Per la risoluzione è stato eseguito lo script di prontuario `04_hash_cracker.py`.

Procedura operativa applicata:
1. Impostata la stringa di hash target ed identificato l'algoritmo di compressione (es. MD5).
2. Configurato il generatore combinatorio su $k$ posizioni con il set di caratteri opportuno (`itertools.product`).
3. Calcolato l'hash di ogni candidato formattato secondo la maschera definita e confrontato il digest risultante con l'hash target fino al rilevamento della corrispondenza.

### 3. Remediation / Hardening
Per mettere in sicurezza la memorizzazione di credenziali e segreti:
- Sostituire le funzioni di hashing generiche e veloci (MD5, SHA-1, SHA-256) con funzioni di Password Hashing volutamente lenti ed ad alta occupazione di memoria (*key stretching*), come Argon2id, bcrypt o PBKDF2.
- Introdurre un Salt crittografico univoco per ciascun utente/record (lunghezza $\ge 16$ byte generato tramite CSPRNG) concatenato all'input prima del calcolo ($H(m \mathbin{\Vert} \text{salt})$), rendendo inefficaci gli attacchi combinatori e il riuso di dizionari precalcolati.
