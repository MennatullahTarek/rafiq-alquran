# import streamlit as st
# import random

# # إعداد الصفحة
# st.set_page_config(
#     page_title="رفيق القرآن",
#     layout="wide",
#     page_icon="https://cdn-icons-png.flaticon.com/512/4358/4358773.png"
# )

# # الألوان
# theme = {
#     "primary": "#2E7D32",
#     "secondary": "#009688",
#     "accent": "#FFC107",
#     "background": "#EDE7D9"
# }

# # مقتطفات يومية
# daily_ayahs = [
#     "إِنَّ مَعَ الْعُسْرِ يُسْرًا ﴿٦﴾ - الشرح",
#     "وَقُل رَّبِّ زِدْنِي عِلْمًا ﴿١١٤﴾ - طه",
#     "إِنَّ اللَّهَ مَعَ الصَّابِرِينَ ﴿١٥٣﴾ - البقرة",
#     "فَاذْكُرُونِي أَذْكُرْكُمْ ﴿١٥٢﴾ - البقرة"
# ]

# # الصفحات المتاحة
# pages = {
#     "🏠 الرئيسية": None,
#     "🎧 الاستماع":       "safahat.estimaa_02",
#     "🗓️ مُخطط الحفظ":    "safahat.hifz_planner_03",
#     "🔁 مُساعد الحفظ":    "safahat.hifz_helper_04",
#     "📖 تفسير":         "safahat.tafsir_05",
#     "🧠 لعبة المراجعة":  "safahat.moraj3a",
#     "❓ سؤال قرآنى":     "safahat.ask_quran"
# }

# # قراءة صفحة محددة من رابط المتصفح
# query_params = st.query_params
# current_page = query_params.get("page", "🏠 الرئيسية")

# if current_page not in pages:
#     current_page = "🏠 الرئيسية"

# def load_page(page_key):
#     mod_name = pages.get(page_key)
#     if mod_name:
#         mod = __import__(mod_name, fromlist=['app'])
#         mod.app()

# # التنسيق (CSS)
# st.markdown(f"""
# <style>
#     .stApp {{background-color: {theme['background']}; font-family: 'Segoe UI', sans-serif;}}
#     .main-title {{color: {theme['primary']}; font-size: 42px; font-weight: bold; text-align: center; margin: 20px 0 10px;}}
#     .quote {{font-size: 18px; color: {theme['secondary']}; text-align:center; font-style: italic; margin-bottom:30px;}}
#     .centered-image img {{
#         width: 500px;
#         border-radius: 20px;
#         box-shadow: 0 8px 20px rgba(0,0,0,0.2);
#         transition: transform 0.3s ease;
#         margin: 80px auto 40px auto;
#         display: block;
#     }}
#     .centered-image img:hover {{transform: scale(1.05);}}
#     .bottom-nav {{
#         position: fixed; bottom:0; left:0; width:100%;
#         background-color: {theme['primary']};
#         display:flex; justify-content:center;
#         padding:12px 0; border-top:3px solid {theme['accent']};
#         z-index: 999;
#     }}
#     .bottom-nav a {{
#         color:white;
#         margin:0 15px;
#         text-decoration:none;
#         font-weight:bold;
#         font-size:14px;
#         padding:6px 12px;
#         border-radius:8px;
#         transition: background-color 0.3s;
#         cursor:pointer;
#     }}
#     .bottom-nav a:hover {{
#         background-color:{theme['accent']};
#         color:black;
#     }}
#     .bottom-nav a.active {{
#         background-color:{theme['accent']};
#         color:black;
#     }}
# </style>
# """, unsafe_allow_html=True)

# # شريط علوي
# st.markdown("""
# <div style="background-color:#2E7D32; padding: 15px; color:white; text-align:center; font-weight:bold; font-size:26px; position: fixed; top:0; width:100%; z-index: 1000;">
#     📖 رفيق القرآن
# </div>
# """, unsafe_allow_html=True)

# # محتوى الصفحة
# if current_page == "🏠 الرئيسية":
#     st.markdown('<div class="main-title" style="margin-top:70px;">  رفيق القرآن : ابدأ رحلتك الآن ✨</div>', unsafe_allow_html=True)
#     st.markdown('<div class="quote">“خيرهم من تعلم القرآن وعلمه” – النبي محمد ﷺ</div>', unsafe_allow_html=True)
#     st.markdown("""
#     <div class="centered-image">
#         <img src="https://png.pngtree.com/png-clipart/20220223/original/pngtree-moslem-kid-read-quran-png-image_7311235.png" alt="Quran Kid">
#     </div>
#     """, unsafe_allow_html=True)
#     st.markdown(f'<div class="quote">🌟 مقتطف اليوم: {random.choice(daily_ayahs)}</div>', unsafe_allow_html=True)
# else:
#     load_page(current_page)

# # شريط التنقل السفلي
# footer_html = ""
# for page_name in pages.keys():
#     active = "active" if page_name == current_page else ""
#     footer_html += f'<a href="/?page={page_name}" class="{active}">{page_name}</a>'

# st.markdown(f'<div class="bottom-nav">{footer_html}</div>', unsafe_allow_html=True)



import streamlit as st
import random

# إعداد الصفحة
st.set_page_config(
    page_title="رفيق القرآن",
    layout="wide",
    page_icon="https://cdn-icons-png.flaticon.com/512/4358/4358773.png"
)

# الألوان
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

# الصفحات المتاحة
pages = {
    "🏠 الرئيسية": None,
    "🎧 الاستماع":       "safahat.estimaa_02",
    "🗓️ مُخطط الحفظ":    "safahat.hifz_planner_03",
    "🔁 مُساعد الحفظ":    "safahat.hifz_helper_04",
    "📖 تفسير":         "safahat.tafsir_05",
    "🧠 لعبة المراجعة":  "safahat.moraj3a",
    "❓ سؤال قرآنى":     "safahat.ask_quran"
}

# تهيئة الحالة
if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 الرئيسية"

# التنسيق (CSS)
st.markdown(f"""
<style>
    .stApp {{background-color: {theme['background']}; font-family: 'Segoe UI', sans-serif;}}
    .main-title {{color: {theme['primary']}; font-size: 42px; font-weight: bold; text-align: center; margin: 20px 0 10px;}}
    .quote {{font-size: 18px; color: {theme['secondary']}; text-align:center; font-style: italic; margin-bottom:30px;}}
    .centered-image img {{
        width: 500px;
        border-radius: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
        margin: 80px auto 40px auto;
        display: block;
    }}
    .centered-image img:hover {{transform: scale(1.05);}}
    .bottom-nav {{
        position: fixed; bottom:0; left:0; width:100%;
        background-color: {theme['primary']};
        display:flex; justify-content:center;
        padding:12px 0; border-top:3px solid {theme['accent']};
        z-index: 999;
    }}
    .bottom-nav button {{
        color:white;
        margin:0 15px;
        background:none;
        border:none;
        font-weight:bold;
        font-size:14px;
        padding:6px 12px;
        border-radius:8px;
        transition: background-color 0.3s;
        cursor:pointer;
    }}
    .bottom-nav button:hover {{
        background-color:{theme['accent']};
        color:black;
    }}
    .bottom-nav button.active {{
        background-color:{theme['accent']};
        color:black;
    }}
</style>
""", unsafe_allow_html=True)

# شريط علوي
st.markdown("""
<div style="background-color:#2E7D32; padding: 15px; color:white; text-align:center; font-weight:bold; font-size:26px; position: fixed; top:0; width:100%; z-index: 1000;">
    📖 رفيق القرآن
</div>
""", unsafe_allow_html=True)

# محتوى الصفحة
current_page = st.session_state.current_page

if current_page == "🏠 الرئيسية":
    st.markdown('<div class="main-title" style="margin-top:70px;">رفيق القرآن : ابدأ رحلتك الآن ✨</div>', unsafe_allow_html=True)
    st.markdown('<div class="quote">“خيركم من تعلم القرآن وعلمه” – النبي محمد ﷺ</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="centered-image">
        <img src="https://png.pngtree.com/png-clipart/20220223/original/pngtree-moslem-kid-read-quran-png-image_7311235.png" alt="Quran Kid">
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f'<div class="quote">🌟 مقتطف اليوم: {random.choice(daily_ayahs)}</div>', unsafe_allow_html=True)
else:
    # تحميل الصفحة المحددة
    mod_name = pages.get(current_page)
    if mod_name:
        mod = __import__(mod_name, fromlist=['app'])
        mod.app()

# شريط التنقل السفلي (باستخدام buttons لتحديث session_state بدون reload)
footer_html = '<div class="bottom-nav">'
for page_name in pages.keys():
    active_class = "active" if page_name == current_page else ""
    footer_html += f"""
    <form action="" method="post">
        <button class="{active_class}" name="nav_button" value="{page_name}" formmethod="post">{page_name}</button>
    </form>
    """
footer_html += '</div>'

# التحكم في التنقل
if "nav_button" in st.session_state:
    st.session_state.current_page = st.session_state.nav_button

st.markdown(footer_html, unsafe_allow_html=True)

