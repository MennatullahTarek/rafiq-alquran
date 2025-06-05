import streamlit as st
import requests
import json
from crewai import Agent, LLM
from huggingface_hub import InferenceClient
import pandas as pd


HUGGINGFACE_API_TOKEN = st.secrets["HUGGINGFACE_API_TOKEN"]  
MODEL_NAME = "gpt2"  

client = InferenceClient(token=HUGGINGFACE_API_TOKEN)

# معجم السور مع أرقامها
surahs = {
    "الفاتحة": 1, "البقرة": 2, "آل عمران": 3, "النساء": 4, "المائدة": 5,
    "الأنعام": 6, "الأعراف": 7, "الأنفال": 8, "التوبة": 9, "يونس": 10,
    # ... ممكن تكمل بقية السور حسب الحاجة
}

def get_ayah_text(surah_num, ayah_num):
    url = f"https://api.quran.com/api/v4/quran/verses/uthmani?verse_key={surah_num}:{ayah_num}"
    r = requests.get(url)
    if r.status_code == 200:
        try:
            return r.json()['verses'][0]['text_uthmani']
        except (KeyError, IndexError):
            return None
    return None

def get_tafsir(surah_num, ayah_num, tafsir_id=91):
    url = f"https://api.quran.com/api/v4/tafsirs/{tafsir_id}/by_ayah/{surah_num}:{ayah_num}"
    r = requests.get(url)
    if r.status_code == 200:
        try:
            return r.json()['tafsir']['text']
        except (KeyError, TypeError):
            return None
    return None

# وكلاء CrewAI
class MemorizationAgent(Agent):
    role: str = "memorization_checker"
    goal: str = "تحقق من صحة الحفظ بمطابقة النص الأصلي"
    backstory: str = "يتحقق من تطابق نص الآية مع إدخال المستخدم"

    def run(self, ayah_text: str, user_input: str):
        correct = ayah_text.strip() == user_input.strip()
        return {"memorization_correct": correct}

class InterpretationAgent(Agent):
    role: str = "interpretation_checker"
    goal: str = "تأكد من وجود تفسير أو شرح للنص"
    backstory: str = "يتحقق من تقديم المستخدم لتفسير للنص"

    def run(self, correct_interpretation: str, user_input: str):
        correct = user_input.strip() != ""
        return {"interpretation_provided": correct}

class TajweedAgent(Agent):
    role: str = "tajweed_checker"
    goal: str = "تحقق من صحة حكم التجويد المدخل"
    backstory: str = "يقارن حكم التجويد الصحيح مع إدخال المستخدم"

    def run(self, correct_rule: str, user_input: str):
        correct = user_input.strip() == correct_rule.strip()
        return {"tajweed_correct": correct}

class EvaluationLLM(LLM):
    model: str =  "gpt2"  

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
            model=self.model,
            inputs=prompt,
            max_new_tokens=100,
            temperature=0.7,
        )
        # النص الناتج من النموذج
        generated_text = response.generated_text

        try:
            result = json.loads(generated_text)
        except Exception:
            # fallback بسيط لو JSON مش نازل مظبوط
            result = {
                "memorization_score": float(memorization_res.get("memorization_correct", False)),
                "interpretation_score": float(interpretation_res.get("interpretation_provided", False)),
                "tajweed_score": float(tajweed_res.get("tajweed_correct", False)),
            }
        return result

def app():
    st.title("Memory Game مع CrewAI و LLM من Hugging Face")

    surah_name = st.selectbox("اختر السورة", list(surahs.keys()))
    start_ayah = st.number_input("من الآية", min_value=1, step=1, value=1)
    end_ayah = st.number_input("إلى الآية", min_value=1, step=1, value=start_ayah)

    # حفظ حالة النتائج
    if "results" not in st.session_state:
        st.session_state.results = []

    if st.button("ابدأ اللعبة") or st.session_state.get("playing", False):
        st.session_state.playing = True
        surah_num = surahs[surah_name]
        ayah_range = range(start_ayah, end_ayah + 1)

        memorization_agent = MemorizationAgent()
        interpretation_agent = InterpretationAgent()
        tajweed_agent = TajweedAgent()
        llm = EvaluationLLM()

        results = []

        for ayah_num in ayah_range:
            ayah_text = get_ayah_text(surah_num, ayah_num)
            tafsir = get_tafsir(surah_num, ayah_num) or ""

            if ayah_text is None:
                st.error(f"لم يتم العثور على نص الآية رقم {ayah_num} في سورة {surah_name}")
                continue

            st.markdown(f"### الآية رقم {ayah_num}")
            st.markdown(f"**نص الآية:**  {ayah_text}")
            st.markdown(f"**التفسير:**  {tafsir}")

            user_mem_key = f"mem_{ayah_num}"
            user_int_key = f"int_{ayah_num}"
            user_taj_key = f"taj_{ayah_num}"

            user_memorization = st.text_area("سرد الآية (حفظ)", key=user_mem_key, value=st.session_state.get(user_mem_key, ""))
            user_interpretation = st.text_area("التفسير / معنى الكلمات", key=user_int_key, value=st.session_state.get(user_int_key, ""))
            user_tajweed = st.text_input("حكم التجويد", key=user_taj_key, value=st.session_state.get(user_taj_key, ""))

            # حفظ القيم في session_state عشان ما تروحش بعد إعادة التحميل
            st.session_state[user_mem_key] = user_memorization
            st.session_state[user_int_key] = user_interpretation
            st.session_state[user_taj_key] = user_tajweed

            mem_res = memorization_agent.run(ayah_text, user_memorization)
            int_res = interpretation_agent.run(tafsir, user_interpretation)
            taj_res = tajweed_agent.run("", user_tajweed)  # مفيش قاعدة صحيحة في API، تخلي التحقق بسيط

            llm_res = llm.run(mem_res, int_res, taj_res, ayah_text, user_memorization, user_interpretation, user_tajweed)

            total_score = sum(llm_res.values())

            results.append({
                "ayah_number": ayah_num,
                "user_memorization": user_memorization,
                "memorization_score": llm_res.get("memorization_score", 0),
                "user_interpretation": user_interpretation,
                "interpretation_score": llm_res.get("interpretation_score", 0),
                "user_tajweed": user_tajweed,
                "tajweed_score": llm_res.get("tajweed_score", 0),
                "total_score": total_score,
            })

            st.write(f"نتيجة الحفظ: {llm_res.get('memorization_score', 0):.2f}")
            st.write(f"نتيجة التفسير: {llm_res.get('interpretation_score', 0):.2f}")
            st.write(f"نتيجة التجويد: {llm_res.get('tajweed_score', 0):.2f}")
            st.write(f"المجموع: {total_score:.2f}")
            st.markdown("---")

        st.session_state.results = results

    if st.session_state.results:
        if st.button("تحميل النتائج كملف CSV"):
            df = pd.DataFrame(st.session_state.results)
            csv_data = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="تحميل ملف النتائج (CSV)",
                data=csv_data,
                file_name=f"results_{surah_name}_{start_ayah}_to_{end_ayah}.csv",
                mime='text/csv'
            )


if __name__ == "__main__":
    app()
