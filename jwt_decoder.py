import base64
import json

payload_b64 = "eyJuYW1lIjoibWFydGluIiwiYWRtaW4iOnRydWUsImV4cGlyYXRpb24iOjE1MTYyMzkwMjIsImZsYWciOiJTUFJJVFp7QSBncm91cCBvZiBjcm93cyBpcyBjYWxsZWQgYSBNdXJkZXJ9In0"

# Aggiusta il padding Base64 per evitare errori di lunghezza
padded_b64 = payload_b64 + '=' * (-len(payload_b64) % 4)

decoded_bytes = base64.urlsafe_b64decode(padded_b64)
payload_json = json.loads(decoded_bytes.decode('utf-8'))

print(payload_json)
