import streamlit as st
import requests

def app():
  
  
  st.title("📖 صفحة التفسير - تفسير الآيات  ")
  
  
  surah = st.number_input("ادخل رقم السورة", min_value=1, max_value=114, value=1)
  ayah = st.number_input("ادخل رقم الآية", min_value=1, value=1)
  tafseer_type = st.selectbox("اختر التفسير", ["التفسير الميسر", "تفسير السعدي", "تفسير الطبري"])
  
  
  tafseer_dict = {
      "التفسير الميسر": "ar.muyassar",
      "تفسير السعدي": "ar.saadi",
      "تفسير الطبري": "ar.tabari"
  }
  selected_code = tafseer_dict[tafseer_type]
  
  if st.button("عرض التفسير"):
      url = f"https://api.quranenc.com/v1/translation/aya/?language=arabic&surah={surah}&ayah={ayah}&translator={selected_code}"
  
      response = requests.get(url)
  
      if response.status_code == 200:
          data = response.json()
          st.markdown(f"### الآية {ayah} من سورة {surah}")
          st.markdown(f"#### الآية:")
          st.write(data["result"]["arabic_text"])
  
          st.markdown(f"#### التفسير ({tafseer_type}):")
          st.write(data["result"]["translation"])
      else:
          st.error("حدث خطأ أثناء جلب التفسير. تأكد من إدخالك الصحيح.")


if __name__ == "__main__":
    app()
