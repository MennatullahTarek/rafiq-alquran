import streamlit as st
import random

# إعداد صفحة ستريمليت
st.set_page_config(page_title="رفيق القرآن", layout="wide")

# ألوان روحانية
theme = {
    "primary": "#2E7D32",      # أخضر زيتوني غامق
    "secondary": "#009688",    # تركوازي
    "accent": "#FFC107",       # ذهبي دافئ
    "background": "#EDE7D9"    # خلفية بيج غامقة قليلاً
}

# اقتباسات يومية من القرآن
daily_ayahs = [
    "إِنَّ مَعَ الْعُسْرِ يُسْرًا ﴿٦﴾ - الشرح",
    "وَقُل رَّبِّ زِدْنِي عِلْمًا ﴿١١٤﴾ - طه",
    "إِنَّ اللَّهَ مَعَ الصَّابِرِينَ ﴿١٥٣﴾ - البقرة",
    "فَاذْكُرُونِي أَذْكُرْكُمْ ﴿١٥٢﴾ - البقرة"
]

# إدراج CSS لتخصيص الخلفية والثيم
st.markdown(f"""
    <style>
        .stApp {{
            background-color: {theme['background']};
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        .main-title {{
            color: {theme['primary']};
            font-size: 42px;
            font-weight: bold;
            text-align: center;
            margin-top: 10px;
        }}
        .quote {{
            font-size: 18px;
            color: {theme['secondary']};
            text-align: center;
            margin-bottom: 25px;
            font-style: italic;
        }}
        .header-bar {{
            background-color: {theme['primary']};
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: white;
            border-bottom: 4px solid {theme['accent']};
        }}
        .header-title {{
            font-size: 26px;
            font-weight: bold;
        }}
        .quick-links a {{
            color: white;
            margin-left: 25px;
            text-decoration: none;
            font-weight: 500;
        }}
        .quick-links a:hover {{
            text-decoration: underline;
            color: {theme['accent']};
        }}
        .bottom-nav {{
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: {theme['primary']};
            display: flex;
            justify-content: center;
            padding: 10px;
            border-top: 2px solid {theme['accent']};
            z-index: 100;
        }}
        .bottom-nav a {{
            color: white;
            margin: 0 15px;
            text-decoration: none;
            font-weight: bold;
        }}
        .bottom-nav a:hover {{
            color: {theme['accent']};
        }}
        hr {{
            border: none;
            border-top: 2px solid {theme['secondary']};
            margin: 20px 0;
        }}
        .image-row {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin: 20px 0;
        }}
        .image-row img {{
            width: 150px;
            border-radius: 12px;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
        }}
    </style>
""", unsafe_allow_html=True)

# 🔝 الشريط العلوي
st.markdown(f"""
<div class="header-bar">
    <div class="header-title">📖 رفيق القرآن</div>
    <div class="quick-links">
        <a href="#الرئيسية">🏠 الرئيسية</a>
        <a href="#مقتطف">📜 مقتطف</a>
        <a href="#القائمة">📚 دروس</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ✅ صورة رأسية وصور إضافية
st.markdown("""
<div class="image-row">
    <img src="https://png.pngtree.com/png-clipart/20220223/original/pngtree-moslem-kid-read-quran-png-image_7311235.png" alt="Quran Kid">
    <img src="https://img.freepik.com/free-vector/flat-ramadan-background_23-2149274996.jpg" alt="Ramadan">
    <img src="https://img.freepik.com/free-vector/gradient-islamic-background_23-2149247122.jpg" alt="Islamic">
</div>
""", unsafe_allow_html=True)

# ✨ عنوان رئيسي
st.markdown('<div class="main-title" id="الرئيسية">مرحباً بك في تطبيق رفيق القرآن 🌙</div>', unsafe_allow_html=True)

# ✅ مقتطف يومي من القرآن
st.markdown(f'<div class="quote" id="مقتطف">🌟 مقتطف اليوم: {random.choice(daily_ayahs)}</div>', unsafe_allow_html=True)

st.markdown("<hr />", unsafe_allow_html=True)

# ✅ تعريف الصفحات
pages = {
    "لوحة التحكم": "ملخص شامل وإحصائيات التطبيق",
    "الاستماع": "استمع إلى التلاوات الصوتية",
    "مُخطط الحفظ": "خطط جدول حفظك بطريقة منظمة",
    "مُساعد الحفظ (تكرار)": "ساعد نفسك بالتكرار والتركيز",
    "تفسير": "فهم معاني القرآن الكريم",
    "لعبة المراجعة": "اختبر معلوماتك في مراجعة ممتعة",
    "سؤال قرآنى": "اسأل أي سؤال عن القرآن واستفد"
}

# ✅ القائمة الجانبية
st.sidebar.title("📌 القائمة الرئيسية")
page = st.sidebar.radio("اختر الصفحة:", list(pages.keys()))

# وصف مختصر تحت الاختيار الحالي
for p, desc in pages.items():
    if p == page:
        st.sidebar.markdown(f'<span style="color:{theme['secondary']}; font-size:13px;">{desc}</span>', unsafe_allow_html=True)
        break

st.markdown("<hr />", unsafe_allow_html=True)

# ✅ تحميل وتشغيل الصفحة المناسبة
if page == "لوحة التحكم":
    import safahat.dash_01 as dash
    dash.app()
elif page == "الاستماع":
    import safahat.estimaa_02 as estimaa
    estimaa.app()
elif page == "مُخطط الحفظ":
    import safahat.hifz_planner_03 as hifz
    hifz.app()
elif page == "مُساعد الحفظ (تكرار)":
    import safahat.hifz_helper_04 as helper
    helper.app()
elif page == "تفسير":
    import safahat.tafsir_05 as tafsir
    tafsir.app()
elif page == "لعبة المراجعة":
    import safahat.moraj3a as memory
    memory.app()
elif page == "سؤال قرآنى":
    import safahat.ask_quran as ask
    ask.app()

# ✅ شريط سفلي للتنقل
st.markdown(f"""
<div class="bottom-nav">
    {''.join([f'<a href="#" onclick="window.location.reload()">{p}</a>' for p in pages])}
</div>
""", unsafe_allow_html=True)
