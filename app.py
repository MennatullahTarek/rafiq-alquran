import streamlit as st
import random

# إعداد صفحة ستريمليت
st.set_page_config(page_title="رفيق القرآن", layout="wide", icon="🕌")

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

# الصفحات
pages = {
    "لوحة التحكم": "📊",
    "الاستماع": "🎧",
    "مُخطط الحفظ": "🗓️",
    "مُساعد الحفظ (تكرار)": "🔁",
    "تفسير": "📘",
    "لعبة المراجعة": "🧠",
    "سؤال قرآنى": "❓"
}

# إدراج CSS مخصص
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
        .hero-img {{
            display: flex;
            justify-content: center;
            margin: 30px auto;
        }}
        .hero-img img {{
            width: 300px;
            max-width: 90%;
            border-radius: 20px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.25);
            transition: transform 0.3s ease;
        }}
        .hero-img img:hover {{
            transform: scale(1.05);
        }}
    </style>
""", unsafe_allow_html=True)

# 🔝 الشريط العلوي
st.markdown(f"""
<div class="header-bar">
    <div class="header-title">📖 رفيق القرآن</div>
    <div class="quick-links">
        <a href="#الرئيسية">🏠 الرئيسية</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ✨ عنوان رئيسي
st.markdown('<div class="main-title" id="الرئيسية">مرحباً بك في تطبيق رفيق القرآن 🌙</div>', unsafe_allow_html=True)

# 💡 اقتباس
st.markdown('<div class="quote">"خيركم من تعلم القرآن وعلمه" – النبي محمد ﷺ</div>', unsafe_allow_html=True)

# ✅ صورة منمقة (Hero Image)
st.markdown("""
<div class="hero-img">
    <img src="https://png.pngtree.com/png-clipart/20220223/original/pngtree-moslem-kid-read-quran-png-image_7311235.png" alt="Quran Kid">
</div>
""", unsafe_allow_html=True)

# 📌 مقتطف يومي
st.markdown(f'<div class="quote" id="مقتطف">🌟 مقتطف اليوم: {random.choice(daily_ayahs)}</div>', unsafe_allow_html=True)

# 🔹 فاصل جمالي
st.markdown("<hr />", unsafe_allow_html=True)

# ✅ تحميل الصفحة المناسبة حسب التنقل
if "page" not in st.session_state:
    st.session_state.page = list(pages.keys())[0]

clicked_page = st.session_state.page

if clicked_page == "لوحة التحكم":
    import safahat.dash_01 as dash
    dash.app()
elif clicked_page == "الاستماع":
    import safahat.estimaa_02 as estimaa
    estimaa.app()
elif clicked_page == "مُخطط الحفظ":
    import safahat.hifz_planner_03 as hifz
    hifz.app()
elif clicked_page == "مُساعد الحفظ (تكرار)":
    import safahat.hifz_helper_04 as helper
    helper.app()
elif clicked_page == "تفسير":
    import safahat.tafsir_05 as tafsir
    tafsir.app()
elif clicked_page == "لعبة المراجعة":
    import safahat.moraj3a as memory
    memory.app()
elif clicked_page == "سؤال قرآنى":
    import safahat.ask_quran as ask
    ask.app()

# ✅ شريط سفلي للتنقل
nav_links = ''.join([
    f'<a href="#" onclick="window.location.reload()">{emoji} {name}</a>'
    for name, emoji in pages.items()
])
st.markdown(f"""
<div class="bottom-nav">
    {nav_links}
</div>
""", unsafe_allow_html=True)
