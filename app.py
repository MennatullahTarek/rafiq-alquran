import streamlit as st
from PIL import Image
import base64

# إعداد الصفحة
st.set_page_config(page_title="رفيق القرآن", layout="wide")

# ألوان روحانية
primary_color = "#2E7D32"    # أخضر زيتوني غامق
secondary_color = "#009688"  # تركوازي
accent_color = "#FFC107"     # ذهبي دافئ
background_color = "#F3EFE5" # بيج كريمي فاتح

# إدراج CSS لتخصيص الخلفية والثيم
background_image_url = "https://png.pngtree.com/png-clipart/20220223/original/pngtree-moslem-kid-read-quran-png-image_7311235.png"
st.markdown(f"""
    <style>
        .stApp {{
            background-color: {background_color};
            background-image: url('{background_image_url}');
            background-size: 200px;
            background-position: bottom left;
            background-repeat: no-repeat;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        .main-title {{
            color: {primary_color};
            font-size: 42px;
            font-weight: bold;
            text-align: center;
            margin-top: 10px;
        }}
        .quote {{
            font-size: 18px;
            color: {secondary_color};
            text-align: center;
            margin-bottom: 25px;
            font-style: italic;
        }}
        .header-bar {{
            background-color: {primary_color};
            padding: 10px 20px;
            border-bottom: 3px solid {accent_color};
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: white;
        }}
        .header-title {{
            font-size: 24px;
            font-weight: bold;
        }}
        .quick-links a {{
            color: white;
            margin-left: 20px;
            text-decoration: none;
            font-weight: 500;
        }}
        .quick-links a:hover {{
            text-decoration: underline;
            color: {accent_color};
        }}
    </style>
""", unsafe_allow_html=True)

# شريط علوي ثابت
st.markdown("""
<div class="header-bar">
    <div class="header-title">📖 رفيق القرآن</div>
    <div class="quick-links">
        <a href="#" onclick="window.scrollTo(0, 0)">🏠 الرئيسية</a>
        <a href="#sidebar">📚 القائمة</a>
        <a href="#" onclick="window.scrollTo(0, document.body.scrollHeight)">🕋 تواصل</a>
    </div>
</div>
""", unsafe_allow_html=True)

# عنوان رئيسي واقتباس
st.markdown('<div class="main-title">مرحباً بك في تطبيق رفيق القرآن 🌙</div>', unsafe_allow_html=True)
st.markdown('<div class="quote">"خيركم من تعلم القرآن وعلمه" – النبي محمد ﷺ</div>', unsafe_allow_html=True)

# تعريف الصفحات
pages = {
    "لوحة التحكم": "ملخص شامل وإحصائيات التطبيق",
    "الاستماع": "استمع إلى التلاوات الصوتية",
    "مُخطط الحفظ": "خطط جدول حفظك بطريقة منظمة",
    "مُساعد الحفظ (تكرار)": "ساعد نفسك بالتكرار والتركيز",
    "تفسير": "فهم معاني القرآن الكريم",
    "لعبة المراجعة": "اختبر معلوماتك في مراجعة ممتعة",
    "سؤال قرآنى": "اسأل أي سؤال عن القرآن واستفد"
}

# القائمة الجانبية
st.sidebar.title("📌 القائمة الرئيسية")
page = st.sidebar.radio("اختر الصفحة:", list(pages.keys()))

# وصف مختصر تحت الاختيار الحالي
for p, desc in pages.items():
    if p == page:
        st.sidebar.markdown(f'<span style="color:{secondary_color}; font-size:13px;">{desc}</span>', unsafe_allow_html=True)
        break

# تحميل وتشغيل الصفحة المناسبة
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
