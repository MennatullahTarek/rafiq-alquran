import pysqlite3
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import requests
import pandas as pd
from crewai import Agent, LLM
from huggingface_hub import InferenceClient
import json


surahs = {
    "الفاتحة": 1, "البقرة": 2, "آل عمران": 3, "النساء": 4, "المائدة": 5, "الأنعام": 6,
    "الأعراف": 7, "الأنفال": 8, "التوبة": 9, "يونس": 10, "هود": 11, "يوسف": 12,
    "الرعد": 13, "إبراهيم": 14, "الحجر": 15, "النحل": 16, "الإسراء": 17, "الكهف": 18,
    "مريم": 19, "طه": 20, "الأنبياء": 21, "الحج": 22, "المؤمنون": 23, "النور": 24,
    "الفرقان": 25, "الشعراء": 26, "النمل": 27, "القصص": 28, "العنكبوت": 29, "الروم": 30,
    "لقمان": 31, "السجدة": 32, "الأحزاب": 33, "سبأ": 34, "فاطر": 35, "يس": 36,
    "الصافات": 37, "ص": 38, "الزمر": 39, "غافر": 40, "فصلت": 41, "الشورى": 42,
    "الزخرف": 43, "الدخان": 44, "الجاثية": 45, "الأحقاف": 46, "محمد": 47, "الفتح": 48,
    "الحجرات": 49, "ق": 50, "الذاريات": 51, "الطور": 52, "النجم": 53, "القمر": 54,
    "الرحمن": 55, "الواقعة": 56, "الحديد": 57, "المجادلة": 58, "الحشر": 59,
    "الممتحنة": 60, "الصف": 61, "الجمعة": 62, "المنافقون": 63, "التغابن": 64,
    "الطلاق": 65, "التحريم": 66, "الملك": 67, "القلم": 68, "الحاقة": 69, "المعارج": 70,
    "نوح": 71, "الجن": 72, "المزّمّل": 73, "المدّثر": 74, "القيامة": 75, "الإنسان": 76,
    "المرسلات": 77, "النبأ": 78, "النازعات": 79, "عبس": 80, "التكوير": 81,
    "الإنفطار": 82, "المطفّفين": 83, "الإنشقاق": 84, "البروج": 85, "الطارق": 86,
    "الأعلى": 87, "الغاشية": 88, "الفجر": 89, "البلد": 90, "الشمس": 91, "الليل": 92,
    "الضحى": 93, "الشرح": 94, "التين": 95, "العلق": 96, "القدر": 97, "البينة": 98,
    "الزلزلة": 99, "العاديات": 100, "القارعة": 101, "التكاثر": 102, "العصر": 103,
    "الهمزة": 104, "الفيل": 105, "قريش": 106, "الماعون": 107, "الكوثر": 108,
    "الكافرون": 109, "النصر": 110, "المسد": 111, "الإخلاص": 112, "الفلق": 113, "الناس": 114
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

# 3 Agents للتقييم البسيط
class MemorizationAgent(Agent):
    def run(self, correct_text, user_text):
        return {"memorization_correct": user_text.strip() == correct_text.strip()}

class InterpretationAgent(Agent):
    def run(self, correct_interpretation, user_text):
       
        return {"interpretation_provided": user_text.strip() != ""}

class TajweedAgent(Agent):
    def run(self, correct_rule, user_text):
        return {"tajweed_correct": user_text.strip() == correct_rule.strip()}


class EvaluationLLM(LLM):
    def __init__(self, client):
        self.client = client

    def run(self, mem_res, int_res, taj_res, ayah_text, user_mem, user_int, user_taj):
        prompt = f"""
الآية: "{ayah_text}"
حفظ المستخدم: "{user_mem}"
تفسير المستخدم: "{user_int}"
حكم التجويد: "{user_taj}"

قيم الحفظ، التفسير، والتجويد بين 0 و 1، وأرجع JSON بالشكل التالي:
{{"memorization_score": float, "interpretation_score": float, "tajweed_score": float}}
"""
        response = self.client.text_generation(
            model="gpt2",  # ممكن تغيري لموديل تاني مناسب
            inputs=prompt,
            max_new_tokens=100,
        )
        try:
            result = json.loads(response.generated_text)
        except Exception:
            # لو فشل التحليل، نعتمد على تقييمات الوكلاء البسيطة
            result = {
                "memorization_score": float(mem_res.get("memorization_correct", False)),
                "interpretation_score": float(int_res.get("interpretation_provided", False)),
                "tajweed_score": float(taj_res.get("tajweed_correct", False)),
            }
        return result

def app():
    st.title("Memory Game - حفظ القرآن مع التفسير والتجويد")

    surah_name = st.text_input("أدخل اسم السورة (مثال: الفاتحة)").strip()
    start_ayah = st.number_input("من الآية", min_value=1, step=1, value=1)
    end_ayah = st.number_input("إلى الآية", min_value=1, step=1, value=1)

    if st.button("ابدأ الاختبار"):
        if surah_name not in surahs:
            st.error("السورة غير موجودة في القاموس.")
            return

        surah_num = surahs[surah_name]
        if start_ayah > end_ayah:
            st.error("رقم الآية البداية يجب أن يكون أصغر أو يساوي رقم الآية النهاية.")
            return

        ayah_list = []
        for ayah_num in range(start_ayah, end_ayah + 1):
            text = get_ayah_text(surah_num, ayah_num)
            tafsir = get_tafsir_quran_api(surah_num, ayah_num)
            if not text or not tafsir:
                st.warning(f"الآية رقم {ayah_num} غير متوفرة أو حدث خطأ في جلب البيانات.")
                continue
            ayah_list.append({"ayah_num": ayah_num, "text": text, "tafsir": tafsir})

        if not ayah_list:
            st.error("لم يتم جلب أي آيات.")
            return

        st.write(f"تم جلب {len(ayah_list)} آيات من سورة {surah_name}")

        # تفاعل المستخدم - بسيط جدًا (تذكير: هذا مثال)
        results = []
        mem_agent = MemorizationAgent()
        int_agent = InterpretationAgent()
        taj_agent = TajweedAgent()
        client = InferenceClient(token="YOUR_HF_TOKEN")
        llm = EvaluationLLM(client)

        for ayah in ayah_list:
            st.subheader(f"الآية رقم {ayah['ayah_num']}")
            st.markdown(f"**النص:** {ayah['text']}")
            mem_answer = st.text_area(f"اكتب حفظك لنص الآية رقم {ayah['ayah_num']}")
            int_answer = st.text_area(f"اكتب تفسيرك للآية رقم {ayah['ayah_num']}")
            taj_answer = st.text_area(f"اكتب حكم التجويد للآية رقم {ayah['ayah_num']}")

            mem_res = mem_agent.run(ayah['text'], mem_answer)
            int_res = int_agent.run(ayah['tafsir'], int_answer)
            taj_res = taj_agent.run("حكم تجويد نموذجي", taj_answer)  # ممكن تحطي القواعد الصحيحة هنا

            eval_res = llm.run(mem_res, int_res, taj_res, ayah['text'], mem_answer, int_answer, taj_answer)

            results.append({
                "ayah_num": ayah['ayah_num'],
                "text": ayah['text'],
                "user_mem": mem_answer,
                "user_int": int_answer,
                "user_taj": taj_answer,
                **eval_res
            })

   
        df = pd.DataFrame(results)
        st.dataframe(df)

        csv_data = df.to_csv(index=False)
        st.download_button(
            label="تحميل النتائج كملف CSV",
            data=csv_data,
            file_name=f"results_{surah_name}_{start_ayah}_{end_ayah}.csv",
            mime="text/csv"
        )


if __name__ == "__main__":
    app()
