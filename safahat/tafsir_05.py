import streamlit as st
import requests

def get_tafsir(surah_num, ayah_num):
    tafsir_id = 91  # تفسير السعدي (ممكن تغييره لأي ID تاني من الجدول)
    url = f"https://api.quran.com/api/v4/verses/by_key/{surah_num}:{ayah_num}?language=ar&tafsirs={tafsir_id}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        
        # نشوف المحتوى بالكامل في حالة الخطأ
        st.json(data)  # دي هتطبع محتوى JSON بالكامل في Streamlit

        tafsir_text = None
        try:
            tafsir_text = data['verse']['tafsirs'][0]['text']
        except (KeyError, IndexError):
            tafsir_text = "لا يوجد تفسير متاح لهذه الآية."
        return tafsir_text
    else:
        st.error(f"فشل في الاتصال بالسيرفر. كود الحالة: {response.status_code}")
        return None

def app():
    st.title("📖 تفسير آية من القرآن الكريم")

    surah_number = st.number_input("رقم السورة", min_value=1, max_value=114, value=1)
    ayah_number = st.number_input("رقم الآية", min_value=1, value=1)

    if st.button("عرض التفسير"):
        st.info("جاري جلب التفسير...")
        tafsir = get_tafsir(surah_number, ayah_number)
        if tafsir:
            st.success("✅ التفسير:")
            st.write(tafsir)
        else:
            st.warning("⚠️ لم يتم العثور على التفسير.")

if __name__ == "__main__":
    app()
