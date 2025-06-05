import streamlit as st
import requests
import os

def app():
  st.title("📖 تفسير آية من القرآن")
  
 
  surah_list = [
      ("الفاتحة", 1),
      ("البقرة", 2),
      ("آل عمران", 3),
      ("النساء", 4),
      ("المائدة", 5),
  ]
  surah_name = st.selectbox("اختر السورة", [name for name, _ in surah_list])
  aya_number = st.number_input("اكتب رقم الآية", min_value=1, step=1)
  
  if st.button("عرض التفسير"):
      prompt = f"""
      فسر لي الآية رقم {aya_number} من سورة {surah_name} من القرآن الكريم، 
      بلغة عربية مبسطة وسهلة الفهم، مع الحفاظ على المعنى الصحيح والدقيق.
      """
  
      st.info("جارٍ الاتصال بـ LLM للحصول على التفسير...")

  
    HF_TOKEN = st.secrets["HF_TOKEN"]  
    API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }

    payload = {
        "inputs": prompt,
        "parameters": {"temperature": 0.7, "max_new_tokens": 300}
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        tafsir = result[0]["generated_text"].split(prompt)[-1].strip()
        st.success("📘 التفسير:")
        st.markdown(tafsir)
    else:
        st.error("حدث خطأ أثناء جلب التفسير.")
        st.text(response.text)
