#!/usr/bin/env python3
"""
PRONTUARIO #02: Repeating-Key XOR (Vigenère-XOR)
------------------------------------------------
Descrizione:
Decifrazione e attacco a cifrari XOR con chiave multi-byte ripetuta ciclicamente.

Uso in sede d'esame:
1. Inserisci la stringa esadecimale cifrata in `HEX_CIPHERTEXT`.
2. Se conosci la chiave, inseriscila in `KNOWN_KEY`.
3. Se conosci il prefisso (es. 'flag{'), lo script estrae automaticamente i primi byte della chiave.
"""

# ==================== INPUT DATI D'ESAME ====================
HEX_CIPHERTEXT = "252d35243a222a26312d2426261e2c2c330b2028242b24263e"
KNOWN_KEY = ""        # Se nota (es. "CAT" o "SECRET")
KNOWN_PREFIX = "flag{" # Prefisso noto per il ricavo algebrico della chiave
# ============================================================


def repeating_key_xor(ciphertext_bytes: bytes, key_bytes: bytes) -> str:
    """Decifra il testo cifrato riapplicando la chiave ciclicamente (chiave_len % i)."""
    plaintext = []
    key_len = len(key_bytes)
    for i, b in enumerate(ciphertext_bytes):
        k = key_bytes[i % key_len]
        plaintext.append(chr(b ^ k))
    return "".join(plaintext)


def derive_key_bytes(ciphertext_bytes: bytes, prefix: str) -> bytes:
    """Ricava i byte della chiave facendo XOR tra il ciphertext e il prefisso noto."""
    key_bytes = []
    for i in range(len(prefix)):
        key_bytes.append(ciphertext_bytes[i] ^ ord(prefix[i]))
    return bytes(key_bytes)


def main():
    c_bytes = bytes.fromhex(HEX_CIPHERTEXT)
    print("[*] Esecuzione Analisi Repeating-Key XOR...\n")

    # MODO A: Ricavo algebrico della chiave tramite prefisso noto
    if KNOWN_PREFIX:
        partial_key = derive_key_bytes(c_bytes, KNOWN_PREFIX)
        print("=== 1. RICAVO ALGEBRICO DELLA CHIAVE (Known-Plaintext) ===")
        print(f"I primi {len(KNOWN_PREFIX)} byte della chiave estratta:")
        print(f" -> Hex  : {partial_key.hex()}")
        print(f" -> ASCII: {partial_key.decode('utf-8', errors='replace')}")
        print(" -> NOTA: Identifica il pattern ripetuto nella stringa ASCII per isolare la chiave reale!\n")

    # MODO B: Decifrazione con chiave definita
    if KNOWN_KEY:
        k_bytes = KNOWN_KEY.encode('utf-8')
        plaintext = repeating_key_xor(c_bytes, k_bytes)
        print("=== 2. DECRYPT CON CHIAVE DEFINITA ===")
        print(f"Chiave usata: {KNOWN_KEY}")
        print(f"Flag/Plaintext: {plaintext}")


if __name__ == "__main__":
    main()
