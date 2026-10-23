#!/usr/bin/env python3
"""
PRONTUARIO #10: Multi-Stage Encoding & Classical Ciphers Solver
--------------------------------------------------------------
Modulo: Crittografia / Codifiche e Cifrari Classici
Descrizione: Script modulare per decodificare catene multi-stage (Base64, Hex,
            URL Decode, Reverse) e decifrare cifrari a spostamento (Caesar/ROT).
"""

import base64
import urllib.parse
import string

# ==================== INPUT DATI D'ESAME ====================
# Stringa codificata/cifrata iniziale estratta dalla traccia
ENCODED_DATA = "c3RyaW5nX2VuY29kZWRfdGVzdA=="
# ============================================================

def try_caesar(text: str):
    """Esegue il brute-force di tutti i possibili shift (0-25) per il cifrario di Cesare."""
    print("[*] --- Tentativi Cifrario di Cesare (ROT-N) ---")
    for shift in range(1, 26):
        decoded = []
        for char in text:
            if 'a' <= char <= 'z':
                decoded.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
            elif 'A' <= char <= 'Z':
                decoded.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
            else:
                decoded.append(char)
        result = "".join(decoded)
        if "flag" in result.lower() or "unipd" in result.lower():
            print(f"[+] SHIFT {shift} TROVATO: {result}")


def main():
    print(f"[*] Analisi stringa iniziale: {ENCODED_DATA}\n")
    current_data = ENCODED_DATA
    
    # 1. URL Unquote
    try:
        current_data = urllib.parse.unquote(current_data)
        print(f"[*] Dopo URL Decode : {current_data}")
    except Exception:
        pass

    # 2. Hex Decode (se applicabile)
    try:
        # Rimuove spazi o prefissi 0x se presenti
        clean_hex = current_data.strip().replace("0x", "")
        if all(c in string.hexdigits for c in clean_hex) and len(clean_hex) % 2 == 0:
            current_data = bytes.fromhex(clean_hex).decode('utf-8', errors='ignore')
            print(f"[*] Dopo Hex Decode : {current_data}")
    except Exception:
        pass

    # 3. Base64 Decode
    try:
        current_data = base64.b64decode(current_data).decode('utf-8', errors='ignore')
        print(f"[*] Dopo Base64 Decode: {current_data}")
    except Exception:
        pass

    # 4. Inversione di stringa (Reverse)
    print(f"[*] Inversione Stringa (Reverse): {current_data[::-1]}")

    # 5. Tentativo di Forza Bruta Cifrario Classico (Cesare)
    try_caesar(current_data)


if __name__ == "__main__":
    main()
