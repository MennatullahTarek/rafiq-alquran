import streamlit as st
import requests
import pandas as pd
import difflib
import os
from huggingface_hub import InferenceClient



HF_TOKEN = os.getenv("HF_TOKEN")  
HF_MODEL = "gpt2" 

client = InferenceClient(model=HF_MODEL, token=HF_TOKEN)


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
        except Exception:
            return None
    return None

def get_tafsir(surah_num, ayah_num, tafsir_id=91):
    url = f"https://api.quran.com/api/v4/tafsirs/{tafsir_id}/by_ayah/{surah_num}:{ayah_num}"
    res = requests.get(url)
    if res.status_code == 200:
        try:
            return res.json()['tafsir']['text']
        except Exception:
            return None
    return None

# =========== Agent 4: LLM ذكي (تصحيح وتقييم) ==========
class SmartAgent:
    def __init__(self, client):
        self.client = client

    def correct_text(self, user_text, original_text):
        prompt = (
            f"صحح لي النص التالي بناءً على النص الأصلي.\n\n"
            f"النص الأصلي:\n{original_text}\n\n"
            f"النص المدخل:\n{user_text}\n\n"
            f"أعطني النص المصحح فقط."
        )
        try:
            response = self.client.text_generation(
                inputs=prompt,
                max_new_tokens=150,
                temperature=0.3,
            )
            # بعض ال API ترجع dict او list
            if isinstance(response, dict):
                return response.get('generated_text', '')
            elif isinstance(response, list):
                return response[0].get('generated_text', '')
            else:
                return str(response)
        except Exception as e:
            return f"خطأ في التصحيح: {e}"

    def evaluate_similarity(self, user_text, original_text):
        ratio = difflib.SequenceMatcher(None, user_text, original_text).ratio()
        return round(ratio, 3)

    def evaluate_explanation(self, user_explanation, official_explanation):
        # ممكن تستخدم LLM لتقييم الجودة لكن هنا بمقارنة نصية مبسطة
        return self.evaluate_similarity(user_explanation, official_explanation)


# =========== Agent 1: استقبال البيانات وتنسيقها ==========
class InputAgent:
    def __init__(self, surahs):
        self.surahs = surahs

    def surah_number(self, surah_name):
        return self.surahs.get(surah_name, None)

# =========== Agent 2: اختبار الحفظ ==========
class MemorizationAgent:
    def __init__(self):
        pass

    def evaluate_memorization(self, user_answer, correct_text):
        ratio = difflib.SequenceMatcher(None, user_answer.strip(), correct_text.strip()).ratio()
        return round(ratio, 3)  # بين 0 و 1


# =========== Agent 3: التفسير ==========
class TafsirAgent:
    def __init__(self):
        pass

    def evaluate_tafsir(self, user_tafsir, official_tafsir):
        ratio = difflib.SequenceMatcher(None, user_tafsir.strip(), official_tafsir.strip()).ratio()
        return round(ratio, 3)


def app():
    st.title("🕌 اختبار حفظ وتفسير آيات القرآن الكريم")

 
    if 'results' not in st.session_state:
        st.session_state.results = []

    input_agent = InputAgent(surahs)
    memorization_agent = MemorizationAgent()
    tafsir_agent = TafsirAgent()
    smart_agent = SmartAgent(client)

 
    st.sidebar.header("إعدادات الاختبار")

    surah_name = st.sidebar.selectbox("اختر السورة", list(surahs.keys()))
    surah_num = input_agent.surah_number(surah_name)

    start_ayah = st.sidebar.number_input("بداية الآيات", min_value=1, value=1)
    end_ayah = st.sidebar.number_input("نهاية الآيات", min_value=start_ayah, value=start_ayah+2)

    if st.sidebar.button("ابدأ الاختبار"):

        
        ayahs_list = list(range(start_ayah, end_ayah+1))
        st.session_state.ayahs_list = ayahs_list
        st.session_state.current_index = 0
        st.session_state.surah_num = surah_num
        st.session_state.surah_name = surah_name
        st.session_state.results = []

        st.experimental_rerun()

   
    if 'ayahs_list' in st.session_state and st.session_state.ayahs_list:

        idx = st.session_state.current_index
        ayah_num = st.session_state.ayahs_list[idx]
        surah_num = st.session_state.surah_num
        surah_name = st.session_state.surah_name

        # جلب نص الآية
        correct_ayah_text = get_ayah_text(surah_num, ayah_num) or "لا يوجد نص الآية"
        official_tafsir = get_tafsir(surah_num, ayah_num) or "لا يوجد تفسير"

        st.markdown(f"### السورة: **{surah_name}** | الآية رقم: **{ayah_num}**")
        st.markdown(f"**النص الأصلي للآية:** {correct_ayah_text}")

        st.markdown("### 📝 أكمل الآية التالية كتابة:")
        user_memorization = st.text_area("أكتب الآية من الذاكرة هنا:")

        st.markdown("### 📖 اكتب تفسيرك أو شرح معاني الكلمات:")
        user_tafsir = st.text_area("تفسيرك هنا:")

        if st.button("تقييم وإرسال"):
            # Agent2: تقييم الحفظ
            memorization_score = memorization_agent.evaluate_memorization(user_memorization, correct_ayah_text)

            # Agent3: تقييم التفسير
            tafsir_score = tafsir_agent.evaluate_tafsir(user_tafsir, official_tafsir)

            # Agent4: الدعم الذكي - التصحيح
            corrected_memorization = smart_agent.correct_text(user_memorization, correct_ayah_text)

            # Agent4: الدعم الذكي - تقييم التفسير
            explanation_eval = smart_agent.evaluate_explanation(user_tafsir, official_tafsir)

           
            st.session_state.results.append({
                "سورة": surah_name,
                "آية": ayah_num,
                "الآية الأصلية": correct_ayah_text,
                "إجابة اليوزر": user_memorization,
                "تصحيح الآية": corrected_memorization,
                "تقييم الحفظ": memorization_score,
                "تفسير اليوزر": user_tafsir,
                "تقييم التفسير": tafsir_score,
                "تقييم التفسير الذكي": explanation_eval,
                "التفسير الرسمي": official_tafsir
            })

           
            if idx + 1 < len(st.session_state.ayahs_list):
                st.session_state.current_index += 1
                st.experimental_rerun()
            else:
                st.success("تم الانتهاء من جميع الآيات!")
                st.rerun()


    if st.session_state.results:
        st.markdown("---")
        st.header(" نتائج الاختبار")

        df = pd.DataFrame(st.session_state.results)

        st.dataframe(df)

        # تنزيل النتائج
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="تحميل النتائج CSV",
            data=csv,
            file_name='quran_memorization_results.csv',
            mime='text/csv'
        )

if __name__ == "__main__":
    app()
