import streamlit as st
import requests

def app():
  st.title("🕋 تفسير الآيات")
  
  surah_number = st.number_input("رقم السورة", min_value=1, max_value=114, value=1)
  ayah_number = st.number_input("رقم الآية", min_value=1, value=1)
  language = st.selectbox("اختر اللغة", ["ar", "en"])
  
  if st.button("عرض التفسير"):
      try:
          response = requests.get(
              f"https://api.alquran.cloud/v1/ayah/{surah_number}:{ayah_number}/editions/quran-uthmani,en.asad"
          )
  
          if response.status_code == 200:
              data = response.json()
              ayah_ar = data["data"][0]["text"]
              ayah_en = data["data"][1]["text"]
  
              st.markdown("### الآية:")
              st.write(ayah_ar if language == "ar" else ayah_en)
  
              st.markdown("### التفسير :")
              st.write(ayah_en)
  
          else:
              st.error("حدث خطأ أثناء تحميل البيانات. حاول مرة أخرى.")
  
      except Exception as e:
          st.error(f"حدث خطأ: {e}")

if __name__ == "__main__":
    app()
