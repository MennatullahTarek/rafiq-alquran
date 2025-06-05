import pysqlite3
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import pandas as pd
from crewai import Agent, LLM
from huggingface_hub import InferenceClient
import json
import requests

# بيانات السور مع أرقامها
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
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()['verses'][0]['text_uthmani']
        except (KeyError, IndexError):
            return None
    else:
        return None

def get_tafsir_quran_api(surah_num, ayah_num, tafsir_id=91):
    url = f"https://api.quran.com/api/v4/tafsirs/{tafsir_id}/by_ayah/{surah_num}:{ayah_num}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()['tafsir']['text']
        except (KeyError, TypeError):
            return None
    else:
        return None

# Agents مع الحقول المطلوبة
class MemorizationAgent(Agent):
    role: str = "Evaluator"
    goal: str = "تحقق من حفظ المستخدم للآيات بشكل صحيح"
    backstory: str = "وكيل مسؤول عن تقييم حفظ المستخدم للآيات."

    def run(self, correct_text, user_text):
        return {"memorization_correct": user_text.strip() == correct_text.strip()}

class InterpretationAgent(Agent):
    role: str = "Evaluator"
    goal: str = "تحقق من تفسير المستخدم ومعرفته بمعاني الكلمات"
    backstory: str = "وكيل مسؤول عن تقييم تفسير المستخدم للآيات."

    def run(self, correct_interpretation, user_text):
        return {"interpretation_provided": user_text.strip() != ""}

class TajweedAgent(Agent):
    role: str = "Evaluator"
    goal: str = "تحقق من تطابق حكم التجويد مع ما قدمه المستخدم"
    backstory: str = "وكيل مسؤول عن تقييم التجويد."

    def run(self, correct_rule, user_text):
        return {"tajweed_correct": user_text.strip() == correct_rule.strip()}

# LLM حقيقي من Hugging Face لتقييم الإجابات
class EvaluationLLM(LLM):
    role: str = "Evaluator"
    goal: str = "تقييم إجابات المستخدم في الحفظ، التفسير، التجويد"
    backstory: str = "LLM مسؤول عن إعطاء تقييم رقمي للإجابات."

    def __init__(self, client):
        self.client = client

    def run(self, memorization_res, interpretation_res, tajweed_res, ayah_text, user_mem, user_int, user_taj):
        prompt = f"""
القرآن الآية: "{ayah_text}"
حفظ المستخدم: "{user_mem}"
تفسير المستخدم: "{user_int}"
حكم التجويد: "{user_taj}"

قيم الإجابات من 0 إلى 1 لكل قسم: الحفظ، التفسير، التجويد.
أعطني النتائج في شكل JSON: {{"memorization_score": float, "interpretation_score": float, "tajweed_score": float}}
"""
        response = self.client.text_generation(
            model="gpt2",  # ممكن تغيري لموديل أكبر حسب الحاجة
            inputs=prompt,
            max_new_tokens=100,
        )

        try:
            result = json.loads(response.generated_text)
        except Exception:
            # لو حصل خطأ في التحليل، نرجع نتائج مباشرة
            result = {
                "memorization_score": float(memorization_res.get("memorization_correct", False)),
                "interpretation_score": float(interpretation_res.get("interpretation_provided", False)),
                "tajweed_score": float(tajweed_res.get("tajweed_correct", False)),
            }
        return result

def app():
    st.title("Memory Game مع CrewAI وLLM من Hugging Face")

    client = InferenceClient(token=st.secrets["HUGGINGFACE_API_TOKEN"])  # خذ التوكن من secrets
    llm = EvaluationLLM(client)

    memorization_agent = MemorizationAgent()
    interpretation_agent = InterpretationAgent()
    tajweed_agent = TajweedAgent()

    sura_name = st.text_input("اسم السورة (مثال: الفاتحة)").strip()
    start_ayah = st.number_input("من الآية", min_value=1, step=1)
    end_ayah = st.number_input("إلى الآية", min_value=1, step=1)

    if st.button("ابدأ اللعبة"):
        if sura_name not in surahs:
            st.error("السورة غير موجودة في القاموس")
            return

        surah_num = surahs[sura_name]
        for ayah in range(start_ayah, end_ayah + 1):
            ayah_text = get_ayah_text(surah_num, ayah)
            if not ayah_text:
                st.warning(f"لم أتمكن من جلب نص الآية {ayah}")
                continue

            user_mem = st.text_area(f"حفظ الآية {ayah}", key=f"mem_{ayah}")
            user_int = st.text_area(f"تفسير الآية {ayah}", key=f"int_{ayah}")
            user_taj = st.text_input(f"حكم التجويد للآية {ayah}", key=f"taj_{ayah}")

            if st.button(f"تقييم الآية {ayah}"):
                mem_res = memorization_agent.run(ayah_text, user_mem)
                int_res = interpretation_agent.run("", user_int)
                taj_res = tajweed_agent.run("", user_taj)

                evaluation = llm.run(mem_res, int_res, taj_res, ayah_text, user_mem, user_int, user_taj)
                st.json(evaluation)

if __name__ == "__main__":
    app()
