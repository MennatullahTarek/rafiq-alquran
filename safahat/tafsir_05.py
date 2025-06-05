import streamlit as st
import requests

def get_tafsir_en(surah_num, ayah_num):
    url = f"https://api.alquran.cloud/v1/ayah/{surah_num}:{ayah_num}/editions/ar,en-tafsir-ibn-kathir"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        tafsir_en = None
        if "data" in data and len(data["data"]) > 0:
            for item in data["data"]:
                if item.get("edition", {}).get("identifier") == "en-tafsir-ibn-kathir":
                    tafsir_en = item.get("text", None)
                    break
            if tafsir_en:
                return tafsir_en
            else:
                return "لا يوجد تفسير متاح لهذه الآية."
        else:
            return "لا يوجد تفسير متاح."
    else:
        return None


def translate_to_arabic(text):
    HF_TOKEN = st.secrets["HF_TOKEN"]  # لازم تحطي التوكن في secrets
    API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-ar"

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": text,
        "parameters": {"max_new_tokens": 512}
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        # ترجمة النص مباشرة
        translated_text = result[0]["translation_text"]
        return translated_text
    else:
        st.error("حدث خطأ أثناء الترجمة.")
        st.text(response.text)
        return None

def app():
    st.title("📖 تفسير آية من القرآن وترجمتها للعربية")

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

    if st.button("عرض التفسير وترجمته"):
        st.info("جاري جلب التفسير الإنجليزي...")
        tafsir_en = get_tafsir_en(surah_number, aya_number)
        

        if tafsir_en is None:
            st.error("❌ لم يتم العثور على تفسير في هذه الصفحة أو حدث خطأ في الاتصال.")
            return
        
        st.success("✅ تم الحصول على التفسير الإنجليزي:")
        st.markdown(tafsir_en)

        st.info("جاري ترجمة التفسير إلى العربية...")
        tafsir_ar = translate_to_arabic(tafsir_en)

        if tafsir_ar:
            st.success("📘 التفسير مترجم للعربية:")
            st.markdown(tafsir_ar)
        else:
            st.warning("لم يتم الترجمة.")

if __name__ == "__main__":
    app()
