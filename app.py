import streamlit as st
from PIL import Image

# -------------------- Page Configuration --------------------
st.set_page_config(page_title="رفيق القرآن", layout="wide")

# -------------------- Theme Colors --------------------
primary_color = "#2E7D32"    # Olive Green (spiritual peace)
secondary_color = "#009688"  # Turquoise (calm)
accent_color = "#FFC107"     # Warm Gold (luxury)
background_color = "#F3EFE5" # Light Cream Beige (purity)

# -------------------- Background & Styling --------------------
background_image_url = "https://png.pngtree.com/png-clipart/20220223/original/pngtree-moslem-kid-read-quran-png-image_7311235.png"
st.markdown(f"""
    <style>
        .stApp {{
            background-color: {background_color};
            background-image: url('{background_image_url}');
            background-size: 180px;
            background-position: bottom left;
            background-repeat: no-repeat;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        .main-title {{
            color: {primary_color};
            font-size: 40px;
            font-weight: bold;
            text-align: center;
            margin-top: 20px;
        }}
        .quote {{
            font-size: 18px;
            color: {secondary_color};
            text-align: center;
            margin-bottom: 30px;
            font-style: italic;
        }}
        .header-bar {{
            background-color: {primary_color};
            padding: 12px 25px;
            border-bottom: 3px solid {accent_color};
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: white;
            position: fixed;
            top: 0;
            width: 100%;
            z-index: 999;
        }}
        .header-title {{
            font-size: 22px;
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
            color: {accent_color};
        }}
        .block-container {{
            padding-top: 100px !important;
        }}
        .sidebar .sidebar-content {{
            padding-top: 30px;
        }}
    </style>
""", unsafe_allow_html=True)

# -------------------- Header --------------------
st.markdown("""
<div class="header-bar">
    <div class="header-title">📖 رفيق القرآن</div>
    <div class="quick-links">
        <a href="#">🏠 الرئيسية</a>
        <a href="#sidebar">📚 القائمة</a>
        <a href="#footer">🕋 تواصل</a>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------- Welcome & Quote --------------------
st.markdown('<div class="main-title">مرحباً بك في تطبيق رفيق القرآن 🌙</div>', unsafe_allow_html=True)
st.markdown('<div class="quote">"خيركم من تعلم القرآن وعلمه" – النبي محمد ﷺ</div>', unsafe_allow_html=True)

# -------------------- Sidebar --------------------
pages = {
    "لوحة التحكم": "ملخص شامل وإحصائيات التطبيق",
    "الاستماع": "استمع إلى التلاوات الصوتية",
    "مُخطط الحفظ": "خطط جدول حفظك بطريقة منظمة",
    "مُساعد الحفظ (تكرار)": "ساعد نفسك بالتكرار والتركيز",
    "تفسير": "فهم معاني القرآن الكريم",
    "لعبة المراجعة": "اختبر معلوماتك في مراجعة ممتعة",
    "سؤال قرآنى": "اسأل أي سؤال عن القرآن واستفد"
}

st.sidebar.title("📌 القائمة الرئيسية")
page = st.sidebar.radio("اختر الصفحة:", list(pages.keys()))

for p, desc in pages.items():
    if p == page:
        st.sidebar.markdown(f'<span style="color:{secondary_color}; font-size:13px;">{desc}</span>', unsafe_allow_html=True)
        break

# -------------------- Page Loading --------------------
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

# -------------------- Footer --------------------
st.markdown("""
<hr style="border: none; border-top: 1px solid #ccc; margin: 50px 0 10px;"/>
<div id="footer" style="text-align:center; font-size: 13px; color: #666;">
    تم التطوير بواسطة فريق <strong>رفيق القرآن</strong> © 2025
</div>
""", unsafe_allow_html=True)
