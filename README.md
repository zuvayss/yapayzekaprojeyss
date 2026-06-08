# ✈️ YOLO Nesne Tespit Arayüzü

Eğitilmiş bir **YOLO (Ultralytics)** modeli (`best.pt`) ile resim üzerinde nesne tespiti yapan basit bir web arayüzü. Kullanıcı bir resim yükler, modele gönderir ve tespit edilen sınıfları (örn. *ucak*) güven yüzdeleriyle birlikte ekranda görür.

Arayüz **Streamlit** ile geliştirilmiştir.

---

## 📸 Ne yapar?

- Bilgisayardan resim (jpg / jpeg / png) yükleme
- Yüklenen resmi önizleme
- Tek tıkla modele gönderme
- Üzerine kutu (bounding box) çizilmiş sonuç resmini gösterme
- Tespit edilen her nesnenin **sınıf adı + güven yüzdesi** listesi
- Ayarlanabilir güven eşiği (confidence threshold)

---

## 📂 Proje Yapısı

```
ucak_tespit/
├── app.py                 # Streamlit arayüz kodu
├── best.pt                # Eğitilmiş YOLO modeli (sizin tarafınızdan eklenir)
├── requirements.txt       # Gerekli kütüphaneler
├── README.md              # Bu dosya
└── KURULUM_KILAVUZU.md    # Detaylı, adım adım kurulum anlatımı
```

> ⚠️ `best.pt` dosyası `app.py` ile **aynı klasörde** olmalıdır.

---

## ⚡ Hızlı Başlangıç

```bash
# 1) Kütüphaneleri kur
pip install -r requirements.txt

# 2) Arayüzü başlat
streamlit run app.py
```

Tarayıcı otomatik açılır: `http://localhost:8501`

> Daha ayrıntılı, hiç bilmeyenler için anlatım: **KURULUM_KILAVUZU.md**

---

## 🧰 Gereksinimler

- Python 3.9+
- streamlit
- ultralytics (YOLO)
- pillow
- numpy

---

## 🚀 Kullanım

1. **Resim seç** alanından bir resim yükle.
2. **🚀 Modele Gönder** butonuna bas.
3. Sonuç resmini ve tespit edilen sınıf listesini gör.
4. Gerekirse **güven eşiği** kaydırıcısıyla hassasiyeti ayarla.

---

## 🛠️ Sık Karşılaşılan Sorunlar

| Sorun | Çözüm |
|-------|-------|
| `streamlit tanınmıyor` | `python -m streamlit run app.py` |
| `FileNotFoundError: best.pt` | `best.pt`'yi `app.py` ile aynı klasöre koy |
| Sınıf adı `class0` görünüyor | Eğitimde sınıf isimleri tanımlı değil (teknik dokümana bak) |
| Hiçbir nesne bulunamıyor | Güven eşiğini düşür (örn. 0.10) |

---

## Model Dosyası
https://drive.google.com/file/d/1XgiCWVMF945xBDZeVwnSR7m6fWaXqelQ/view?usp=sharing

---

## 👤 Geliştiriciler

- Yavuz Selim Serdar
