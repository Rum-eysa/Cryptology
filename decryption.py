# decryption.py
from encryption import ALPHABET

def caesar_decrypt(text, shift):
    decrypted = ""
    for char in text.lower():
        if char in ALPHABET:
            idx = (ALPHABET.index(char) - shift) % len(ALPHABET)
            decrypted += ALPHABET[idx]
        else:
            decrypted += char
    return decrypted

def linear_decrypt():
    decrypted = ""
    return decrypted

def substitution_decrypt():
    decrypted = ""
    return decrypted

def permutation_decrypt():
    decrypted = ""
    return decrypted

def numberkey_decrypt():
    decrypted = ""
    return decrypted

def rota_decrypt():
    decrypted = ""
    return decrypted

def zikzak_decrypt():
    decrypted = ""
    return decrypted

def vigenere_decrypt():
    decrypted = ""
    return decrypted
