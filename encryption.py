# encryption.py
import random 
import math
import numpy as np
from numpy.linalg import inv


ALPHABET = "abcçdefgğhıijklmnoöprsştuüvyz"
EXTENDED = "qwx"

def caesar_encrypt(text, shift):

    encrypted = ""
    for char in text:
        lower_char = char.lower()
        if lower_char in ALPHABET:  # Sadece Türk alfabesindeki karakterleri işle
            idx = (ALPHABET.index(lower_char) + shift) % len(ALPHABET)
            new_char = ALPHABET[idx]
            encrypted += new_char.upper() if char.isupper() else new_char
    return encrypted

def linear_encrypt(text, a, b):
    
    encrypted = ""
    m = len(ALPHABET)  # 29 (Türk alfabesi)

    # Anahtar doğrulama
    def gcd(x, y):
        while y:
            x, y = y, x % y
        return x

    if gcd(a, m) != 1:
        raise ValueError("'a' parametresi 29 ile aralarında asal olmalıdır")

    # Sadece ALPHABET'teki karakterleri işle
    for char in text.lower():
        if char in ALPHABET:
            x = ALPHABET.index(char)
            encrypted_index = (a * x + b) % m
            encrypted += ALPHABET[encrypted_index]
    return encrypted


def substitution_encrypt(text, key_alphabet):
    
    # Anahtar kontrolü
    if len(key_alphabet) != len(ALPHABET):
        raise ValueError("Anahtar alfabe tam olarak 29 karakterden oluşmalıdır")
    
    # Sadece ALPHABET'teki karakterleri işle
    encrypted = []
    for char in text.lower():
        if char in ALPHABET:
            index = ALPHABET.index(char)
            encrypted.append(key_alphabet[index])
    
    return ''.join(encrypted)

def gcd(a, b):   #BU FONKSİYON DA YER DEĞİŞTİRMEYE DAHİL ASLINDA 
    while b:
        a, b = b, a % b
    return a

def permutation_encrypt(text, perm_str):
    try:
        # Permütasyon dizisini oluştur ve kontrol et
        perm = [int(p) for p in perm_str.strip().split()]
        block_size = len(perm)
        
        if sorted(perm) != list(range(1, block_size + 1)):
            raise ValueError("Geçersiz permütasyon! 1'den n'e kadar tüm sayılar olmalı.")
        
        # Metni temizle ve küçük harfe çevir
        clean_text = ''.join(ch.lower() for ch in text if ch.lower() in ALPHABET)
        
        # Eksik karakterleri rastgele doldur
        padding_length = (block_size - (len(clean_text) % block_size)) % block_size
        if padding_length > 0:
            clean_text += ''.join(random.choices(ALPHABET, k=padding_length))
        
        # Şifreleme işlemi
        encrypted = []
        for i in range(0, len(clean_text), block_size):
            block = clean_text[i:i+block_size]
            # Permütasyonu uygula: perm[j]-1 -> yeni pozisyon, j -> orijinal pozisyon
            permuted_block = [block[p-1] for p in perm]
            encrypted.append(''.join(permuted_block))
        
        return ''.join(encrypted)
    except Exception as e:
        raise ValueError(f"Şifreleme hatası: {str(e)}")
    
def numberkey_encrypt(text, key):
    
    # Anahtarın sayısal değerini al (sütun sayısı olarak kullan)
    try:
        num_cols = int(key)
    except ValueError:
        raise ValueError("Anahtar geçerli bir tam sayı olmalıdır")
    
    if num_cols <= 0:
        raise ValueError("Sütun sayısı pozitif olmalıdır")

    # Metni temizle (yalnızca Türkçe harfler)
    clean_text = ''.join(ch.lower() for ch in text if ch.lower() in ALPHABET)
    
    # Eksik karakterleri rastgele doldur
    padding_length = (num_cols - (len(clean_text) % num_cols)) % num_cols
    if padding_length > 0:
        clean_text += ''.join(random.choices(ALPHABET, k=padding_length))
    
    # Tabloyu oluştur
    table = []
    for i in range(0, len(clean_text), num_cols):
        row = clean_text[i:i+num_cols]
        table.append(row)
    
    # Sütun sütun okuyarak şifrele
    encrypted = []
    for col in range(num_cols):
        for row in table:
            encrypted.append(row[col])
    
    return ''.join(encrypted)

def rota_encrypt(text, columns):

    columns = int(columns)
    if columns <= 0:
        raise ValueError("Sütun sayısı pozitif olmalıdır")
    
    # Metni temizle ve boyut ayarla
    clean_text = ''.join(ch.lower() for ch in text if ch.lower() in ALPHABET)
    rows = math.ceil(len(clean_text) / columns)
    total_chars = rows * columns
    clean_text += ''.join(random.choices(ALPHABET, k=total_chars - len(clean_text)))
    
    # Tablo oluştur
    table = [list(clean_text[i*columns:(i+1)*columns]) for i in range(rows)]
    
    result = []
    left, right = 0, columns - 1
    top, bottom = 0, rows - 1
    
    while left <= right and top <= bottom:
        # Yukarı ↑ (sol kenar)
        if left <= right:  # Ek kontrol
            for row in range(bottom, top - 1, -1):
                result.append(table[row][left])
            left += 1

        # Sağa → (üst kenar)
        if top <= bottom:  # Ek kontrol
            for col in range(left, right + 1):
                result.append(table[top][col])
            top += 1

        # Aşağı ↓ (sağ kenar)
        if left <= right:  # Ek kontrol
            for row in range(top, bottom + 1):
                result.append(table[row][right])
            right -= 1

        # Sola ← (alt kenar)
        if top <= bottom:  # Ek kontrol
            for col in range(right, left - 1, -1):
                result.append(table[bottom][col])
            bottom -= 1

    return ''.join(result)


def zikzak_encrypt(text, rows):
    """Zikzak şifreleme yöntemi"""
    rows = int(rows)
    if rows <= 0:
        raise ValueError("Satır sayısı pozitif olmalıdır")
    
    clean_text = ''.join(ch.lower() for ch in text if ch.lower() in ALPHABET)
    
    # Zikzak düzeninde satırlara yerleştirme
    zigzag = [[] for _ in range(rows)]
    row, direction = 0, 1
    
    for char in clean_text:
        zigzag[row].append(char)
        row += direction
        if row == rows or row == -1:
            direction *= -1
            row += 2 * direction
    
    # Satırları birleştir
    return ''.join([''.join(row) for row in zigzag])

def vigenere_encrypt(text, key):
    """Vigenère şifreleme yöntemi"""
    clean_text = ''.join(ch.lower() for ch in text if ch.lower() in ALPHABET)
    clean_key = ''.join(ch.lower() for ch in key if ch.lower() in ALPHABET)
    
    if not clean_key:
        raise ValueError("Geçersiz anahtar - Türkçe harf içermeli")
    
    encrypted = []
    key_len = len(clean_key)
    
    for i, char in enumerate(clean_text):
        text_idx = ALPHABET.index(char)
        key_idx = ALPHABET.index(clean_key[i % key_len])
        new_idx = (text_idx + key_idx) % len(ALPHABET)
        encrypted.append(ALPHABET[new_idx])
    
    return ''.join(encrypted)


def four_square_encrypt(text, key1, key2, columns):
    columns = int(columns)
    
    key1 = "".join(dict.fromkeys(key1.lower()))  # remove duplicates
    key2 = "".join(dict.fromkeys(key2.lower()))
    
    square1 = [c for c in ALPHABET if c not in key1] + list(key1)
    square2 = [c for c in ALPHABET if c not in key2] + list(key2)
    
    result = ""
    # Girdiyi temizle: boşlukları ve Türk alfabesi dışındaki karakterleri çıkar
    text = text.lower()
    text = "".join(c for c in text if c in ALPHABET)
    
    if len(text) % 2 != 0:
        text += random.choice(EXTENDED)
    for i in range(0, len(text), 2):
        a = text[i]
        b = text[i+1]
        if a in ALPHABET and b in ALPHABET:
            ra, ca = divmod(ALPHABET.index(a), columns)
            rb, cb = divmod(ALPHABET.index(b), columns)
            new_a = square1[ra * columns + cb]
            new_b = square2[rb * columns + ca]
            result += new_a + new_b
        else:
            result += a + b
    return result

def hill_encrypt(text, key_matrix_str):
    """
    Hill şifreleme algoritması (Türk alfabesi, 29 harf)
    :param text: Şifrelenecek metin
    :param key_matrix_str: String formatında matris (örn: "5 8;17 3")
    :return: Şifrelenmiş metin (BÜYÜK harflerle)
    """
    try:
        # Anahtar matrisini oluştur
        key_matrix = np.array([[int(x) for x in row.split()] for row in key_matrix_str.strip().split(';')])
        n = key_matrix.shape[0]
        
        # Metni temizle
        clean_text = ''.join([c for c in text.lower() if c in ALPHABET])
        
        # Uzunluk n'in katı değilse padding yap
        padding_length = (n - len(clean_text) % n) % n
        if padding_length > 0:
            clean_text += ''.join(random.choices(ALPHABET, k=padding_length))
        
        # Harf → Sayı dönüşüm
        def char_to_num(c):
            return ALPHABET.index(c)
        
        # Sayı → Harf dönüşüm
        def num_to_char(num):
            return ALPHABET[num % len(ALPHABET)]
        
        # Şifreleme işlemi
        encrypted_text = []
        for i in range(0, len(clean_text), n):
            block = clean_text[i:i+n]
            vector = np.array([char_to_num(c) for c in block])
            encrypted_vector = np.dot(key_matrix, vector) % len(ALPHABET)
            encrypted_text.extend([num_to_char(num) for num in encrypted_vector])
        
        return ''.join(encrypted_text)
    
    except Exception as e:
        raise ValueError(f"Hill şifreleme hatası: {str(e)}")