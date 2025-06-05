import pysqlite3
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os
import streamlit as st
import pandas as pd
from crewai import Agent, LLM
from huggingface_hub import InferenceClient
import json

hf_token = os.getenv("HF_TOKEN")
if not hf_token:
    st.error("Error: Please set the HF_TOKEN environment variable with your Hugging Face token.")
    st.stop()

client = InferenceClient(token=hf_token)

class MemorizationAgent(Agent):
    def run(self, ayah_text, user_input):
        correct = ayah_text.strip() == user_input.strip()
        return {"memorization_correct": correct}

class InterpretationAgent(Agent):
    def run(self, correct_interpretation, user_input):
        correct = user_input.strip() != ""
        return {"interpretation_provided": correct}

class TajweedAgent(Agent):
    def run(self, correct_rule, user_input):
        correct = user_input.strip() == correct_rule.strip()
        return {"tajweed_correct": correct}

class EvaluationLLM(LLM):
    def run(self, memorization_res, interpretation_res, tajweed_res, ayah_text, user_mem, user_int, user_taj):
        prompt = f"""
        القرآن الآية: "{ayah_text}"
        حفظ المستخدم: "{user_mem}"
        تفسير المستخدم: "{user_int}"
        حكم التجويد: "{user_taj}"

        قيم الإجابات من 0 إلى 1 لكل قسم: الحفظ، التفسير، التجويد.
        أعطني النتائج في شكل JSON: {{"memorization_score": float, "interpretation_score": float, "tajweed_score": float}}
        """
        response = client.text_generation(
            model="gpt2",
            inputs=prompt,
            max_new_tokens=100,
        )
        generated_text = response.generated_text if hasattr(response, 'generated_text') else response[0]['generated_text']
        try:
            result = json.loads(generated_text)
        except Exception:
            result = {
                "memorization_score": float(memorization_res.get("memorization_correct", False)),
                "interpretation_score": float(interpretation_res.get("interpretation_provided", False)),
                "tajweed_score": float(tajweed_res.get("tajweed_correct", False)),
            }
        return result

QURAN_DATA = {
    "الفاتحة": [
        {"number": 1, "text": "بسم الله الرحمن الرحيم", "interpretation": "بسم الله المهيمن الرحيم", "tajweed": "إظهار"},
        {"number": 2, "text": "الحمد لله رب العالمين", "interpretation": "الحمد والثناء لله رب العالمين", "tajweed": "إدغام"},
        {"number": 3, "text": "الرحمن الرحيم", "interpretation": "الرحمن والرحيم", "tajweed": "إظهار"},
    ]
}

def get_ayahs(sura_name, start, end):
    if sura_name not in QURAN_DATA:
        return []
    ayahs = QURAN_DATA[sura_name]
    return [a for a in ayahs if start <= a['number'] <= end]

def app():
    st.title("Memory Game مع CrewAI وLLM حقيقي من Hugging Face")

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

            mem_res = memorization_agent.run(ayah['text'], user_memorization)
            int_res = interpretation_agent.run(ayah['interpretation'], user_interpretation)
            taj_res = tajweed_agent.run(ayah['tajweed'], user_tajweed)

            llm_res = llm.run(mem_res, int_res, taj_res, ayah['text'], user_memorization, user_interpretation, user_tajweed)

            results.append({
                "ayah_number": ayah['number'],
                "user_memorization": user_memorization,
                "memorization_score": llm_res.get("memorization_score", 0),
                "user_interpretation": user_interpretation,
                "interpretation_score": llm_res.get("interpretation_score", 0),
                "user_tajweed": user_tajweed,
                "tajweed_score": llm_res.get("tajweed_score", 0),
                "total_score": sum(llm_res.values()),
            })

            st.write(f"نتيجة الحفظ: {llm_res.get('memorization_score', 0):.2f}")
            st.write(f"نتيجة التفسير: {llm_res.get('interpretation_score', 0):.2f}")
            st.write(f"نتيجة التجويد: {llm_res.get('tajweed_score', 0):.2f}")
            st.write(f"المجموع: {sum(llm_res.values()):.2f}")
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
