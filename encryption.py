# encryption.py
import random 
import math

ALPHABET = "abcçdefgğhıijklmnoöprsştuüvyz"

def caesar_encrypt(text, shift):
    encrypted = ""
   
    for char in text.lower():
        if char in ALPHABET:
            idx = (ALPHABET.index(char) + shift) % len(ALPHABET)
            encrypted += ALPHABET[idx]
        else:
            encrypted += char  # boşluk veya noktalama
    return encrypted

def linear_encrypt(text, a, b):
    encrypted = ""
    m = len(ALPHABET)

    # Anahtar doğrulama (a ve m aralarında asal olmalı)
    def gcd(x, y):
        while y:
            x, y = y, x % y
        return x

    if gcd(a, m) != 1:
        return "Hata: 'a' ve alfabe uzunluğu (29) aralarında asal olmalı."

    for char in text:
        if char in ALPHABET:
            x = ALPHABET.index(char)
            encrypted_index = (a * x + b) % m
            encrypted += ALPHABET[encrypted_index]
        else:
            encrypted += char  # harf dışı karakterleri olduğu gibi bırak
    return encrypted


def substitution_encrypt(text, key_alphabet):
    
    if len(key_alphabet) != len(ALPHABET):
        raise ValueError("Alfabe tam olarak 29 karakterden oluşmalıdır.")
    encrypted = ""
    
    
    for char in text:
        if char in ALPHABET:
            index = ALPHABET.index(char)
            encrypted += key_alphabet[index]
        else:
            encrypted += char  # boşluk, noktalama vs. koru
    return encrypted

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
    """Özelleştirilmiş Dört Kare şifreleme"""
    columns = int(columns)
    if columns <= 0:
        raise ValueError("Sütun sayısı pozitif olmalıdır")
    
    # Alfabe ve anahtarları temizle
    clean_text = ''.join(ch.lower() for ch in text if ch.lower() in ALPHABET)
    key1 = ''.join(ch.lower() for ch in key1 if ch.lower() in ALPHABET)
    key2 = ''.join(ch.lower() for ch in key2 if ch.lower() in ALPHABET)
    
    if len(key1) != 29 or len(key2) != 29:
        raise ValueError("Anahtarlar 29 harflik Türkçe alfabe içermeli")
    
    # 4 kare oluştur
    square1 = ALPHABET  # Standart alfabe
    square2 = key1       # 1. karıştırılmış alfabe
    square3 = key2       # 2. karıştırılmış alfabe
    square4 = ALPHABET  # Alfabenin tersi
    
    # Metni sütunlara böl
    rows = math.ceil(len(clean_text) / columns)
    padded_text = clean_text.ljust(rows * columns, 'x')  # Eksikleri 'x' ile doldur
    
    # Şifreleme
    encrypted = []
    for i in range(0, len(padded_text), 2):
        char1 = padded_text[i]
        char2 = padded_text[i+1] if i+1 < len(padded_text) else 'x'
        
        # Karakterlerin konumlarını bul
        row1, col1 = divmod(square1.index(char1), 5)  # 5x6 matris (29 harf)
        row2, col2 = divmod(square3.index(char2), 5)
        
        # Yeni karakterleri bul
        encrypted.append(square2[row1*6 + col2])  # 1. çapraz
        encrypted.append(square4[row2*6 + col1])  # 2. çapraz
    
    return ''.join(encrypted)