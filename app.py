import streamlit as st
import random

# إعداد صفحة ستريمليت
st.set_page_config(
    page_title="رفيق القرآن",
    layout="wide",
    icon="https://cdn-icons-png.flaticon.com/512/4358/4358773.png"
)

# ألوان روحانية
theme = {
    "primary": "#2E7D32",      # أخضر زيتوني غامق
    "secondary": "#009688",    # تركوازي
    "accent": "#FFC107",       # ذهبي دافئ
    "background": "#EDE7D9"    # خلفية بيج دافئة
}

# اقتباسات يومية من القرآن
daily_ayahs = [
    "إِنَّ مَعَ الْعُسْرِ يُسْرًا ﴿٦﴾ - الشرح",
    "وَقُل رَّبِّ زِدْنِي عِلْمًا ﴿١١٤﴾ - طه",
    "إِنَّ اللَّهَ مَعَ الصَّابِرِينَ ﴿١٥٣﴾ - البقرة",
    "فَاذْكُرُونِي أَذْكُرْكُمْ ﴿١٥٢﴾ - البقرة"
]

# تعريف الصفحات
pages = {
    "🏠 الرئيسية": None,
    "📊 لوحة التحكم": "safahat.dash_01",
    "🎧 الاستماع": "safahat.estimaa_02",
    "🗓️ مُخطط الحفظ": "safahat.hifz_planner_03",
    "🔁 مُساعد الحفظ": "safahat.hifz_helper_04",
    "📖 تفسير": "safahat.tafsir_05",
    "🧠 لعبة المراجعة": "safahat.moraj3a",
    "❓ سؤال قرآنى": "safahat.ask_quran"
}

# إدراج CSS للتنسيق
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
            margin: 20px 0 10px;
        }}
        .quote {{
            font-size: 18px;
            color: {theme['secondary']};
            text-align: center;
            margin-bottom: 30px;
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
            padding: 12px 5px;
            border-top: 3px solid {theme['accent']};
            z-index: 999;
        }}
        .bottom-nav a {{
            color: white;
            margin: 0 15px;
            text-decoration: none;
            font-weight: bold;
            font-size: 14px;
        }}
        .bottom-nav a:hover {{
            color: {theme['accent']};
        }}
        .centered-image {{
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-top: 10px;
        }}
        .centered-image img {{
            width: 240px;
            border-radius: 20px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
        }}
        hr {{
            border: none;
            border-top: 2px solid {theme['secondary']};
            margin: 25px 0;
        }}
    </style>
""", unsafe_allow_html=True)

# ✅ الشريط العلوي
st.markdown(f"""
<div class="header-bar">
    <div class="header-title">📖 رفيق القرآن</div>
    <div class="quick-links">
        <a href="#الرئيسية">الرئيسية</a>
        <a href="#مقتطف">مقتطف</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ✅ عنوان ترحيبي وصورة واحدة
st.markdown('<div class="main-title" id="الرئيسية">خيركم من تعلم القرآن وعلمه ✨</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="centered-image">
    <img src="https://png.pngtree.com/png-clipart/20220223/original/pngtree-moslem-kid-read-quran-png-image_7311235.png" alt="Quran Kid">
</div>
""", unsafe_allow_html=True)

# ✅ مقتطف قرآني
st.markdown(f'<div class="quote" id="مقتطف">🌟 مقتطف اليوم: {random.choice(daily_ayahs)}</div>', unsafe_allow_html=True)

st.markdown("<hr />", unsafe_allow_html=True)

# ✅ استيراد الصفحات
page_names = list(pages.keys())
selected_page = st.selectbox("⬇️ اختر صفحة:", page_names, index=0)

if pages[selected_page]:
    module_path = pages[selected_page]
    exec(f"import {module_path} as page_module; page_module.app()")

# ✅ شريط التنقل السفلي
st.markdown(f"""
<div class="bottom-nav">
    {"".join([f'<a href="?selected_page={name}">{name}</a>' for name in page_names])}
</div>
""", unsafe_allow_html=True)
