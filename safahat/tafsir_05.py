import streamlit as st
import requests
from bs4 import BeautifulSoup

def get_tafsir_from_surahquran(page_num):
    url = f"https://surahquran.com/tafsir-mokhtasar/{page_num}.htm"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            tafsir_blocks = soup.find_all("div", class_="tafser")
            if not tafsir_blocks:
                return None
            tafsir_texts = [block.text.strip() for block in tafsir_blocks]
            return "\n\n".join(tafsir_texts)
        else:
            return None
    except Exception as e:
        return None

def summarize_tafsir_with_llm(text, page_num):
    prompt = f"""
    لخص التفسير التالي (من الصفحة {page_num} من المصحف) بلغة عربية مبسطة وسهلة الفهم، مع الحفاظ على المعنى الأصلي:

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
        st.error("❌ حدث خطأ أثناء تلخيص التفسير.")
        return None

def app():
    st.title("📖 تفسير المصحف الشريف")
    st.markdown("اختر رقم الصفحة (من 1 إلى 604) لعرض التفسير من موقع [surahquran.com](https://surahquran.com/tafsir-mokhtasar/)")

    page_num = st.number_input("📄 رقم الصفحة", min_value=1, max_value=604, step=1)

    if st.button("عرض التفسير"):
        st.info("⏳ جاري جلب التفسير من الموقع...")
        tafsir_text = get_tafsir_from_surahquran(page_num)

        if tafsir_text:
            st.success("✅ تم جلب التفسير بنجاح")
            st.markdown(tafsir_text)

            if st.checkbox("تلخيص التفسير بلغة مبسطة؟"):
                st.info("🔁 جاري تلخيص التفسير...")
                simplified = summarize_tafsir_with_llm(tafsir_text, page_num)
                if simplified:
                    st.success("📘 التفسير المبسط:")
                    st.markdown(simplified)
                else:
                    st.warning("⚠️ لم يتم تلخيص التفسير.")
        else:
            st.error("❌ لم يتم العثور على تفسير في هذه الصفحة أو حدث خطأ في الاتصال.")

if __name__ == "__main__":
    app()
