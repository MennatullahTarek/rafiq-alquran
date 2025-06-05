import streamlit as st
import requests
import json
from huggingface_hub import InferenceClient
from io import StringIO
import csv
import os

# خلي توكن Hugging Face محفوظ في متغير بيئة (Env Var)
HF_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
if not HF_TOKEN:
    st.error("⚠️ رجاءً قم بتعيين متغير البيئة HUGGINGFACE_API_TOKEN بالتوكن الخاص بك")
    st.stop()

# إعداد عميل Hugging Face مع موديل مناسب (مثلا gpt2-large)
client = InferenceClient(model="gpt2-large", token=HF_TOKEN)

# قاموس السور ورقمها
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

# API جلب نص الآية
def get_ayah_text(surah_num, ayah_num):
    url = f"https://api.quran.com/api/v4/quran/verses/uthmani?verse_key={surah_num}:{ayah_num}"
    res = requests.get(url)
    if res.status_code == 200:
        try:
            return res.json()['verses'][0]['text_uthmani']
        except:
            return None
    return None

# API جلب التفسير
def get_tafsir(surah_num, ayah_num, tafsir_id=91):
    url = f"https://api.quran.com/api/v4/tafsirs/{tafsir_id}/by_ayah/{surah_num}:{ayah_num}"
    res = requests.get(url)
    if res.status_code == 200:
        try:
            return res.json()['tafsir']['text']
        except:
            return None
    return None

# 3 Agents بتوعك

class MemorizationAgent:
    def __init__(self):
        self.name = "agent_memorization"

    def evaluate(self, ayah_text, user_memorization):
        prompt = f"""قيم حفظ المستخدم للآية التالية (مقياس من 0 إلى 1):

الآية: "{ayah_text}"

حفظ المستخدم: "{user_memorization}"

ارسل فقط رقم التقييم بدون أي شرح.
"""
        response = client.text_generation(
            model="gpt2-large",
            inputs=prompt,
            max_new_tokens=20,
            temperature=0.1,
        )
        result = response.generated_text.strip()
        try:
            score = float(result)
            if 0 <= score <= 1:
                return score
            else:
                return 0.0
        except:
            return 0.0

class InterpretationAgent:
    def __init__(self):
        self.name = "agent_interpretation"

    def evaluate(self, ayah_text, user_interpretation):
        prompt = f"""قيم تفسير المستخدم للآية التالية (مقياس من 0 إلى 1):

الآية: "{ayah_text}"

تفسير المستخدم: "{user_interpretation}"

ارسل فقط رقم التقييم بدون أي شرح.
"""
        response = client.text_generation(
            model="gpt2-large",
            inputs=prompt,
            max_new_tokens=20,
            temperature=0.1,
        )
        result = response.generated_text.strip()
        try:
            score = float(result)
            if 0 <= score <= 1:
                return score
            else:
                return 0.0
        except:
            return 0.0

class TajweedAgent:
    def __init__(self):
        self.name = "agent_tajweed"

    def evaluate(self, ayah_text, user_tajweed):
        prompt = f"""قيم حكم التجويد الخاص بالمستخدم على الآية التالية (مقياس من 0 إلى 1):

الآية: "{ayah_text}"

تجويد المستخدم: "{user_tajweed}"

ارسل فقط رقم التقييم بدون أي شرح.
"""
        response = client.text_generation(
            model="gpt2-large",
            inputs=prompt,
            max_new_tokens=20,
            temperature=0.1,
        )
        result = response.generated_text.strip()
        try:
            score = float(result)
            if 0 <= score <= 1:
                return score
            else:
                return 0.0
        except:
            return 0.0

# انشأ الـ agents
memorization_agent = MemorizationAgent()
interpretation_agent = InterpretationAgent()
tajweed_agent = TajweedAgent()

def app():
    st.title("لعبة حفظ القرآن وتقييم الحفظ، التفسير، والتجويد")

    if "results" not in st.session_state:
        st.session_state.results = {}

    # اختيار السورة والآيات
    surah_name = st.selectbox("اختر السورة", list(surahs.keys()))
    surah_num = surahs[surah_name]

    col1, col2 = st.columns(2)
    with col1:
        start_ayah = st.number_input("من الآية", min_value=1, value=1, step=1)
    with col2:
        end_ayah = st.number_input("إلى الآية", min_value=start_ayah, value=start_ayah, step=1)

    # لكل آية: عرض النص، التفسير، وخانات المستخدم، مع حفظ النصوص في session_state
    for ayah_num in range(start_ayah, end_ayah + 1):
        ayah_text = get_ayah_text(surah_num, ayah_num)
        if not ayah_text:
            st.error(f"⚠️ الآية رقم {ayah_num} في سورة {surah_name} غير موجودة")
            continue

        tafsir_text = get_tafsir(surah_num, ayah_num)
        if not tafsir_text:
            tafsir_text = "لا يوجد تفسير متاح."

        st.markdown(f"### الآية {ayah_num}:")
        st.write(f"**النص:** {ayah_text}")
        st.write(f"**التفسير:** {tafsir_text}")

        # مفاتيح للحفظ في الجلسة
        mem_key = f"mem_{ayah_num}"
        tafsir_key = f"tafsir_{ayah_num}"
        tajweed_key = f"tajweed_{ayah_num}"

        if mem_key not in st.session_state:
            st.session_state[mem_key] = ""
        if tafsir_key not in st.session_state:
            st.session_state[tafsir_key] = ""
        if tajweed_key not in st.session_state:
            st.session_state[tajweed_key] = ""

        st.text_area(f"اكتب الحفظ الخاص بك للآية {ayah_num}", key=mem_key)
        st.text_area(f"اكتب التفسير الخاص بك للآية {ayah_num}", key=tafsir_key)
        st.text_area(f"اكتب حكم التجويد الخاص بك للآية {ayah_num}", key=tajweed_key)

    # زر التقييم
    if st.button("قيم كل الإجابات"):
        st.session_state.results = {}
        for ayah_num in range(start_ayah, end_ayah + 1):
            ayah_text = get_ayah_text(surah_num, ayah_num)
            if not ayah_text:
                continue

            user_mem = st.session_state.get(f"mem_{ayah_num}", "")
            user_tafsir = st.session_state.get(f"tafsir_{ayah_num}", "")
            user_tajweed = st.session_state.get(f"tajweed_{ayah_num}", "")

            mem_score = memorization_agent.evaluate(ayah_text, user_mem)
            interp_score = interpretation_agent.evaluate(ayah_text, user_tafsir)
            tajweed_score = tajweed_agent.evaluate(ayah_text, user_tajweed)

            st.session_state.results[ayah_num] = {
                "memorization_score": mem_score,
                "interpretation_score": interp_score,
                "tajweed_score": tajweed_score,
            }
        st.success("تم التقييم بنجاح! ✅")

    # عرض النتائج
    if st.session_state.results:
        st.subheader("نتائج التقييم:")
        for ayah_num, scores in st.session_state.results.items():
            st.markdown(f"**الآية {ayah_num}:**")
            st.json(scores)

    # زر تحميل CSV
    if st.button("تصدير النتائج كملف CSV"):
        if st.session_state.results:
            output = StringIO()
            writer = csv.writer(output)
            writer.writerow(["آية", "تقييم الحفظ", "تقييم التفسير", "تقييم التجويد"])
            for ayah_num, scores in st.session_state.results.items():
                writer.writerow([
                    ayah_num,
                    scores.get("memorization_score", ""),
                    scores.get("interpretation_score", ""),
                    scores.get("tajweed_score", "")
                ])
            st.download_button(
                label="تحميل ملف التقييمات",
                data=output.getvalue(),
                file_name="quran_evaluation.csv",
                mime="text/csv"
            )
        else:
            st.warning("لا توجد نتائج للتصدير")

if __name__ == "__main__":
    app()
