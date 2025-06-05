import streamlit as st
import pandas as pd
from crewai import Agent, LLM



# تعريف الوكلاء
class MemorizationAgent(Agent):
    def run(self, ayah_text, user_input):
        # يقارن الحفظ (ممكن تستخدم تقنيات نصية متقدمة)
        return {"memorization_correct": user_input.strip() == ayah_text.strip()}

class InterpretationAgent(Agent):
    def run(self, correct_interpretation, user_input):
        # يقيم تفسير المستخدم (ممكن LLM يتدخل لتحسين التقييم)
        correct = user_input.strip() == correct_interpretation.strip()
        return {"interpretation_correct": correct}

class TajweedAgent(Agent):
    def run(self, correct_rule, user_input):
        # يقارن حكم التجويد
        correct = user_input.strip() == correct_rule.strip()
        return {"tajweed_correct": correct}

# تعريف LLM (بمهمة التنسيق والتقييم النهائي)
class EvaluationLLM(LLM):
    def run(self, memorization_res, interpretation_res, tajweed_res):
        total_score = sum([
            memorization_res.get("memorization_correct", False),
            interpretation_res.get("interpretation_correct", False),
            tajweed_res.get("tajweed_correct", False)
        ])
        return {"total_score": total_score}

# داتا تجريبية (تقدري تستبدليها بمصدر موثوق أو API)
QURAN_DATA = {
    "الفاتحة": [
        {"number": 1, "text": "بسم الله الرحمن الرحيم", "interpretation": "بسم الله المهيمن الرحيم", "tajweed": "إظهار"},
        {"number": 2, "text": "الحمد لله رب العالمين", "interpretation": "الحمد والثناء لله رب العالمين", "tajweed": "إدغام"},
        {"number": 3, "text": "الرحمن الرحيم", "interpretation": "الرحمن والرحيم", "tajweed": "إظهار"},
        # ... ممكن تضيفي باقي الآيات
    ]
}

def get_ayahs(sura_name, start, end):
    if sura_name not in QURAN_DATA:
        return []
    ayahs = QURAN_DATA[sura_name]
    return [a for a in ayahs if start <= a['number'] <= end]

def app():
    st.title("Memory Game مع CrewAI")

    sura_name = st.text_input("اسم السورة (مثال: الفاتحة)").strip()
    start_ayah = st.number_input("من الآية", min_value=1, step=1)
    end_ayah = st.number_input("إلى الآية", min_value=1, step=1)

    if st.button("ابدأ اللعبة"):
        ayahs = get_ayahs(sura_name, start_ayah, end_ayah)
        if not ayahs:
            st.error("السورة أو الآيات غير موجودة")
            return

        memorization_agent = MemorizationAgent()
        interpretation_agent = InterpretationAgent()
        tajweed_agent = TajweedAgent()
        llm = EvaluationLLM()

        results = []

        for ayah in ayahs:
            st.markdown(f"### الآية رقم {ayah['number']}")
            st.write(f"النص: {ayah['text']}")

            user_memorization = st.text_area(f"سرد الآية (حفظ)", key=f"mem_{ayah['number']}")
            user_interpretation = st.text_area(f"التفسير / معنى الكلمات", key=f"int_{ayah['number']}")
            user_tajweed = st.text_input(f"حكم التجويد", key=f"taj_{ayah['number']}")

            # تقييم الوكلاء
            mem_res = memorization_agent.run(ayah['text'], user_memorization)
            int_res = interpretation_agent.run(ayah['interpretation'], user_interpretation)
            taj_res = tajweed_agent.run(ayah['tajweed'], user_tajweed)

            # تقييم LLM
            total = llm.run(mem_res, int_res, taj_res)['total_score']

            results.append({
                "ayah_number": ayah['number'],
                "user_memorization": user_memorization,
                "memorization_correct": mem_res["memorization_correct"],
                "user_interpretation": user_interpretation,
                "interpretation_correct": int_res["interpretation_correct"],
                "user_tajweed": user_tajweed,
                "tajweed_correct": taj_res["tajweed_correct"],
                "total_score": total,
            })

            st.write(f"نتيجة الحفظ: {'✔️' if mem_res['memorization_correct'] else '❌'}")
            st.write(f"نتيجة التفسير: {'✔️' if int_res['interpretation_correct'] else '❌'}")
            st.write(f"نتيجة التجويد: {'✔️' if taj_res['tajweed_correct'] else '❌'}")
            st.write(f"المجموع: {total} / 3")
            st.markdown("---")

        if st.button("تحميل النتائج كملف CSV"):
            df = pd.DataFrame(results)
            csv_data = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="تحميل ملف النتائج (CSV)",
                data=csv_data,
                file_name=f"results_{sura_name}_{start_ayah}_to_{end_ayah}.csv",
                mime='text/csv'
            )

if __name__ == "__main__":
   app()
