import streamlit as st
import requests

# القايمة دي من اللي انت عرضتهم، ID واسم التفسير، واللغة
tafsir_options = {
    "Tafseer Al Saddi (ar)": "ar-tafseer-al-saddi",
    "Tafsir Ibn Kathir (ar)": "ar-tafsir-ibn-kathir",
    "Tafseer Al-Baghawi (ar)": "ar-tafseer-al-baghawi",
    "Tafseer Tanwir al-Miqbas (ar)": "ar-tafseer-tanwir-al-miqbas",
    "Tafsir Al Wasit (ar)": "ar-tafseer-al-wasit",
    "Tafsir al-Tabari (ar)": "ar-tafseer-al-tabari",
    "Tafsir Muyassar (ar)": "ar-tafsir-muyassar",
    "Tafsir Ibn Kathir (en)": "en-tafisr-ibn-kathir",
    "Tazkirul Quran (en)": "en-tazkirul-quran",
    "Kashf Al-Asrar Tafsir (en)": "en-kashf-al-asrar-tafsir",
    "Al Qushairi Tafsir (en)": "en-al-qushairi-tafsir",
    "Al-Jalalayn (en)": "en-al-jalalayn",
    "Maarif-ul-Quran (en)": "en-tafsir-maarif-ul-quran",
}

def get_tafsir(surah_num, ayah_num, tafsir_id):
    url = f"https://api.quran.com/api/v4/verses/{surah_num}:{ayah_num}/tafsirs/{tafsir_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        tafsir_text = data.get("tafsir", {}).get("text", None)
        if tafsir_text:
            return tafsir_text
        else:
            return "لا يوجد تفسير متاح لهذه الآية."
    else:
        return None

def translate_to_arabic(text):
    HF_TOKEN = st.secrets["HF_TOKEN"]
    API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-ar"

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": text}

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result[0]["translation_text"]
    else:
        st.error("حدث خطأ أثناء الترجمة.")
        st.text(response.text)
        return None

def app():
    st.title("📖 تفسير آيات القرآن الكريم")

    surah_list = [
        ("الفاتحة", 1),
        ("البقرة", 2),
        ("آل عمران", 3),
        ("النساء", 4),
        ("المائدة", 5),
        # ممكن تزود سور أكثر لو حبيت
    ]

    surah_name = st.selectbox("اختر السورة", [name for name, _ in surah_list])
    surah_number = dict(surah_list)[surah_name]
    aya_number = st.number_input("اكتب رقم الآية", min_value=1, step=1)

    tafsir_name = st.selectbox("اختر التفسير", list(tafsir_options.keys()))
    tafsir_id = tafsir_options[tafsir_name]

    if st.button("عرض التفسير"):
        st.info("جاري جلب التفسير من المصدر...")
        tafsir_text = get_tafsir(surah_number, aya_number, tafsir_id)

        if tafsir_text is None:
            st.error("❌ لم يتم العثور على تفسير أو حدث خطأ في الاتصال.")
            return

        # عرض التفسير الأصلي
        st.success(f"📘 التفسير ({tafsir_name}):")
        st.markdown(tafsir_text)

        # لو التفسير إنجليزي، نترجمه للعربي
        if tafsir_id.startswith("en-"):
            st.info("جاري ترجمة التفسير إلى العربية...")
            tafsir_ar = translate_to_arabic(tafsir_text)
            if tafsir_ar:
                st.success("📙 التفسير مترجم للعربية:")
                st.markdown(tafsir_ar)
            else:
                st.warning("لم يتم الترجمة.")

if __name__ == "__main__":
    app()
