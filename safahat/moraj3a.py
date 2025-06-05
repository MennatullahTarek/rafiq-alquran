import os
import streamlit as st
import requests
import json
from crewai import Agent, LLM
from huggingface_hub import InferenceClient
from io import StringIO
import csv

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






def get_tafsir_quran_api(surah, ayah, tafsir_id=91):
    url = f"https://api.quran.com/api/v4/tafsirs/{tafsir_id}/by_ayah/{surah}:{ayah}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()['tafsir']['text']
        except (KeyError, TypeError):
            return "⚠️ لم يتم العثور على التفسير."
    else:
        return "❌ فشل في الاتصال بالـ API."

def get_ayah_text(surah, ayah):
    url = f"https://api.quran.com/api/v4/quran/verses/uthmani?verse_key={surah}:{ayah}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()['verses'][0]['text_uthmani']
        except (KeyError, IndexError):
            return "⚠️ لم يتم العثور على نص الآية."
    else:
        return "❌ فشل في الاتصال بجلب نص الآية."

# تعريف الوكلاء (Agents)
class MemorizationAgent(Agent):
    role: str = "Memorization Agent"
    goal: str = "Check if user's memorization matches the ayah text."
    backstory: str = "This agent evaluates memorization accuracy."

    def run(self, ayah_text: str, user_input: str):
        correct = ayah_text.strip() == user_input.strip()
        return {"memorization_correct": correct}

class InterpretationAgent(Agent):
    role: str = "Interpretation Agent"
    goal: str = "Check if user provided an interpretation."
    backstory: str = "This agent checks if interpretation is given."

    def run(self, correct_interpretation: str, user_input: str):
        correct = user_input.strip() != ""
        return {"interpretation_provided": correct}

class TajweedAgent(Agent):
    role: str = "Tajweed Agent"
    goal: str = "Check if user's tajweed rule matches the correct one."
    backstory: str = "This agent evaluates tajweed correctness."

    def run(self, correct_rule: str, user_input: str):
        correct = user_input.strip() == correct_rule.strip()
        return {"tajweed_correct": correct}

# LLM من Hugging Face لتقييم الإجابات
class EvaluationLLM(LLM):
    role: str = "Evaluation LLM"
    goal: str = "Evaluate user answers and give scores from 0 to 1."
    backstory: str = "Uses Hugging Face model to score memorization, interpretation, and tajweed."

    def __init__(self, model: str, token: str):
        super().__init__(model=model)
        self.client = InferenceClient(token=token)

    def run(self, memorization_res, interpretation_res, tajweed_res, ayah_text, user_mem, user_int, user_taj):
        prompt = f"""
الآية: "{ayah_text}"
حفظ المستخدم: "{user_mem}"
تفسير المستخدم: "{user_int}"
حكم التجويد: "{user_taj}"

قيم كل قسم من 0 إلى 1:
الحفظ، التفسير، التجويد.

أرجوك أعطني النتائج في JSON بهذا الشكل:
{{"memorization_score": float, "interpretation_score": float, "tajweed_score": float}}
"""
        response = self.client.text_generation(
            model=self.model,
            inputs=prompt,
            max_new_tokens=100,
        )

        try:
            result = json.loads(response.generated_text)
        except Exception:
            # لو في مشكلة في التحليل نرجع القيم اللي حسبها الوكلاء كقيم افتراضية
            result = {
                "memorization_score": float(memorization_res.get("memorization_correct", False)),
                "interpretation_score": float(interpretation_res.get("interpretation_provided", False)),
                "tajweed_score": float(tajweed_res.get("tajweed_correct", False)),
            }
        return result

# بيانات التجويد الصحيحة (ممكن تضيف أو تعدل)
TAJWEED_RULES = {
    # مثال: {("الفاتحة", 1): "إظهار"}
    ("الفاتحة", 1): "إظهار",
    ("الفاتحة", 2): "إدغام",
    ("الفاتحة", 3): "إظهار",
}

def app():
    st.title("لعبة حفظ وتفسير القرآن مع تقييم ذكي باستخدام CrewAI وHugging Face")

    # خزن حالة المدخلات عشان الصفحة ماتتعادش
    if "responses" not in st.session_state:
        st.session_state.responses = {}

    # اختيار السورة والآيات
    surah_name = st.selectbox("اختر السورة", list(surahs.keys()))
    surah_num = surahs[surah_name]

    start_ayah = st.number_input("من الآية", min_value=1, max_value=286, value=1, step=1)  # 286 أكبر سورة البقرة مثلا
    end_ayah = st.number_input("إلى الآية", min_value=start_ayah, max_value=286, value=start_ayah, step=1)

    # مفاتيح خاصة بالحالة
    def make_key(num, field):
        return f"{surah_name}_{num}_{field}"

    if st.button("ابدأ"):
        st.session_state.responses.clear()  # تمسح الإجابات القديمة وتبدأ جديدة

    # لو بدأنا أو في إدخال بيانات
    ayah_range = range(start_ayah, end_ayah + 1)
    memorization_agent = MemorizationAgent()
    interpretation_agent = InterpretationAgent()
    tajweed_agent = TajweedAgent()

    # تأكد من وجود التوكن في البيئة
    token = os.getenv("HUGGINGFACE_API_TOKEN")
    if not token:
        st.error("خطأ: من فضلك اضف متغير البيئة HUGGINGFACE_API_TOKEN بالتوكن الخاص بك")
        return

    # الموديل ممكن تختار واحد مناسب من Hugging Face مثل: "gpt2" أو "gpt2-large" أو غيره حسب توكنك وإمكانياتك
    hf_model = "gpt2"

    llm = EvaluationLLM(model=hf_model, token=token)

    results = []

    for ayah_num in ayah_range:
        ayah_text = get_ayah_text(surah_num, ayah_num)
        tafsir_text = get_tafsir_quran_api(surah_num, ayah_num)
        tajweed_rule = TAJWEED_RULES.get((surah_name, ayah_num), "")

        st.markdown(f"### الآية رقم {ayah_num}")
        st.markdown(f"**النص:** {ayah_text}")

        mem_key = make_key(ayah_num, "memorization")
        int_key = make_key(ayah_num, "interpretation")
        taj_key = make_key(ayah_num, "tajweed")

        if mem_key not in st.session_state.responses:
            st.session_state.responses[mem_key] = ""
        if int_key not in st.session_state.responses:
            st.session_state.responses[int_key] = ""
        if taj_key not in st.session_state.responses:
            st.session_state.responses[taj_key] = ""

        user_memorization = st.text_area(f"سرد الآية (حفظ)", key=mem_key, value=st.session_state.responses[mem_key])
        user_interpretation = st.text_area(f"التفسير / معنى الكلمات", key=int_key, value=st.session_state.responses[int_key])
        user_tajweed = st.text_input(f"حكم التجويد", key=taj_key, value=st.session_state.responses[taj_key])

        # حفظ البيانات في الحالة
        st.session_state.responses[mem_key] = user_memorization
        st.session_state.responses[int_key] = user_interpretation
        st.session_state.responses[taj_key] = user_tajweed

        mem_res = memorization_agent.run(ayah_text, user_memorization)
        int_res = interpretation_agent.run(tafsir_text, user_interpretation)
        taj_res = tajweed_agent.run(tajweed_rule, user_tajweed)

        llm_res = llm.run(mem_res, int_res, taj_res, ayah_text, user_memorization, user_interpretation, user_tajweed)

        total_score = sum(llm_res.values())
        max_score = len(llm_res)

        st.markdown(f"**التقييم:**")
        st.markdown(f"- الحفظ: {llm_res.get('memorization_score', 0):.2f}")
        st.markdown(f"- التفسير: {llm_res.get('interpretation_score', 0):.2f}")
        st.markdown(f"- التجويد: {llm_res.get('tajweed_score', 0):.2f}")
        st.markdown(f"- المجموع: {total_score:.2f} / {max_score}")

        results.append({
            "ayah_num": ayah_num,
            "memorization": user_memorization,
            "interpretation": user_interpretation,
            "tajweed": user_tajweed,
            "scores": llm_res,
        })

    # زر تحميل النتائج ك CSV
    if st.button("تحميل النتائج كملف CSV"):
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["رقم الآية", "الحفظ", "التفسير", "التجويد", "درجة الحفظ", "درجة التفسير", "درجة التجويد"])
        for r in results:
            writer.writerow([
                r["ayah_num"],
                r["memorization"],
                r["interpretation"],
                r["tajweed"],
                r["scores"].get("memorization_score", 0),
                r["scores"].get("interpretation_score", 0),
                r["scores"].get("tajweed_score", 0),
            ])
        st.download_button("تحميل CSV", data=output.getvalue(), file_name="results.csv", mime="text/csv")

if __name__ == "__main__":
    app()
