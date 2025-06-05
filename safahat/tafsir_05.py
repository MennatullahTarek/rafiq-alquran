import streamlit as st
from tafsir_api import TafsirAPI  # لازم تكون منصب المكتبة دي
import requests

# دالة ترجمة بسيطة باستخدام HuggingFace API كمثال
def translate_to_arabic(text):
    HF_TOKEN = st.secrets["HF_TOKEN"]
    API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-ar"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": text, "parameters": {"max_new_tokens": 512}}

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result[0]["translation_text"]
    else:
        st.error("حدث خطأ أثناء الترجمة.")
        return None

def app():
    st.title("📖 تفسير وترجمة آيات القرآن")

    tafsir = TafsirAPI()

    surah_number = st.number_input("ادخل رقم السورة", min_value=1, max_value=114, step=1)
    aya_number = st.number_input("ادخل رقم الآية", min_value=1, step=1)

    if st.button("جلب التفسير وترجمته"):
        st.info("جاري جلب التفسير بالإنجليزية...")
        try:
            tafsir_en = tafsir.get_tafsir(surah_number, aya_number, lang="en")
        except Exception as e:
            st.error(f"حدث خطأ في جلب التفسير: {e}")
            return

        if tafsir_en:
            st.markdown(f"### التفسير بالإنجليزية:\n{tafsir_en}")
            st.info("جاري ترجمة التفسير إلى العربية...")
            tafsir_ar = translate_to_arabic(tafsir_en)
            if tafsir_ar:
                st.markdown(f"### التفسير مترجم للعربية:\n{tafsir_ar}")
            else:
                st.warning("لم يتم الحصول على الترجمة.")
        else:
            st.error("لم يتم العثور على تفسير لهذه الآية.")

if __name__ == "__main__":
    app()
