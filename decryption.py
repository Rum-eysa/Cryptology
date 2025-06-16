# decryption.py
from encryption import ALPHABET

ALPHABET = "abcçdefgğhıijklmnoöprsştuüvyz"

def caesar_decrypt(cipher, shift):
    decrypted = ""
    for char in cipher:
        lower_char = char.lower()
        if lower_char in ALPHABET:
            idx = (ALPHABET.index(lower_char) - shift) % len(ALPHABET)
            new_char = ALPHABET[idx]
            decrypted += new_char  # Tüm harfler küçük olacak
        else:
            decrypted += char  # Harf dışındaki karakterleri aynen ekle
    return decrypted


#linear decyricption
def linear_decrypt(cipher, a, b):
    decrypted = ""
    m = len(ALPHABET)

    # Modüler ters bul
    def modinv(a, m):
        for i in range(1, m):
            if (a * i) % m == 1:
                return i
        raise ValueError("Modüler ters yok (a ile m aralarında asal değil)")

    a_inv = modinv(a, m)

    for char in cipher.lower():
        if char in ALPHABET:
            y = ALPHABET.index(char)
            decrypted_index = (a_inv * (y - b)) % m
            decrypted += ALPHABET[decrypted_index]
        # Sayı veya boşluk varsa yok say (eklenmez)
        else:
            continue

    return decrypted

#substitution_decrypt
def substitution_decrypt(cipher, key_alphabet):
    if len(key_alphabet) != len(ALPHABET):
        raise ValueError("Anahtar alfabe tam olarak 29 karakterden oluşmalıdır")

    decrypted = []
    for char in cipher.lower():
        if char in key_alphabet:
            index = key_alphabet.index(char)
            decrypted.append(ALPHABET[index])
        # Sayılar ve boşluklar yok sayılır
        else:
            continue

    return ''.join(decrypted)

# permürtasyon 
def permutation_decrypt(cipher, perm_str):
    try:
        perm = [int(p) for p in perm_str.strip().split()]
        block_size = len(perm)

        if sorted(perm) != list(range(1, block_size + 1)):
            raise ValueError("Permütasyon 1'den n'e kadar olmalı")

        clean_cipher = ''.join(ch.lower() for ch in cipher if ch.lower() in ALPHABET)

        decrypted = []
        for i in range(0, len(clean_cipher), block_size):
            block = clean_cipher[i:i + block_size]
            if len(block) < block_size:
                continue

            reordered = [''] * block_size
            for j in range(block_size):
                reordered[perm[j] - 1] = block[j]  # ÇÖZÜM: karakteri doğru orijinal konumuna koy
            decrypted.append(''.join(reordered))

        return ''.join(decrypted)

    except Exception as e:
        raise ValueError(f"Permütasyon çözme hatası: {str(e)}")



def numberkey_decrypt(text, key):
    """
    NumberKey şifresini çözer (sadece Türk alfabesindeki karakterleri işler)
    :param text: Şifrelenmiş metin
    :param key: Kullanılan sütun sayısı (orijinal şifrelemede kullanılan)
    :return: Çözülmüş orijinal metin (sadece Türkçe harfler)
    """
    try:
        num_cols = int(key)
    except ValueError:
        raise ValueError("Anahtar geçerli bir tam sayı olmalıdır")
    
    if num_cols <= 0:
        raise ValueError("Sütun sayısı pozitif olmalıdır")

    # Sadece Türkçe harfleri al
    clean_text = ''.join(ch.lower() for ch in text if ch.lower() in ALPHABET)
    
    # Satır sayısını hesapla
    num_rows = len(clean_text) // num_cols
    if len(clean_text) % num_cols != 0:
        num_rows += 1
    
    # Tabloyu oluştur (sütun sütun doldur)
    table = []
    for i in range(num_rows):
        table.append([''] * num_cols)
    
    # Şifreli metni tabloya yerleştir
    index = 0
    for col in range(num_cols):
        for row in range(num_rows):
            if index < len(clean_text):
                table[row][col] = clean_text[index]
                index += 1
    
    # Orijinal metni satır satır oku
    decrypted = []
    for row in table:
        decrypted.extend(row)
    
    # Dolgu karakterlerini kaldır (son kısımdaki fazlalıkları at)
    original_length = (len(decrypted) // num_cols) * num_cols - (num_cols - (len(decrypted) % num_cols)) % num_cols
    return ''.join(decrypted[:original_length])


import math

def rota_decrypt(cipher, columns):
    columns = int(columns)
    if columns <= 0:
        raise ValueError("Sütun sayısı pozitif olmalı")

    # Sadece ALPHABET karakterlerini al
    clean_cipher = ''.join(ch.lower() for ch in cipher if ch.lower() in ALPHABET)

    length = len(clean_cipher)
    rows = math.ceil(length / columns)

    # Boş tablo oluştur
    table = [['' for _ in range(columns)] for _ in range(rows)]

    left, right = 0, columns - 1
    top, bottom = 0, rows - 1
    index = 0

    # Şifreli metni tabloya spiral şekilde doldur
    while left <= right and top <= bottom:
        # Yukarı ↑ (sol kenar)
        for row in range(bottom, top - 1, -1):
            if index < length:
                table[row][left] = clean_cipher[index]
                index += 1
        left += 1

        # Sağa → (üst kenar)
        for col in range(left, right + 1):
            if index < length:
                table[top][col] = clean_cipher[index]
                index += 1
        top += 1

        # Aşağı ↓ (sağ kenar)
        for row in range(top, bottom + 1):
            if index < length:
                table[row][right] = clean_cipher[index]
                index += 1
        right -= 1

        # Sola ← (alt kenar)
        for col in range(right, left - 1, -1):
            if index < length:
                table[bottom][col] = clean_cipher[index]
                index += 1
        bottom -= 1

    # Orijinal metni satır satır oku
    decrypted = ''.join([''.join(row) for row in table])
    return decrypted


def zikzak_decrypt(cipher, rows):
    rows = int(rows)
    if rows <= 0:
        raise ValueError("Satır sayısı pozitif olmalı")

    # Sadece Türk alfabesinden karakterleri kullan
    clean_cipher = ''.join(ch.lower() for ch in cipher if ch.lower() in ALPHABET)

    pattern = [0] * len(clean_cipher)
    row = 0
    direction = 1

    # Her harfin hangi satıra ait olduğunu belirle
    for i in range(len(clean_cipher)):
        pattern[i] = row
        row += direction
        if row == rows or row == -1:
            direction *= -1
            row += 2 * direction

    # Her satırda kaç harf olacağını hesapla
    counts = [pattern.count(r) for r in range(rows)]

    # Şifreli metni satırlara böl
    zigzag_rows = []
    index = 0
    for count in counts:
        zigzag_rows.append(clean_cipher[index:index+count])
        index += count

    # Satırlardan orijinal sırayı geri oluştur
    row_indexes = [0] * rows
    result = ""
    for r in pattern:
        result += zigzag_rows[r][row_indexes[r]]
        row_indexes[r] += 1

    return result

def vigenere_decrypt(cipher, key):
    # Yalnızca Türk alfabesinden karakterler içeren anahtarı al
    clean_key = ''.join(ch.lower() for ch in key if ch.lower() in ALPHABET)

    if not clean_key:
        raise ValueError("Geçersiz anahtar - Türkçe harf içermeli")

    # Şifreli metni sadece Türk harflerinden oluşacak şekilde filtrele
    clean_cipher = ''.join(ch.lower() for ch in cipher if ch.lower() in ALPHABET)

    decrypted = []
    key_len = len(clean_key)

    for i, char in enumerate(clean_cipher):
        cipher_idx = ALPHABET.index(char)
        key_idx = ALPHABET.index(clean_key[i % key_len])
        new_idx = (cipher_idx - key_idx) % len(ALPHABET)
        decrypted.append(ALPHABET[new_idx])

    return ''.join(decrypted)


def four_square_decrypt(cipher, key1, key2, columns):
    columns = int(columns)

    # Anahtar karakterleri tekrar etmeyecek şekilde temizle
    key1 = "".join(dict.fromkeys(key1.lower()))
    key2 = "".join(dict.fromkeys(key2.lower()))

    # İkincil kare alfabeleri oluştur
    square1 = [c for c in ALPHABET if c not in key1] + list(key1)
    square2 = [c for c in ALPHABET if c not in key2] + list(key2)

    # Girdiyi temizle
    cipher = cipher.lower()
    clean_cipher = "".join(c for c in cipher if c in ALPHABET)

    result = ""
    if len(clean_cipher) % 2 != 0:
        clean_cipher = clean_cipher[:-1]  # son karakteri at (tekse)

    for i in range(0, len(clean_cipher), 2):
        a = clean_cipher[i]
        b = clean_cipher[i + 1]

        if a in square1 and b in square2:
            ra, ca = divmod(square1.index(a), columns)
            rb, cb = divmod(square2.index(b), columns)
            orig_a = ALPHABET[ra * columns + cb]
            orig_b = ALPHABET[rb * columns + ca]
            result += orig_a + orig_b

    return result


import numpy as np
from numpy.linalg import inv
ALPHABET_SIZE = len(ALPHABET)


def hill_decrypt(cipher_text, key_matrix_str):
    
    try:
        # Anahtar matrisini oluştur
        key_matrix = np.array([[int(x) for x in row.split()] for row in key_matrix_str.strip().split(';')])
        n = key_matrix.shape[0]
        mod = ALPHABET_SIZE

        # Sadece alfabe içindeki karakterleri al (küçük harfe çevirerek)
        clean_cipher = ''.join([c.lower() for c in cipher_text if c.lower() in ALPHABET])

        # Modüler ters matris hesapla
        def matrix_mod_inverse(matrix, modulus):
            det = int(round(np.linalg.det(matrix)))  # determinant
            det_mod = det % modulus
            det_inv = pow(det_mod, -1, modulus)  # modüler tersi
            matrix_minor = np.linalg.inv(matrix) * det  # adjoint (yardımcı matris)
            matrix_mod_inv = (det_inv * matrix_minor) % modulus
            return np.round(matrix_mod_inv).astype(int)

        inv_key_matrix = matrix_mod_inverse(key_matrix, mod)

        # Harf → Sayı dönüşüm
        def char_to_num(c):
            return ALPHABET.index(c)

        # Sayı → Harf dönüşüm
        def num_to_char(num):
            return ALPHABET[num % mod]

        # Şifre çözme işlemi
        decrypted_text = []
        for i in range(0, len(clean_cipher), n):
            block = clean_cipher[i:i+n]
            if len(block) < n:
                continue  # eksik blok varsa atla
            vector = np.array([char_to_num(c) for c in block])
            decrypted_vector = np.dot(inv_key_matrix, vector) % mod
            decrypted_text.extend([num_to_char(int(round(num))) for num in decrypted_vector])

        return ''.join(decrypted_text)

    except Exception as e:
        raise ValueError(f"Hill şifre çözme hatası: {str(e)}")
