# 📖 Scheda Operativa: 01_single_byte_xor

## 1. QUANDO USARE QUESTO SCRIPT (30 Secondi)
* **Scenario:** Challenge con stringa cifrata in esadecimale/byte.
* **Criterio:** Cifratura XOR con chiave di 1 solo byte ($0 \le K \le 255$).
* **Input Noto:** Prefisso noto della flag (es. `flag{`, `CTF{`).

---

## 2. VARIABILI DA MODIFICARE IN SEDE D'ESAME
1. `HEX_CIPHERTEXT = "..."`: Incolla il ciphertext della traccia.
2. `KNOWN_PREFIX = "flag{"`: Modifica solo se il prefisso è diverso.

---

## 3. WRITE-UP TEORICO MODELLO (Da personalizzare)

### 1. Vulnerabilità e Modello Teorico
Il meccanismo di cifratura è un cifrario a sostituzione monoalfabetica XOR a singolo byte ($C_i = P_i \oplus K$).
Il sistema presenta due vulnerabilità:
- **Key Space Ridotto:** $K \in [0, 255]$ ($2^8 = 256$ combinazioni), soggetto a Brute-force.
- **Known-Plaintext Attack (KPA):** Sfruttando la proprietà involutiva dello XOR ($A \oplus B = C \iff A \oplus C = B$) e il prefisso noto `flag{`, la chiave si ricava direttamente: $K = C_0 \oplus P_0$.

### 2. Approccio e Script
Eseguito lo script `01_single_byte_xor.py`:
1. Isolato il primo byte $C_0$ e associato a $P_0 = \text{'f'}$.
2. Calcolata la chiave $K = C_0 \oplus P_0$.
3. Decifrato l'intero messaggio applicando $K$ via XOR.

### 3. Remediation
- Adottare cifrari simmetrici sicuri come AES-256-GCM con IV univoco.
- Se si usa XOR, la chiave deve essere lunga quanto il messaggio, generata da un CSPRNG e usata una sola volta (One-Time Pad).
