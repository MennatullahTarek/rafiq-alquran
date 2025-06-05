import streamlit as st
import requests

def get_english_tafsir(surah_num, ayah_num):
    url = f"https://api.alquran.cloud/v1/ayah/{surah_num}:{ayah_num}/en.asad"
    # هنا بنستخدم تفسير محمد أسعد (en.asad) لأنه من التفاسير الإنجليزية الجيدة
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        tafsir_text = data.get("data", {}).get("edition", {}).get("englishName", "")
        tafsir_text = data.get("data", {}).get("text", "")
        if tafsir_text:
            return tafsir_text
        else:
            return None
    else:
        return None

def translate_to_arabic(text, surah_name, ayah_number):
    prompt = f"""
ترجم التفسير التالي للآية رقم {ayah_number} من سورة {surah_name} إلى اللغة العربية الفصحى بدقة ووضوح، بدون تكرار أو إعادة الصياغة، فقط ترجمة واحدة مفهومة:

"{text}"
"""
    HF_TOKEN = st.secrets["HF_TOKEN"]
    API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.3,
            "max_new_tokens": 200,
            "repetition_penalty": 1.5
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        translated_text = result[0]["generated_text"].split(prompt)[-1].strip()
        return translated_text
    else:
        st.error("❌ حدث خطأ أثناء الترجمة.")
        st.text(response.text)
        return None

def app():
    st.title("📖 تفسير آية من القرآن (الإنجليزي + ترجمة عربية)")

    surah_list = [
        ("الفاتحة", 1),
        ("البقرة", 2),
        ("آل عمران", 3),
        ("النساء", 4),
        ("المائدة", 5),
    ]

    surah_name = st.selectbox("اختر السورة", [name for name, _ in surah_list])
    surah_number = dict(surah_list)[surah_name]
    ayah_number = st.number_input("اكتب رقم الآية", min_value=1, step=1)

    if st.button("عرض التفسير"):
        st.info("جاري جلب التفسير الإنجليزي...")
        tafsir_en = get_english_tafsir(surah_number, ayah_number)

        if tafsir_en:
            st.success("✅ تم الحصول على التفسير الإنجليزي:")
            st.markdown(f"> {tafsir_en}")

            st.info("🔁 جاري الترجمة للعربية...")
            tafsir_ar = translate_to_arabic(tafsir_en, surah_name, ayah_number)
            if tafsir_ar:
                st.success("📘 التفسير المترجم بالعربية:")
                st.markdown(tafsir_ar)
            else:
                st.warning("لم يتم الترجمة بنجاح.")
        else:
            st.error("❌ لم يتم العثور على التفسير الإنجليزي لهذه الآية.")

if __name__ == "__main__":
    app()
