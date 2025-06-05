import streamlit as st
import requests

def get_tafsirs_list():
    url = "https://api.quran.com/api/v4/tafsirs"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("tafsirs", [])
    return []

def get_tafsir(chapter, verse, tafsir_id):
    url = f"https://api.quran.com/api/v4/verses/by_key/{chapter}:{verse}"
    params = {
        "tafsirs": tafsir_id,
        "language": "ar",
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        verse_data = data.get("verse", {})
        tafsirs = verse_data.get("tafsirs", [])
        if tafsirs:
            return tafsirs[0].get("text", "لا يوجد تفسير متاح لهذه الآية.")
        else:
            return "لا يوجد تفسير متاح لهذه الآية."
    else:
        return None

def app():
    st.title("📖 تفسير الميسر للقرآن الكريم")

    # جلب التفسيرات المتاحة
    tafsirs = get_tafsirs_list()
    tafsir_map = {t['name']: t['id'] for t in tafsirs}

    tafsir_name = st.selectbox("اختر التفسير", list(tafsir_map.keys()))
    tafsir_id = tafsir_map[tafsir_name]

    surah_list = [
        ("الفاتحة", 1),
        ("البقرة", 2),
        ("آل عمران", 3),
        ("النساء", 4),
        ("المائدة", 5),
    ]

    surah_name = st.selectbox("اختر السورة", [name for name, _ in surah_list])
    surah_number = dict(surah_list)[surah_name]
    aya_number = st.number_input("اكتب رقم الآية", min_value=1, step=1)

    if st.button("عرض التفسير"):
        st.info("جاري جلب التفسير...")
        tafsir_text = get_tafsir(surah_number, aya_number, tafsir_id)
        if tafsir_text:
            st.markdown(f"### تفسير الآية {aya_number} من سورة {surah_name}")
            st.write(tafsir_text)
        else:
            st.error("❌ لم يتم العثور على تفسير لهذه الآية.")

if __name__ == "__main__":
    app()
