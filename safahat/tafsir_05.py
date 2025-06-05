import streamlit as st
import requests

def get_tafsir(surah_num, ayah_num):
    url = f"https://api.quran.com/api/v4/verses/by_key/{surah_num}:{ayah_num}?language=ar&words=false&translations=131&tafsirs=16"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        tafsir_text = None
        try:
            tafsir_text = data['verse']['tafsirs'][0]['text']
        except (KeyError, IndexError):
            tafsir_text = "لا يوجد تفسير متاح لهذه الآية."
        return tafsir_text
    else:
        return None

def app():
    st.title("تفسير الآية من القرآن (تفسير الميسر)")

    surah_number = st.number_input("رقم السورة", min_value=1, max_value=114, value=1)
    ayah_number = st.number_input("رقم الآية", min_value=1, value=1)

    if st.button("احصل على التفسير"):
        st.info("جاري جلب التفسير...")
        tafsir = get_tafsir(surah_number, ayah_number)
        if tafsir:
            st.success("📘 تفسير الميسر:")
            st.write(tafsir)
        else:
            st.error("حدث خطأ أو لم يتوفر تفسير.")

if __name__ == "__main__":
    app()
