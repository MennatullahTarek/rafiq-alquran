import streamlit as st
import requests

def get_tafsir_en(surah_num, ayah_num):
    url = f"https://api.alquran.cloud/v1/ayah/{surah_num}:{ayah_num}/en.tafsir"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        tafsir_en = data['data']['tafsir']
        if tafsir_en:
            return tafsir_en
        else:
            return "لا يوجد تفسير متاح لهذه الآية."
    else:
        return None

def translate_to_arabic(text, surah_name, aya_number):
    prompt = f"""
    ترجم التفسير الإنجليزي التالي للآية رقم {aya_number} من سورة {surah_name} إلى اللغة العربية الفصحى بشكل دقيق وواضح، بدون أي شرح إضافي أو تلخيص، فقط الترجمة الحرفية للنص التالي:

    "{text}"
    """

    HF_TOKEN = st.secrets["HF_TOKEN"]
    API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": prompt,
        "parameters": {"temperature": 0.3, "max_new_tokens": 400}
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        # إرجاع الترجمة فقط بدون النص الأصلي
        generated_text = result[0]["generated_text"]
        translated_text = generated_text.split(prompt)[-1].strip()
        return translated_text
    else:
        st.error("حدث خطأ أثناء الترجمة.")
        st.text(response.text)
        return None

def app():
    st.title("📖 تفسير  القرآن ")

    surah_list = [
        ("الفاتحة", 1),
        ("البقرة", 2),
        ("آل عمران", 3),
        ("النساء", 4),
        ("المائدة", 5),
    ]

    surah_name = st.selectbox("اختر السورة", [name for name, _ in surah_list])
    surah_number = dict(surah_list)[surah_name]
    aya_number = st.number_input("اكتب رقم الآية", min_value=1, step=1)

    if st.button("عرض التفسير "):
        st.info("جاري  التفسير من مصدر معتمد ...")
        tafsir_en = get_tafsir_en(surah_number, aya_number)

        if tafsir_en is None:
            st.error("❌ لم يتم العثور على تفسير في هذه الصفحة أو حدث خطأ في الاتصال.")
            return


        st.info("جاري التلخيص  ...")
        tafsir_ar = translate_to_arabic(tafsir_en, surah_name, aya_number)

        if tafsir_ar:
            st.success("📘 التفسير الميسر :")
            st.markdown(tafsir_ar)
        else:
            st.warning("لم يتم التلخيص.")

if __name__ == "__main__":
    app()
