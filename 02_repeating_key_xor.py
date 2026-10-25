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




#!/usr/bin/env python3
"""
PRONTUARIO #02: Decrypter Base64 (XOR / Cifrari Classici)
-----------------------------------------------------------
Modulo: Crittografia / XOR & Cifrari Classici
Descrizione: Decodifica di chiavi e ciphertext forniti in formato Base64
            ed esecuzione della decifrazione.
"""

import base64
import codecs
import itertools
import urllib.parse

# ==================== INPUT DATI D'ESAME ====================
# Chiave in Base64 ("Caesar\n")
B64_KEY = "Q2Flc2FyCg=="

# Ciphertext / Puzzle in Base64
B64_CIPHERTEXT = "RkNFVkdNJTdPRmhvZmd2Z2hndmJhJTVTcHZjdXJlZiU1U25lciU1U2FiZyU1U2ZycGhlciU3UQ=="
# ============================================================


def repeating_key_xor(data_bytes: bytes, key_bytes: bytes) -> bytes:
    """Applica lo XOR a chiave ripetuta tra i dati e la chiave."""
    key_stream = itertools.cycle(key_bytes)
    return bytes([b ^ k for b, k in zip(data_bytes, key_stream)])


def main():
    # 1. Decodifica dei dati da Base64
    key_bytes = base64.b64decode(B64_KEY).strip()
    c_bytes = base64.b64decode(B64_CIPHERTEXT)

    print(f"[*] Chiave Base64 Decodificata : '{key_bytes.decode('utf-8', errors='ignore')}'")
    print(f"[*] Ciphertext Raw (ASCII)     : {c_bytes.decode('utf-8', errors='ignore')}\n")

    # 2. Tentativo 1: XOR a chiave ripetuta
    xor_result = repeating_key_xor(c_bytes, key_bytes)
    print("--- Tentativo XOR a chiave ripetuta ---")
    print(f"Risultato XOR: {xor_result.decode('utf-8', errors='ignore')}\n")

    # 3. Interpretazione della chiave 'Caesar' (Cifrario di Cesare / ROT13 + URL Decode)
    # Se la chiave indichi il tipo di algoritmo ("Caesar"), si applica ROT13 e URL decoding
    cipher_text_str = c_bytes.decode('utf-8', errors='ignore')
    rot13_decoded = codecs.encode(cipher_text_str, 'rot_13')
    flag_final = urllib.parse.unquote(rot13_decoded)

    print("=== DECODIFICA COMPLETATA (ROT13 + URL-Decode) ===")
    print(f" Flag Decifrata: {flag_final}")
    print("==================================================")


if __name__ == "__main__":
    main()
