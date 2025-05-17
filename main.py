import tkinter as tk
import random
from tkinter import ttk
from encryption import caesar_encrypt,linear_encrypt,substitution_encrypt,permutation_encrypt,numberkey_encrypt,rota_encrypt,zikzak_encrypt,vigenere_encrypt
from decryption import caesar_decrypt,linear_decrypt,substitution_decrypt,permutation_decrypt,numberkey_decrypt,rota_decrypt,zikzak_decrypt,vigenere_decrypt

# Algoritma parametre sözlüğü
ALGORITHM_PARAMS = {
    "Kaydırmalı": ["Shift"],
    "Doğrusal": ["a", "b"],
    "YerDeğiştirme": ["Alfabe"],
    "Permutasyon": ["Anahtar Sayısı", "Permutasyon Dizisi"],
    "SayıAnahtarlı": ["Sayı Anahtar"],
    "Rota": ["Boyut"],
    "ZikZak": ["Satır Sayısı"],
    "Vigenere": ["Anahtar"],
    "DörtKare": ["Anahtar1", "Anahtar2"],
    "Hill": ["Matris Anahtarı"]
}

class CryptoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MainPage")
        self.geometry("1000x700")
        self.configure(padx=10, pady=10)

        # Girdi
        tk.Label(self, text="Girdi", font=("Arial", 12)).pack(anchor="w")
        self.input_text = tk.Text(self, height=8, font=("Arial", 12))
        self.input_text.pack(fill="x")

        # Çıktı
        tk.Label(self, text="Çıktı", font=("Arial", 12)).pack(anchor="w", pady=(10, 0))
        self.output_text = tk.Text(self, height=8, font=("Arial", 12))
        self.output_text.pack(fill="x")

        # Alt Panel
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(fill="x", pady=10)

        # Algoritma seçimi
        tk.Label(bottom_frame, text="Yöntem").grid(row=0, column=0, sticky="w")
        self.method_combo = ttk.Combobox(bottom_frame, values=list(ALGORITHM_PARAMS.keys()), state="readonly")
        self.method_combo.grid(row=1, column=0, padx=5)
        self.method_combo.bind("<<ComboboxSelected>>", self.update_dynamic_panel)

        # Şifrele / Çöz
        self.mode = tk.StringVar(value="encrypt")
        tk.Radiobutton(bottom_frame, text="Şifrele", variable=self.mode, value="encrypt").grid(row=1, column=1)
        tk.Radiobutton(bottom_frame, text="Çöz", variable=self.mode, value="decrypt").grid(row=1, column=2)

        # Parametre paneli
        self.param_frame = tk.Frame(bottom_frame, bg="#eee")
        self.param_frame.grid(row=1, column=3, padx=10)
        self.param_entries = {}

        # Uygula butonu
        tk.Button(bottom_frame, text="Uygula", command=self.apply_algorithm).grid(row=1, column=4, padx=10)

    def update_dynamic_panel(self, event=None):
        # Eski girdileri temizle
        for widget in self.param_frame.winfo_children():
            widget.destroy()
        self.param_entries.clear()

        method = self.method_combo.get()
        for param in ALGORITHM_PARAMS.get(method, []):
            label = tk.Label(self.param_frame, text=param, bg="#eee")
            label.pack(anchor="w")

            entry = tk.Entry(self.param_frame)
            entry.pack(fill="x", padx=5, pady=2)
            self.param_entries[param] = entry

            # Rastgele alfabe oluşturma butonunu burada kontrol et
            if method == "YerDeğiştirme" and param == "Alfabe":
                gen_button = tk.Button(self.param_frame, text="Rastgele Alfabe Oluştur", 
                                       command=lambda e=entry: self.generate_random_alphabet(e))
                gen_button.pack(pady=2)


    def generate_random_alphabet(self, entry_widget):
        ALPHABET = "abcçdefgğhıijklmnoöprsştuüvyz"
        shuffled = list(ALPHABET)
        random.shuffle(shuffled)
        random_alphabet = ''.join(shuffled)
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, random_alphabet)

    def apply_algorithm(self):
        text = self.input_text.get("1.0", tk.END).strip()
        method = self.method_combo.get()
        mode = self.mode.get()
        params = {k: v.get() for k, v in self.param_entries.items()}

        result = ""

        try:
            if method == "Kaydırmalı":
                shift = int(params.get("Shift", 0))
                result = caesar_encrypt(text, shift) if mode == "encrypt" else caesar_decrypt(text, shift)

            elif method == "Doğrusal":
                a = int(params.get("a", 1))
                b = int(params.get("b", 0))
                result = linear_encrypt(text, a, b) if mode == "encrypt" else linear_decrypt(text, a, b)

            elif method == "YerDeğiştirme":
                key_alphabet = params.get("Alfabe", "")
                if len(key_alphabet) != 29:
                    raise ValueError("Alfabe tam olarak 29 harften oluşmalıdır.")
                if mode == "encrypt":
                    result = substitution_encrypt(text, key_alphabet)
                else:
                    result = substitution_decrypt(text, key_alphabet)

            elif method == "Permutasyon":
                key_size = int(params.get("Anahtar Sayısı", 0))
                perm_str = params.get("Permutasyon Dizisi", "")
                perm = list(map(int, perm_str.strip().split()))

                if key_size <= 0:
                    raise ValueError("Anahtar sayısı pozitif bir tam sayı olmalıdır.")
                if len(perm) != key_size:
                    raise ValueError(f"Permütasyon dizisi {key_size} uzunluğunda olmalıdır.")
                if sorted(perm) != list(range(1, key_size + 1)):
                    raise ValueError("Geçersiz permütasyon dizisi. 1'den n'e kadar tüm sayılar yer almalı.")

                if mode == "encrypt":
                    result = permutation_encrypt(text, perm_str)
                else:
                        result = permutation_decrypt(text, perm_str)
            
            elif method == "SayıAnahtarlı":
                number_key = params.get("Sayı Anahtar", "")
                if not number_key.isdigit():
                    raise ValueError("Sayı anahtar yalnızca rakamlardan oluşmalıdır.")
                if mode == "encrypt":
                    result = numberkey_encrypt(text, number_key)
                else:
                    result = numberkey_decrypt(text, number_key)

            elif method == "Rota":
                size = params.get("Boyut", "0")
                if not size.isdigit():
                    raise ValueError("Boyut pozitif bir tam sayı olmalıdır")
                if mode == "encrypt":
                    result = rota_encrypt(text, size)
                else:
                    result = rota_decrypt(text, size)
            
            elif method == "ZikZak":
                rows = params.get("Satır Sayısı", "0")
                if not rows.isdigit():
                    raise ValueError("Satır sayısı pozitif bir tam sayı olmalıdır")
                if mode == "encrypt":
                    result = zikzak_encrypt(text, rows)
                else:
                    result = zikzak_decrypt(text, rows)
            
            elif method == "Vigenere":
                key = params.get("Anahtar", "")
                if not key:
                    raise ValueError("Anahtar boş olamaz")
                if mode == "encrypt":
                    result = vigenere_encrypt(text, key)
                else:
                    result = vigenere_decrypt(text, key)

            else:
                result = f"[UYARI] '{method}' yöntemi henüz uygulanmadı."

        except Exception as e:
            result = f"Hata: {str(e)}"

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, result)

if __name__ == "__main__":
    app = CryptoApp()
    app.mainloop()
