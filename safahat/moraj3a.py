import streamlit as st
import requests
import difflib
import re
import csv
from io import StringIO
from huggingface_hub import InferenceClient

# Agent 4: LLM Helper 
class LLMHelper:
    def __init__(self, hf_token, model="HuggingFaceH4/zephyr-7b-beta"):
        self.client = InferenceClient(token=hf_token)
        self.model = model

    def ask(self, prompt):
        try:
            response = self.client.text_generation(
                model=self.model,
                inputs=prompt,
                max_new_tokens=100,
                temperature=0.7
            )
            # response هو dict، النص في response['generated_text']
            return response.get('generated_text', '').strip()
        except Exception as e:
            return f"خطأ في التوليد: {str(e)}"

# Agent 1: سور وآيات
def get_surahs():
    return {
        "الفاتحة": 1, "البقرة": 2, "آل عمران": 3, "النساء": 4, "المائدة": 5, "الأنعام": 6, "الأعراف": 7,
        # ممكن تكمل باقي السور لو حبيت
        "الناس": 114
    }

def get_ayah_text(surah_num, ayah_num):
    url = f"https://api.quran.com/api/v4/quran/verses/uthmani?verse_key={surah_num}:{ayah_num}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()['verses'][0]['text_uthmani']
        except (KeyError, IndexError):
            return "⚠️ لم يتم العثور على نص الآية."
    return "❌ فشل الاتصال بنص الآية."

# Agent 2: تفسير
def get_tafsir(surah_num, ayah_num, tafsir_id=91):
    url = f"https://api.quran.com/api/v4/tafsirs/{tafsir_id}/by_ayah/{surah_num}:{ayah_num}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()['tafsir']['text']
        except (KeyError, TypeError):
            return "⚠️ لم يتم العثور على التفسير."
    return "❌ فشل الاتصال بالتفسير."

# أدوات تقييم الحفظ

def strip_tashkeel(text):
    return re.sub(r'[\u064B-\u0652]', '', text)

def compare_ayah(user_input, actual_text):
    actual_clean = strip_tashkeel(actual_text.replace('\n', '').strip())
    user_clean = user_input.replace('\n', '').strip()
    ratio = difflib.SequenceMatcher(None, actual_clean, user_clean).ratio()
    return round(ratio * 100, 2)

# تقسيم الآية بحيث لا يتم قطع الكلمة (تقريباً عند أقرب فراغ)
def split_ayah_text(text, split_at=15):
    if len(text) <= split_at:
        return text, ""
    space_pos = text.rfind(" ", 0, split_at)
    if space_pos == -1:
        space_pos = split_at
    return text[:space_pos], text[space_pos:].strip()

# التطبيق الرئيسي

def app():
    st.title("📖 رفيق القرآن - مراجعة وحفظ وتفسير")

    hf_token = st.secrets["hf_token"]
    llm_helper = LLMHelper(hf_token)
    surahs = get_surahs()

    if 'started' not in st.session_state:
        st.session_state.started = False

    if not st.session_state.started:
        st.session_state.surah_name = st.selectbox("اختر السورة", list(surahs.keys()))
        st.session_state.start_ayah = st.number_input("من الآية رقم", min_value=1, value=1, key="start")
        st.session_state.end_ayah = st.number_input("إلى الآية رقم", min_value=st.session_state.start_ayah, value=st.session_state.start_ayah, key="end")

        if st.button("ابدأ الإختبار"):
            st.session_state.started = True
            st.session_state.current_ayah = st.session_state.start_ayah
            st.session_state.responses = []
            st.experimental_rerun()
    else:
        surah_num = surahs[st.session_state.surah_name]
        ayah_num = st.session_state.current_ayah

        actual_ayah = get_ayah_text(surah_num, ayah_num)
        tafsir = get_tafsir(surah_num, ayah_num)

        # تقسيم الآية بطريقة لا تقطع كلمة
        prefix, remainder = split_ayah_text(actual_ayah, split_at=15)
        st.markdown(f"### 🧠 اختبار الحفظ - أكمل بعد: **{prefix}...**")

        user_mem = st.text_area(f"أكمل الآية رقم {ayah_num}:", key=f"mem_{ayah_num}", height=100)

        score = "-"
        if user_mem:
            full_input = prefix + " " + user_mem
            score = compare_ayah(full_input, actual_ayah)
            st.markdown(f"✅ تقييم الحفظ: **{score}%**")

        st.markdown("### 📘 التفسير")
        user_tafsir = st.text_area(f"اشرح معنى الآية رقم {ayah_num} أو الكلمات:", key=f"tafsir_{ayah_num}", height=100)

        correction = ""
        if user_tafsir:
            prompt = f"قارن التفسير التالي بالتفسير الرسمي: '''{user_tafsir}'''. التفسير الرسمي: '''{tafsir}'''. قيمه من ١٠ مع تصحيح الأخطاء."
            correction = llm_helper.ask(prompt)
            st.markdown("🧾 تقييم التفسير:")
            st.write(correction)

        if st.button("التالي"):
            # حفظ الردود الحالية
            st.session_state.responses.append({
                "السورة": st.session_state.surah_name,
                "رقم الآية": ayah_num,
                "محاولة الحفظ": user_mem,
                "تقييم الحفظ": f"{score}%",
                "محاولة التفسير": user_tafsir,
                "تقييم التفسير": correction
            })
            # تحديث رقم الآية التالي
            if ayah_num < st.session_state.end_ayah:
                st.session_state.current_ayah += 1
            else:
                st.session_state.started = False  # انتهاء الاختبار
            st.experimental_rerun()

      
        if not st.session_state.started and st.session_state.responses:
            csv_buffer = StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow(["السورة", "رقم الآية", "محاولة الحفظ", "تقييم الحفظ", "محاولة التفسير", "تقييم التفسير"])
            for res in st.session_state.responses:
                writer.writerow([
                    res["السورة"],
                    res["رقم الآية"],
                    res["محاولة الحفظ"],
                    res["تقييم الحفظ"],
                    res["محاولة التفسير"],
                    res["تقييم التفسير"]
                ])

            st.download_button(
                label="💾 تحميل النتيجة",
                data=csv_buffer.getvalue(),
                file_name="quran_review_results.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    app()
