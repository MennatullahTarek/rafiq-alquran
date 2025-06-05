import streamlit as st
import requests

def get_english_tafsir(surah_num, ayah_num):
    tafsir_id = 169  # Tafsir Ibn Kathir (abridged) in English
    ayah_key = f"{surah_num}:{ayah_num}"
    url = f"https://api.quran.com/v4/tafsirs/{tafsir_id}/by_ayah/{ayah_key}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        try:
            return data['tafsir']['text']
        except (KeyError, TypeError):
            return "⚠️ No tafsir found for this verse."
    else:
        return None

def translate_to_arabic(text):
    # ترجمة تجريبية باستخدام LLM (مش ترجمة احترافية أو Google Translate)
    # تقدر تدمج Google Translate API هنا لو عندك API Key
    try:
        from deep_translator import GoogleTranslator
        return GoogleTranslator(source='en', target='ar').translate(text)
    except:
        return "⚠️ فشل في الترجمة. تأكد من وجود مكتبة deep_translator."

def app():
    st.title("📘 تفسير آية بالإنجليزي وترجمتها للعربية")

    surah_number = st.number_input("رقم السورة", min_value=1, max_value=114, value=1)
    ayah_number = st.number_input("رقم الآية", min_value=1, value=1)

    if st.button("عرض التفسير"):
        st.info("🔄 جاري جلب التفسير...")
        eng_tafsir = get_english_tafsir(surah_number, ayah_number)
        if eng_tafsir:
            st.subheader("📖 Tafsir (English):")
            st.write(eng_tafsir)

            st.subheader("🔁 الترجمة للعربية:")
            translated = translate_to_arabic(eng_tafsir)
            st.write(translated)
        else:
            st.error("❌ لم يتم العثور على التفسير أو حدث خطأ في الاتصال.")

if __name__ == "__main__":
    app()
