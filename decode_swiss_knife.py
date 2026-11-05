#!/usr/bin/env python3
"""Small collection of encoders and decoders used by the CTF challenges."""

import argparse
import base64
import hashlib
import re
from urllib.parse import unquote


HASH_ALGORITHMS = (
    "md5",
    "sha1",
    "sha224",
    "sha256",
    "sha384",
    "sha512",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
)


def hash_text(text: str, algorithm: str) -> str:
    """Return a hashlib digest as hexadecimal."""
    try:
        digest = hashlib.new(algorithm)
    except ValueError as error:
        raise ValueError(f"Algoritmo hash non supportato: {algorithm}") from error
    digest.update(text.encode("utf-8"))
    return digest.hexdigest()


def sha256(text: str) -> str:
    """Return the SHA-256 digest of text as hexadecimal."""
    return hash_text(text, "sha256")


def rot(text: str, amount: int) -> str:
    def rotate(char: str, start: int) -> str:
        return chr((ord(char) - start + amount) % 26 + start)

    return "".join(
        rotate(char, ord("a") if char.islower() else ord("A"))
        if char.isascii() and char.isalpha() else char
        for char in text
    )


def atbash(text: str) -> str:
    return "".join(
        chr(ord("z") - ord(char) + ord("a")) if char.islower()
        else chr(ord("Z") - ord(char) + ord("A")) if char.isupper()
        else char
        for char in text
    )


def decode_vigenere(text: str, key: str, *, key_advances_on_symbols: bool = True) -> str:
    if not key or not key.isascii() or not key.isalpha():
        raise ValueError("La chiave deve contenere solo lettere ASCII.")

    decoded = []
    key_index = 0
    key = key.lower()
    for char in text:
        if char.isascii() and char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord("a")
            plain = chr((ord(char.lower()) - ord("a") - shift) % 26 + ord("a"))
            decoded.append(plain.upper() if char.isupper() else plain)
            key_index += 1
        else:
            decoded.append(char)
            if key_advances_on_symbols:
                key_index += 1
    return "".join(decoded)


def decode_hex(text: str) -> bytes:
    return bytes.fromhex(re.sub(r"\s+", "", text))


def decode_binary(text: str) -> bytes:
    bits = re.sub(r"\s+", "", text)
    if not bits or re.search(r"[^01]", bits) or len(bits) % 8:
        raise ValueError("Il binario deve contenere gruppi completi di 8 bit.")
    return bytes(int(bits[index:index + 8], 2) for index in range(0, len(bits), 8))


def decode_base64(text: str) -> bytes:
    return base64.b64decode(text, validate=True)


def decode_morse(text: str) -> str:
    morse = {
        ".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E",
        "..-.": "F", "--.": "G", "....": "H", "..": "I", ".---": "J",
        "-.-": "K", ".-..": "L", "--": "M", "-.": "N", "---": "O",
        ".--.": "P", "--.-": "Q", ".-.": "R", "...": "S", "-": "T",
        "..-": "U", "...-": "V", ".--": "W", "-..-": "X", "-.--": "Y",
        "--..": "Z", "-----": "0", ".----": "1", "..---": "2",
        "...--": "3", "....-": "4", ".....": "5", "-....": "6",
        "--...": "7", "---..": "8", "----.": "9",
    }
    return " ".join(
        "".join(morse[letter] for letter in word.split())
        for word in text.strip().split(" / ")
    )


def decode_xor_repeating(data: bytes, key: bytes) -> bytes:
    if not key:
        raise ValueError("La chiave XOR non può essere vuota.")
    return bytes(value ^ key[index % len(key)] for index, value in enumerate(data))


def decode_seeded_xor(text: str, seed: int, low: int = 50, high: int = 100) -> str:
    import numpy as np

    masks = np.random.RandomState(seed).randint(low, high, size=len(text))
    return "".join(chr(ord(char) ^ int(mask)) for char, mask in zip(text, masks))


def bruteforce_seeded_xor(
    text: str, seeds: range, known_text: str, low: int = 50, high: int = 100
) -> tuple[int, str] | None:
    if not known_text:
        raise ValueError("Il testo noto non può essere vuoto.")
    for seed in seeds:
        decoded = decode_seeded_xor(text, seed, low, high)
        if known_text in decoded:
            return seed, decoded
    return None


def show_bytes(label: str, data: bytes) -> None:
    print(f"{label} (hex): {data.hex()}")
    try:
        print(f"{label} (testo): {data.decode('utf-8')}")
    except UnicodeDecodeError:
        print(f"{label}: non è testo UTF-8 valido")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("value", help="Testo o valore da elaborare")
    parser.add_argument("operation", choices=(*HASH_ALGORITHMS, "url", "atbash", "rot"))
    parser.add_argument("--amount", type=int, default=13, help="Rotazione per rot")
    args = parser.parse_args()

    if args.operation in HASH_ALGORITHMS:
        print(hash_text(args.value, args.operation))
    elif args.operation == "url":
        print(unquote(args.value))
    elif args.operation == "atbash":
        print(atbash(args.value))
    else:
        print(rot(args.value, args.amount))


if __name__ == "__main__":
    main()
