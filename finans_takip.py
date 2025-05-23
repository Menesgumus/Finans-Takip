import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import calendar
import locale
from tkcalendar import DateEntry
import pandas as pd
import numpy as np

# Türkçe tarih formatı için
try:
    locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')
except:
    locale.setlocale(locale.LC_ALL, 'Turkish_Turkey.1254')

class ModernButton(ttk.Button):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self['style'] = 'Modern.TButton'
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
    def on_enter(self, e):
        self['style'] = 'Hover.TButton'
    def on_leave(self, e):
        self['style'] = 'Modern.TButton'

class FinansTakip:
    def __init__(self):
        # Ana pencere ayarları
        self.pencere = tk.Tk()
        self.pencere.title("Finans Takip")
        self.pencere.geometry("1400x800")
        self.pencere.configure(bg='#2b2b2b')
        
        # Stil ayarları
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#2b2b2b')
        self.style.configure('TLabel', background='#2b2b2b', foreground='white')
        self.style.configure('Modern.TButton', 
                           background='#3498db', 
                           foreground='white', 
                           font=('Helvetica', 10, 'bold'),
                           padding=5)
        self.style.map('Modern.TButton',
                      background=[('active', '#2980b9')],
                      foreground=[('active', 'white')])
        self.style.configure('Hover.TButton', 
                           background='#2980b9', 
                           foreground='white', 
                           font=('Helvetica', 10, 'bold'),
                           padding=5)
        
        # Modern Giriş ve Combobox Stilleri
        self.style.configure('Modern.TEntry', 
                           fieldbackground='#3c3c3c', 
                           foreground='white', 
                           borderwidth=0,
                           focusthickness=3,
                           focuscolor='#3498db',
                           padding=[5, 5])
        self.style.configure('Modern.TCombobox', 
                           fieldbackground='#3c3c3c', 
                           foreground='white', 
                           background='#3c3c3c',
                           selectbackground='#3498db',
                           selectforeground='white',
                           borderwidth=0,
                           focusthickness=3,
                           focuscolor='#3498db',
                           padding=[5, 5])
        self.style.map('Modern.TCombobox', 
                      fieldbackground=[('readonly', '#3c3c3c')],
                      selectbackground=[('readonly', '#3498db')],
                      selectforeground=[('readonly', 'white')])
        
        # Verileri yükle
        self.veriler = self.verileri_yukle()
        self.butceler = self.butceleri_yukle()
        
        # Ana container
        self.container = ttk.Frame(self.pencere)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Sol panel (Giriş formu)
        self.sol_panel = ttk.Frame(self.container)
        self.sol_panel.pack(side="left", fill="y", padx=(0, 10))
        
        # Başlık
        ttk.Label(self.sol_panel, text="Yeni İşlem", font=("Helvetica", 20, "bold")).pack(pady=20)
        
        # Giriş formu
        self.form_frame = ttk.Frame(self.sol_panel)
        self.form_frame.pack(fill="x", padx=20, pady=10)
        
        # Tutar
        ttk.Label(self.form_frame, text="Tutar:").pack(anchor="w")
        self.tutar = ttk.Entry(self.form_frame, style='Modern.TEntry')
        self.tutar.pack(fill="x", pady=(0, 10))
        
        # Açıklama
        ttk.Label(self.form_frame, text="Açıklama:").pack(anchor="w")
        self.aciklama = ttk.Entry(self.form_frame, style='Modern.TEntry')
        self.aciklama.pack(fill="x", pady=(0, 10))
        
        # Tür
        ttk.Label(self.form_frame, text="Tür:").pack(anchor="w")
        self.tur = ttk.Combobox(self.form_frame, values=["Gelir", "Gider"], state="readonly", style='Modern.TCombobox')
        self.tur.set("Gelir")
        self.tur.pack(fill="x", pady=(0, 10))
        
        # Kategori
        ttk.Label(self.form_frame, text="Kategori:").pack(anchor="w")
        self.kategori = ttk.Combobox(self.form_frame, values=[
            "Maaş", "Yatırım", "Kira Geliri", "Diğer Gelir",  # Gelir kategorileri
            "Market", "Faturalar", "Ulaşım", "Sağlık", "Eğlence", "Kira", "Diğer"  # Gider kategorileri
        ], state="readonly", style='Modern.TCombobox')
        self.kategori.set("Maaş")
        self.kategori.pack(fill="x", pady=(0, 10))
        
        # Tarih
        ttk.Label(self.form_frame, text="Tarih:").pack(anchor="w")
        self.tarih = DateEntry(self.form_frame, width=12, background='#3c3c3c',
                             foreground='white', borderwidth=2, locale='tr_TR')
        self.tarih.pack(fill="x", pady=(0, 10))
        
        # Kaydet butonu
        ModernButton(
            self.form_frame, 
            text="Kaydet",
            command=self.kaydet
        ).pack(fill="x", pady=10)
        
        # Bütçe ekleme butonu
        ModernButton(
            self.form_frame,
            text="Bütçe Ekle",
            command=self.butce_ekle_pencere
        ).pack(fill="x", pady=5)
        
        # Sağ panel (Grafikler ve liste)
        self.sag_panel = ttk.Frame(self.container)
        self.sag_panel.pack(side="right", fill="both", expand=True)
        
        # Filtre frame
        self.filtre_frame = ttk.Frame(self.sag_panel)
        self.filtre_frame.pack(fill="x", padx=10, pady=5)
        
        # Tarih filtreleri
        ttk.Label(self.filtre_frame, text="Tarih Aralığı:").pack(side="left", padx=5)
        self.baslangic_tarih = DateEntry(self.filtre_frame, width=12, background='#3c3c3c',
                                       foreground='white', borderwidth=2, locale='tr_TR')
        self.baslangic_tarih.pack(side="left", padx=5)
        
        ttk.Label(self.filtre_frame, text="-").pack(side="left", padx=5)
        
        self.bitis_tarih = DateEntry(self.filtre_frame, width=12, background='#3c3c3c',
                                   foreground='white', borderwidth=2, locale='tr_TR')
        self.bitis_tarih.pack(side="left", padx=5)
        
        # Filtre butonu
        ModernButton(
            self.filtre_frame,
            text="Filtrele",
            command=self.filtrele,
            width=10
        ).pack(side="left", padx=10)
        
        # Üst bilgi kartları
        self.bilgi_frame = ttk.Frame(self.sag_panel)
        self.bilgi_frame.pack(fill="x", padx=10, pady=10)
        
        # Gelir kartı
        self.gelir_kart = ttk.Frame(self.bilgi_frame)
        self.gelir_kart.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Label(self.gelir_kart, text="Toplam Gelir", font=("Helvetica", 14)).pack(pady=5)
        self.gelir_label = ttk.Label(self.gelir_kart, text="0.00 TL", font=("Helvetica", 20, "bold"))
        self.gelir_label.pack(pady=5)
        
        # Gider kartı
        self.gider_kart = ttk.Frame(self.bilgi_frame)
        self.gider_kart.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Label(self.gider_kart, text="Toplam Gider", font=("Helvetica", 14)).pack(pady=5)
        self.gider_label = ttk.Label(self.gider_kart, text="0.00 TL", font=("Helvetica", 20, "bold"))
        self.gider_label.pack(pady=5)
        
        # Bakiye kartı
        self.bakiye_kart = ttk.Frame(self.bilgi_frame)
        self.bakiye_kart.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Label(self.bakiye_kart, text="Bakiye", font=("Helvetica", 14)).pack(pady=5)
        self.bakiye_label = ttk.Label(self.bakiye_kart, text="0.00 TL", font=("Helvetica", 20, "bold"))
        self.bakiye_label.pack(pady=5)
        
        # Grafik frame
        self.grafik_frame = ttk.Frame(self.sag_panel)
        self.grafik_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Grafik oluştur
        self.grafik_olustur()
        
        # Liste frame
        self.liste_frame = ttk.Frame(self.sag_panel)
        self.liste_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Liste başlığı
        ttk.Label(self.liste_frame, text="İşlem Geçmişi", font=("Helvetica", 16, "bold")).pack(pady=10)
        
        # Liste ve butonlar için container
        self.liste_container = ttk.Frame(self.liste_frame)
        self.liste_container.pack(fill="both", expand=True)
        
        # Liste
        self.liste = tk.Text(self.liste_container, height=20, bg='#2b2b2b', fg='white')
        self.liste.pack(side="left", fill="both", expand=True)
        
        # Butonlar için frame
        self.buton_frame = ttk.Frame(self.liste_container)
        self.buton_frame.pack(side="right", fill="y", padx=5)
        
        # Verileri güncelle
        self.ozeti_guncelle()
        self.listeyi_guncelle()
        self.butce_kontrol()
    
    def verileri_yukle(self):
        try:
            with open("finans_verileri.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    
    def butceleri_yukle(self):
        try:
            with open("butceler.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    
    def verileri_kaydet(self):
        with open("finans_verileri.json", "w", encoding="utf-8") as f:
            json.dump(self.veriler, f, ensure_ascii=False, indent=2)
    
    def butceleri_kaydet(self):
        with open("butceler.json", "w", encoding="utf-8") as f:
            json.dump(self.butceler, f, ensure_ascii=False, indent=2)
    
    def kaydet(self):
        try:
            tutar = float(self.tutar.get())
            aciklama = self.aciklama.get()
            tur = self.tur.get()
            kategori = self.kategori.get()
            tarih = self.tarih.get_date().strftime("%d.%m.%Y")
            
            if not aciklama:
                messagebox.showerror("Hata", "Lütfen bir açıklama girin!")
                return
            
            yeni_kayit = {
                "tarih": tarih,
                "tur": tur,
                "tutar": tutar,
                "aciklama": aciklama,
                "kategori": kategori
            }
            
            self.veriler.append(yeni_kayit)
            self.verileri_kaydet()
            self.listeyi_guncelle()
            self.ozeti_guncelle()
            self.grafik_olustur()
            self.butce_kontrol()
            
            # Alanları temizle
            self.tutar.delete(0, "end")
            self.aciklama.delete(0, "end")
            self.tur.set("Gelir")
            self.kategori.set("Maaş")
            
            messagebox.showinfo("Başarılı", "Kayıt başarıyla eklendi!")
            
        except ValueError:
            messagebox.showerror("Hata", "Lütfen geçerli bir tutar girin!")
    
    def butce_ekle_pencere(self):
        butce_pencere = tk.Toplevel(self.pencere)
        butce_pencere.title("Bütçe Ekle")
        butce_pencere.geometry("400x300")
        butce_pencere.configure(bg='#2b2b2b')
        
        # Form frame
        form_frame = ttk.Frame(butce_pencere)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Kategori
        ttk.Label(form_frame, text="Kategori:").pack(anchor="w")
        kategori = ttk.Combobox(form_frame, values=[
            "Market", "Faturalar", "Ulaşım", "Sağlık", "Eğlence", "Kira", "Diğer"
        ], state="readonly", style='Modern.TCombobox')
        kategori.pack(fill="x", pady=(0, 10))
        
        # Tutar
        ttk.Label(form_frame, text="Aylık Bütçe:").pack(anchor="w")
        tutar = ttk.Entry(form_frame, style='Modern.TEntry')
        tutar.pack(fill="x", pady=(0, 10))
        
        # Kaydet butonu
        def butce_kaydet():
            try:
                yeni_butce = {
                    "kategori": kategori.get(),
                    "tutar": float(tutar.get()),
                    "ay": datetime.now().strftime("%Y-%m")
                }
                self.butceler.append(yeni_butce)
                self.butceleri_kaydet()
                self.butce_kontrol()
                butce_pencere.destroy()
                messagebox.showinfo("Başarılı", "Bütçe başarıyla eklendi!")
            except ValueError:
                messagebox.showerror("Hata", "Lütfen geçerli bir tutar girin!")
        
        ModernButton(form_frame, text="Kaydet", command=butce_kaydet).pack(fill="x", pady=20)
    
    def butce_kontrol(self):
        # Bu ayki bütçeleri kontrol et
        bu_ay = datetime.now().strftime("%Y-%m")
        bu_ay_butceler = [b for b in self.butceler if b["ay"] == bu_ay]
        
        # Bu ayki giderleri hesapla
        bu_ay_giderler = {}
        for kayit in self.veriler:
            if kayit["tur"] == "Gider":
                tarih = datetime.strptime(kayit["tarih"], "%d.%m.%Y")
                if tarih.strftime("%Y-%m") == bu_ay:
                    kategori = kayit["kategori"]
                    bu_ay_giderler[kategori] = bu_ay_giderler.get(kategori, 0) + kayit["tutar"]
        
        # Bütçe aşımı kontrolü
        for butce in bu_ay_butceler:
            kategori = butce["kategori"]
            if kategori in bu_ay_giderler:
                gider = bu_ay_giderler[kategori]
                if gider > butce["tutar"]:
                    messagebox.showwarning(
                        "Bütçe Aşımı",
                        f"{kategori} kategorisinde bütçe aşımı!\n"
                        f"Bütçe: {butce['tutar']:.2f} TL\n"
                        f"Harcama: {gider:.2f} TL"
                    )
    
    def filtrele(self):
        baslangic = self.baslangic_tarih.get_date()
        bitis = self.bitis_tarih.get_date()
        
        filtrelenmis_veriler = []
        for kayit in self.veriler:
            tarih = datetime.strptime(kayit["tarih"], "%d.%m.%Y").date()
            if baslangic <= tarih <= bitis:
                filtrelenmis_veriler.append(kayit)
        
        self.listeyi_guncelle(filtrelenmis_veriler)
        self.ozeti_guncelle(filtrelenmis_veriler)
        self.grafik_olustur(filtrelenmis_veriler)
    
    def listeyi_guncelle(self, veriler=None):
        if veriler is None:
            veriler = self.veriler
        
        self.liste.delete("1.0", "end")
        
        # Butonları temizle
        for widget in self.buton_frame.winfo_children():
            widget.destroy()
        
        # Son 10 işlemi göster
        son_islemler = veriler[-10:] if len(veriler) > 10 else veriler
        
        for i, kayit in enumerate(reversed(son_islemler)):
            renk = "#2ecc71" if kayit.get("tur", "") == "Gelir" else "#e74c3c"
            self.liste.insert("end", f"{kayit.get('tarih', '')} - {kayit.get('kategori', 'Bilinmiyor')}\n", "normal")
            self.liste.insert("end", f"{kayit.get('aciklama', '')}\n", "normal")
            self.liste.insert("end", f"{kayit.get('tutar', 0):.2f} TL\n", "normal")
            
            # Her kayıt için buton frame'i
            btn_frame = ttk.Frame(self.buton_frame)
            btn_frame.pack(fill="x", pady=2)
            
            # Düzenle ve Sil butonları
            ModernButton(btn_frame, text="Düzenle", 
                        command=lambda idx=len(veriler)-1-i: self.islem_duzenle(idx),
                        width=8).pack(side="top", pady=1)
            ModernButton(btn_frame, text="Sil", 
                        command=lambda idx=len(veriler)-1-i: self.islem_sil(idx),
                        width=8).pack(side="top", pady=1)
            
            self.liste.insert("end", "-" * 40 + "\n", "normal")
    
    def ozeti_guncelle(self, veriler=None):
        if veriler is None:
            veriler = self.veriler
            
        toplam_gelir = sum(kayit["tutar"] for kayit in veriler if kayit["tur"] == "Gelir")
        toplam_gider = sum(kayit["tutar"] for kayit in veriler if kayit["tur"] == "Gider")
        bakiye = toplam_gelir - toplam_gider
        
        self.gelir_label.configure(text=f"{toplam_gelir:.2f} TL")
        self.gider_label.configure(text=f"{toplam_gider:.2f} TL")
        self.bakiye_label.configure(text=f"{bakiye:.2f} TL")
        
        # Bakiye rengini ayarla
        if bakiye >= 0:
            self.bakiye_label.configure(foreground="#2ecc71")
        else:
            self.bakiye_label.configure(foreground="#e74c3c")
    
    def grafik_olustur(self, veriler=None):
        if veriler is None:
            veriler = self.veriler
            
        # Mevcut grafiği temizle
        for widget in self.grafik_frame.winfo_children():
            widget.destroy()
        
        # Yeni grafik oluştur (Aylık trend grafiği kaldırıldı)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        fig.patch.set_facecolor('#2b2b2b')
        
        # Gelir/Gider dağılımı
        gelirler = [kayit.get("tutar", 0) for kayit in veriler if kayit.get("tur") == "Gelir"]
        giderler = [kayit.get("tutar", 0) for kayit in veriler if kayit.get("tur") == "Gider"]
        
        total_gelir = sum(gelirler)
        total_gider = sum(giderler)
        
        # Veri varsa pie chartı çiz
        if total_gelir > 0 or total_gider > 0:
            ax1.pie([total_gelir, total_gider], 
                    labels=["Gelir", "Gider"],
                    colors=["#2ecc71", "#e74c3c"],
                    autopct='%1.1f%%',
                    textprops={'color': 'white'})
            ax1.set_title("Gelir/Gider Dağılımı", color='white')
        else:
            # Veri yoksa bilgilendirme metni ekle
            ax1.text(0.5, 0.5, "Grafik için veri yok", 
                     horizontalalignment='center', 
                     verticalalignment='center', 
                     color='white', 
                     fontsize=12)
            ax1.set_title("Gelir/Gider Dağılımı", color='white')
            ax1.axis('equal') # Pie chart gibi görünmesi için
        
        # Kategori dağılımı
        kategoriler = {}
        for kayit in veriler:
            if kayit.get("tur") == "Gider" and kayit.get("kategori"):
                kategori = kayit["kategori"]
                kategoriler[kategori] = kategoriler.get(kategori, 0) + kayit.get("tutar", 0)
        
        if kategoriler:
            ax2.pie(kategoriler.values(),
                   labels=kategoriler.keys(),
                   autopct='%1.1f%%',
                   textprops={'color': 'white'})
            ax2.set_title("Gider Kategorileri", color='white')
        
        # Grafik kenarlarını ayarla
        plt.tight_layout()
        
        # Grafiği Tkinter'a ekle
        canvas = FigureCanvasTkAgg(fig, master=self.grafik_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def islem_sil(self, idx):
        kayit = self.veriler[idx]
        cevap = messagebox.askyesno("İşlem Sil", f"{kayit.get('aciklama', '')} kaydını silmek istediğinize emin misiniz?")
        if cevap:
            self.veriler.pop(idx)
            self.verileri_kaydet()
            self.listeyi_guncelle()
            self.ozeti_guncelle()
            self.grafik_olustur()
            self.butce_kontrol()

    def islem_duzenle(self, idx):
        kayit = self.veriler[idx]
        duzenle_pencere = tk.Toplevel(self.pencere)
        duzenle_pencere.title("İşlem Düzenle")
        duzenle_pencere.geometry("400x400")
        duzenle_pencere.configure(bg='#2b2b2b')
        
        # Form frame
        form_frame = ttk.Frame(duzenle_pencere)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ttk.Label(form_frame, text="Tutar:").pack(anchor="w")
        tutar_entry = ttk.Entry(form_frame, style='Modern.TEntry')
        tutar_entry.insert(0, str(kayit.get('tutar', '')))
        tutar_entry.pack(fill="x", pady=(0, 10))
        
        ttk.Label(form_frame, text="Açıklama:").pack(anchor="w")
        aciklama_entry = ttk.Entry(form_frame, style='Modern.TEntry')
        aciklama_entry.insert(0, kayit.get('aciklama', ''))
        aciklama_entry.pack(fill="x", pady=(0, 10))
        
        ttk.Label(form_frame, text="Tür:").pack(anchor="w")
        tur_combo = ttk.Combobox(form_frame, values=["Gelir", "Gider"], state="readonly", style='Modern.TCombobox')
        tur_combo.set(kayit.get('tur', 'Gelir'))
        tur_combo.pack(fill="x", pady=(0, 10))
        
        ttk.Label(form_frame, text="Kategori:").pack(anchor="w")
        kategori_combo = ttk.Combobox(form_frame, values=[
            "Maaş", "Yatırım", "Kira Geliri", "Diğer Gelir",  # Gelir kategorileri
            "Market", "Faturalar", "Ulaşım", "Sağlık", "Eğlence", "Kira", "Diğer"  # Gider kategorileri
        ], state="readonly", style='Modern.TCombobox')
        kategori_combo.set(kayit.get('kategori', ''))
        kategori_combo.pack(fill="x", pady=(0, 10))
        
        ttk.Label(form_frame, text="Tarih:").pack(anchor="w")
        tarih_entry = DateEntry(form_frame, width=12, background='#3c3c3c', foreground='white', borderwidth=2, locale='tr_TR')
        try:
            tarih_entry.set_date(datetime.strptime(kayit.get('tarih', ''), '%d.%m.%Y'))
        except:
            pass
        tarih_entry.pack(fill="x", pady=(0, 10))
        
        def kaydet_duzenle():
            try:
                self.veriler[idx] = {
                    "tutar": float(tutar_entry.get()),
                    "aciklama": aciklama_entry.get(),
                    "tur": tur_combo.get(),
                    "kategori": kategori_combo.get(),
                    "tarih": tarih_entry.get_date().strftime('%d.%m.%Y')
                }
                self.verileri_kaydet()
                self.listeyi_guncelle()
                self.ozeti_guncelle()
                self.grafik_olustur()
                self.butce_kontrol()
                duzenle_pencere.destroy()
                messagebox.showinfo("Başarılı", "Kayıt güncellendi!")
            except ValueError:
                messagebox.showerror("Hata", "Lütfen geçerli bir tutar girin!")
        
        ModernButton(form_frame, text="Kaydet", command=kaydet_duzenle).pack(fill="x", pady=20)
    
    def baslat(self):
        self.pencere.mainloop()

if __name__ == "__main__":
    uygulama = FinansTakip()
    uygulama.baslat() 