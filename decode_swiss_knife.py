#!/usr/bin/env python3
import base64
import re
from urllib.parse import unquote


ENCODED = "ltctfd{p-peye-mp-raee-ieu}"
KEY = "tellmewhy"


def decode_vigenere(text: str, key: str, *, key_advances_on_symbols: bool = True) -> str:
    """Decode a Vigenere-style cipher over ASCII letters."""
    if not key or not key.isascii() or not key.isalpha():
        raise ValueError("La chiave deve contenere solo lettere ASCII.")

    decoded = []
    key_index = 0
    normalized_key = key.lower()

    for char in text:
        if "a" <= char.lower() <= "z" and char.isascii():
            shift = ord(normalized_key[key_index % len(normalized_key)]) - ord("a")
            plain = chr((ord(char.lower()) - ord("a") - shift) % 26 + ord("a"))
            decoded.append(plain.upper() if char.isupper() else plain)
            key_index += 1
        else:
            decoded.append(char)
            if key_advances_on_symbols:
                key_index += 1

    return "".join(decoded)


def rot(text: str, amount: int) -> str:
    def rotate_char(char: str) -> str:
        if "a" <= char <= "z":
            return chr((ord(char) - ord("a") + amount) % 26 + ord("a"))
        if "A" <= char <= "Z":
            return chr((ord(char) - ord("A") + amount) % 26 + ord("A"))
        return char

    return "".join(rotate_char(char) for char in text)


def atbash(text: str) -> str:
    def mirror(char: str) -> str:
        if "a" <= char <= "z":
            return chr(ord("z") - (ord(char) - ord("a")))
        if "A" <= char <= "Z":
            return chr(ord("Z") - (ord(char) - ord("A")))
        return char

    return "".join(mirror(char) for char in text)


def decode_hex(text: str) -> bytes:
    return bytes.fromhex(re.sub(r"\s+", "", text))


def decode_binary(text: str) -> bytes:
    bits = re.sub(r"\s+", "", text)
    if not bits or re.search(r"[^01]", bits) or len(bits) % 8:
        raise ValueError("Il binario deve contenere gruppi completi di 8 bit.")
    return bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8))


def decode_base64(text: str) -> bytes:
    return base64.b64decode(text, validate=True)


def decode_xor_repeating(data: bytes, key: bytes) -> bytes:
    if not key:
        raise ValueError("La chiave XOR non può essere vuota.")
    return bytes(value ^ key[i % len(key)] for i, value in enumerate(data))


def decode_seeded_xor(text: str, seed: int, low: int = 50, high: int = 100) -> str:
    """Decode character-wise XOR using NumPy's legacy seeded random sequence."""
    import numpy as np

    masks = np.random.RandomState(seed).randint(low, high, size=len(text))
    return "".join(chr(ord(char) ^ int(mask)) for char, mask in zip(text, masks))


def bruteforce_seeded_xor(
    text: str,
    seeds: range,
    known_text: str,
    low: int = 50,
    high: int = 100,
) -> tuple[int, str] | None:
    """Find a seed whose decoded text contains known_text."""
    if not known_text:
        raise ValueError("Il testo noto non può essere vuoto.")
    if len(known_text) > len(text):
        return None

    for seed in seeds:
        decoded = decode_seeded_xor(text, seed, low, high)
        if known_text in decoded:
            return seed, decoded
    return None


MORSE = {
    ".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E",
    "..-.": "F", "--.": "G", "....": "H", "..": "I", ".---": "J",
    "-.-": "K", ".-..": "L", "--": "M", "-.": "N", "---": "O",
    ".--.": "P", "--.-": "Q", ".-.": "R", "...": "S", "-": "T",
    "..-": "U", "...-": "V", ".--": "W", "-..-": "X", "-.--": "Y",
    "--..": "Z", "-----": "0", ".----": "1", "..---": "2",
    "...--": "3", "....-": "4", ".....": "5", "-....": "6",
    "--...": "7", "---..": "8", "----.": "9",
}


def decode_morse(text: str) -> str:
    words = text.strip().split(" / ")
    return " ".join(
        "".join(MORSE[letter] for letter in word.split())
        for word in words
    )


def show_bytes(label: str, data: bytes) -> None:
    print(f"{label} (hex): {data.hex()}")
    try:
        print(f"{label} (testo): {data.decode('utf-8')}")
    except UnicodeDecodeError:
        print(f"{label}: non è testo UTF-8 valido")


if __name__ == "__main__":
    # Variante dell'esercizio: la chiave avanza anche sui simboli.
    print("Vigenere dell'esercizio:", decode_vigenere(ENCODED, KEY))

    # Per un Vigenere classico, in cui la chiave avanza solo sulle lettere:
    # print("Vigenere classico:", decode_vigenere(ENCODED, KEY, key_advances_on_symbols=False))

    # Per provare tutte le rotazioni di Cesare:
    # for shift in range(26):
    #     print(f"ROT-{shift:02}:", rot(ENCODED, -shift))

    # Altri decoder: sostituire ENCODED con il testo/codice corrispondente.
    # print("Atbash:", atbash(ENCODED))
    # print("URL:", unquote(ENCODED))
    # print("Morse:", decode_morse(ENCODED))
    # show_bytes("Base64", decode_base64(ENCODED))
    # show_bytes("Esadecimale", decode_hex(ENCODED))
    # show_bytes("Binario", decode_binary(ENCODED))
    # show_bytes("XOR", decode_xor_repeating(bytes.fromhex(ENCODED), KEY.encode("utf-8")))

    # XOR con maschera pseudo-casuale e seed noto/sconosciuto (richiede NumPy).
    # CIPHER = open("message.txt", encoding="utf-8").read()
    # match = bruteforce_seeded_xor(CIPHER, range(3500), "spritzCTF{")
    # print(f"Seed: {match[0]}\nTesto: {match[1]}" if match else "Seed non trovato")
