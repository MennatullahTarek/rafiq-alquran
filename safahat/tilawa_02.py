import streamlit as st

def app():
    st.title("مدرب التلاوة")

    readers = {
        "عبد الباسط": "server10.mp3quran.net/abdulbasit/",
        "الحصري": "server8.mp3quran.net/husary/",
        "المنشاوي": "server7.mp3quran.net/minshawi/"
    }

    surahs = {
        "الفاتحة": "001",
        "البقرة": "002",
        "آل عمران": "003",
        "النساء": "004",
        # ... أكمل باقي السور
    }

    reader_choice = st.selectbox("اختر القارئ:", list(readers.keys()))
    surah_choice = st.selectbox("اختر السورة:", list(surahs.keys()))

    if reader_choice and surah_choice:
        base_url = readers[reader_choice]
        surah_num = surahs[surah_choice]
        audio_url = f"https://{base_url}{surah_num}.mp3"
        
        st.write(f"تلاوة سورة {surah_choice} بصوت {reader_choice}:")
        st.audio(audio_url, format="audio/mp3")

if __name__ == "__main__":
    app()
