#!/usr/bin/env python3
"""
PRONTUARIO #03: Weak PRNG & Timestamp Seeding Recovery
------------------------------------------------------
Modulo: Crittografia / PRNG Weakness & Keystream Reuse
Descrizione: Attacco di re-seeding su generatore Mersenne Twister (random.py)
            con seed basato su timestamp UNIX (time.time()).
"""

import random

# ==================== INPUT DATI D'ESAME ====================
# Sostituire con il ciphertext esadecimale fornito dalla traccia
HEX_CIPHERTEXT = "411f2a3328312e2b380f2d251c142b2f"

# Timestamp UNIX indicativo dell'esecuzione (es. orario del server o dell'esame)
APPROX_TIMESTAMP = 1700000000

# Finestra temporale di ricerca in secondi (+/- 24 ore = 86400)
WINDOW_SECONDS = 86400

# Prefisso noto della flag per convalidare la decifrazione
KNOWN_PREFIX = "flag{"
# ============================================================


def decrypt_with_seed(ciphertext_bytes: bytes, seed_candidate: int) -> bytes:
    """Rigenera il flusso pseudo-casuale partendo dal seed e applica lo XOR."""
    random.seed(seed_candidate)
    plaintext = []
    for b in ciphertext_bytes:
        # Estrae l'esatto byte generato al momento della cifratura
        key_byte = random.randint(0, 255)
        plaintext.append(b ^ key_byte)
    return bytes(plaintext)


def main():
    c_bytes = bytes.fromhex(HEX_CIPHERTEXT)
    start_time = APPROX_TIMESTAMP - WINDOW_SECONDS
    end_time = APPROX_TIMESTAMP + WINDOW_SECONDS

    print(f"[*] Avvio Brute-Force sul Seed PRNG nell'intervallo timestamp:")
    print(f"    [{start_time} -> {end_time}]...\n")

    found = False
    for candidate_seed in range(start_time, end_time):
        candidate_pt = decrypt_with_seed(c_bytes, candidate_seed)
        
        # Verifica se l'output decifrato contiene il prefisso della flag
        if KNOWN_PREFIX.encode('utf-8') in candidate_pt:
            print("=== SEED TROVATO! ===")
            print(f" Timestamp Seed : {candidate_seed}")
            print(f" Flag Decifrata  : {candidate_pt.decode('utf-8', errors='ignore')}")
            print("=====================")
            found = True
            break

    if not found:
        print("[!] Nessun seed valido trovato nel range specificato. Ampliare WINDOW_SECONDS.")


if __name__ == "__main__":
    main()
