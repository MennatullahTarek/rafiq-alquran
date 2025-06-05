import streamlit as st
import datetime
import time
import pandas as pd
import os

def get_menshawi_audio_url(sura, aya):

    try:
        sura_str = str(sura).zfill(3)
        aya_str = str(aya).zfill(3)
        return f"https://verses.quran.com/Menshawi/Mujawwad/Menshawi_Muallim_{sura_str}{aya_str}.mp3"
    except:
        return None

def save_hifz_record(sura, aya, repeat):
    row = {
        "سورة": sura,
        "آية": aya,
        "عدد التكرار": repeat,
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
    st.title("🎧 مساعد الحفظ - بصوت المنشاوي (معلم)")
    
    sura_number = st.number_input("اختر رقم السورة", min_value=1, max_value=114, step=1)
    aya_number = st.number_input("اختر رقم الآية", min_value=1, step=1)
    repeat_count = st.slider("عدد مرات التكرار", 1, 10, 3)

    if st.button("ابدأ التكرار"):
        audio_url = get_menshawi_audio_url(sura_number, aya_number)
        if audio_url:
            for i in range(repeat_count):
                st.audio(audio_url, format="audio/mp3")
                st.info(f"تشغيل رقم {i+1}")
                time.sleep(6)  
            save_hifz_record(sura_number, aya_number, repeat_count)
            st.success("✅ تم تشغيل الآية وتسجيل التكرار.")
        else:
            st.error("⚠️ لم يتم العثور على الصوت.")

if __name__ == "__main__":
    app()
