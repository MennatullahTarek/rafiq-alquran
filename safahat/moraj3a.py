import nest_asyncio
nest_asyncio.apply()

import streamlit as st
import requests
import difflib
import re
import csv
from io import StringIO

# --- تنسيقات CSS ---
def apply_custom_styles():
    st.markdown("""
        <style>
            .stApp {
                background-color: #f7fdf9;
                font-family: 'Arial', sans-serif;
            }
            h1, h2, h3 {
                color: #2e7d32;
            }
            .ayah-box {
                background-color: #ffffff;
                border-left: 5px solid #2e7d32;
                padding: 1.2rem;
                margin-bottom: 1.5rem;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            }
            .stButton > button {
                background-color: #2e7d32;
                color: white;
                font-size: 1rem;
                padding: 0.5rem 1.2rem;
                border-radius: 8px;
                border: none;
                transition: all 0.3s ease;
            }
            .stButton > button:hover {
                background-color: #1b5e20;
                transform: scale(1.03);
            }
            .stDownloadButton > button {
                background-color: #388E3C;
                color: white;
                font-size: 1rem;
                border-radius: 8px;
                padding: 0.4rem 1rem;
                border: 2px solid #2E7D32;
                transition: all 0.3s ease;
                font-weight: bold;
            }
            .stDownloadButton > button:hover {
                background-color: #1B5E20;
                border-color: #1B5E20;
                transform: scale(1.03);
            }
            .st-success, .st-info {
                font-weight: bold;
            }
            textarea {
                background-color: #f0fdf4;
            }
        </style>
    """, unsafe_allow_html=True)

# --- Agent: Text Processor ---
class TextProcessor:
    @staticmethod
    def strip_tashkeel(text):
        return re.sub(r'[\u064B-\u0652]', '', text)

    @staticmethod
    def compare_ayah(user_input, actual_text):
        actual_clean = TextProcessor.strip_tashkeel(actual_text.replace('\n', '').strip())
        user_clean = TextProcessor.strip_tashkeel(user_input.replace('\n', '').strip())
        similarity_ratio = difflib.SequenceMatcher(None, actual_clean, user_clean).ratio()
        return round(similarity_ratio * 100, 2)

# --- Agent: Ayah Fetcher ---
class AyahFetcher:
    @staticmethod
    def get_ayah_text(surah_id, ayah_number):
        url = f"https://api.quran.com/api/v4/quran/verses/uthmani?verse_key={surah_id}:{ayah_number}"
        response = requests.get(url)
        if response.status_code == 200:
            try:
                return response.json()['verses'][0]['text_uthmani']
            except (KeyError, IndexError):
                return "⚠️ لم يتم العثور على نص الآية."
        return "❌ فشل الاتصال بجلب الآية."

# --- Agent: Tafsir Fetcher ---
class TafsirFetcher:
    @staticmethod
    def get_tafsir(surah_id, ayah_number, tafsir_id=91):
        url = f"https://api.quran.com/api/v4/tafsirs/{tafsir_id}/by_ayah/{surah_id}:{ayah_number}"
        response = requests.get(url)
        if response.status_code == 200:
            try:
                return response.json()['tafsir']['text']
            except (KeyError, TypeError):
                return "⚠️ لم يتم العثور على التفسير."
        return "❌ فشل الاتصال بجلب التفسير."

# --- جلب سور القرآن ---
def get_surahs():
    return {
        # (تم اختصارها هنا للحجم، أكمل باقي السور كما في نسختك الأصلية)
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
        "الناس": 114
    }

# --- تقييم مبسط للتفسير ---
def simple_tafsir_evaluation(user_tafsir, actual_tafsir):
    if not user_tafsir.strip():
        return "❌ لم تقم بإدخال تفسير."
    elif len(user_tafsir.strip().split()) < 5:
        return "🔸 التفسير قصير جدًا. حاول التوضيح أكثر. التقييم: 3/10"
    elif any(word in actual_tafsir for word in user_tafsir.strip().split()):
        return "✅ جيد، التفسير يحتوي على كلمات من التفسير الرسمي. التقييم: 7/10"
    else:
        return "❌ التفسير غير واضح أو لا يتطابق مع التفسير الرسمي. التقييم: 4/10"

# --- التطبيق الرئيسي ---
def app():
    apply_custom_styles()

    st.title("📖 رفيق القرآن - مراجعة وحفظ وتفسير")

    ayah_fetcher = AyahFetcher()
    tafsir_fetcher = TafsirFetcher()
    text_processor = TextProcessor()
    surahs = get_surahs()

    if 'started' not in st.session_state:
        st.session_state.started = False

    if not st.session_state.started:
        surah_name = st.selectbox("اختر السورة", ["اختر السورة..."] + list(surahs.keys()))
        if surah_name == "اختر السورة...":
            st.stop()

        st.session_state.surah_name = surah_name
        st.session_state.surah_id = surahs[surah_name]

        st.session_state.start_ayah = st.number_input("من الآية رقم", min_value=1, value=1, key="start")
        st.session_state.end_ayah = st.number_input("إلى الآية رقم", min_value=st.session_state.start_ayah,
                                                   value=st.session_state.start_ayah, key="end")

        if st.button("✅ ابدأ الإختبار"):
            st.session_state.started = True
            st.rerun()

    else:
        responses = []

        for ayah_num in range(st.session_state.start_ayah, st.session_state.end_ayah + 1):
            st.markdown(f"""<div class="ayah-box"><h3>الآية {ayah_num}</h3>""", unsafe_allow_html=True)

            actual_ayah = ayah_fetcher.get_ayah_text(st.session_state.surah_id, ayah_num)
            tafsir_text = tafsir_fetcher.get_tafsir(st.session_state.surah_id, ayah_num)

            words = actual_ayah.split()
            prompt_prefix = " ".join(words[:2]) if len(words) > 2 else actual_ayah

            st.markdown(f"### اختبار الحفظ\nأكمل بعد: **{prompt_prefix}...**")
            user_input = st.text_area("أكمل الآية:", key=f"mem_{ayah_num}")

            if user_input.strip():
                full_input = prompt_prefix + " " + user_input.strip()
                score = text_processor.compare_ayah(full_input, actual_ayah)
                st.success(f"✅ تقييم الحفظ: **{score}%**")
            else:
                score = "-"

            st.markdown("### التفسير")
            user_tafsir = st.text_area("اشرح معنى الآية أو الكلمات:", key=f"tafsir_{ayah_num}")
            tafsir_eval = simple_tafsir_evaluation(user_tafsir, tafsir_text)
            st.info(f"🧾 تقييم التفسير: {tafsir_eval}")

            responses.append([
                st.session_state.surah_name,
                ayah_num,
                user_input,
                f"{score}%" if isinstance(score, (int, float)) else score,
                user_tafsir,
                tafsir_eval
            ])

            st.markdown("</div>", unsafe_allow_html=True)

        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(["السورة", "رقم الآية", "محاولة الحفظ", "تقييم الحفظ", "محاولة التفسير", "تقييم التفسير"])
        writer.writerows(responses)

        st.download_button(
            label="💾 تحميل النتيجة كملف CSV",
            data=csv_buffer.getvalue().encode('utf-8-sig'),
            file_name="نتائج_مراجعة_القرآن.csv",
            mime="text/csv"
        )

        if st.button("🔁 ابدأ من جديد"):
            st.session_state.started = False
            st.rerun()

if __name__ == "__main__":
    app()
