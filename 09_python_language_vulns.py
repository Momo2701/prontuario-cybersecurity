#!/usr/bin/env python3
"""
PRONTUARIO #09: Python Language Vulnerabilities (eval() & Format String Tester)
-------------------------------------------------------------------------------
Modulo: Web & Language Security / Python Injection
Descrizione: Tester per la verifica di espressioni dinamiche (eval) e
            introspezione tramite format string su parametri HTTP.
"""

import requests

# ==================== INPUT DATI D'ESAME ====================
TARGET_URL = "http://127.0.0.1:5000/calc"  # URL dell'endpoint da testare
PARAM_NAME = "expr"                         # Nome del parametro GET/POST
METHOD = "GET"                              # Metodo HTTP: "GET" o "POST"

# TEST PAYLOADS
# 1. Test Aritmetico per eval(): se 7*7 restituisce 49, l'espressione viene valutata
EVAL_TEST = "7*7"

# 2. Test Introspezione per Format String: tenta di accedere a variabili di contesto
FORMAT_TEST = "{self.__class__}"
# ============================================================


def main():
    print(f"[*] Avvio verifica vulnerabilità Python su: {TARGET_URL}\n")
    
    # 1. Test di Valutazione Dinamica (eval)
    payload_eval = {PARAM_NAME: EVAL_TEST}
    try:
        if METHOD.upper() == "GET":
            res_eval = requests.get(TARGET_URL, params=payload_eval, timeout=5)
        else:
            res_eval = requests.post(TARGET_URL, data=payload_eval, timeout=5)
            
        if "49" in res_eval.text:
            print("[!] VULNERABILITÀ EVAL() RILEVATA: L'espressione '7*7' ha restituito '49'.")
        else:
            print("[-] Nessuna risposta aritmetica diretta da eval().")
    except Exception as e:
        print(f"[!] Errore durante il test eval(): {e}")

    # 2. Test di Introspezione (Format String)
    payload_format = {PARAM_NAME: FORMAT_TEST}
    try:
        if METHOD.upper() == "GET":
            res_format = requests.get(TARGET_URL, params=payload_format, timeout=5)
        else:
            res_format = requests.post(TARGET_URL, data=payload_format, timeout=5)

        if "<class" in res_format.text or "type" in res_format.text:
            print("[!] VULNERABILITÀ FORMAT STRING RILEVATA: Rivelato riferimento a classe/oggetto.")
        else:
            print("[-] Nessun riflesso di introspezione rilevato.")
    except Exception as e:
        print(f"[!] Errore durante il test Format String: {e}")


if __name__ == "__main__":
    main()
