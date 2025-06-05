import streamlit as st
import requests
from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup

# دالة لجلب التفسير من Quran.com API
def get_tafsir_quran_api(surah, ayah, tafsir_id=169):  # Tafsir Ibn Kathir English (abridged)
    url = f"https://api.quran.com/api/v4/tafsirs/{tafsir_id}/by_ayah/{surah}:{ayah}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()['tafsir']['text']
        except (KeyError, TypeError):
            return "⚠️ لم يتم العثور على التفسير."
    else:
        return "❌ فشل في الاتصال بالـ API."



def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text(separator="\n")

def translate_to_arabic(text):
    try:
        clean_text = clean_html(text)
        return GoogleTranslator(source='en', target='ar').translate(clean_text)
    except:
        return "⚠️ فشل في الترجمة."


# واجهة المستخدم
def app():
    st.title("📖 تفسير آية من القرآن الكريم")
    
    surah = st.number_input("🔢 رقم السورة", min_value=1, max_value=114, value=1)
    ayah = st.number_input("🔢 رقم الآية", min_value=1, value=1)
    
    if st.button("📚 عرض التفسير"):
        st.info("⏳ جاري جلب التفسير من API...")
        tafsir_en = get_tafsir_quran_api(surah, ayah)
        st.subheader("📘 التفسير (بالإنجليزية):")
        st.write(tafsir_en)
        
        st.subheader("📗 الترجمة للعربية:")
        tafsir_ar = translate_to_arabic(tafsir_en)
        st.write(tafsir_ar)

if __name__ == "__main__":
    app()
