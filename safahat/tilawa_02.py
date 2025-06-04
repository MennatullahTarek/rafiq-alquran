import streamlit as st

def app():
    st.title("مدرب التلاوة")
    st.write("اختر القارئ والسورة للاستماع إلى تلاوتها:")

    readers = {
        "محمد صديق المنشاوي": "minsh",
        "عبد الباسط عبد الصمد": "abdulbasit_mujawwad",
        "محمود الحصري": "husr"
    }

    # قائمة السور (كمثال - تقدر تضيف كل السور)
    surahs = {
        "الفاتحة": "1",
        "البقرة": "2",
        "آل عمران": "3",
        "النساء": "4",
        "المائدة": "5",
        "الأنعام": "6",
        # ممكن تضيف باقي السور هنا
    }

    reader_choice = st.selectbox("اختر القارئ:", list(readers.keys()))
    surah_choice = st.selectbox("اختر السورة:", list(surahs.keys()))

    if reader_choice and surah_choice:

        server_map = {
            "husr": 8,
            "abdulbasit_mujawwad": 10,
            "minsh": 7
        }

        qaree_code = readers[reader_choice]
        server_num = server_map.get(qaree_code, 8)  # افتراضياً الحصري
        surah_num = surahs[surah_choice]

        audio_url = f"https://server{server_num}.mp3quran.net/{qaree_code}/{surah_num}.mp3"

        st.write(f"تلاوة سورة {surah_choice} بصوت {reader_choice}:")
        st.audio(audio_url, format="audio/mp3")
