# Teknik Doküman — YOLO Nesne Tespit Arayüzü

**Proje:** Eğitilmiş YOLO modeli ile web tabanlı nesne tespit arayüzü
**Teknoloji:** Python, Streamlit, Ultralytics YOLO
**Belge türü:** Teknik tasarım ve çalışma prensibi dokümanı

---

## 1. Amaç ve Kapsam

Bu projenin amacı, daha önce eğitilmiş bir YOLO (You Only Look Once) nesne tespit modelini (`best.pt`) son kullanıcının kolayca kullanabileceği bir grafiksel arayüze bağlamaktır. Kullanıcı, herhangi bir kod yazmadan veya komut satırı bilmeden, bir resim yükleyerek model çıktısını (tespit edilen sınıflar ve konumları) görsel olarak elde edebilir.

Kapsam, tek bir resim üzerinde çıkarım (inference) yapmak ve sonucu görselleştirmekle sınırlıdır. Model eğitimi bu projenin kapsamı dışındadır; model hazır kabul edilir.

---

## 2. Sistem Mimarisi

Uygulama, üç katmanlı basit bir akıştan oluşur:

```
┌─────────────┐     resim      ┌──────────────┐    numpy dizisi   ┌─────────────┐
│  Kullanıcı  │  ───────────▶  │   Streamlit  │  ──────────────▶  │  YOLO Model │
│ (Tarayıcı)  │                │   Arayüzü    │                   │  (best.pt)  │
│             │  ◀───────────  │   (app.py)   │  ◀──────────────  │             │
└─────────────┘   sonuç+kutu   └──────────────┘   tespit sonucu   └─────────────┘
```

1. **Sunum katmanı (Streamlit):** Tarayıcıda çalışan arayüz. Dosya yükleme, buton ve sonuç gösterimini sağlar.
2. **İşlem katmanı (app.py):** Yüklenen resmi modele uygun formata çevirir, modeli çağırır, dönen sonucu görsel ve metin olarak hazırlar.
3. **Model katmanı (YOLO / best.pt):** Asıl tespiti yapan eğitilmiş ağ. Resmi alır, içindeki nesnelerin sınıfını ve sınır kutularını döndürür.

Tüm bileşenler aynı makinede (yerel) çalışır; harici bir API veya sunucu gerektirmez. Streamlit kendi içinde gömülü bir web sunucusu çalıştırarak arayüzü `localhost:8501` üzerinden sunar.

---

## 3. Kullanılan Teknolojiler

| Teknoloji | Görevi |
|-----------|--------|
| **Python 3.9+** | Programlama dili |
| **Streamlit** | Web arayüzü (kullanıcı etkileşimi, dosya yükleme, görsel gösterim) |
| **Ultralytics YOLO** | Model yükleme ve çıkarım (inference) |
| **Pillow (PIL)** | Resim açma ve format dönüşümü |
| **NumPy** | Resmi sayısal diziye (array) çevirme |

---

## 4. Veri Akışı (Çalışma Prensibi)

Bir resim yüklendiğinde gerçekleşen adımlar:

1. **Yükleme:** Kullanıcı `st.file_uploader` ile bir resim seçer. Streamlit bu dosyayı bellekte tutar.
2. **Açma:** Resim Pillow ile açılır ve `RGB` formatına çevrilir (`convert("RGB")`). Bu, PNG'lerdeki alfa kanalı gibi sorunları engeller.
3. **Dönüştürme:** Resim `numpy.array()` ile sayısal bir diziye çevrilir; YOLO bu formatı kabul eder.
4. **Çıkarım:** `model.predict(...)` çağrılır. Belirlenen güven eşiği (`conf`) altındaki tespitler elenir.
5. **Görselleştirme:** `sonuc.plot()` ile resmin üzerine sınır kutuları ve etiketler çizilir. YOLO'nun çıktısı BGR kanal sırasında olduğu için `[:, :, ::-1]` ile RGB'ye çevrilir.
6. **Listeleme:** Her tespit kutusu için sınıf kimliği (`cls`), sınıf adı (`model.names[id]`) ve güven değeri (`conf`) okunarak ekrana yazılır.

---

## 5. Önemli Tasarım Kararları

### 5.1 Model Önbelleğe Alma (Caching)
Model `@st.cache_resource` dekoratörü ile yüklenir. Streamlit, kullanıcı her etkileşimde bulunduğunda betiği baştan çalıştırır; bu dekoratör olmasaydı model **her seferinde** yeniden diskten yüklenir ve uygulama çok yavaşlardı. Dekoratör sayesinde model bellekte bir kez tutulur.

### 5.2 Ayarlanabilir Güven Eşiği
Sabit bir eşik yerine kullanıcıya kaydırıcı (`st.slider`) sunulmuştur. Bu, farklı modellerin ve sahnelerin farklı hassasiyet gerektirebilmesi nedeniyle esneklik sağlar. Varsayılan değer 0.25'tir.

### 5.3 Sınıf İsimleri
Sınıf adları modelin kendi içinde gömülü olan `model.names` sözlüğünden okunur. Eğer eğitim sırasında anlamlı isimler tanımlanmadıysa, etiketler `class0`, `class1` şeklinde görünür. Bu durumda `app.py` içinde elle bir eşleme sözlüğü tanımlanarak düzeltilebilir.

---

## 6. Kod Yapısının Özeti (app.py)

| Bölüm | İşlevi |
|-------|--------|
| Sayfa ayarları | Başlık, ikon ve düzen tanımı |
| `modeli_yukle()` | Modeli önbellekli şekilde yükler |
| Güven eşiği kaydırıcısı | Hassasiyet ayarı |
| Dosya yükleyici | Resim alır ve önizler |
| "Modele Gönder" bloğu | Çıkarım yapar, sonucu görselleştirir |
| Sınıf listeleme döngüsü | Tespitleri metin olarak yazar |

---

## 7. Kurulum ve Çalıştırma (Özet)

```bash
pip install -r requirements.txt
streamlit run app.py
```

> `best.pt` modeli `app.py` ile aynı dizinde bulunmalıdır.
> Ayrıntılı, adım adım kurulum için **KURULUM_KILAVUZU.md** belgesine bakınız.

---

## 8. Sınırlamalar ve Geliştirme Önerileri

**Mevcut sınırlamalar:**
- Aynı anda tek resim işlenir (toplu işlem yoktur).
- Yalnızca yerel makinede çalışır.
- Video veya gerçek zamanlı kamera desteği yoktur.

**Olası geliştirmeler:**
- Birden fazla resmin toplu işlenmesi.
- Sonuçların `.csv` veya `.json` olarak dışa aktarılması.
- Video/kamera akışı üzerinde gerçek zamanlı tespit.
- Tespit sonuçlarının kutu koordinatlarıyla birlikte tabloda gösterilmesi.
- Bulut sunucuya dağıtım (Streamlit Community Cloud, Hugging Face Spaces vb.).

---

## 9. Test ve Doğrulama

Uygulamanın doğru çalıştığı şu adımlarla doğrulanabilir:

1. Bilinen bir nesne içeren bir test resmi yükle.
2. Modelin doğru sınıfı, makul bir güven değeriyle (örn. > %50) tespit ettiğini gözlemle.
3. Güven eşiğini artırıp azaltarak tespit sayısının beklendiği gibi değiştiğini doğrula.
4. Nesne içermeyen bir resimde uygulamanın "tespit edilemedi" uyarısı verdiğini kontrol et.

---

## 10. Geliştirici Bilgileri

- Yavuz Selim Serdar
