import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# ---------- إعداد الصفحة ----------
st.set_page_config(page_title="رفيق القرآن", layout="wide")

# ---------- الألوان والثيم ----------
primary_color = "#2E7D32"    # أخضر زيتوني غامق
secondary_color = "#009688"  # تركوازي
accent_color = "#FFC107"     # ذهبي دافئ
background_color = "#F3EFE5" # بيج كريمي فاتح

# ---------- تحميل صورة الهيدر ----------
image_url = "https://png.pngtree.com/png-clipart/20220223/original/pngtree-moslem-kid-read-quran-png-image_7311235.png"
response = requests.get(image_url)
header_image = Image.open(BytesIO(response.content))

# ---------- تنسيق مخصص ----------
st.markdown(f"""
    <style>
    .main-title {{
        color: {primary_color};
        font-size: 42px;
        font-weight: bold;
        text-align: center;
        margin-top: 20px;
    }}
    .quote {{
        font-size: 18px;
        color: {secondary_color};
        text-align: center;
        margin-bottom: 25px;
        font-style: italic;
    }}
    .header-container {{
        background-color: {primary_color};
        padding: 15px 30px;
        border-radius: 12px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
    }}
    .header-text {{
        color: white;
        font-size: 26px;
        font-weight: bold;
        margin-left: 20px;
    }}
    .section-divider {{
        border-top: 2px solid {accent_color};
        margin: 30px 0;
    }}
    .sidebar .sidebar-content {{
        background-color: #fff7e6;
        padding: 20px;
        border-radius: 10px;
    }}
    </style>
""", unsafe_allow_html=True)

# ---------- شريط علوي ----------
col1, col2 = st.columns([1, 8])
with col1:
    st.image(header_image, width=70)
with col2:
    st.markdown("""
    <div class="header-text">📖 رفيق القرآن</div>
    """, unsafe_allow_html=True)

# ---------- عنوان رئيسي واقتباس ----------
st.markdown('<div class="main-title">مرحباً بك في تطبيق رفيق القرآن 🌙</div>', unsafe_allow_html=True)
st.markdown('<div class="quote">"خيركم من تعلم القرآن وعلمه" – النبي محمد ﷺ</div>', unsafe_allow_html=True)

# ---------- تعريف الصفحات ----------
pages = {
    "لوحة التحكم": "ملخص شامل وإحصائيات التطبيق",
    "الاستماع": "استمع إلى التلاوات الصوتية",
    "مُخطط الحفظ": "خطط جدول حفظك بطريقة منظمة",
    "مُساعد الحفظ (تكرار)": "ساعد نفسك بالتكرار والتركيز",
    "تفسير": "فهم معاني القرآن الكريم",
    "لعبة المراجعة": "اختبر معلوماتك في مراجعة ممتعة",
    "سؤال قرآنى": "اسأل أي سؤال عن القرآن واستفد"
}

# ---------- القائمة الجانبية ----------
st.sidebar.title("📌 القائمة الرئيسية")
page = st.sidebar.radio("اختر الصفحة:", list(pages.keys()))

# وصف مختصر تحت الاختيار الحالي
for p, desc in pages.items():
    if p == page:
        st.sidebar.markdown(f'<span style="color:{secondary_color}; font-size:13px;">{desc}</span>', unsafe_allow_html=True)
        break

# ---------- فاصل مرئي ----------
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ---------- تحميل الصفحة المختارة ----------
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
