import streamlit as st

# إعداد صفحة ستريمليت مع عنوان وعرض واسع
st.set_page_config(page_title="رفيق القرآن", layout="wide")

# ألوان إسلامية دافئة
primary_color = "#1B512D"    # أخضر زيتوني غامق (السلام والبركة)
secondary_color = "#3A8669"  # أخضر فاتح (الهدوء)
accent_color = "#D4AF37"     # ذهبي دافئ (الفخامة)
background_color = "#F9F7F1" # بيج فاتح دافئ (النقاء)
text_color = "#2E2E2E"       # رمادي غامق للنصوص

# تخصيص الستايل CSS للألوان والخطوط
st.markdown(f"""
    <style>
        /* عام */
        .stApp {{
            background-color: {background_color};
            color: {text_color};
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        h1, h2, h3, h4 {{
            color: {primary_color};
            font-weight: 700;
            margin-bottom: 0.25em;
        }}
        /* Sidebar */
        .sidebar .sidebar-content {{
            background-color: white;
            padding: 30px 25px 40px 25px;
            border-radius: 20px;
            box-shadow: 0 0 20px rgb(26 90 34 / 0.15);
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .sidebar .stRadio > label {{
            color: {primary_color};
            font-weight: 700;
            font-size: 20px;
            margin-bottom: 8px;
        }}
        .sidebar .description {{
            font-size: 14px;
            color: {secondary_color};
            margin-top: -10px;
            margin-bottom: 20px;
            font-style: italic;
            text-align: center;
        }}
        /* روابط وأزرار */
        a, .stButton>button {{
            background-color: {secondary_color};
            color: white !important;
            border-radius: 12px;
            padding: 10px 22px;
            font-weight: 700;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease;
            box-shadow: 0 4px 10px rgb(58 134 105 / 0.3);
        }}
        a:hover, .stButton>button:hover {{
            background-color: {primary_color};
            box-shadow: 0 6px 12px rgb(26 90 34 / 0.5);
        }}
        /* صورة رأس القائمة الجانبية */
        .sidebar-img-top {{
            width: 85%;
            margin-bottom: 25px;
            border-radius: 16px;
            box-shadow: 0 8px 15px rgb(26 90 34 / 0.25);
            transition: transform 0.3s ease;
        }}
        .sidebar-img-top:hover {{
            transform: scale(1.05);
        }}
        /* صورة أسفل القائمة */
        .sidebar-img-bottom {{
            width: 65%;
            margin-top: auto;
            margin-bottom: 15px;
            border-radius: 12px;
            opacity: 0.8;
        }}
        /* الشعار والاقتباس */
        .slogan {{
            color: {accent_color};
            font-size: 28px;
            font-weight: 900;
            text-align: center;
            margin-bottom: 10px;
            direction: rtl;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        .quote {{
            font-size: 16px;
            font-style: italic;
            text-align: center;
            color: {secondary_color};
            margin-bottom: 40px;
            direction: rtl;
        }}
        .footer-comment {{
            font-size: 12px;
            color: {secondary_color};
            text-align: center;
            margin-top: 50px;
            font-style: italic;
            direction: rtl;
        }}
    </style>
""", unsafe_allow_html=True)

# قائمة الصفحات مع وصف بسيط لكل صفحة لتحسين تجربة المستخدم
pages = {
    "لوحة التحكم": "إحصائيات شاملة وتحكم كامل بالتطبيق",
    "الاستماع": "استمتع بتلاوات صوتية مميزة بجودة عالية",
    "مُخطط الحفظ": "خطط جدول الحفظ الخاص بك بشكل منظم وفعال",
    "مُساعد الحفظ (تكرار)": "أداة فعالة لمساعدتك على تكرار وحفظ الآيات",
    "تفسير": "فهم عميق لمعاني القرآن الكريم عبر التفسير الميسر",
    "لعبة المراجعة": "اختبر معلوماتك واذكر ما حفظته بطريقة ممتعة",
    "سؤال قرآنى": "اسأل أي سؤال يتعلق بالقرآن الكريم واحصل على إجابة"
}

# عنوان القائمة الجانبية مع صورة إسلامية بسم الله
st.sidebar.title("🕌 رفيق القرآن")
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Arabic_calligraphy_of_the_word_Bismillah.svg/1024px-Arabic_calligraphy_of_the_word_Bismillah.svg.png",
    use_column_width=True,
    clamp=True,
    output_format="PNG",
    class_="sidebar-img-top",
    caption="بسم الله الرحمن الرحيم"
)

# اختيار الصفحة مع عرض وصفها
page = st.sidebar.radio("اختر الصفحة:", list(pages.keys()))
st.sidebar.markdown(f'<div class="description">{pages[page]}</div>', unsafe_allow_html=True)

# صورة إسلامية روحية في أسفل القائمة الجانبية
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/Green_Mosque_Dome_-_Masjid_al-Nabawi.jpg/320px-Green_Mosque_Dome_-_Masjid_al-Nabawi.jpg",
    use_column_width=False,
    width=160,
    caption="المسجد النبوي الشريف",
    output_format="JPEG",
    class_="sidebar-img-bottom"
)

# عرض الشعار والاقتباس في بداية الصفحة (قبل استدعاء الصفحة)
st.markdown("""
    <div class="slogan">رفيق القرآن - معك في رحلتك الروحية مع كتاب الله</div>
    <div class="quote">"وَنَزَّلْنَا عَلَيْكَ الْكِتَابَ تِبْيَانًا لِكُلِّ شَيْءٍ" – سورة النحل: 89</div>
""", unsafe_allow_html=True)

# استيراد الصفحة المختارة وتشغيلها
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
