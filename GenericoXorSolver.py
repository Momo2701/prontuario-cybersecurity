# -------------------------------------------------
# GENERIC SOLVER FOR XOR-BASED CHALLENGE
# -------------------------------------------------
# Idea:
#   - leggi il file con il testo cifrato
#   - prova tutte le chiavi possibili
#   - decifra con XOR
#   - controlla se il risultato ha senso
#   - se trovi un testo leggibile, hai trovato la flag
# -------------------------------------------------

def xor_decode(text, key):
    """
    Decifra un testo cifrato con XOR usando una singola chiave.
    Se il testo originale è m, il cifrato è c = m ^ key
    Quindi per decifrare: m = c ^ key
    """
    return "".join(chr(ord(ch) ^ key) for ch in text)


def is_likely_plaintext(text):
    """
    Verifica se il testo decifrato sembra "leggibile".
    Non è perfetto, ma per challenge di CTF è molto utile.
    """
    if not text:
        return False

    printable = 0
    for ch in text:
        if ch.isprintable() or ch in "\n\r\t":
            printable += 1

    ratio = printable / len(text)

    # Se il testo contiene una flag/chiave/marker, è molto probabile
    lower = text.lower()
    flags = ["spritzctf{", "flag{", "ctf{", "secret", "password"]

    has_flag_like_marker = any(marker in lower for marker in flags)

    # Un testo "normale" ha alta percentuale di caratteri stampabili
    return ratio > 0.85 and (has_flag_like_marker or any(ch.isalpha() for ch in text))


def solve_xor_challenge(file_path, max_key=256, target_prefix="spritzCTF{"):
    """
    Trova la chiave giusta provando tutte le chiavi da 0 a max_key-1.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        cipher = f.read()

    for key in range(max_key):
        decoded = xor_decode(cipher, key)

        if is_likely_plaintext(decoded):
            lower_decoded = decoded.lower()
            if target_prefix.lower() in lower_decoded or "{" in decoded:
                print(f"Chiave trovata: {key}")
                print("Testo decifrato:")
                print(decoded)
                return decoded, key

    print("Nessuna chiave plausibile trovata.")
    return None, None


# -------------------------------------------------
# ESEMPIO D'USO
# -------------------------------------------------
if __name__ == "__main__":
    result, key = solve_xor_challenge("message.txt", max_key=256, target_prefix="spritzCTF{")
