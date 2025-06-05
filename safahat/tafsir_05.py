import streamlit as st
import requests


def get_tafsir_quran_api(surah, ayah, tafsir_id=91):  
    url = f"https://api.quran.com/api/v4/tafsirs/{tafsir_id}/by_ayah/{surah}:{ayah}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()['tafsir']['text']
        except (KeyError, TypeError):
            return "⚠️ لم يتم العثور على التفسير."
    else:
        return "❌ فشل في الاتصال بالـ API."


def app():
    st.title("📖 تفسير آية من القرآن الكريم")
    
    surah = st.number_input("🔢 رقم السورة", min_value=1, max_value=114, value=1)
    ayah = st.number_input("🔢 رقم الآية", min_value=1, value=1)
    
    if st.button("📚 عرض التفسير"):
        st.info("⏳ جاري جلب التفسير من API...")
        tafsir = get_tafsir_quran_api(surah, ayah)
        
        st.subheader("📗  التفسير:")
        st.markdown(tafsir, unsafe_allow_html=True)

if __name__ == "__main__":
    app()
