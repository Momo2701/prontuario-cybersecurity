#!/usr/bin/env python3
"""
PRONTUARIO #01: Single-Byte XOR Decryptor & Brute-Force
------------------------------------------------------
Uso:
1. Inserisci la stringa hex cifrata in `HEX_CIPHERTEXT`.
2. Se conosci un prefisso (es. 'flag{'), imposta `KNOWN_PREFIX`.
3. Esegui lo script: `python3 01_single_byte_xor.py`
"""

# ==================== INPUT DATI D'ESAME ====================
HEX_CIPHERTEXT = "302a27212d7b303c277b212f3b3337"  # Inserisci qui l'hex
KNOWN_PREFIX = "flag{"                          # Inserisci il prefisso se noto (oppure "")
# ============================================================


def xor_with_key(data: bytes, key_byte: int) -> str:
    """Esegue lo XOR tra ogni byte e la chiave indicata."""
    res = []
    for b in data:
        res.append(chr(b ^ key_byte))
    return "".join(res)


def main():
    ciphertext_bytes = bytes.fromhex(HEX_CIPHERTEXT)

    print("[*] Analisi Single-Byte XOR in corso...\n")

    # METODO A: Se conosciamo il prefisso della flag (es. 'flag{')
    if KNOWN_PREFIX:
        # Troviamo la chiave facendo XOR tra il 1° byte e il 1° carattere del prefisso
        key = ciphertext_bytes[0] ^ ord(KNOWN_PREFIX[0])
        plaintext = xor_with_key(ciphertext_bytes, key)

        print("=== RESULT (Metodo Prefisso Noto) ===")
        print(f"Chiave trovata : {hex(key)} (Decimale: {key})")
        print(f"Flag Decifrata : {plaintext}")
        print("=====================================\n")

    # METODO B: Brute-Force su tutte le 256 chiavi (0-255)
    print("=== RESULT (Brute-Force Matching 'flag{') ===")
    found = False
    for k in range(256):
        candidate = xor_with_key(ciphertext_bytes, k)
        if "flag{" in candidate or "CTF{" in candidate:
            print(f"[+] Chiave {hex(k)} (dec {k:3d}) -> {candidate}")
            found = True

    if not found and not KNOWN_PREFIX:
        print("[!] Nessuna corrispondenza automatica. Mostro prime 10 decifrature:")
        for k in range(10):
            print(f"Key {hex(k)}: {xor_with_key(ciphertext_bytes, k)}")


if __name__ == "__main__":
    main()
