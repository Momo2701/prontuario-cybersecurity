import base64

def convert_b64_to_hex(b64_string: str) -> str:
    """Converte una stringa Base64 in formato esadecimale."""
    return base64.b64decode(b64_string).hex()

def convert_hex_to_b64(hex_string: str) -> str:
    """Converte una stringa esadecimale in Base64."""
    return base64.b64encode(bytes.fromhex(hex_string)).decode('utf-8')

# Esempio d'uso rapido da terminale o script:
# cipher_hex = convert_b64_to_hex("PzUmJDezFTRRAKXKxkXHB0ra0YEAcSOcQALM1U")
