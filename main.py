import tkinter as tk
from tkinter import ttk, messagebox
import json
import re
import hashlib
import random
import string


class Kullanici:
    def __init__(self, ad_soyad, eposta, sifre):
        self.AdSoyad = ad_soyad
        self.Eposta = eposta
        self.Sifre = self.hash_sifre(sifre)

    def hash_sifre(self, sifre):
        # Şifreleri hashleme işlemi
        return hashlib.sha256(sifre.encode()).hexdigest()


class Uygulama:
    def __init__(self, pencere):
        self.pencere = pencere
        self.pencere.title("Evolvie")
        self.pencere.geometry("400x800")

        self.sayfa_degistirici = tk.StringVar(value="Giris Ekrani")
        self.ad_soyad_entry = None
        self.uyku_saati_entry = None

        self.not_defteri = ttk.Notebook(self.pencere)
        self.not_defteri.pack(fill=tk.BOTH, expand=True)

        # Giriş ekranını oluştur
        self.giris_ekrani_gorunumu()

    def verileri_kaydet(self):
        ad_soyad = self.ad_soyad_entry.get()
        uyku_saati = self.uyku_saati_entry.get()

        veriler = {
            "AdSoyad": ad_soyad,
        }

        with open("kullanici_verileri.json", "w") as dosya:
            json.dump(veriler, dosya, indent=2)

        messagebox.showinfo("Başarılı", "Veriler başarıyla kaydedildi.")

    def giris_ekrani_gorunumu(self):
        giris_tab = ttk.Frame(self.not_defteri)
        self.not_defteri.add(giris_tab, text="Giriş Ekranı")

        tk.Label(giris_tab, text="Hoş Geldiniz!").pack(pady=10)

        tk.Label(giris_tab, text="E-posta Adresi:").pack()
        self.eposta_entry = tk.Entry(giris_tab)
        self.eposta_entry.pack()

        tk.Label(giris_tab, text="Şifre:").pack()
        self.sifre_entry = tk.Entry(giris_tab, show="*")
        self.sifre_entry.pack()

        tk.Button(giris_tab, text="Giriş Yap", command=self.giris_yap).pack(pady=10)

        tk.Button(giris_tab, text="Kayıt Ol", command=self.kayit_ol_gorunumu).pack(pady=10)

    def kayit_ol_gorunumu(self):
        kayit_tab = ttk.Frame(self.not_defteri)
        self.not_defteri.add(kayit_tab, text="Kayıt Ol")

        tk.Label(kayit_tab, text="Ad Soyad:").pack()
        self.ad_soyad_entry = tk.Entry(kayit_tab)
        self.ad_soyad_entry.pack()

        tk.Label(kayit_tab, text="E-posta Adresi:").pack()
        self.eposta_entry_kayit = tk.Entry(kayit_tab)
        self.eposta_entry_kayit.pack()

        tk.Label(kayit_tab, text="Şifre:").pack()
        self.sifre_entry_kayit = tk.Entry(kayit_tab, show="*")
        self.sifre_entry_kayit.pack()

        tk.Button(kayit_tab, text="Kayıt Ol", command=self.kullanici_kaydet).pack(pady=10)

        # Kayıt Ol sekmesine geçiş
        self.not_defteri.select(1)

        # Giriş ekranını gizle
        self.not_defteri.forget(0)

    def kullanici_kaydet(self):
        ad_soyad = self.ad_soyad_entry.get()

        # Kullanıcıların daha önce kayıtlı olup olmadığını kontrol et
        if self.kullanici_var_mi(self.eposta_entry_kayit.get()):
            messagebox.showerror("Hata", "Bu e-posta adresi zaten kullanılmaktadır.")
            return

        if not ad_soyad or not self.eposta_entry_kayit.get() or not self.sifre_entry_kayit.get():
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
            return

        if not self.email_dogrula(self.eposta_entry_kayit.get()):
            return

        yeni_kullanici = Kullanici(
            ad_soyad=ad_soyad,
            eposta=self.eposta_entry_kayit.get(),
            sifre=self.sifre_entry_kayit.get()
        )

        with open("kullanicilar.json", "a") as dosya:
            json.dump(yeni_kullanici.__dict__, dosya)
            dosya.write("\n")  # Her kullanıcıyı yeni bir satıra ekleyin

        messagebox.showinfo("Başarılı", "Kayıt işlemi tamamlandı.")

        # Kayıt işlemi tamamlandıktan sonra kayıt sekmesini kapat
        self.not_defteri.forget(self.not_defteri.select())

        # Giriş ekranını göster
        self.giris_ekrani_gorunumu()

    def email_dogrula(self, email):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(pattern, email):
            messagebox.showerror("Hata", "Geçersiz e-posta adresi.")
            return False
        return True

    def kullanici_var_mi(self, eposta):
        try:
            with open("kullanicilar.json", "r") as dosya:
                kullanicilar = dosya.readlines()

            for kullanici_str in kullanicilar:
                kullanici = json.loads(kullanici_str)
                if kullanici["Eposta"] == eposta:
                    return True
        except FileNotFoundError:
            return False

        return False

    def random_string(self, length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def giris_yap(self):
        eposta = self.eposta_entry.get()
        sifre = self.sifre_entry.get()

        with open("kullanicilar.json", "r") as dosya:
            kullanicilar = dosya.readlines()

        for kullanici_str in kullanicilar:
            kullanici = json.loads(kullanici_str)
            if kullanici["Eposta"] == eposta and kullanici["Sifre"] == hashlib.sha256(sifre.encode()).hexdigest():
                messagebox.showinfo("Başarılı", "Giriş işlemi tamamlandı.")

                # Giriş ekranını kapat
                self.not_defteri.forget(0)
                return

        messagebox.showerror("Hata", "E-posta veya şifre hatalı.")


if __name__ == "__main__":
    pencere = tk.Tk()
    uygulama = Uygulama(pencere)
    pencere.mainloop()
