import tkinter as tk
from tkinter import ttk
class Uygulama(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Evolvie")
        self.geometry("800x600")

        self.not_defteri = ttk.Notebook(self)
        self.not_defteri.pack(expand=True, fill=tk.BOTH)

        self.login_tab = ttk.Frame(self.not_defteri)
        self.anasayfa_tab = ttk.Frame(self.not_defteri)
        self.uyku_ve_aktivite_tab = ttk.Frame(self.not_defteri)
        self.beslenme_ve_spor_tab = ttk.Frame(self.not_defteri)
        
        self.not_defteri.add(self.login_tab, text="Giris Yap")
        self.not_defteri.add(self.anasayfa_tab, text="Anasayfa")
        self.not_defteri.add(self.uyku_ve_aktivite_tab, text="Uyku ve Aktivite")
        self.not_defteri.add(self.beslenme_ve_spor_tab, text="Beslenme ve Spor")

        
        self.login_label = tk.Label(self.login_tab, text="Kullanici Adi")
        self.login_label.pack()
        self.login_entry = tk.Entry(self.login_tab)
        self.login_entry.pack()
        
        self.login_label = tk.Label(self.login_tab, text="Sifre")
        self.login_label.pack()
        self.login_entry = tk.Entry(self.login_tab)
        self.login_entry.pack()

        self.login_giris_button = tk.Button(self.login_tab, text="Giris Yap", command=self.giris)
        self.login_giris_button.pack()
        
        self.uyku_saati_label = tk.Label(self.uyku_ve_aktivite_tab, text="Uyku Saati:")
        self.uyku_saati_label.pack()

        self.uyku_saati_entry = tk.Entry(self.uyku_ve_aktivite_tab)
        self.uyku_saati_entry.pack()

        self.uyku_saati_kaydet_button = tk.Button(self.uyku_ve_aktivite_tab, text="Kaydet", command=self.kaydet)
        self.uyku_saati_kaydet_button.pack()

    def giris(self):
        login = self.login_entry.get()
        
    def kaydet(self):
        uyku_saati = self.uyku_saati_entry.get()
        # Bu noktada veriyi bir yerde saklayabilirsiniz.

if __name__ == "__main__":
    uygulama = Uygulama()
    uygulama.mainloop()

