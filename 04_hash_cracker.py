#!/usr/bin/env python3
"""
PRONTUARIO #04: Unsalted Hash Cracker (MD5 / SHA-1 / SHA-256)
------------------------------------------------------------
Modulo: Crittografia / Hash Cracking & Pattern Brute-Force
Descrizione: Inversione di hash non salati tramite generazione combinatoria 
            su pattern noto (es. flag{NUMERO_4_DIGIT}) o lista di candidati.
"""

import hashlib
import itertools
import string

# ==================== INPUT DATI D'ESAME ====================
# Sostituire con l'hash esadecimale fornito dalla traccia
TARGET_HASH = "c81e728d9d4c2f636f067f89cc14862c"

# Algoritmo da utilizzare: "md5", "sha1", "sha256"
HASH_TYPE = "md5"

# Definizione del pattern di ricerca
PREFIX = "flag{"
SUFFIX = "}"
CHARSET = string.digits  # Alphabeto: string.digits ('0-9'), string.ascii_lowercase, etc.
PATTERN_LENGTH = 4       # Numero di caratteri sconosciuti
# ============================================================


def compute_hash(text: str, algo: str) -> str:
    """Calcola l'hash della stringa fornita usando l'algoritmo specificato."""
    data = text.encode('utf-8')
    algo_lower = algo.lower()

    if algo_lower == "md5":
        return hashlib.md5(data).hexdigest()
    elif algo_lower == "sha1":
        return hashlib.sha1(data).hexdigest()
    elif algo_lower == "sha256":
        return hashlib.sha256(data).hexdigest()
    else:
        raise ValueError(f"Algoritmo non supportato: {algo}")


def main():
    target = TARGET_HASH.lower().strip()
    print(f"[*] Avvio Hash Cracker per algoritmo: {HASH_TYPE.upper()}")
    print(f"[*] Hash Target : {target}")
    print(f"[*] Pattern     : {PREFIX}{'X'*PATTERN_LENGTH}{SUFFIX}\n")

    found = False
    # Genera tutte le combinazioni possibili
    for combination in itertools.product(CHARSET, repeat=PATTERN_LENGTH):
        candidate_middle = "".join(combination)
        candidate_plain = f"{PREFIX}{candidate_middle}{SUFFIX}"

        candidate_hash = compute_hash(candidate_plain, HASH_TYPE)

        if candidate_hash == target:
            print("=== HASH CRACCATO CON SUCCESSO! ===")
            print(f" Plaintext Trovato  : {candidate_plain}")
            print(f" Hash Corrispondente : {candidate_hash}")
            print("===================================")
            found = True
            break

    if not found:
        print("[!] Nessuna corrispondenza trovata. Verificare HASH_TYPE, CHARSET o PATTERN_LENGTH.")


if __name__ == "__main__":
    main()
