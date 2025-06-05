import streamlit as st
import requests
import json
from huggingface_hub import InferenceClient
from io import StringIO
import csv


import os
HF_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
if not HF_TOKEN:
    st.error("⚠️ من فضلك ضيف متغير البيئة HUGGINGFACE_API_TOKEN بتوكن Hugging Face الخاص بك")
    st.stop()


client = InferenceClient(model="gpt2-large", token=HF_TOKEN)

# القاموس للسور وأرقامها
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
    res = requests.get(url)
    if res.status_code == 200:
        try:
            return res.json()['verses'][0]['text_uthmani']
        except (KeyError, IndexError):
            return None
    return None

def get_tafsir(surah_num, ayah_num, tafsir_id=91):
    url = f"https://api.quran.com/api/v4/tafsirs/{tafsir_id}/by_ayah/{surah_num}:{ayah_num}"
    res = requests.get(url)
    if res.status_code == 200:
        try:
            return res.json()['tafsir']['text']
        except (KeyError, TypeError):
            return None
    return None

# تقييم الإجابات باستخدام LLM من Hugging Face
def evaluate_answers(ayah_text, user_mem, user_tafsir, user_tajweed):
    prompt = f"""
الآية: "{ayah_text}"
حفظ المستخدم: "{user_mem}"
تفسير المستخدم: "{user_tafsir}"
حكم التجويد: "{user_tajweed}"

قيم الحفظ والتفسير والتجويد من 0 إلى 1 على شكل JSON كما يلي:
{{"memorization_score": float, "interpretation_score": float, "tajweed_score": float}}
"""

    response = client.text_generation(
        inputs=prompt,
        max_new_tokens=150,
        temperature=0.3,
        top_p=0.9,
        top_k=50,
    )

    # المحتوى الناتج من النموذج ممكن يحتوي نص زائد لذلك نبحث عن JSON داخله
    generated_text = response.generated_text.strip()
    try:
        # محاولة تحويل النص إلى JSON
        start_index = generated_text.find("{")
        end_index = generated_text.rfind("}") + 1
        json_text = generated_text[start_index:end_index]
        scores = json.loads(json_text)
        return scores
    except Exception:
        # لو حصل خطأ نرجع صفر في كل حاجة
        return {
            "memorization_score": 0.0,
            "interpretation_score": 0.0,
            "tajweed_score": 0.0,
        }

def app():
    st.title("لعبة حفظ القرآن مع تفسير وحكم التجويد")

    # حالة حفظ الإدخال في Streamlit
    if "inputs" not in st.session_state:
        st.session_state.inputs = {}

    # اختيار السورة والآيات
    surah_name = st.selectbox("اختر السورة", list(surahs.keys()))
    surah_num = surahs[surah_name]

    col1, col2 = st.columns(2)
    with col1:
        start_ayah = st.number_input("من الآية", min_value=1, value=1, step=1)
    with col2:
        end_ayah = st.number_input("إلى الآية", min_value=start_ayah, value=start_ayah, step=1)

    if st.button("ابدأ التقييم"):
        results = []

        for ayah_num in range(start_ayah, end_ayah + 1):
            ayah_text = get_ayah_text(surah_num, ayah_num)
            if not ayah_text:
                st.error(f"⚠️ لم يتم العثور على نص الآية رقم {ayah_num} في سورة {surah_name}")
                continue

            tafsir_text = get_tafsir(surah_num, ayah_num)
            if not tafsir_text:
                tafsir_text = "لا يوجد تفسير متاح لهذه الآية."

            st.markdown(f"### الآية {ayah_num}:")
            st.write(ayah_text)

            user_mem = st.text_area(f"اكتب الحفظ الخاص بك للآية {ayah_num}", key=f"mem_{ayah_num}")
            user_tafsir = st.text_area(f"اكتب التفسير الخاص بك للآية {ayah_num}", key=f"tafsir_{ayah_num}")
            user_tajweed = st.text_area(f"اكتب حكم التجويد الخاص بك للآية {ayah_num}", key=f"tajweed_{ayah_num}")

            if st.button(f"قيم الإجابة للآية {ayah_num}", key=f"eval_{ayah_num}"):
                scores = evaluate_answers(ayah_text, user_mem, user_tafsir, user_tajweed)
                st.json(scores)
                results.append({"ayah": ayah_num, "scores": scores})

    # لو عايز تصدير النتائج:
    if st.button("تصدير النتائج كملف CSV"):
        if "results" in st.session_state and st.session_state.results:
            output = StringIO()
            writer = csv.writer(output)
            writer.writerow(["آية", "تقييم الحفظ", "تقييم التفسير", "تقييم التجويد"])
            for item in st.session_state.results:
                ayah = item["ayah"]
                scores = item["scores"]
                writer.writerow([
                    ayah,
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
