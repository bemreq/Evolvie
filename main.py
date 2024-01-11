import tkinter as tk
from tkinter import ttk, messagebox
import json
import re
import random
import smtplib
import string
from email.mime.text import MIMEText

#SINIFLAR
class Kullanici:
    def __init__(self, ad_soyad, eposta, sifre):
        self.AdSoyad = ad_soyad
        self.Eposta = eposta
        self.Sifre = sifre

class Uygulama:
    def __init__(self, root):
        self.root = root
        self.root.title("Evolvie")
        self.root.geometry("400x800")
        self.not_defteri = ttk.Notebook(root)

        self.sayfalar = {
            
            0: self.giris_ekrani,
            1: self.anasayfa_ekrani,
            2: self.kayit_ekrani,
            3: self.sifremi_unuttum_ekrani,
            4: self.eposta_dogrulama_ekrani,
            5: self.yeni_sifre_ekrani
        }

        self.sayfa_numarasi = 0
        self.sayfayi_goster()

#YARDIMCI FONKSIYONLAR

    def sayfa_goster(self, sayfa_numarasi):
        self.not_defteri.forget(0)
        self.not_defteri.pack_forget()
        self.sayfa_numarasi = sayfa_numarasi
        self.sayfayi_goster()
        
    def sayfa_gecis(self, hedef_sayfa):
        self.not_defteri.forget(0)
        self.not_defteri.pack_forget()
        self.sayfa_numarasi = hedef_sayfa
        self.sayfayi_goster()
            
    def email_dogrula(self, email):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(pattern, email):
            messagebox.showerror("Hata", "Geçersiz e-posta adresi.")
            return False
        return True
    
    def random_string(self, length):
        digits = string.digits
        return ''.join(random.choice(digits) for i in range(length))
    
    def eposta_gonder(self, eposta, icerik):
        try:
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            smtp_username = "emre.gltkn24@gmail.com"
            smtp_password = "omjb dgjm fpwm xjra"

            msg = MIMEText(icerik)
            msg["Subject"] = "Evolvie Doğrulama Kodu"
            msg["From"] = smtp_username
            msg["To"] = eposta

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(smtp_username, eposta, msg.as_string())
            pass
        except Exception as e:
            messagebox.showerror(
                "Hata", f"E-posta gönderme hatası: {str(e)}")
            
#KULLANICI ISLEMLERI

    def verileri_kaydet(self):
        ad_soyad = self.ad_soyad_entry.get()
        eposta = self.eposta_entry.get()
        sifre = self.sifre_entry.get()
        
        veriler = {
            "Ad Soyad": ad_soyad,
            "Eposta": eposta,
            "Sifre": sifre,
        }

        with open("kullanici_verileri.json", "w") as dosya:
            json.dump(veriler, dosya, indent=2)

        messagebox.showinfo("Başarılı", "Veriler başarıyla kaydedildi.")
        
    def kullanici_kaydet(self):
        ad_soyad = self.ad_soyad_entry.get()

        if self.kullanici_var_mi(self.eposta_entry_kayit.get()):
            messagebox.showerror(
                "Hata", "Bu e-posta adresi zaten kullanılmaktadır.")
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
            dosya.write(json.dumps(yeni_kullanici.__dict__) + "\n")

        messagebox.showinfo("Başarılı", "Kayıt işlemi tamamlandı.")
        self.sayfa_gecis(0 )
        
    def kullanici_var_mi(self, eposta):
        try:
            with open("kullanicilar.json", "r") as dosya:
                kullanicilar = dosya.readlines()

            for kullanici_str in kullanicilar:
                kullanici = json.loads(kullanici_str)
                if kullanici["Eposta"] == eposta:
                    self.kullanici_bilgisi = Kullanici(
                        ad_soyad=kullanici.get("AdSoyad", ""),
                        eposta=kullanici.get("Eposta", ""),
                        sifre=kullanici.get("Sifre", "")
                    )
                    return True
        except FileNotFoundError:
            return False

        return False

    def giris_yap(self):
        eposta = self.eposta_entry.get()
        sifre = self.sifre_entry.get()

        if not eposta or not sifre:
            messagebox.showerror("Hata", "E-posta ve şifre alanları boş bırakılamaz.")
            return

        if not self.kullanici_var_mi(eposta):
            messagebox.showerror("Hata", "Bu e-posta adresi kayıtlı değil.")
            return

        if self.kullanici_bilgisi.Sifre == sifre and self.kullanici_bilgisi.Eposta == eposta:
            messagebox.showinfo("Başarılı", "Giriş işlemi tamamlandı.")
            self.sayfa_gecis(1)   
        else:
            messagebox.showerror("Hata", "E-posta veya sifre hatalı.")


    def sifreyi_degistir(self):
        yeni_sifre = self.yeni_sifre_entry.get()
        yeni_sifre_tekrar = self.yeni_sifre_tekrar_entry.get()

        if yeni_sifre != yeni_sifre_tekrar:
            messagebox.showerror("Hata", "Şifreler uyuşmuyor.")
            return

        if self.kullanici_bilgisi:
            self.kullanici_bilgisi.Sifre = self.sifre_entry(yeni_sifre)

            messagebox.showinfo(
                "Başarılı", "Şifre başarıyla güncellendi.")

            self.not_defteri.forget(0)
            self.giris_ekrani()
            
        else:
            messagebox.showerror("Hata", "Kullanıcı bilgisi bulunamadı.")

#DOGRULAMA ISLEMLERI

    def dogrulama_kodu_gonder(self):
        eposta = self.eposta_entry_unuttum.get()

        if not self.kullanici_var_mi(eposta):
            messagebox.showerror("Hata", "Bu e-posta adresi kayıtlı değil.")
            return

        self.dogrulama_kodu = self.random_string(6)
        self.eposta_gonder(eposta, f"Doğrulama Kodu: {self.dogrulama_kodu}")

    def dogrula(self):
        girilen_kod = self.dogrulama_entry.get()

        if girilen_kod == self.dogrulama_kodu:
            messagebox.showinfo("Başarılı", "Doğrulama işlemi tamamlandı.")
            self.yeni_sifre_ekrani()
        else:
            messagebox.showerror("Hata", "Geçersiz doğrulama kodu.")

#ARAYUZ EKRANLARI

    def sayfayi_goster(self):
        if self.sayfa_numarasi in self.sayfalar:
            self.sayfalar[self.sayfa_numarasi]()
            self.not_defteri.pack(expand=1, fill="both")
        else:
            print("Geçersiz sayfa numarası.")
            
    def anasayfa_ekrani(self):
        anasayfa_tab = ttk.Frame(self.not_defteri)
        self.not_defteri.add(anasayfa_tab, text="Ana Sayfa")

        tk.Label(anasayfa_tab, text="Tekrardan Hoş Geldiniz!").pack(pady=10)

    def giris_ekrani(self):
        giris_tab = ttk.Frame(self.not_defteri)
        self.not_defteri.add(giris_tab, text="Giriş Ekranı")

        tk.Label(giris_tab, text="Hoş Geldiniz!").pack(pady=10)

        tk.Label(giris_tab, text="E-posta Adresi:").pack()
        self.eposta_entry = tk.Entry(giris_tab)
        self.eposta_entry.pack()

        tk.Label(giris_tab, text="Şifre:").pack()
        self.sifre_entry = tk.Entry(giris_tab, show="*")
        self.sifre_entry.pack()

        tk.Button(giris_tab, text="Giris Yap", command=self.giris_yap).pack(pady=10)
        tk.Button(giris_tab, text="Şifreni Mi Unuttun ?", command=lambda: self.sayfa_gecis(3)).pack(pady=10)
        tk.Label(giris_tab, text="Hesabin Yok Mu ?").pack(pady=10)
        tk.Button(giris_tab, text="Kayıt Ol", command=lambda: self.sayfa_gecis(2)).pack(pady=10)

    def kayit_ekrani(self):
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

        tk.Button(kayit_tab, text="Kayit Ol", command=self.kullanici_kaydet).pack(pady=10)
        tk.Label(kayit_tab, text="Hesabin Var Mi?").pack(pady=10)
        tk.Button(kayit_tab, text="Giris Yap", command=lambda: self.sayfa_gecis(0)).pack(pady=10)

    def sifremi_unuttum_ekrani(self):
        unuttum_tab = ttk.Frame(self.not_defteri)
        self.not_defteri.add(unuttum_tab, text="Şifremi Unuttum")

        tk.Label(unuttum_tab, text="Giriş Yaparken Sorun mu Yaşıyorsun?").pack(pady=10) 
        tk.Label(unuttum_tab, text="E-posta adresini, telefon numaranı veya").pack(pady=10)
        tk.Label(unuttum_tab, text="kullanıcı adını gir ve hesabına yeniden").pack(pady=10)
        tk.Label(unuttum_tab, text="girebilmen için sana bir bağlantı gönderelim.").pack(pady=10)
        
        tk.Label(unuttum_tab, text="Ad Soyad:").pack()
        self.ad_soyad_entry_unuttum = tk.Entry(unuttum_tab)
        self.ad_soyad_entry_unuttum.pack()

        tk.Label(unuttum_tab, text="E-posta Adresi:").pack()
        self.eposta_entry_unuttum = tk.Entry(unuttum_tab)
        self.eposta_entry_unuttum.pack()

        tk.Button(unuttum_tab, text="Doğrulama Kodu Gönder", command=lambda: self.sayfa_gecis(4)).pack(pady=10)
        tk.Label(unuttum_tab, text="Veya").pack(pady=10)   
        tk.Button(unuttum_tab, text="Yeni Hesap Olustur", command=lambda: self.sayfa_gecis(2)).pack(pady=10)  
        tk.Button(unuttum_tab, text="Giris Ekranina Don", command=lambda: self.sayfa_gecis(0)).pack(pady=10)

    def eposta_dogrulama_ekrani(self):
        dogrulama_tab = ttk.Frame(self.not_defteri)
        self.not_defteri.add(dogrulama_tab, text="E-Posta Doğrulama")

        tk.Label(dogrulama_tab, text="Doğrulama Kodu").pack()
        self.dogrulama_entry = tk.Entry(dogrulama_tab)
        self.dogrulama_entry.pack()

        tk.Button(dogrulama_tab, text="Önceki Sayfa", command=lambda: self.sayfa_gecis(3)).pack(pady=10)
        tk.Button(dogrulama_tab, text="Giris Ekranina Don", command=lambda: self.sayfa_gecis(0)).pack(pady=10)
        tk.Button(dogrulama_tab, text="Yeni Şifre Oluştur", command=lambda: self.sayfa_gecis(5)).pack(pady=10)

    def yeni_sifre_ekrani(self):
        yeni_sifre_tab = ttk.Frame(self.not_defteri)
        self.not_defteri.add(yeni_sifre_tab, text="Yeni Şifre Oluştur")

        tk.Label(yeni_sifre_tab, text="Yeni Şifre:").pack()
        self.yeni_sifre_entry = tk.Entry(yeni_sifre_tab, show="*")
        self.yeni_sifre_entry.pack()

        tk.Label(yeni_sifre_tab, text="Yeni Şifre Tekrar:").pack()
        self.yeni_sifre_tekrar_entry = tk.Entry(
            yeni_sifre_tab, show="*")
        self.yeni_sifre_tekrar_entry.pack()

        tk.Button(yeni_sifre_tab, text="Şifreyi Değiştir", command=self.sifreyi_degistir).pack(pady=10) 
        tk.Button(yeni_sifre_tab, text="Giris Yap", command=lambda: self.sayfa_gecis(0)).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    uygulama = Uygulama(root)
    root.mainloop()
