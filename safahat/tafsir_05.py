import streamlit as st
import requests

def get_tafsir(edition_slug, surah_num, ayah_num):
    url = f"https://cdn.jsdelivr.net/gh/spa5k/tafsir_api@main/tafsir/{edition_slug}/{surah_num}/{ayah_num}.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        tafsir_text = data.get("text")
        if tafsir_text:
            return tafsir_text
        else:
            return "لا يوجد تفسير متاح لهذه الآية."
    else:
        return None  # نرجع None لو في مشكلة في جلب التفسير

def summarize_tafsir_with_llm(text, surah_name, aya_number):
    prompt = f"""
    لخص التفسير التالي للآية رقم {aya_number} من سورة {surah_name} بلغة عربية مبسطة وسهلة الفهم، دون تحريف أو تغيير في المعنى:

    "{text}"
    """
    HF_TOKEN = st.secrets["HF_TOKEN"]
    API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": prompt,
        "parameters": {"temperature": 0.7, "max_new_tokens": 300}
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        return result[0]["generated_text"].split(prompt)[-1].strip()
    else:
        st.error("حدث خطأ أثناء تلخيص التفسير.")
        st.text(response.text)
        return None

def app():
    st.title("📖 تفسير آية من القرآن (بتلخيص مبسط)")

    tafsir_options = {
        "تفسير ابن كثير": "ar-tafseeribnkatheer",
        "تفسير السعدي": "ar-tafseersadi",
        "تفسير الطبري": "ar-tafseertalberi",
        "تفسير الجلالين": "ar-aljalalayn",
    }

    surah_list = [
        ("الفاتحة", 1),
        ("البقرة", 2),
        ("آل عمران", 3),
        ("النساء", 4),
        ("المائدة", 5),
    ]

    tafsir_name = st.selectbox("اختر التفسير", list(tafsir_options.keys()))
    edition_slug = tafsir_options[tafsir_name]
    surah_name = st.selectbox("اختر السورة", [name for name, _ in surah_list])
    surah_number = dict(surah_list)[surah_name]
    aya_number = st.number_input("اكتب رقم الآية", min_value=1, step=1)

    if st.button("عرض التفسير"):
        st.info("جاري جلب التفسير من مصدر موثوق...")
        tafsir_text = get_tafsir(edition_slug, surah_number, aya_number)

        if tafsir_text is None:
            st.error("حدث خطأ في جلب التفسير. ربما الآية أو التفسير غير متوفر.")
            return

        st.success("✅ تم الحصول على التفسير.")
        st.markdown(tafsir_text)

        if st.checkbox("تلخيص التفسير بلغة مبسطة؟"):
            st.info("🔁 جاري تلخيص التفسير بلغة مبسطة...")
            simplified = summarize_tafsir_with_llm(tafsir_text, surah_name, aya_number)

            if simplified:
                st.success("📘 التفسير المبسط:")
                st.markdown(simplified)
            else:
                st.warning("لم يتم تلخيص التفسير.")

if __name__ == "__main__":
    app()
