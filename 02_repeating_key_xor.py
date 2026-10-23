#!/usr/bin/env python3
"""
PRONTUARIO #02: Repeating-Key XOR (Vigenère-XOR) Decrypter
-----------------------------------------------------------
Modulo: Crittografia / XOR & Cifrari Classici
Descrizione: Estrazione automatica della chiave e decifrazione per cifrari XOR 
            a chiave ripetuta tramite Known-Plaintext Attack (KPA) sul prefisso.
"""

import itertools

# ==================== INPUT DATI D'ESAME ====================
# Sostituire con il ciphertext esadecimale fornito dalla traccia
HEX_CIPHERTEXT = "2529384634331c511e2425482522064a1e3406592433064c26362544393424"

# Sostituire con il prefisso noto della flag (es. "flag{", "CTF{", "UNIPD{")
KNOWN_PREFIX = "flag{"

# Lunghezza stimata/nota della chiave in byte
KEY_LENGTH = 4
# ============================================================


def repeating_key_xor(data_bytes: bytes, key_bytes: bytes) -> bytes:
    """Applica lo XOR a chiave ripetuta tra i dati forniti e la chiave."""
    key_stream = itertools.cycle(key_bytes)
    return bytes([b ^ k for b, k in zip(data_bytes, key_stream)])


def derive_key_from_prefix(c_bytes: bytes, prefix: str, key_len: int) -> bytes:
    """Ricava i byte della chiave usando i caratteri noti del prefisso."""
    prefix_bytes = prefix.encode('utf-8')
    key = bytearray(key_len)
    
    # Ricaviamo i byte della chiave fino alla lunghezza key_len
    for i in range(min(len(prefix_bytes), key_len)):
        key[i] = c_bytes[i] ^ prefix_bytes[i]
        
    return bytes(key)


def main():
    c_bytes = bytes.fromhex(HEX_CIPHERTEXT)
    print(f"[*] Dimensione Ciphertext: {len(c_bytes)} byte")
    print(f"[*] Estrazione chiave per lunghezza L = {KEY_LENGTH}...")

    # 1. Calcolo della chiave dal prefisso noto
    derived_key = derive_key_from_prefix(c_bytes, KNOWN_PREFIX, KEY_LENGTH)
    key_str = "".join([chr(k) if 32 <= k <= 126 else f"\\x{k:02x}" for k in derived_key])
    
    print(f"[+] Chiave estratta (Hex)  : {derived_key.hex()}")
    print(f"[+] Chiave estratta (ASCII): '{key_str}'\n")

    # 2. Decifrazione del messaggio
    plaintext_bytes = repeating_key_xor(c_bytes, derived_key)
    plaintext_str = plaintext_bytes.decode('utf-8', errors='ignore')

    print("=== DECODIFICA COMPLETATA ===")
    print(f" Flag Decifrata: {plaintext_str}")
    print("=============================")


if __name__ == "__main__":
    main()
