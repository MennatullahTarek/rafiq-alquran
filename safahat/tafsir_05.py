import streamlit as st
import requests

def get_tafsir_en(surah_num, ayah_num):
    """
    جلب التفسير بالإنجليزية من tafsir_api (spa5k)
    """
    url = f"https://tafsir-api.spakky.dev/api/v1/tafsir?surah={surah_num}&ayah={ayah_num}&tafsir=1"  # tafsir=1 يعني تفسير مبسط
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            tafsir = data.get('data', {}).get('text', None)
            if tafsir:
                return tafsir
            else:
                return "لا يوجد تفسير متاح لهذه الآية."
        else:
            return None
    except Exception as e:
        return None

def translate_google(text):
    """
    ترجمة باستخدام Google Translate API
    """
    try:
        translate_client = translate.Client()
        result = translate_client.translate(text, target_language="ar")
        return result['translatedText']
    except Exception as e:
        return None

def translate_huggingface(text):
    """
    ترجمة باستخدام HuggingFace API (موديل ترجمة)
    """
    HF_TOKEN = st.secrets["HF_TOKEN"]  # لازم تحط التوكن في secrets
    API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-ar"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": text, "parameters": {"max_new_tokens": 512}}

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result[0]["translation_text"]
    else:
        return None

def translate_text(text):
    if USE_GOOGLE_TRANSLATE:
        translated = translate_google(text)
        if translated:
            return translated
        else:
            st.warning("فشل ترجمة النص باستخدام Google Translate. سيتم تجربة HuggingFace.")
            return translate_huggingface(text)
    else:
        return translate_huggingface(text)

def app():
    st.title("📖 تفسير آية من القرآن وترجمتها للعربية")

    surah_list = [
        ("الفاتحة", 1),
        ("البقرة", 2),
        ("آل عمران", 3),
        ("النساء", 4),
        ("المائدة", 5),
        # ممكن تضيف المزيد حسب الحاجة
    ]

    surah_name = st.selectbox("اختر السورة", [name for name, _ in surah_list])
    surah_number = dict(surah_list)[surah_name]
    aya_number = st.number_input("اكتب رقم الآية", min_value=1, step=1)

    if st.button("عرض التفسير وترجمته"):
        st.info("جاري جلب التفسير الإنجليزي...")
        tafsir_en = get_tafsir_en(surah_number, aya_number)

        if tafsir_en is None:
            st.error("❌ لم يتم العثور على تفسير أو حدث خطأ في الاتصال.")
            return

        st.success("✅ تم الحصول على التفسير الإنجليزي:")
        st.markdown(tafsir_en)

        st.info("جاري ترجمة التفسير إلى العربية...")
        tafsir_ar = translate_text(tafsir_en)

        if tafsir_ar:
            st.success("📘 التفسير مترجم للعربية:")
            st.markdown(tafsir_ar)
        else:
            st.warning("لم يتم الترجمة.")

if __name__ == "__main__":
    app()
