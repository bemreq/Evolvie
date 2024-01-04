import tkinter as tk
from tkinter import ttk, messagebox
import json
import re
import hashlib
import random
import smtplib
import string
from email.mime.text import MIMEText

class Kullanici:
    def __init__(self, ad_soyad, eposta, sifre):
        self.AdSoyad = ad_soyad
        self.Eposta = eposta
        self.Sifre = self.hash_sifre(sifre)

    def hash_sifre(self, sifre):
        return hashlib.sha256(sifre.encode()).hexdigest()

class Uygulama:
    def __init__(self, pencere):
        self.pencere = pencere
        self.pencere.title("Evolvie")
        self.pencere.geometry("400x800")

        self.sayfa_degistirici = tk.StringVar(value="Giris Ekrani")
        self.ad_soyad_entry = None
        self.eposta_entry_unuttum = None
        self.dogrulama_kodu = None
        self.kullanici_bilgisi = None

        self.not_defteri = ttk.Notebook(self.pencere)
        self.not_defteri.pack(fill=tk.BOTH, expand=True)

        # Initialize kullanici_bilgisi
        self.kullanici_bilgisi = None

        # Giriş ekranını oluştur
        self.giris_ekrani_gorunumu()

    def verileri_kaydet(self):
        ad_soyad = self.ad_soyad_entry.get()

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

        tk.Button(giris_tab, text="Şifremi Unuttum", command=self.sifremi_unuttum_gorunumu).pack(pady=10)

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
            dosya.write(json.dumps(yeni_kullanici.__dict__) + "\n")  # Corrected the writing format

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

    def sifremi_unuttum_gorunumu(self):
        unuttum_tab = ttk.Frame(self.not_defteri)
        self.not_defteri.add(unuttum_tab, text="Şifremi Unuttum")

        tk.Label(unuttum_tab, text="E-posta Adresi:").pack()
        self.eposta_entry_unuttum = tk.Entry(unuttum_tab)
        self.eposta_entry_unuttum.pack()

        tk.Button(unuttum_tab, text="Doğrulama Kodu Gönder", command=self.dogrulama_kodu_gonder).pack(pady=10)

    def dogrulama_kodu_gonder(self):
        eposta = self.eposta_entry_unuttum.get()

        # Kullanıcının daha önce kayıtlı olup olmadığını kontrol et
        if not self.kullanici_var_mi(eposta):
            messagebox.showerror("Hata", "Bu e-posta adresi kayıtlı değil.")
            return

        # Doğrulama kodu oluştur ve e-posta ile gönder
        self.dogrulama_kodu = self.random_string(6)
        self.eposta_gonder(eposta, f"Doğrulama Kodu: {self.dogrulama_kodu}")

        # Doğrulama sayfasına geçiş
        self.not_defteri.add(ttk.Frame(self.not_defteri), text="Doğrulama Sayfası")
        self.not_defteri.select(len(self.not_defteri.tabs()) - 1)
        self.dogrulama_sayfasi_gorunumu()

        # Şifremi Unuttum sekmesini gizle
        self.not_defteri.forget(len(self.not_defteri.tabs()) - 2)

        messagebox.showinfo("Başarılı", "Doğrulama kodu e-posta adresinize gönderildi.")

    def dogrulama_sayfasi_gorunumu(self):
        dogrulama_tab = self.not_defteri.tabs()[-1]

        tk.Label(dogrulama_tab, text="Doğrulama Kodu:").pack()
        self.dogrulama_entry = tk.Entry(dogrulama_tab)
        self.dogrulama_entry.pack()

        tk.Button(dogrulama_tab, text="Doğrula", command=self.dogrula).pack(pady=10)

    def dogrula(self):
        girilen_kod = self.dogrulama_entry.get()

        # Doğrulama kodunu kontrol et
        if girilen_kod == self.dogrulama_kodu:
            messagebox.showinfo("Başarılı", "Doğrulama işlemi tamamlandı.")
            self.yeni_sifre_gorunumu()
        else:
            messagebox.showerror("Hata", "Geçersiz doğrulama kodu.")

    def yeni_sifre_gorunumu(self):
        yeni_sifre_tab = ttk.Frame(self.not_defteri)
        self.not_defteri.add(yeni_sifre_tab, text="Yeni Şifre Oluştur")

        tk.Label(yeni_sifre_tab, text="Yeni Şifre:").pack()
        self.yeni_sifre_entry = tk.Entry(yeni_sifre_tab, show="*")
        self.yeni_sifre_entry.pack()

        tk.Label(yeni_sifre_tab, text="Yeni Şifre Tekrar:").pack()
        self.yeni_sifre_tekrar_entry = tk.Entry(yeni_sifre_tab, show="*")
        self.yeni_sifre_tekrar_entry.pack()

        tk.Button(yeni_sifre_tab, text="Şifreyi Değiştir", command=self.sifreyi_degistir).pack(pady=10)

    def sifreyi_degistir(self):
        yeni_sifre = self.yeni_sifre_entry.get()
        yeni_sifre_tekrar = self.yeni_sifre_tekrar_entry.get()

        # Yeni şifreleri kontrol et
        if yeni_sifre != yeni_sifre_tekrar:
            messagebox.showerror("Hata", "Şifreler uyuşmuyor.")
            return

        # Kullanıcıya ait şifreyi güncelle
        # Bu bölümü uygun bir şekilde güncellemeniz gerekiyor.
        self.kullanici_bilgisi.Sifre = self.hash_sifre(yeni_sifre)

        messagebox.showinfo("Başarılı", "Şifre başarıyla güncellendi.")

        # Tüm sayfaları kapat ve giriş ekranına yönlendir
        self.not_defteri.forget(0)
        self.giris_ekrani_gorunumu()

    def eposta_gonder(self, eposta, icerik):
        # E-posta gönderme işlemini gerçekleştir
        # Bu bölümü uygun bir şekilde güncellemeniz gerekiyor.
        try:
            pass  # E-posta gönderme işlemi buraya eklenecek
        except Exception as e:
            messagebox.showerror("Hata", f"E-posta gönderme hatası: {str(e)}")

    def kullanici_var_mi(self, eposta):
        try:
            with open("kullanicilar.json", "r") as dosya:
                kullanicilar = dosya.readlines()

            for kullanici_str in kullanicilar:
                kullanici = json.loads(kullanici_str)
                if kullanici["Eposta"] == eposta:
                    self.kullanici_bilgisi = Kullanici(**kullanici)
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