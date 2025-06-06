import streamlit as st
import random
from typing import Callable

# === Agentic Structure ===
class QuranAppAgent:
    def __init__(self):
        self.theme = {
            "primary": "#2E7D32",
            "secondary": "#009688",
            "accent": "#FFC107",
            "background": "#EDE7D9"
        }
        self.daily_ayahs = [
            "إِنَّ مَعَ الْعُسْرِ يُسْرًا ﴿٦﴾ - الشرح",
            "وَقُل رَّبِّ زِدْنِي عِلْمًا ﴿١١٤﴾ - طه",
            "إِنَّ اللَّهَ مَعَ الصَّابِرِينَ ﴿١٥٣﴾ - البقرة",
            "فَاذْكُرُونِي أَذْكُرْكُمْ ﴿١٥٢﴾ - البقرة"
        ]
        self.pages = {
            "🏠 الرئيسية": None,
            "🎧 الاستماع": "safahat.estimaa_02",
            "🗓️ مُخطط الحفظ": "safahat.hifz_planner_03",
            "🔁 مُساعد الحفظ": "safahat.hifz_helper_04",
            "📖 تفسير": "safahat.tafsir_05",
            "🧠 لعبة المراجعة": "safahat.moraj3a",
            "❓ سؤال قرآنى": "safahat.ask_quran",
            "من نحن 👀": "safahat.about_app"
        ]

    def run(self):
        st.set_page_config(
            page_title="رفيق القرآن",
            layout="wide",
            page_icon="https://cdn-icons-png.flaticon.com/512/4358/4358773.png"
        )

        self._apply_styles()
        self._render_header()

        current_page = st.query_params.get("page", "🏠 الرئيسية")
        if current_page not in self.pages:
            current_page = "🏠 الرئيسية"

        st.markdown('<div class="fade-in">', unsafe_allow_html=True)
        if current_page == "🏠 الرئيسية":
            self._render_home()
        else:
            self._load_page(current_page)
        st.markdown('</div>', unsafe_allow_html=True)

        self._render_footer(current_page)

    def _apply_styles(self):
        st.markdown(f"""
        <style>
            .stApp {{ background-color: {self.theme['background']}; font-family: 'Segoe UI', sans-serif; }}
            .fade-in {{ animation: fadeIn 0.8s ease-in-out; }}
            @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
            .main-title {{ color: {self.theme['primary']}; font-size: 42px; font-weight: bold; text-align: center; margin: 20px 0 10px; }}
            .quote {{ font-size: 18px; color: {self.theme['secondary']}; text-align: center; font-style: italic; margin-bottom: 30px; }}
            .centered-image img {{ width: 500px; border-radius: 20px; box-shadow: 0 8px 20px rgba(0,0,0,0.2); transition: transform 0.3s ease; margin: 80px auto 40px auto; display: block; }}
            .centered-image img:hover {{ transform: scale(1.05); }}
            .bottom-nav {{ position: fixed; bottom: 0; left: 0; width: 100%; background-color: {self.theme['primary']}; display: flex; justify-content: center; padding: 12px 0; border-top: 3px solid {self.theme['accent']}; z-index: 999; }}
            .bottom-nav a {{ color: white; margin: 0 15px; text-decoration: none; font-weight: bold; font-size: 14px; padding: 6px 12px; border-radius: 8px; transition: background-color 0.3s; cursor: pointer; }}
            .bottom-nav a:hover {{ background-color: {self.theme['accent']}; color: black; }}
            .bottom-nav a.active {{ background-color: {self.theme['accent']}; color: black; }}
        </style>
        """, unsafe_allow_html=True)

    def _render_header(self):
        st.markdown("""
        <div style="background-color:#2E7D32; padding: 15px; color:white; text-align:center; font-weight:bold; font-size:26px; position: fixed; top:0; width:100%; z-index: 1000;">
            📖 رفيق القرآن
        </div>
        """, unsafe_allow_html=True)

    def _render_home(self):
        st.markdown('<div class="main-title" style="margin-top:70px;">  رفيق القرآن : ابدأ رحلتك الآن ✨</div>', unsafe_allow_html=True)
        st.markdown('<div class="quote">“خيركم من تعلم القرآن وعلمه” – النبي محمد ﷺ</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="centered-image">
            <img src="https://png.pngtree.com/png-clipart/20220223/original/pngtree-moslem-kid-read-quran-png-image_7311235.png" alt="Quran Kid">
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<div class="quote">🌟 مقتطف اليوم: {random.choice(self.daily_ayahs)}</div>', unsafe_allow_html=True)

    def _render_footer(self, current_page: str):
        footer_html = ""
        for page_name in self.pages.keys():
            active = "active" if page_name == current_page else ""
            footer_html += f'<a href="/?page={page_name}" class="{active}">{page_name}</a>'
        st.markdown(f'<div class="bottom-nav">{footer_html}</div>', unsafe_allow_html=True)

    def _load_page(self, page_key: str):
        mod_name = self.pages.get(page_key)
        if mod_name:
            mod = __import__(mod_name, fromlist=['app'])
            mod.app()


# === Run the App ===
if __name__ == '__main__':
    agent = QuranAppAgent()
    agent.run()
