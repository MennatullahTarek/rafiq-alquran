import streamlit as st
import requests

def get_english_tafsir(surah, ayah):
    url = f"http://api.alquran.cloud/v1/ayah/{surah}:{ayah}/en.asad"  # ممكن تغيير 'en.asad' حسب النسخة
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        return data['data']['text']
    else:
        return None

def translate_to_arabic(text, surah_name, ayah_number):
    prompt = f"""
    ترجم التفسير التالي للآية {ayah_number} من سورة {surah_name} إلى اللغة العربية الفصحى، مع الحفاظ على المعنى الدقيق:

    "{text}"
    """
    HF_TOKEN = st.secrets["HF_TOKEN"]
    API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": prompt,
        "parameters": {"temperature": 0.5, "max_new_tokens": 300}
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        output = response.json()
        return output[0]["generated_text"].split(prompt)[-1].strip()
    else:
        return "حدث خطأ أثناء الترجمة."

def app():
    st.title("📖 ترجمة تفسير الآيات من الإنجليزية إلى العربية")

    surah = st.number_input("رقم السورة", min_value=1, max_value=114, value=1)
    ayah = st.number_input("رقم الآية", min_value=1, step=1, value=1)
    surah_name = st.text_input("اسم السورة (اختياري للعرض)", value="")

    if st.button("عرض التفسير"):
        tafsir_en = get_english_tafsir(surah, ayah)
        if tafsir_en:
            st.markdown("### ✨ التفسير الإنجليزي:")
            st.markdown(tafsir_en)

            st.markdown("### 🌐 الترجمة إلى العربية:")
            tafsir_ar = translate_to_arabic(tafsir_en, surah_name or f"سورة {surah}", ayah)
            st.markdown(tafsir_ar)
        else:
            st.error("❌ لم يتم العثور على التفسير الإنجليزي.")

if __name__ == "__main__":
    app()
