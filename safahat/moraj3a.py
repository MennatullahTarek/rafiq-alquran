import streamlit as st
import requests
import difflib
import re
import csv
from io import StringIO
from huggingface_hub import InferenceClient

# ==== LLM Helper ====
class LLMHelper:
    def __init__(self, hf_token, model="tiiuae/falcon-7b-instruct"):
        self.client = InferenceClient(token=hf_token)
        self.model = model

    def ask(self, prompt):
        response = self.client.text_generation(
            model=self.model,
            prompt=prompt,
            max_new_tokens=200,
            temperature=0.7
        )
        return response

# ==== Quran & Tafsir API ====
def get_surahs():
    return {"الفاتحة": 1, "البقرة": 2, "آل عمران": 3}  # اختصار

def get_ayah_text(surah, ayah):
    url = f"https://api.quran.com/api/v4/quran/verses/uthmani?verse_key={surah}:{ayah}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['verses'][0]['text_uthmani']
    return "⚠️ لم يتم العثور على نص الآية."

def get_tafsir(surah, ayah, tafsir_id=91):
    url = f"https://api.quran.com/api/v4/tafsirs/{tafsir_id}/by_ayah/{surah}:{ayah}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['tafsir']['text']
    return "⚠️ لم يتم العثور على التفسير."

def strip_tashkeel(text):
    return re.sub(r'[\u064B-\u0652]', '', text)

def compare_ayah(user_input, actual_text):
    actual_clean = strip_tashkeel(actual_text.replace('\n', '').strip())
    user_clean = user_input.replace('\n', '').strip()
    ratio = difflib.SequenceMatcher(None, actual_clean, user_clean).ratio()
    return round(ratio * 100, 2)

# ==== Agents ====
class Agent1_InputHandler:
    def __init__(self, surah_name, start_ayah, end_ayah, surahs):
        self.surah_name = surah_name
        self.start_ayah = start_ayah
        self.end_ayah = end_ayah
        self.surahs = surahs

class Agent2_Memorization:
    def test(self, user_input, actual_ayah):
        return compare_ayah(user_input, actual_ayah)

class Agent3_Tafsir:
    def __init__(self, llm_helper):
        self.llm_helper = llm_helper

    def evaluate(self, user_tafsir, official_tafsir):
        prompt = f"قارن التفسير التالي بالتفسير الرسمي: '{user_tafsir}'. التفسير الرسمي: '{official_tafsir}'. قيمه من ١٠ مع توضيح الخطأ."
        return self.llm_helper.ask(prompt)

# ==== Main App ====
def app():
    st.title("📖 رفيق القرآن - مراجعة وحفظ وتفسير")

    hf_token = st.secrets["hf_token"]
    llm_helper = LLMHelper(hf_token)
    memorization_agent = Agent2_Memorization()
    tafsir_agent = Agent3_Tafsir(llm_helper)

    surahs = get_surahs()
    surah_name = st.selectbox("اختر السورة", list(surahs.keys()))
    start_ayah = st.number_input("من الآية رقم", min_value=1, value=1)
    end_ayah = st.number_input("إلى الآية رقم", min_value=start_ayah, value=start_ayah)

    if st.button("ابدأ الإختبار"):
        agent1 = Agent1_InputHandler(surah_name, start_ayah, end_ayah, surahs)
        responses = []

        for ayah_num in range(agent1.start_ayah, agent1.end_ayah + 1):
            st.subheader(f"الآية {ayah_num}")

            actual_ayah = get_ayah_text(agent1.surahs[agent1.surah_name], ayah_num)
            tafsir = get_tafsir(agent1.surahs[agent1.surah_name], ayah_num)

            st.markdown("### 🧠 اختبار الحفظ")
            user_mem = st.text_area(f"أكمل الآية ({ayah_num})")
            score = ""
            if user_mem:
                score = memorization_agent.test(user_mem, actual_ayah)
                st.markdown(f"✅ تقييم الحفظ: **{score}%**")

            st.markdown("### 📘 تفسير الآية")
            user_tafsir = st.text_area(f"اشرح معنى الآية ({ayah_num})")
            correction = ""
            if user_tafsir:
                correction = tafsir_agent.evaluate(user_tafsir, tafsir)
                st.markdown(f"🧾 تقييم التفسير:
{correction}")

            responses.append([
                agent1.surah_name,
                ayah_num,
                user_mem,
                f"{score}%",
                user_tafsir,
                correction
            ])

        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(["السورة", "رقم الآية", "محاولة الحفظ", "تقييم الحفظ", "محاولة التفسير", "تقييم التفسير"])
        writer.writerows(responses)

        st.download_button(
            label="💾 تحميل النتيجة",
            data=csv_buffer.getvalue(),
            file_name="quran_review_results.csv",
            mime="text/csv"
        )
