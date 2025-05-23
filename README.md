# Kişisel Finans Takip Uygulaması

## Proje Açıklaması
Bu proje, kullanıcıların gelir ve giderlerini kolayca takip etmelerini sağlayan basit bir masaüstü finans yönetim uygulamasıdır. Uygulama, işlem ekleme, düzenleme ve silme gibi temel fonksiyonların yanı sıra, finansal durumu görselleştirmek için grafikler sunar. Kullanıcı verileri yerel olarak JSON dosyalarında saklanır.

## Özellikler
- Gelir ve gider kaydı
- İşlemleri düzenleme ve silme
- İşlem geçmişini görüntüleme
- Tarih aralığına göre filtreleme
- Gelir/Gider dağılım grafiği
- Gider kategorileri dağılım grafiği
- Bütçe belirleme ve bütçe aşımı uyarıları
- Koyu tema desteği

## Teknolojiler
- Python
- Tkinter (GUI için)
- Matplotlib (Grafikler için)
- tkcalendar (Tarih seçimi için)
- pandas (Veri işleme için)
- numpy (pandas bağımlılığı)

## Kurulum

### Gereksinimler
- Python 3.6 veya üzeri
- Gerekli Python kütüphaneleri

### Kütüphanelerin Kurulumu
Projeyi çalıştırmadan önce gerekli kütüphaneleri kurmanız gerekmektedir. Terminal veya komut istemcisini açın ve projenin ana dizinine gidin. Ardından aşağıdaki komutları çalıştırın:

```bash
pip install matplotlib
pip install tkcalendar
pip install pandas
pip install numpy
```

### Projeyi Çalıştırma
Kütüphaneleri kurduktan sonra uygulamayı çalıştırmak çok basittir. Projenin ana dizininde terminal veya komut istemcisini açın ve aşağıdaki komutu çalıştırın:

```bash
python finans_takip.py
```

veya

```bash
py finans_takip.py
```

Uygulamanın arayüzü açılacaktır.

## Veri Saklama
Uygulama verileri, projenin ana dizininde bulunan `finans_verileri.json` ve `butceler.json` dosyalarında saklanır. Bu dosyaları silerseniz tüm verileriniz kaybolur, bu yüzden dikkatli olun.

## Katkıda Bulunma
Projeye katkıda bulunmak isterseniz, pull request göndererek veya issues açarak geliştirmelere yardımcı olabilirsiniz.

## İletişim
Sorularınız veya geri bildirimleriniz için lütfen muhammetenesgumus0@gmail.com adresine ulaşın veya bir issue açın. 
