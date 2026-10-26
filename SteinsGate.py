#!/usr/bin/env python3
"""
===============================================================================
SWISS ARMY KNIFE: XOR & KNOWN-PLAINTEXT ATTACK (CTF / ESAME)
===============================================================================
QUANDO USARLO:
 1. La traccia dice che il cifrario è "XOR" o usa il simbolo '^'.
 2. Hai una flag cifrata in Base64, Hex o Raw Bytes.
 3. Hai un esempio "Testo Chiaro <-> Testo Cifrato" (Known-Plaintext Attack).
 4. Conosci il formato/prefisso della flag (es. "SPRITZ{", "FLAG=", "CTF{")
    anche senza avere l'esempio completo.
 5. La chiave è riusata per cifrare più messaggi (Reuse of OTP / Stream Cipher).

PROPRIETÀ FONDAMENTALE DI XOR:
 Cifratura : Plaintext  ^ Key       = Ciphertext
 Decifratura: Ciphertext ^ Key       = Plaintext
 Attacco    : Plaintext  ^ Ciphertext = Key
===============================================================================
"""

import base64


# =============================================================================
# UTILITY DI DECODIFICA (MODIFICA QUI IN BASE AL FORMATO DELLA TRACCIA)
# =============================================================================
def parse_input(data_str: str, encoding: str = "base64") -> bytes:
    """
    Converte la stringa della traccia in byte grezzi.
    Scegli 'encoding' in base a come ti viene dato il dato d'esame:
      - "base64" : es. "IFhiPhZNYi0K..."
      - "hex"    : es. "2076223e16..."
      - "raw"    : es. "stringa standard"
    """
    data_str = data_str.strip()
    if encoding == "base64":
        return base64.b64decode(data_str)
    elif encoding == "hex":
        return bytes.fromhex(data_str)
    elif encoding == "raw":
        return data_str.encode("utf-8")
    else:
        raise ValueError(f"Encoding non supportato: {encoding}")


def xor_bytes(b1: bytes, b2: bytes) -> bytes:
    """
    Esegue lo XOR byte per byte tra due sequenze di byte.
    Se hanno lunghezze diverse, si ferma alla lunghezza del più corto (zip).
    """
    return bytes(x ^ y for x, y in zip(b1, b2))


def xor_repeating_key(data: bytes, key: bytes) -> bytes:
    """
    Esegue lo XOR applicando la chiave in modo CICLICO (modulo lunghezza chiave).
    Utile se la chiave è più corta del messaggio da decifrare.
    """
    return bytes(data[i] ^ key[i % len(key)] for i in range(len(data)))


# =============================================================================
# SCENARIO A: KNOWN-PLAINTEXT COMPLETO
# (Hai un esempio completo "Chiaro <-> Cifrato" e devi decifrare la Flag)
# =============================================================================
def attack_known_plaintext(orig_plain: bytes, enc_data: bytes, enc_flag: bytes):
    print("\n--- [SCENARIO A] Attacco Known-Plaintext Completo ---")

    # 1. Ricava la chiave: Plain ^ Cipher = Key
    key = xor_bytes(orig_plain, enc_data)
    print(f"[*] Chiave ricavata (Hex)   : {key.hex()}")
    print(f"[*] Chiave ricavata (Text)  : {key}")

    # 2. Decifra la flag usabile con la chiave trovata
    # Usiamo xor_repeating_key nel caso la flag sia più lunga della chiave
    decrypted_flag = xor_repeating_key(enc_flag, key)

    print(f"[+] Flag Decifrata (Raw)    : {decrypted_flag}")
    print(
        f"[+] FLAG FINALE (ASCII)     : {decrypted_flag.decode('utf-8', errors='ignore')}"
    )


# =============================================================================
# SCENARIO B: PREFISSO NOTO (KNOWN-PREFIX / CRADLE ATTACK)
# (Non hai l'esempio, ma sai che la flag inizia con es. "SPRITZ{" o "FLAG=")
# =============================================================================
def attack_known_prefix(enc_flag: bytes, known_prefix: str):
    print("\n--- [SCENARIO B] Attacco su Prefisso Noto ---")

    prefix_bytes = known_prefix.encode("utf-8")

    # Ricava i primi N byte della chiave sfruttando il prefisso noto
    partial_key = xor_bytes(enc_flag[: len(prefix_bytes)], prefix_bytes)
    print(f"[*] Prefisso provato        : {known_prefix}")
    print(f"[*] Parte di Chiave (Hex)   : {partial_key.hex()}")
    print(f"[*] Parte di Chiave (Text)  : {partial_key}")

    # Applica la chiave parziale ripetuta a tutta la flag
    decrypted_flag = xor_repeating_key(enc_flag, partial_key)
    print(
        f"[+] Decifratura parziale    : {decrypted_flag.decode('utf-8', errors='ignore')}"
    )


# =============================================================================
# MAIN / CONFIGURAZIONE DA MODIFICARE DURANTE L'ESAME
# =============================================================================
if __name__ == "__main__":
    # -------------------------------------------------------------------------
    # 1. CONFIGURA INPUT DELLA TRACCIA
    # -------------------------------------------------------------------------
    # Formato input: "base64", "hex", oppure "raw"
    INPUT_ENCODING = "base64"

    # Inserisci i dati della traccia
    RAW_ORIGINAL_PLAIN = "El Psy Congroo"
    RAW_ENCRYPTED_DATA = "IFhiPhZNYi0KWiUcCls="
    RAW_ENCRYPTED_FLAG = "I3gDKVh1Lh4EVyMDBFo="

    # Prefisso noto ipotetico se non hai l'esempio completo (Scenario B)
    KNOWN_FLAG_PREFIX = "FLAG="

    # -------------------------------------------------------------------------
    # 2. PARSING AUTOMATICO IN BYTES
    # -------------------------------------------------------------------------
    plain_bytes = parse_input(RAW_ORIGINAL_PLAIN, encoding="raw")
    enc_data_bytes = parse_input(RAW_ENCRYPTED_DATA, encoding=INPUT_ENCODING)
    enc_flag_bytes = parse_input(RAW_ENCRYPTED_FLAG, encoding=INPUT_ENCODING)

    # -------------------------------------------------------------------------
    # 3. ESECUZIONE ATTACCHI
    # -------------------------------------------------------------------------
    # Esegui Scenario A se hai l'esempio "Plain <-> Cipher"
    attack_known_plaintext(plain_bytes, enc_data_bytes, enc_flag_bytes)

    # Esegui Scenario B se vuoi tentare il recupero chiave solo dal prefisso della flag
    # attack_known_prefix(enc_flag_bytes, KNOWN_FLAG_PREFIX)
