import streamlit as st
import random

# إعداد الصفحة (مع تحديد أيقونة صحيحة)
st.set_page_config(
    page_title="رفيق القرآن",
    layout="wide",
    page_icon="https://cdn-icons-png.flaticon.com/512/4358/4358773.png"
)

# ألوان روحانية
theme = {
    "primary": "#2E7D32",
    "secondary": "#009688",
    "accent": "#FFC107",
    "background": "#EDE7D9"
}

# مقتطفات يومية
daily_ayahs = [
    "إِنَّ مَعَ الْعُسْرِ يُسْرًا ﴿٦﴾ - الشرح",
    "وَقُل رَّبِّ زِدْنِي عِلْمًا ﴿١١٤﴾ - طه",
    "إِنَّ اللَّهَ مَعَ الصَّابِرِينَ ﴿١٥٣﴾ - البقرة",
    "فَاذْكُرُونِي أَذْكُرْكُمْ ﴿١٥٢﴾ - البقرة"
]

# صفحات التطبيق
pages = {
    "🏠 الرئيسية": None,
    "📊 لوحة التحكم":  "safahat.dash_01",
    "🎧 الاستماع":       "safahat.estimaa_02",
    "🗓️ مُخطط الحفظ":    "safahat.hifz_planner_03",
    "🔁 مُساعد الحفظ":    "safahat.hifz_helper_04",
    "📖 تفسير":         "safahat.tafsir_05",
    "🧠 لعبة المراجعة":  "safahat.moraj3a",
    "❓ سؤال قرآنى":     "safahat.ask_quran"
}

# CSS
st.markdown(f"""
<style>
    .stApp {{background-color: {theme['background']}; font-family: 'Segoe UI', sans-serif;}}
    .main-title {{color: {theme['primary']}; font-size: 42px; font-weight: bold; text-align: center; margin: 20px 0 10px;}}
    .quote {{font-size: 18px; color: {theme['secondary']}; text-align:center; font-style: italic; margin-bottom:30px;}}
    .header-bar {{background-color: {theme['primary']}; padding:15px 30px; display:flex; justify-content:space-between; align-items:center; color: white; border-bottom:4px solid {theme['accent']}; position: fixed; top:0; width:100%; z-index: 1000;}}
    .header-title {{font-size: 26px; font-weight:bold;}}
    .quick-links a {{color:white; margin-left:25px; text-decoration:none; font-weight:500;}}
    .quick-links a:hover {{color: {theme['accent']}; text-decoration: underline;}}
    .centered-image {{
        display: flex;
        justify-content: center;
        margin-top: 20px;
        margin-bottom: 30px;
    }}
    .centered-image img {{
        width: 480px;
        border-radius: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }}
    .centered-image img:hover {{
        transform: scale(1.05);
    }}
    .bottom-nav {{position: fixed; bottom:0; left:0; width:100%; background-color: {theme['primary']}; display:flex; justify-content:center; padding:12px 0; border-top:3px solid {theme['accent']}; z-index: 999;}}
    .bottom-nav a {{
        color:white; 
        margin:0 15px; 
        text-decoration:none; 
        font-weight:bold; 
        font-size:14px; 
        padding:6px 12px; 
        border-radius:8px; 
        transition: background-color 0.3s;
        cursor: pointer;
    }}
    .bottom-nav a:hover {{background-color:{theme['accent']}; color:black;}}
    hr {{border:none; border-top:2px solid {theme['secondary']}; margin:25px 0;}}
</style>
""", unsafe_allow_html=True)

# شريط علوي ثابت
st.markdown("""
<div class="header-bar">
    <div class="header-title">📖 رفيق القرآن</div>
    <div class="quick-links">
        <a href="#الرئيسية">الرئيسية</a>
        <a href="#مقتطف">مقتطف اليوم</a>
    </div>
</div>
""", unsafe_allow_html=True)

# قراءة صفحة محددة من query params أو الافتراضي "🏠 الرئيسية"
query_params = st.experimental_get_query_params()
current_page = query_params.get("page", ["🏠 الرئيسية"])[0]

# عرض محتوى الصفحة الرئيسية
if current_page == "🏠 الرئيسية":
    st.markdown('<div class="main-title" id="الرئيسية">  رفيق القرآن : ابدأ رحلتك الآن  ✨</div>', unsafe_allow_html=True)
    st.markdown('<div class="quote">“خيرهم من تعلم القرآن وعلمه” – النبي محمد ﷺ</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="centered-image">
        <img src="https://png.pngtree.com/png-clipart/20220223/original/pngtree-moslem-kid-read-quran-png-image_7311235.png" alt="Quran Kid">
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f'<div class="quote" id="مقتطف">🌟 مقتطف اليوم: {random.choice(daily_ayahs)}</div>', unsafe_allow_html=True)
    st.markdown("<hr />", unsafe_allow_html=True)
else:
    # استيراد وعرض صفحة أخرى حسب التحديد
    page_mod = pages.get(current_page)
    if page_mod:
        mod = __import__(page_mod, fromlist=['app'])
        mod.app()
    else:
        st.warning("هذه الصفحة غير متوفرة حالياً.")

# شريط تنقل سفلي متفاعل (يستخدم query params لتغيير الصفحة)
links_html = ""
for name in pages.keys():
    active_style = "background-color:" + theme['accent'] + "; color:black;" if name == current_page else ""
    links_html += f'<a href="?page={name}" style="{active_style}">{name}</a>'

st.markdown(f'<div class="bottom-nav">{links_html}</div>', unsafe_allow_html=True)
