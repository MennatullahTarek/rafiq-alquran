import streamlit as st
import requests
from crewai import Agent, LLM
from huggingface_hub import InferenceClient
import json
import pandas as pd

client = InferenceClient(token="YOUR_HUGGINGFACE_API_TOKEN")

# معجم السور من الكود اللي ادتهولك
surahs = {
    "الفاتحة": 1,
    "البقرة": 2,
    "آل عمران": 3,
    "النساء": 4,
    "المائدة": 5,
    "الأنعام": 6,
    "الأعراف": 7,
    "الأنفال": 8,
    "التوبة": 9,
    "يونس": 10,
    "هود": 11,
    "يوسف": 12,
    "الرعد": 13,
    "إبراهيم": 14,
    "الحجر": 15,
    "النحل": 16,
    "الإسراء": 17,
    "الكهف": 18,
    "مريم": 19,
    "طه": 20,
    "الأنبياء": 21,
    "الحج": 22,
    "المؤمنون": 23,
    "النور": 24,
    "الفرقان": 25,
    "الشعراء": 26,
    "النمل": 27,
    "القصص": 28,
    "العنكبوت": 29,
    "الروم": 30,
    "لقمان": 31,
    "السجدة": 32,
    "الأحزاب": 33,
    "سبأ": 34,
    "فاطر": 35,
    "يس": 36,
    "الصافات": 37,
    "ص": 38,
    "الزمر": 39,
    "غافر": 40,
    "فصلت": 41,
    "الشورى": 42,
    "الزخرف": 43,
    "الدخان": 44,
    "الجاثية": 45,
    "الأحقاف": 46,
    "محمد": 47,
    "الفتح": 48,
    "الحجرات": 49,
    "ق": 50,
    "الذاريات": 51,
    "الطور": 52,
    "النجم": 53,
    "القمر": 54,
    "الرحمن": 55,
    "الواقعة": 56,
    "الحديد": 57,
    "المجادلة": 58,
    "الحشر": 59,
    "الممتحنة": 60,
    "الصف": 61,
    "الجمعة": 62,
    "المنافقون": 63,
    "التغابن": 64,
    "الطلاق": 65,
    "التحريم": 66,
    "الملك": 67,
    "القلم": 68,
    "الحاقة": 69,
    "المعارج": 70,
    "نوح": 71,
    "الجن": 72,
    "المزّمّل": 73,
    "المدّثر": 74,
    "القيامة": 75,
    "الإنسان": 76,
    "المرسلات": 77,
    "النبأ": 78,
    "النازعات": 79,
    "عبس": 80,
    "التكوير": 81,
    "الإنفطار": 82,
    "المطفّفين": 83,
    "الإنشقاق": 84,
    "البروج": 85,
    "الطارق": 86,
    "الأعلى": 87,
    "الغاشية": 88,
    "الفجر": 89,
    "البلد": 90,
    "الشمس": 91,
    "الليل": 92,
    "الضحى": 93,
    "الشرح": 94,
    "التين": 95,
    "العلق": 96,
    "القدر": 97,
    "البينة": 98,
    "الزلزلة": 99,
    "العاديات": 100,
    "القارعة": 101,
    "التكاثر": 102,
    "العصر": 103,
    "الهمزة": 104,
    "الفيل": 105,
    "قريش": 106,
    "الماعون": 107,
    "الكوثر": 108,
    "الكافرون": 109,
    "النصر": 110,
    "المسد": 111,
    "الإخلاص": 112,
    "الفلق": 113,
    "الناس": 114
}

def get_ayah_text(surah_num, ayah_num):
    url = f"https://api.quran.com/api/v4/quran/verses/uthmani?verse_key={surah_num}:{ayah_num}"
    r = requests.get(url)
    if r.status_code == 200:
        try:
            return r.json()['verses'][0]['text_uthmani']
        except Exception:
            return None
    return None

def get_tafsir(surah_num, ayah_num, tafsir_id=91):
    url = f"https://api.quran.com/api/v4/tafsirs/{tafsir_id}/by_ayah/{surah_num}:{ayah_num}"
    r = requests.get(url)
    if r.status_code == 200:
        try:
            return r.json()['tafsir']['text']
        except Exception:
            return None
    return None

class MemorizationAgent(Agent):
    role: str = "memorization"
    goal: str = "Verify user's memorization"
    backstory: str = "Compares user's memorized text to the correct ayah text"

    def run(self, ayah_text, user_input):
        correct = ayah_text.strip() == user_input.strip()
        return {"memorization_correct": correct}

class InterpretationAgent(Agent):
    role: str = "interpretation"
    goal: str = "Check if user provided interpretation"
    backstory: str = "Checks if user wrote something as interpretation"

    def run(self, tafsir_text, user_input):
        correct = user_input.strip() != ""
        return {"interpretation_provided": correct}

class TajweedAgent(Agent):
    role: str = "tajweed"
    goal: str = "Verify tajweed rule correctness"
    backstory: str = "Compares user's tajweed input to the correct tajweed rule"

    def run(self, correct_rule, user_input):
        correct = user_input.strip() == correct_rule.strip()
        return {"tajweed_correct": correct}

class EvaluationLLM(LLM):
    role: str = "llm"
    goal: str = "Evaluate memorization, interpretation, and tajweed scores"
    backstory: str = "Uses a language model to score user's answers based on correctness"

    def run(self, memorization_res, interpretation_res, tajweed_res, ayah_text, user_mem, user_int, user_taj):
        prompt = f"""
الآية: "{ayah_text}"
حفظ المستخدم: "{user_mem}"
تفسير المستخدم: "{user_int}"
حكم التجويد: "{user_taj}"

قيم كل قسم من 0 إلى 1: الحفظ، التفسير، التجويد.
أعطني النتائج كـ JSON بهذا الشكل: {{"memorization_score": float, "interpretation_score": float, "tajweed_score": float}}
"""

        response = client.text_generation(
            model="gpt2",
            inputs=prompt,
            max_new_tokens=100,
        )

        try:
            result = json.loads(response.generated_text)
        except Exception:
            result = {
                "memorization_score": float(memorization_res.get("memorization_correct", False)),
                "interpretation_score": float(interpretation_res.get("interpretation_provided", False)),
                "tajweed_score": float(tajweed_res.get("tajweed_correct", False)),
            }
        return result

def app():
    st.title("Memory Game مع تفسير القرآن باستخدام API")

    surah_name = st.selectbox("اختر السورة", list(surahs.keys()))
    ayah_start = st.number_input("من الآية", min_value=1, value=1)
    ayah_end = st.number_input("إلى الآية", min_value=ayah_start, value=ayah_start)

    if st.button("ابدأ اللعبة"):
        surah_num = surahs[surah_name]

        results = []

        for ayah_num in range(ayah_start, ayah_end + 1):
            ayah_text = get_ayah_text(surah_num, ayah_num)
            tafsir_text = get_tafsir(surah_num, ayah_num)

            if not ayah_text:
                st.error(f"الآية {ayah_num} غير موجودة في السورة {surah_name}")
                continue

            st.markdown(f"### الآية رقم {ayah_num}")
            st.markdown(f"**نص الآية:** {ayah_text}")

            user_memorization = st.text_area(f"سرد الآية (حفظ)", key=f"mem_{ayah_num}")
            user_interpretation = st.text_area(f"التفسير / معنى الكلمات", key=f"int_{ayah_num}")
            user_tajweed = st.text_input(f"حكم التجويد", key=f"taj_{ayah_num}")

            memorization_agent = MemorizationAgent()
            interpretation_agent = InterpretationAgent()
            tajweed_agent = TajweedAgent()
            llm = EvaluationLLM()

            mem_res = memorization_agent.run(ayah_text, user_memorization)
            int_res = interpretation_agent.run(tafsir_text or "", user_interpretation)
            taj_res = tajweed_agent.run("إظهار", user_tajweed)  # ممكن تغير القاعدة حسب الآية

            llm_res = llm.run(mem_res, int_res, taj_res, ayah_text, user_memorization, user_interpretation, user_tajweed)

            st.write(f"نتيجة الحفظ: {llm_res.get('memorization_score', 0):.2f}")
            st.write(f"نتيجة التفسير: {llm_res.get('interpretation_score', 0):.2f}")
            st.write(f"نتيجة التجويد: {llm_res.get('tajweed_score', 0):.2f}")
            st.markdown("---")

            results.append({
                "ayah_number": ayah_num,
                "user_memorization": user_memorization,
                "memorization_score": llm_res.get("memorization_score", 0),
                "user_interpretation": user_interpretation,
                "interpretation_score": llm_res.get("interpretation_score", 0),
                "user_tajweed": user_tajweed,
                "tajweed_score": llm_res.get("tajweed_score", 0),
            })

        if results:
            if st.button("تحميل النتائج كملف CSV"):
                df = pd.DataFrame(results)
                csv_data = df.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="تحميل ملف النتائج (CSV)",
                    data=csv_data,
                    file_name=f"results_{surah_name}_{ayah_start}_to_{ayah_end}.csv",
                    mime='text/csv'
                )

if __name__ == "__main__":
    app()
