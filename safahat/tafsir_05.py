import streamlit as st
import requests

def get_tafsir(surah_number, aya_number):
    """جلب التفسير من Quran.com API (تفسير السعدي)"""
    url = f"https://api.quran.com:443/v4/verses/{aya_number}/tafsirs"
    params = {"language": "ar", "tafsir_id": 169"}  # 169 = تفسير السعدي
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data["tafsirs"]:
            return data["tafsirs"][0]["text"]
    return None

def summarize_tafsir_with_llm(text, surah_name, aya_number):
    """تلخيص التفسير بلغة مبسطة باستخدام LLM"""
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

    if st.button("عرض التفسير"):
        st.info("جاري التفسير من مصدر موثوق...")
        tafsir_text = get_tafsir(surah_number, aya_number)

        if tafsir_text:
            st.success("✅ تم  التفسير المعتمد.")
            st.info("🔁 جاري تلخيص التفسير بلغة مبسطة...")
            simplified = summarize_tafsir_with_llm(tafsir_text, surah_name, aya_number)

            if simplified:
                st.success("📘 التفسير المبسط:")
                st.markdown(simplified)
        else:
            st.error("لم يتم العثور على تفسير للآية المحددة.")

if __name__ == "__main__":
    app()
