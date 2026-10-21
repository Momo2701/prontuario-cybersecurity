#!/usr/bin/env python3
"""
PRONTUARIO #04: Hash Cracker (MD5 / SHA-1 / SHA-256)
---------------------------------------------------
Modulo: Crittografia / Hash Cracking & Pattern Brute-Force
Descrizione: Inversione di hash non salati tramite brute-force di pattern
            o ricerca combinatoria.
"""

import hashlib
import string
import itertools

# ==================== INPUT DATI D'ESAME ====================
TARGET_HASH = "8d89e50882e3791e84a29a1f18501e51"  # Hash da craccare
HASH_TYPE = "md5"  # Opzioni: "md5", "sha1", "sha256"

# Definizione del Pattern della Flag (es. flag{NUMERO_4_DIGIT})
PREFIX = "flag{"
SUFFIX = "}"
CHARSET = string.digits  # string.digits = "0123456789"
PATTERN_LENGTH = 4       # Numero di caratteri sconosciuti nel pattern
# ============================================================


def compute_hash(text: str, algo: str) -> str:
    """Calcola l'hash della stringa fornita usando l'algoritmo specificato."""
    data = text.encode('utf-8')
    if algo.lower() == "md5":
        return hashlib.md5(data).hexdigest()
    elif algo.lower() == "sha1":
        return hashlib.sha1(data).hexdigest()
    elif algo.lower() == "sha256":
        return hashlib.sha256(data).hexdigest()
    return ""


def main():
    target = TARGET_HASH.lower().strip()
    print(f"[*] Avvio Hash Cracker per algoritmo: {HASH_TYPE.upper()}")
    print(f"[*] Hash Target : {target}")
    print(f"[*] Pattern     : {PREFIX}{'X'*PATTERN_LENGTH}{SUFFIX}\n")

    found = False
    # Genera tutte le combinazioni possibili per la lunghezza specificata
    for p in itertools.product(CHARSET, repeat=PATTERN_LENGTH):
        candidate_middle = "".join(p)
        candidate_plain = f"{PREFIX}{candidate_middle}{SUFFIX}"
        
        candidate_hash = compute_hash(candidate_plain, HASH_TYPE)
        
        if candidate_hash == target:
            print("=== HASH CRACCATO CON SUCCESSO! ===")
            print(f" Plaintext Trovato : {candidate_plain}")
            print(f" Hash Corrispondente: {candidate_hash}")
            print("===================================")
            found = True
            break

    if not found:
        print("[!] Nessuna corrispondenza trovata. Verifica HASH_TYPE o CHARSET.")


if __name__ == "__main__":
    main()
