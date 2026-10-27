#!/usr/bin/env python3
"""
PRONTUARIO: Client-Side Bypass & Request Forgery
"""

import requests

BASE = "http://localhost:8093"
URL = f"{BASE}/api/endpoint"


# ==============================================================================
# CASO 1: CUSTOM HEADERS
# ==============================================================================
# QUANDO USARLO:
# - Nel JS trovi: fetch("/api", { headers: { "X-Key": "...", "Authorization": "..." } })
# - I parametri o i token di autorizzazione sono inviati nelle intestazioni HTTP
#   e NON nel corpo della richiesta.
# ==============================================================================
def caso_1_headers():
    headers = {
        "X-Key": "DAJE"
    }
    
    r = requests.post(URL, headers=headers)
    print("[1] Risposta Headers:", r.text)


# ==============================================================================
# CASO 2: FORM DATA (data=)
# ==============================================================================
# QUANDO USARLO:
# - Nel JS trovi: fetch("/submit", { body: new URLSearchParams({ user: "...", level: ... }) })
# - C'è un form HTML standard o una richiesta "application/x-www-form-urlencoded"
# - Vuoi bypassare o modificare i valori dei campi (es. user="admin", level=9999).
# ==============================================================================
def caso_2_form_data():
    data = {
        "user": "admin",
        "level": 9999
    }
    
    r = requests.post(URL, data=data)
    print("[2] Risposta Form Data:", r.text)


# ==============================================================================
# CASO 3: JSON BODY (json=)
# ==============================================================================
# QUANDO USARLO:
# - Nel JS trovi: fetch("/api", { body: JSON.stringify({ user: "...", level: ... }) })
# - Nel JS c'è l'header: "Content-Type": "application/json"
# - L'endpoint backend accetta e processa un oggetto JSON.
# ==============================================================================
def caso_3_json_body():
    json_data = {
        "user": "admin",
        "level": 9999
    }
    
    r = requests.post(URL, json=json_data)
    print("[3] Risposta JSON Body:", r.text)


# ==============================================================================
# CASO 4: SESSIONE + ORIGIN / REFERER BYPASS
# ==============================================================================
# QUANDO USARLO:
# - Ricevi errori HTTP "403 Forbidden" o "405 Method Not Allowed" con i metodi sopra.
# - Il server verifica che la richiesta provenga dallo stesso dominio (Origin/Referer).
# - Il server richiede un cookie o un ID di sessione generato visitando prima la Home.
# ==============================================================================
def caso_4_sessione_e_origin():
    session = requests.Session()

    # 1. Visita la Home per ottenere eventuali cookie di sessione
    session.get(BASE)

    # 2. Emula gli header di sicurezza che il browser invia automaticamente con fetch()
    headers = {
        "X-Key": "DAJE",
        "Origin": BASE,
        "Referer": f"{BASE}/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    r = session.post(URL, headers=headers)
    print("[4] Risposta Sessione + Origin:", r.text)


if __name__ == "__main__":
    # Decommenta la funzione che ti serve in base alla struttura del JS:
    
    # caso_1_headers()
    # caso_2_form_data()
    # caso_3_json_body()
    # caso_4_sessione_e_origin()
    pass
