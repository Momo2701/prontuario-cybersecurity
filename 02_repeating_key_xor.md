# 📖 Scheda Operativa: 02_repeating_key_xor

## 1. QUANDO USARE QUESTO SCRIPT (30 Secondi)
* **Scenario:** Challenge con testo cifrato in esadecimale/byte cifrato con chiave ripetuta (Vigenère-XOR).
* **Criterio Identificativo:** La chiave ha una lunghezza $L > 1$ byte (es. 3, 4, 8 byte) che si applica ciclicamente sul messaggio ($C_i = P_i \oplus K[i \bmod L]$).
* **Input Noto:** Si conosce un prefisso noto della flag (es. `flag{`, `CTF{`, `UNIPD{`) di lunghezza pari o superiore alla lunghezza della chiave $L$.

---

## 2. VARIABILI DA MODIFICARE IN SEDE D'ESAME
1. `HEX_CIPHERTEXT = "..."`: Incolla la stringa esadecimale cifrata fornita dalla traccia.
2. `KNOWN_PREFIX = "flag{"`: Modifica solo se il prefisso noto della flag è diverso (es. `CTF{`, `UNIPD{`).
3. `KEY_LENGTH = 4`: Imposta la lunghezza stimata o indicata della chiave $L$ (es. 4, 8).

---

## 3. WRITE-UP TEORICO MODELLO (Da personalizzare)

### 1. Vulnerabilità e Modello Teorico
L'applicazione utilizza un cifrario a sostituzione polialfabetica Repeating-Key XOR (Vigenère-XOR).
La trasformazione applicata sul byte $i$-esimo è definita dalla relazione algebrica:
C_i = P_i ⊕ K[i mod L]

dove L rappresenta la lunghezza della chiave periodica.

Il sistema soffre di debolezza strutturale dovuta al riuso del keystream:
1. **Periodicità della Chiave:** La chiave si ripete ciclicamente con periodo L sul testo in chiaro, rendendo l'algoritmo vulnerabile a Known-Plaintext Attacks (KPA).
2. **Derivazione Diretta dei Byte di Chiave:** Sfruttando la proprietà involutiva dello XOR ($A \oplus B = C \iff A \oplus C = B$) unitamente alla conoscenza del prefisso del testo in chiaro (es. "flag{") di lunghezza $\ge L$, ciascun byte di chiave $k_j$ (con $0 \le j < L$) si calcola direttamente mediante:
k_j = C_j ⊕ P_j

La conoscenza di L byte del testo in chiaro riduce la complessità computazionale dell'attacco da un'esplorazione combinatoria $\mathcal{O}(2^{8L})$ a un'estrazione deterministica $\mathcal{O}(L)$.

### 2. Approccio e Payload/Script
È stato impiegato lo script di prontuario `02_repeating_key_xor.py`.

Procedura operativa applicata:
1. Isolate le prime posizioni del ciphertext esadecimale $C$ e correlate con i corrispettivi byte del prefisso noto $P$ ("flag{").
2. Calcolati i singoli byte della chiave di lunghezza $L = [INSERISCI_LUNGHEZZA]$:
   k_j = C_j ⊕ P_j
   Ottenendo la chiave espressa in ASCII: "[INSERISCI_CHIAVE_ESTRATTA]" (es. "KEY!").
3. Verificata la periodicità della chiave sulle posizioni successive del prefisso ($C_{L} \oplus P_{L} = k_0$).
4. Applicata la chiave ciclica "[INSERISCI_CHIAVE_ESTRATTA]" su tutto il ciphertext via XOR per ricostruire l'intero plaintext in chiaro.

### 3. Remediation / Hardening
Per mettere in sicurezza la cifratura simmetrica:
- Sostituire il cifrario a chiave ripetuta con cifrari a blocchi standardizzati e provatamente sicuri, come AES-256 in modalità autenticata GCM o modalità CTR.
- Qualora si utilizzi un cifrario a flusso (Stream Cipher), garantire che la sequenza di cifratura sia generata da un generatore crittograficamente sicuro (CSPRNG) e non venga mai riutilizzata per più di un messaggio (One-Time Pad).
