import streamlit as st
import requests
from io import StringIO
import csv



# ----------------------------- Custom CSS Theme -----------------------------
st.markdown("""
<style>
body, .stApp {
    background-color: #F5F0E6;
    direction: rtl;
    font-family: 'Cairo', sans-serif;
}

.main-title {
    color: #2E7D32;
    font-size: 2.5rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    color: #555;
    font-size: 1.1rem;
    margin-bottom: 25px;
}

div.stButton > button {
    background-color: #388E3C !important;
    color: white !important;
    font-weight: bold !important;
    font-size: 1rem !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.3s ease;
}

div.stButton > button:hover {
    background-color: #1B5E20 !important;
    transform: scale(1.05);
}

.card {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
    border-right: 5px solid #2E7D32;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------- Surahs -----------------------------
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
    "الرحمن": 55, "الواقعة": 56, "الحديد": 57, "المجادلة": 58, "الحشر": 59, "الممتحنة": 60,
    "الصف": 61, "الجمعة": 62, "المنافقون": 63, "التغابن": 64, "الطلاق": 65, "التحريم": 66,
    "الملك": 67, "القلم": 68, "الحاقة": 69, "المعارج": 70, "نوح": 71, "الجن": 72,
    "المزّمّل": 73, "المدّثر": 74, "القيامة": 75, "الإنسان": 76, "المرسلات": 77, "النبأ": 78,
    "النازعات": 79, "عبس": 80, "التكوير": 81, "الإنفطار": 82, "المطفّفين": 83,
    "الإنشقاق": 84, "البروج": 85, "الطارق": 86, "الأعلى": 87, "الغاشية": 88,
    "الفجر": 89, "البلد": 90, "الشمس": 91, "الليل": 92, "الضحى": 93, "الشرح": 94,
    "التين": 95, "العلق": 96, "القدر": 97, "البينة": 98, "الزلزلة": 99, "العاديات": 100,
    "القارعة": 101, "التكاثر": 102, "العصر": 103, "الهمزة": 104, "الفيل": 105,
    "قريش": 106, "الماعون": 107, "الكوثر": 108, "الكافرون": 109, "النصر": 110,
    "المسد": 111, "الإخلاص": 112, "الفلق": 113, "الناس": 114
}

# ----------------------------- API Functions -----------------------------
def get_ayah_text(surah, ayah):
    url = f"https://api.quran.com/api/v4/quran/verses/uthmani?verse_key={surah}:{ayah}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()['verses'][0]['text_uthmani']
        except:
            return "⚠️ لم يتم العثور على نص الآية."
    else:
        return "❌ خطأ في الاتصال."

def get_tafsir(surah, ayah, tafsir_id=91):
    url = f"https://api.quran.com/api/v4/tafsirs/{tafsir_id}/by_ayah/{surah}:{ayah}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()['tafsir']['text']
        except:
            return "⚠️ لم يتم العثور على التفسير."
    else:
        return "❌ خطأ في الاتصال."

# ----------------------------- Main App -----------------------------
def app():
    st.markdown("<h1 class='main-title'>📖 رفيق القرآن: التفسير الميسر</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>🎯 اختر السورة والآية، وسنُظهر لك نص الآية وتفسيرها، مع إمكانية التحميل كملف CSV.</p>", unsafe_allow_html=True)

    surah_name = st.selectbox("🕌 اختر السورة", list(surahs.keys()))
    ayah_number = st.number_input("🔢 رقم الآية", min_value=1, value=1)

    if st.button("📚 عرض التفسير"):
        surah_num = surahs[surah_name]
        ayah_text = get_ayah_text(surah_num, ayah_number)
        tafsir = get_tafsir(surah_num, ayah_number)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"📖 <strong>نص الآية:</strong>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:28px; text-align:right'>{ayah_text}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"📗 <strong>التفسير:</strong>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:right'>{tafsir}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # CSV
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(["السورة", "رقم الآية", "نص الآية", "التفسير"])
        writer.writerow([surah_name, ayah_number, ayah_text, tafsir])

        st.download_button(
            label="💾 تحميل التفسير كـ CSV",
            data=csv_buffer.getvalue(),
            file_name=f"tafsir_{surah_name}_{ayah_number}.csv",
            mime="text/csv"
        )
