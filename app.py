import streamlit as st

st.set_page_config(page_title="رفيق القرآن", layout="wide")

primary_color = "#2E7D32"    # أخضر زيتوني غامق
secondary_color = "#009688"  # تركوازي
accent_color = "#FFC107"     # ذهبي
background_color = "#FAF3E0" # بيج فاتح

st.markdown(f"""
    <style>
        .sidebar .sidebar-content {{
            background-color: {background_color};
            padding: 20px 15px 30px 15px;
            border-radius: 12px;
            display: flex;
            flex-direction: column;
            align-items: center;
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
            align-self: flex-start;
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
        /* صور في السايدبار */
        .sidebar-img-top {{
            width: 80%;
            border-radius: 15px;
            margin-bottom: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        .sidebar-img-top:hover {{
            transform: scale(1.05);
        }}
        .sidebar-img-bottom {{
            width: 60%;
            margin-top: auto;
            margin-bottom: 10px;
            opacity: 0.7;
        }}
    </style>
""", unsafe_allow_html=True)

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

# صورة إسلامية في أعلى الشريط الجانبي (رابط لصورة مجانية)
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Arabic_calligraphy_of_the_word_Bismillah.svg/2560px-Arabic_calligraphy_of_the_word_Bismillah.svg.png",
    use_column_width=True,
    clamp=True,
    caption="بسم الله الرحمن الرحيم",
    output_format="PNG",
    class_="sidebar-img-top"
)

page = st.sidebar.radio("اختر الصفحة:", list(pages.keys()))

for p, desc in pages.items():
    if p == page:
        st.sidebar.markdown(f'<div class="description">{desc}</div>', unsafe_allow_html=True)
        break

# صورة إسلامية صغيرة في أسفل الشريط الجانبي
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/Green_Mosque_Dome_-_Masjid_al-Nabawi.jpg/320px-Green_Mosque_Dome_-_Masjid_al-Nabawi.jpg",
    use_column_width=False,
    width=150,
    caption="المسجد النبوي الشريف",
    output_format="JPEG",
    class_="sidebar-img-bottom"
)

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
