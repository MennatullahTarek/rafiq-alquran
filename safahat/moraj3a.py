import streamlit as st
import requests
import difflib
import re
import csv
from io import StringIO
from huggingface_hub import InferenceClient

# Agent 4: LLM
class LLMHelper:
    def __init__(self, hf_token, model="tiiuae/falcon-7b-instruct"):
        self.client = InferenceClient(token=hf_token)
        self.model = model

    def ask(self, prompt):
        response = self.client.text_generation(
            model=self.model,
            prompt=prompt,
            max_new_tokens=100,
            temperature=0.7
        )
        return response

# Agent 1: سور وآيات
def get_surahs():
    return {
        "الفاتحة": 1, "البقرة": 2, "آل عمران": 3, "النساء": 4, "المائدة": 5, "الأنعام": 6, "الأعراف": 7,
        "الأنفال": 8, "التوبة": 9, "يونس": 10, "هود": 11, "يوسف": 12, "الرعد": 13, "إبراهيم": 14,
        "الحجر": 15, "النحل": 16, "الإسراء": 17, "الكهف": 18, "مريم": 19, "طه": 20, "الأنبياء": 21,
        "الحج": 22, "المؤمنون": 23, "النور": 24, "الفرقان": 25, "الشعراء": 26, "النمل": 27, "القصص": 28,
        "العنكبوت": 29, "الروم": 30, "لقمان": 31, "السجدة": 32, "الأحزاب": 33, "سبأ": 34, "فاطر": 35,
        "يس": 36, "الصافات": 37, "ص": 38, "الزمر": 39, "غافر": 40, "فصلت": 41, "الشورى": 42, "الزخرف": 43,
        "الدخان": 44, "الجاثية": 45, "الأحقاف": 46, "محمد": 47, "الفتح": 48, "الحجرات": 49, "ق": 50,
        "الذاريات": 51, "الطور": 52, "النجم": 53, "القمر": 54, "الرحمن": 55, "الواقعة": 56, "الحديد": 57,
        "المجادلة": 58, "الحشر": 59, "الممتحنة": 60, "الصف": 61, "الجمعة": 62, "المنافقون": 63, "التغابن": 64,
        "الطلاق": 65, "التحريم": 66, "الملك": 67, "القلم": 68, "الحاقة": 69, "المعارج": 70, "نوح": 71,
        "الجن": 72, "المزمل": 73, "المدثر": 74, "القيامة": 75, "الإنسان": 76, "المرسلات": 77, "النبأ": 78,
        "النازعات": 79, "عبس": 80, "التكوير": 81, "الإنفطار": 82, "المطففين": 83, "الانشقاق": 84, "البروج": 85,
        "الطارق": 86, "الأعلى": 87, "الغاشية": 88, "الفجر": 89, "البلد": 90, "الشمس": 91, "الليل": 92,
        "الضحى": 93, "الشرح": 94, "التين": 95, "العلق": 96, "القدر": 97, "البينة": 98, "الزلزلة": 99,
        "العاديات": 100, "القارعة": 101, "التكاثر": 102, "العصر": 103, "الهمزة": 104, "الفيل": 105, "قريش": 106,
        "الماعون": 107, "الكوثر": 108, "الكافرون": 109, "النصر": 110, "المسد": 111, "الإخلاص": 112,
        "الفلق": 113, "الناس": 114
    }

def get_ayah_text(surah, ayah):
    url = f"https://api.quran.com/api/v4/quran/verses/uthmani?verse_key={surah}:{ayah}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()['verses'][0]['text_uthmani']
        except (KeyError, IndexError):
            return "⚠️ لم يتم العثور على نص الآية."
    return "❌ فشل الاتصال بنص الآية."

# Agent 2: تفسير

def get_tafsir(surah, ayah, tafsir_id=91):
    url = f"https://api.quran.com/api/v4/tafsirs/{tafsir_id}/by_ayah/{surah}:{ayah}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()['tafsir']['text']
        except (KeyError, TypeError):
            return "⚠️ لم يتم العثور على التفسير."
    return "❌ فشل الاتصال بالتفسير."

# أدوات تقييم الحفظ

def strip_tashkeel(text):
    return re.sub(r'[\u064B-\u0652]', '', text)

def compare_ayah(user_input, actual_text):
    actual_clean = strip_tashkeel(actual_text.replace('\n', '').strip())
    user_clean = user_input.replace('\n', '').strip()
    ratio = difflib.SequenceMatcher(None, actual_clean, user_clean).ratio()
    return round(ratio * 100, 2)

# التطبيق الرئيسي

def app():
    st.set_page_config(page_title="رفيق القرآن")
    st.title("📖 رفيق القرآن - مراجعة وحفظ وتفسير")

    hf_token = st.secrets["hf_token"]
    llm_helper = LLMHelper(hf_token)
    surahs = get_surahs()

    surah_name = st.selectbox("اختر السورة", list(surahs.keys()))
    start_ayah = st.number_input("من الآية رقم", min_value=1, value=1)
    end_ayah = st.number_input("إلى الآية رقم", min_value=start_ayah, value=start_ayah)

    if "responses" not in st.session_state:
        st.session_state.responses = []

    if st.button("ابدأ الإختبار"):
        for ayah_num in range(start_ayah, end_ayah + 1):
            st.subheader(f"الآية {ayah_num}")
            actual_ayah = get_ayah_text(surahs[surah_name], ayah_num)
            tafsir = get_tafsir(surahs[surah_name], ayah_num)

            st.markdown("### 🧠 اختبار الحفظ")
            # عرض أول كم كلمة من الآية كمحفز
            words = actual_ayah.split(" ")
            clue = " ".join(words[:2]) + " ..."
            st.markdown(f"#### 👇 أكمل بعد: `{clue}`")

            user_mem = st.text_area(f"إكمال الآية ({ayah_num}):", key=f"mem_{ayah_num}")

            score = correction = "-"
            if user_mem:
                score = compare_ayah(user_mem, actual_ayah)
                st.markdown(f"✅ تقييم الحفظ: **{score}%**")

            st.markdown("### 📘 التفسير")
            user_tafsir = st.text_area(f"اشرح معنى الآية أو الكلمات ({ayah_num}):", key=f"tafsir_{ayah_num}")
            if user_tafsir:
                prompt = f"قارن التفسير التالي بالتفسير الرسمي: '{user_tafsir}'. التفسير الرسمي: '{tafsir}'. قيمه من ١٠ مع تصحيح الخطأ."
                correction = llm_helper.ask(prompt)
                st.markdown("🧾 تقييم التفسير:")
                st.write(correction)

            st.session_state.responses.append([
                surah_name,
                ayah_num,
                user_mem,
                f"{score}%",
                user_tafsir,
                correction
            ])

        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(["السورة", "رقم الآية", "محاولة الحفظ", "تقييم الحفظ", "محاولة التفسير", "تقييم التفسير"])
        writer.writerows(st.session_state.responses)

        st.download_button(
            label="💾 تحميل النتيجة",
            data=csv_buffer.getvalue(),
            file_name="quran_review_results.csv",
            mime="text/csv"
        )
