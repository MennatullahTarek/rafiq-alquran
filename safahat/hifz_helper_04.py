import streamlit as st
import datetime
import time
import pandas as pd
import os
import requests

import requests

def get_audio_url(sura, aya, reciter="7"):  
    """
    جلب رابط صوت الآية من Al Quran Cloud API
    """
    try:
        response = requests.get(f"https://api.alquran.cloud/v1/ayah/{sura}:{aya}/ar.alafasy")
        if response.status_code == 200:
            data = response.json()
            return data['data']['audio']
        else:
            return None
    except Exception:
        return None


def save_hifz_record(sura, aya, repeat):
    """
    حفظ سجل التكرار في ملف CSV
    """
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
        audio_url = get_audio_url(sura_number, aya_number)

        if audio_url:
            st.markdown(f"🔗 رابط الصوت المباشر: [اضغط هنا للاستماع]({audio_url})")

            for i in range(repeat_count):
                st.audio(audio_url, format="audio/mp3")
                st.info(f"📻 التشغيل رقم {i + 1}")
                time.sleep(6)

            save_hifz_record(sura_number, aya_number, repeat_count)
            st.success("✅ تم تشغيل الآية وتسجيل التكرار بنجاح.")
        else:
            st.error("⚠️ لم يتم العثور على رابط الصوت. تأكد من اتصالك بالإنترنت وصحة رقم السورة والآية.")

if __name__ == "__main__":
    app()
