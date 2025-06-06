import streamlit as st
import random

# إعداد واجهة الصفحة
st.set_page_config(
    page_title="رفيق القرآن",
    layout="wide",
    page_icon="https://cdn-icons-png.flaticon.com/512/4358/4358773.png"
)

# الثيم العام
theme = {
    "primary": "#2E7D32",
    "secondary": "#009688",
    "accent": "#FFC107",
    "background": "#EDE7D9"
}

# ----------------------------- AGENTS -----------------------------

class HomeAgent:
    def __init__(self):
        self.daily_ayahs = [
            "إِنَّ مَعَ الْعُسْرِ يُسْرًا ﴿٦﴾ - الشرح",
            "وَقُل رَّبِّ زِدْنِي عِلْمًا ﴿١١٤﴾ - طه",
            "إِنَّ اللَّهَ مَعَ الصَّابِرِينَ ﴿١٥٣﴾ - البقرة",
            "فَاذْكُرُونِي أَذْكُرْكُمْ ﴿١٥٢﴾ - البقرة"
        ]

    def act(self):
        st.markdown('<div class="main-title" style="margin-top:70px;">  رفيق القرآن : ابدأ رحلتك الآن ✨</div>', unsafe_allow_html=True)
        st.markdown('<div class="quote">“خيركم من تعلم القرآن وعلمه” – النبي محمد ﷺ</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="centered-image">
            <img src="https://png.pngtree.com/png-clipart/20220223/original/pngtree-moslem-kid-read-quran-png-image_7311235.png" alt="Quran Kid">
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<div class="quote">🌟 مقتطف اليوم: {random.choice(self.daily_ayahs)}</div>', unsafe_allow_html=True)

class TafsirAgent:
    def act(self):
        st.header("📖 تفسير")
        st.write("هنا سيكون محتوى تفسير آيات مختارة...")

class ListenAgent:
    def act(self):
        st.header("🎧 الاستماع")
        st.write("مشغل صوتي للآيات هنا...")

class HifzAgent:
    def __init__(self, mode):
        self.mode = mode

    def act(self):
        if self.mode == "planner":
            st.header("🗓️ مُخطط الحفظ")
            st.write("خطط لحفظك الأسبوعي أو الشهري هنا...")
        else:
            st.header("🔁 مُساعد الحفظ")
            st.write("أداة تفاعلية لمساعدتك على تكرار وتسميع الحفظ...")

class ReviewAgent:
    def act(self):
        st.header("🧠 لعبة المراجعة")
        st.write("هنا لعبة تفاعلية لمراجعة المحفوظات...")

class QuranQuestionAgent:
    def act(self):
        st.header("❓ سؤال قرآنى")
        st.write("سؤال عشوائي من القرآن وتقييم إجابتك...")

class AboutAgent:
    def act(self):
        st.header("من نحن 👀")
        st.markdown("تطبيق رفيق القرآن هو منصة تساعدك على حفظ القرآن الكريم بوسائل حديثة وتفاعلية ✨")

# --------------------------- COORDINATOR --------------------------

class AgentCoordinator:
    def __init__(self):
        self.page_agents = {
            "🏠 الرئيسية": HomeAgent(),
            "🎧 الاستماع": ListenAgent(),
            "🗓️ مُخطط الحفظ": HifzAgent(mode="planner"),
            "🔁 مُساعد الحفظ": HifzAgent(mode="helper"),
            "📖 تفسير": TafsirAgent(),
            "🧠 لعبة المراجعة": ReviewAgent(),
            "❓ سؤال قرآنى": QuranQuestionAgent(),
            "من نحن 👀": AboutAgent()
        }

    def run(self):
        query_params = st.query_params
        current_page = query_params.get("page", ["🏠 الرئيسية"])[0]

        if current_page not in self.page_agents:
            current_page = "🏠 الرئيسية"

        # تصميم الصفحة
        render_page_style(theme)
        render_header()

        # عرض محتوى الصفحة المناسبة
        st.markdown('<div class="fade-in">', unsafe_allow_html=True)
        self.page_agents[current_page].act()
        st.markdown('</div>', unsafe_allow_html=True)

        render_footer(self.page_agents, current_page, theme)

# ------------------------ STATIC UI COMPONENTS ---------------------

def render_page_style(theme):
    st.markdown(f"""
    <style>
        .stApp {{
            background-color: {theme['background']};
            font-family: 'Segoe UI', sans-serif;
        }}
        .fade-in {{
            animation: fadeIn 0.8s ease-in-out;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .main-title {{
            color: {theme['primary']};
            font-size: 42px;
            font-weight: bold;
            text-align: center;
            margin: 20px 0 10px;
        }}
        .quote {{
            font-size: 18px;
            color: {theme['secondary']};
            text-align: center;
            font-style: italic;
            margin-bottom: 30px;
        }}
        .centered-image img {{
            width: 500px;
            border-radius: 20px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            transition: transform 0.3s ease;
            margin: 80px auto 40px auto;
            display: block;
        }}
        .centered-image img:hover {{
            transform: scale(1.05);
        }}
        .bottom-nav {{
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: {theme['primary']};
            display: flex;
            justify-content: flex-start;
            padding: 12px 20px;
            border-top: 3px solid {theme['accent']};
            z-index: 999;
            direction: rtl;
            text-align: right;
        }}
        .bottom-nav a {{
            color: white;
            margin: 0 15px;
            text-decoration: none;
            font-weight: bold;
            font-size: 14px;
            padding: 6px 12px;
            border-radius: 8px;
            transition: background-color 0.3s;
            cursor: pointer;
        }}
        .bottom-nav a:hover {{
            background-color: {theme['accent']};
            color: black;
        }}
        .bottom-nav a.active {{
            background-color: {theme['accent']};
            color: black;
        }}
    </style>
    """, unsafe_allow_html=True)

def render_header():
    st.markdown("""
    <div style="background-color:#2E7D32; padding: 15px; color:white; text-align:center; font-weight:bold; font-size:26px; position: fixed; top:0; width:100%; z-index: 1000;">
        📖 رفيق القرآن
    </div>
    """, unsafe_allow_html=True)

def render_footer(page_agents, current_page, theme):
    footer_html = ""
    for name in page_agents.keys():
        active = "active" if name == current_page else ""
        footer_html += f'<a href="/?page={name}" class="{active}">{name}</a>'
    st.markdown(f'<div class="bottom-nav">{footer_html}</div>', unsafe_allow_html=True)

# ------------------------ MAIN EXECUTION ------------------------

if __name__ == "__main__":
    coordinator = AgentCoordinator()
    coordinator.run()
