import streamlit as st
import requests

def get_tafsir(surah_num, ayah_num):
    tafsir_id = 91  # تفسير السعدي - ممكن تغييره لو عايزة تفسير تاني
    ayah_key = f"{surah_num}:{ayah_num}"
    url = f"https://api.quran.com/v4/tafsirs/{tafsir_id}/by_ayah/{ayah_key}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        try:
            return data['tafsir']['text']
        except (KeyError, TypeError):
            return "⚠️ لم يتم العثور على تفسير لهذه الآية."
    else:
        return f"❌ خطأ في الاتصال: {response.status_code}"

def app():
    st.title("📘 تفسير آية من القرآن الكريم")

    surah_number = st.number_input("رقم السورة", min_value=1, max_value=114, value=1)
    ayah_number = st.number_input("رقم الآية", min_value=1, value=1)

    if st.button("عرض التفسير"):
        st.info("🔄 جاري جلب التفسير...")
        tafsir = get_tafsir(surah_number, ayah_number)
        st.write(tafsir)

if __name__ == "__main__":
    app()
