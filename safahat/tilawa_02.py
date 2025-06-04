import streamlit as st

readers = {
    "هزاع البلوشي": "hazza",
    "الحصري": "husary",
    "عبدالباسط": "abdulbasit"
}

surahs = {
    "الفاتحة": "1",
    "البقرة": "2",
    "آل عمران": "3",

}

def get_mp3_url(reader_slug, surah_num):
    import requests
    from bs4 import BeautifulSoup

    url = f"https://mp3quran.net/ar/{reader_slug}/{surah_num}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    audio_tag = soup.find("audio")
    if audio_tag:
        source = audio_tag.find("source")
        if source and source.get("src"):
            return source["src"]

    link = soup.find("a", {"class": "download"})
    if link and link.get("href"):
        return link["href"]

    return None

def app():
    st.title("مدرب التلاوة")

    reader_choice = st.selectbox("اختر القارئ:", list(readers.keys()))
    surah_choice = st.selectbox("اختر السورة:", list(surahs.keys()))

    if reader_choice and surah_choice:
        mp3_url = get_mp3_url(readers[reader_choice], surahs[surah_choice])
        if mp3_url:
            st.audio(mp3_url, format="audio/mp3")
        else:
            st.error("لم نتمكن من العثور على تلاوة الصوت لهذه السورة مع هذا القارئ.")

if __name__ == "__main__":
    app()
