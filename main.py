import tkinter as tk
from tkinter import ttk, messagebox
import json
import re
import hashlib
import random
import smtplib
import string
from email.mime.text import MIMEText
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

    def sayfayi_goster(self):
        if self.sayfa_numarasi in self.sayfalar:
            self.sayfalar[self.sayfa_numarasi]()
            self.not_defteri.pack(expand=1, fill="both")
        else:
            print("Geçersiz sayfa numarası.")

    def sayfa_gecis(self, hedef_sayfa):
        self.not_defteri.forget(0)
        self.not_defteri.pack_forget()
        self.sayfa_numarasi = hedef_sayfa
        self.sayfayi_goster()

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

        tk.Button(giris_tab, text="Giris Yap", command=lambda: self.sayfa_gecis(1)).pack(pady=10)
        tk.Button(giris_tab, text="Kayıt Ol", command=lambda: self.sayfa_gecis(2)).pack(pady=10)
        tk.Button(giris_tab, text="Şifremi Unuttum", command=lambda: self.sayfa_gecis(3)).pack(pady=10)

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

        tk.Button(kayit_tab, text="Giris Ekranina Don", command=lambda: self.sayfa_gecis(0)).pack(pady=10)
        tk.Button(kayit_tab, text="Şifremi Unuttum", command=lambda: self.sayfa_gecis(3)).pack(pady=10)

    def sifremi_unuttum_ekrani(self):
        unuttum_tab = ttk.Frame(self.not_defteri)
        self.not_defteri.add(unuttum_tab, text="Şifremi Unuttum")

        tk.Label(unuttum_tab, text="Ad Soyad:").pack()
        self.ad_soyad_entry_unuttum = tk.Entry(unuttum_tab)
        self.ad_soyad_entry_unuttum.pack()

        tk.Label(unuttum_tab, text="E-posta Adresi:").pack()
        self.eposta_entry_unuttum = tk.Entry(unuttum_tab)
        self.eposta_entry_unuttum.pack()
        
        tk.Button(unuttum_tab, text="Önceki Sayfa", command=lambda: self.sayfa_gecis(2)).pack(pady=10)
        tk.Button(unuttum_tab, text="Giris Ekranina Don", command=lambda: self.sayfa_gecis(0)).pack(pady=10)
        tk.Button(unuttum_tab, text="Doğrulama Kodu Gönder", command=lambda: self.sayfa_gecis(4)).pack(pady=10)

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
