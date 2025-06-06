import streamlit as st
import datetime
import time
import pandas as pd
import os
import requests


surah_list = [
    ("الفاتحة", 1), ("البقرة", 2), ("آل عمران", 3), ("النساء", 4), ("المائدة", 5),
    ("الأنعام", 6), ("الأعراف", 7), ("الأنفال", 8), ("التوبة", 9), ("يونس", 10),
    # تم تقصير القائمة للعرض فقط، اكمل باقي السور حسب الحاجة
    ("الناس", 114)
]


def get_audio_url(sura, aya):
    try:
        response = requests.get(f"https://api.alquran.cloud/v1/ayah/{sura}:{aya}/ar.alafasy")
        if response.status_code == 200:
            data = response.json()
            return data['data']['audio']
        else:
            return None
    except Exception:
        return None


def save_hifz_record(sura, aya):
    row = {
        "سورة": sura,
        "آية": aya,
        "الوقت": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    file_path = "data/hifz_log.csv"
    os.makedirs("data", exist_ok=True)

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])

    df.to_csv(file_path, index=False)


def app():
    st.set_page_config(page_title="مساعد الحفظ", layout="centered")


    st.markdown("""
        <style>
        body, .stApp {
            background-color: #F5F5F5;
            direction: rtl;
            font-family: 'Cairo', sans-serif;
        }
        .main-title {
            color: #2E7D32;
            font-size: 2.3rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            color: #555;
            font-size: 1.1rem;
            margin-bottom: 25px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-title">🎧 مساعد الحفظ الذكي</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">اختر السورة والآية واستمع إليها بتكرار عند الحاجة ✨</div>', unsafe_allow_html=True)

   
    surah_name = st.selectbox("📘 اختر السورة", [name for name, _ in surah_list])
    sura_number = next(num for name, num in surah_list if name == surah_name)
    aya_number = st.number_input("🔢 رقم الآية", min_value=1, step=1)


    if st.button("▶️ تشغيل الآية"):
        audio_url = get_audio_url(sura_number, aya_number)
        if audio_url:
            st.audio(audio_url, format="audio/mp3")
            st.success("✅ تم تشغيل الآية بنجاح.")
            save_hifz_record(surah_name, aya_number)
        else:
            st.error("⚠️ لم يتم العثور على رابط الصوت.")


    if st.button("🔁 كرر الآية مرة أخرى"):
        audio_url = get_audio_url(sura_number, aya_number)
        if audio_url:
            st.audio(audio_url, format="audio/mp3")
            st.info("🔄 تكرار الآية...")
            save_hifz_record(surah_name, aya_number)
        else:
            st.error("⚠️ لم يتم العثور على رابط الصوت.")

  
    with st.expander("📜 عرض سجل الاستماع"):
        file_path = "data/hifz_log.csv"
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            st.dataframe(df.tail(10), use_container_width=True)
        else:
            st.info("لا يوجد سجل محفوظ بعد.")

if __name__ == "__main__":
    app()
