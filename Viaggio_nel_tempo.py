#!/usr/bin/env python3
"""
===============================================================================
SWISS ARMY KNIFE: PRNG SEED REVERSING & TIME-BASED PRNG ATTACK (CTF / ESAME)
===============================================================================
QUANDO USARLO:
 1. Il codice sorgente dell'esame usa `random.seed(...)` con `time.time()`.
 2. Il cifrario genera la chiave tramite `random.randint()` o `random.randrange()`.
 3. Hai una parte del cifrato di cui conosci la chiave fissa o il testo in chiaro
    (es. un timestamp leak, una costante XOR come 0x88, o il prefisso della flag).

PRINCIPIO:
 `random` di Python (Mersenne Twister) NON è crittograficamente sicuro.
 Se conosci o recuperi il SEED, puoi rigenerare la CHIAVE IDENTICA.
===============================================================================
"""

import base64
import random
import time


def parse_input(data_str: str, encoding: str = "raw") -> bytes:
    """Converte la traccia in byte grezzi."""
    data_str = data_str.strip()
    if encoding == "base64":
        return base64.b64decode(data_str)
    elif encoding == "hex":
        return bytes.fromhex(data_str)
    return data_str.encode("utf-8") if isinstance(data_str, str) else data_str


# =============================================================================
# SCENARIO A: TIMESTAMP RECOVERY DA FIXED-KEY LEAK (Caso dell'esercizio)
# =============================================================================
def solve_with_leaked_timestamp(secret_ciphertext: bytes, fixed_mask: int = 0x88):
    print("\n--- [SCENARIO A] Decifratura tramite Timestamp Leak ---")

    # Si ipotizza che la lunghezza del timestamp float string (es: "1672531199.123456") sia ~18 byte
    # Modificare LEN_TIMESTAMP se la traccia usa time.time() intero (10 byte) o float diverso
    LEN_TIMESTAMP = 18

    # 1. Isoliamo la porzione finale contenente il timestamp cifrato
    encrypted_time = secret_ciphertext[-LEN_TIMESTAMP:]
    encrypted_body = secret_ciphertext[:-LEN_TIMESTAMP]

    # 2. Recuperiamo il timestamp originale eseguendo lo XOR con la maschera nota (es. 0x88)
    recovered_time_bytes = bytes([b ^ fixed_mask for b in encrypted_time])
    print(f"[*] Timestamp recuperato (Raw) : {recovered_time_bytes}")

    # 3. Ripristiniamo il PRNG con il seed estratto
    random.seed(recovered_time_bytes)

    # 4. Rigeneriamo il keystream ed eseguiamo la decifratura
    keystream = bytes([random.randrange(256) for _ in range(len(encrypted_body))])
    plaintext = bytes([c ^ k for c, k in zip(encrypted_body, keystream)])

    print(
        f"[+] FLAG TROVATA : {plaintext.decode('utf-8', errors='ignore')}"
    )


# =============================================================================
# SCENARIO B: BRUTEFORCE DEL SEED TEMPORALE (Se il timestamp non è cifrato nel messaggio)
# =============================================================================
def solve_with_time_bruteforce(
    ciphertext: bytes, approx_timestamp: int, window_seconds: int = 3600
):
    print("\n--- [SCENARIO B] Bruteforce Seed Temporale (Finestra di tempo) ---")

    prefix_known = b"FLAG{"  # Modificare col prefisso noto d'esame

    # Prova tutti i secondi nell'intervallo attorno all'orario approssimativo
    start_t = approx_timestamp - window_seconds
    end_t = approx_timestamp + window_seconds

    for t in range(start_t, end_t):
        # 1. Prova il timestamp come intero o stringa (a seconda di come la traccia ha impostato il seed)
        seed_candidate = str(t).encode("ascii")
        random.seed(seed_candidate)

        # 2. Genera i primi byte di chiave per verificare se il prefisso della flag combacia
        candidate_key = bytes([random.randrange(256) for _ in range(len(prefix_known))])
        test_plain = bytes([c ^ k for c, k in zip(ciphertext[: len(prefix_known)], candidate_key)])

        if test_plain == prefix_known:
            print(f"[+] Seed Trovato! Timestamp: {t}")
            # Rigenera per l'intero messaggio
            random.seed(seed_candidate)
            full_key = bytes([random.randrange(256) for _ in range(len(ciphertext))])
            decrypted = bytes([c ^ k for c, k in zip(ciphertext, full_key)])
            print(f"[+] FLAG TROVATA : {decrypted.decode('utf-8', errors='ignore')}")
            return

    print("[!] Nessun seed valido trovato nell'intervallo.")


# =============================================================================
# MAIN ESECUZIONE
# =============================================================================
if __name__ == "__main__":
    # Carica i byte del file cifrato d'esame
    # Esempio: con open("top_secret", "rb") as f: secret_data = f.read()
    
    # Esecuzione Risolutore per Scenario A
    # solve_with_leaked_timestamp(secret_data, fixed_mask=0x88)
    pass
