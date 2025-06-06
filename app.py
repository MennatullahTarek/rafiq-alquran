import streamlit as st

# إعداد صفحة ستريمليت
st.set_page_config(page_title="رفيق القرآن", layout="wide")

# ألوان إسلامية وروحانية
primary_color = "#2E7D32"    # أخضر زيتوني غامق (السلام والبركة)
secondary_color = "#009688"  # تركوازي هادي (الصفاء)
accent_color = "#FFC107"     # ذهبي دافئ (الفخامة)
background_color = "#FAF3E0" # بيج فاتح كريمي (النقاء)

# تخصيص الستايل (CSS) بالألوان المختارة والصور الإسلامية
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

# شعار وجملة تحفيزية في الأعلى
st.markdown("""
    <div style='text-align: center; margin-top: -30px;'>
        <img src='https://i.ibb.co/4JK93Fj/quran-light.png' width='90' style='margin-bottom: 10px;' />
        <h1>🌙 رفيق القرآن</h1>
        <p style='color: #666; font-size: 17px;'>دليلك اليومي لحفظ، فهم، وتدبر آيات الله 💖</p>
        <hr style='border: 1px solid #ccc; width: 70%; margin: auto;'>
    </div>
""", unsafe_allow_html=True)

# قائمة الصفحات مع وصف بسيط لكل صفحة لتحسين تجربة المستخدم
pages = {
    "لوحة التحكم": "ملخص شامل وإحصائيات التقدم في رحلتك القرآنية.",
    "الاستماع": "استمع إلى تلاوات مؤثرة من كبار القراء.",
    "مُخطط الحفظ": "نظم جدولك لحفظ القرآن الكريم بكل سهولة.",
    "مُساعد الحفظ (تكرار)": "أداة لمساعدتك على التكرار والتثبيت.",
    "تفسير": "تدبر وتفهم معاني الآيات بطريقة مبسطة.",
    "لعبة المراجعة": "اختبر ذاكرتك مع ألعاب مراجعة ممتعة.",
    "سؤال قرآنى": "اطرح أي سؤال عن سور القرآن واحصل على إجابة مدعومة."
}

st.sidebar.title("📚 القائمة الرئيسية")
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
