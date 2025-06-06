import streamlit as st

# إعداد صفحة ستريمليت
st.set_page_config(page_title="رفيق القرآن", layout="wide")

# ألوان إسلامية وروحانية
primary_color = "#2E7D32"    # أخضر زيتوني غامق (السلام والبركة)
secondary_color = "#009688"  # تركوازي هادي (الصفاء)
accent_color = "#FFC107"     # ذهبي دافئ (الفخامة)
background_color = "#FAF3E0" # بيج فاتح كريمي (النقاء)

# تخصيص الستايل (CSS) بالألوان المختارة
st.markdown(f"""
    <style>
        .sidebar .sidebar-content {{
            background-color: {background_color};
            padding: 20px 15px 30px 15px;
            border-radius: 12px;
        }}
        .sidebar .stRadio > label {{
            color: {primary_color};
            font-weight: 700;
            font-size: 18px;
            margin-bottom: 0px;
        }}
        .sidebar .description {{
            font-size: 13px;
            color: {secondary_color};
            margin-top: -8px;
            margin-bottom: 15px;
            padding-left: 10px;
            font-style: italic;
        }}
        .stApp {{
            background-color: #ffffff;
            color: {primary_color};
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        h1 {{
            color: {accent_color};
            font-weight: 800;
            margin-bottom: 10px;
        }}
        a, .stButton>button {{
            background-color: {secondary_color};
            color: white !important;
            border-radius: 8px;
            padding: 8px 18px;
            font-weight: 700;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }}
        a:hover, .stButton>button:hover {{
            background-color: {primary_color};
        }}
    </style>
""", unsafe_allow_html=True)

# قائمة الصفحات مع وصف بسيط لكل صفحة لتحسين تجربة المستخدم
pages = {
    "لوحة التحكم": "ملخص شامل وإحصائيات التطبيق",
    "الاستماع": "استمع إلى التلاوات الصوتية",
    "مُخطط الحفظ": "خطط جدول حفظك بطريقة منظمة",
    "مُساعد الحفظ (تكرار)": "ساعد نفسك بالتكرار والتركيز",
    "تفسير": "فهم معاني القرآن الكريم",
    "لعبة المراجعة": "اختبر معلوماتك في مراجعة ممتعة",
    "سؤال قرآنى": "اسأل أي سؤال عن القرآن واستفد"
}

st.sidebar.title("القائمة الرئيسية")
page = st.sidebar.radio("اختر الصفحة:", list(pages.keys()))

# عرض وصف صغير تحت كل اختيار في القائمة الجانبية
for p, desc in pages.items():
    if p == page:
        st.sidebar.markdown(f'<div class="description">{desc}</div>', unsafe_allow_html=True)
        break

# عرض الصفحة المختارة
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
