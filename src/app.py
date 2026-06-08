# app.py
# YOLO modeli (best.pt) ile resim yukleyip nesne tespiti yapan Streamlit arayuzu
# Calistirmak icin: streamlit run app.py

import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np

# -----------------------------------------------------------
# 1) Sayfa ayarlari
# -----------------------------------------------------------
st.set_page_config(page_title="Ucak Tespit Arayuzu", page_icon="✈️", layout="centered")

st.title("✈️ Nesne Tespit Arayuzu")
st.write("Bir resim yukle, modele gonder, sonucu ekranda gor.")

# -----------------------------------------------------------
# 2) Modeli sadece bir kez yukle
# -----------------------------------------------------------
@st.cache_resource
def modeli_yukle():
    return YOLO("best.pt")  # best.pt aynı klasörde olmalı

model = modeli_yukle()

# -----------------------------------------------------------
# 3) Confidence slider
# -----------------------------------------------------------
guven_esigi = st.slider("Guven esigi (confidence)", 0.0, 1.0, 0.25, 0.05)

# -----------------------------------------------------------
# 4) Image upload
# -----------------------------------------------------------
yuklenen = st.file_uploader(
    "Resim sec (jpg / jpeg / png)",
    type=["jpg", "jpeg", "png"]
)

if yuklenen is not None:
    resim = Image.open(yuklenen).convert("RGB")
    st.image(resim, caption="Yuklenen resim", use_container_width=True)

    # -----------------------------------------------------------
    # 5) Model inference
    # -----------------------------------------------------------
    if st.button("🚀 Modele Gonder"):
        with st.spinner("Model calisiyor, lutfen bekleyin..."):

            sonuclar = model.predict(
                source=np.array(resim),
                conf=guven_esigi,
                imgsz=640   # <<< BURASI EKLENDİ
            )

            sonuc = sonuclar[0]

            # çizilmiş görüntü (BGR -> RGB)
            cizilmis = sonuc.plot()[:, :, ::-1]

        st.success("Tahmin tamamlandi!")
        st.image(cizilmis, caption="Tespit sonucu", use_container_width=True)

        # -----------------------------------------------------------
        # 6) Sonuç listesi
        # -----------------------------------------------------------
        st.subheader("Tespit edilen nesneler:")

        if len(sonuc.boxes) == 0:
            st.warning("Hicbir nesne tespit edilemedi. Guven esigini dusurmeyi dene.")
        else:
            for kutu in sonuc.boxes:
                sinif_id = int(kutu.cls[0])
                sinif_adi = model.names[sinif_id]
                guven = float(kutu.conf[0])
                st.write(f"• **{sinif_adi}** — guven: %{guven*100:.1f}")