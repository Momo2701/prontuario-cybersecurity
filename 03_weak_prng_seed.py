#!/usr/bin/env python3
"""
PRONTUARIO #03: Weak PRNG & Timestamp Seeding Attack
---------------------------------------------------
Modulo: Crittografia / PRNG Weakness
Descrizione: Attacco di re-seeding su generatore Mersenne Twister (random.py)
            in presenza di seed basato su timestamp UNIX time.time().
"""

import random

# ==================== INPUT DATI D'ESAME ====================
HEX_CIPHERTEXT = "411f2a3328312e2b380f2d251c142b2f"
APPROX_TIMESTAMP = 1700000000  # Timestamp UNIX indicativo dell'esecuzione
WINDOW_SECONDS = 3600         # Finestra temporale di ricerca (+/- 1 ora)
KNOWN_PREFIX = "flag{"        # Prefisso noto per validare la decifrazione
# ============================================================


def decrypt_with_seed(ciphertext_bytes: bytes, seed_candidate: int) -> bytes:
    """Rigenera il flusso di byte casuali impostando il seed e applica lo XOR."""
    random.seed(seed_candidate)
    plaintext = []
    for b in ciphertext_bytes:
        key_byte = random.randint(0, 255)
        plaintext.append(b ^ key_byte)
    return bytes(plaintext)


def main():
    c_bytes = bytes.fromhex(HEX_CIPHERTEXT)
    start_time = APPROX_TIMESTAMP - WINDOW_SECONDS
    end_time = APPROX_TIMESTAMP + WINDOW_SECONDS

    print(f"[*] Avvio Brute-Force sul Seed PRNG nell'intervallo:")
    print(f"    [{start_time} -> {end_time}]...\n")

    found = False
    for candidate_seed in range(start_time, end_time):
        candidate_pt = decrypt_with_seed(c_bytes, candidate_seed)
        
        if KNOWN_PREFIX.encode() in candidate_pt:
            print("=== SEED TROVATO! ===")
            print(f" Timestamp Seed : {candidate_seed}")
            print(f" Flag Decifrata  : {candidate_pt.decode('utf-8', errors='ignore')}")
            print("=====================")
            found = True
            break

    if not found:
        print("[!] Nessun seed valido trovato. Amplia WINDOW_SECONDS.")


if __name__ == "__main__":
    main()
