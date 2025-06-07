import streamlit as st
import json
import re
import os
from transformers import pipeline
import nest_asyncio

# Apply asyncio patch for Streamlit compatibility
nest_asyncio.apply()

# ========================
# CONFIGURATION
# ========================
PRIMARY_COLOR = "#2E7D32"
ACCENT_COLOR = "#FFC107"
BACKGROUND_COLOR = "#fffbf2"

# ========================
# ENVIRONMENT & DATA LOADING
# ========================
@st.cache_resource
def load_surah_data(filepath="surah_info.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

class QuranData:
    def __init__(self, filepath="surah_info.json"):
        self.filepath = filepath
        self.data = load_surah_data(self.filepath)

# ========================
# TOOLS & MODEL WRAPPER
# ========================
@st.cache_resource
def load_llm_model():
    with st.spinner("⏳ جاري تحميل نموذج اللغة... يرجى الانتظار"):
        return pipeline("question-answering", model="Damith/AraELECTRA-discriminator-QuranQA")

class QuranQATools:
    def __init__(self):
        self.llm = load_llm_model()

    @staticmethod
    def extract_surah_name(question):
        match = re.search(r"سورة\s+([\w]+)", question)
        return match.group(1) if match else None

    def get_context(self, surah_name, surah_data):
        for surah in surah_data:
            if surah_name == surah["name_ar"]:
                return (
                    f"سورة {surah['name_ar']} هي سورة {surah['revelation_place']}، "
                    f"عدد آياتها {surah['verses_count']}، "
                    f"نزلت في {surah['revelation_time']}، "
                    f"والهدف منها: {surah['reasons']}."
                )
        return ""

    def generate_answer(self, question, context):
        if not context:
            return "لا توجد معلومات كافية للإجابة على هذا السؤال."
        result = self.llm(question=question, context=context)
        return result["answer"]

# ========================
# AGENT
# ========================
class QuranAgent:
    def __init__(self, data: QuranData, tools: QuranQATools):
        self.data = data
        self.tools = tools

    def is_greeting(self, question):
        greetings = {
            "السلام عليكم": "وعليكم السلام ورحمة الله وبركاته 🌸",
            "مرحبا": "مرحبًا بك يا رفيق! 😊 كيف يمكنني مساعدتك في تدبر السور؟",
            "من أنت": "أنا مساعد ذكي لتدبر سور القرآن الكريم ✨ اسألني عن أي سورة وسأساعدك.",
            "أهلا": "أهلاً وسهلاً بك! 🌟 كيف يمكنني خدمتك؟",
        }
        q_clean = question.strip().lower().replace("؟", "").replace("!", "")
        for key in greetings:
            if key in q_clean:
                return greetings[key]
        return None

    def answer_question(self, question):
        greeting_response = self.is_greeting(question)
        if greeting_response:
            return greeting_response

        surah_name = self.tools.extract_surah_name(question)
        if not surah_name:
            return "❗ يرجى ذكر اسم السورة في سؤالك. مثل: ما هدف سورة البقرة؟"

        context = self.tools.get_context(surah_name, self.data.data)
        answer = self.tools.generate_answer(question, context)
        return f"📖 {answer}"

# ========================
# UI
# ========================
def display_ui(agent: QuranAgent):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {BACKGROUND_COLOR};
            direction: rtl;
            font-family: 'Cairo', sans-serif;
        }}
        .main-title {{
            color: {PRIMARY_COLOR};
            font-size: 2.2rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px;
        }}
        .subtitle {{
            text-align: center;
            color: #555;
            font-size: 1rem;
            margin-bottom: 20px;
        }}
        .chat-bubble {{
            background-color: #e0f7fa;
            padding: 1rem;
            border-radius: 20px;
            margin-top: 1rem;
            text-align: right;
            font-size: 1.1rem;
            border: 1px solid #81d4fa;
            color: #004d40;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
        }}
        .user-bubble {{
            background-color: #fff3e0;
            color: #6d4c41;
            text-align: left;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="main-title">🤖 مساعد تدبر السور القرآنية</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">اكتب سؤالك متضمنًا اسم السورة وسيتم استخراج الإجابة ✨</div>', unsafe_allow_html=True)

    question = st.text_input("✍️ اكتب سؤالك هنا")

    if st.button("🔍 الحصول على الإجابة"):
        if question.strip():
            # Show user's question
            st.markdown(
                f"<div class='chat-bubble user-bubble'>👤 {question}</div>",
                unsafe_allow_html=True
            )
            # Show assistant's answer
            answer = agent.answer_question(question)
            st.markdown(
                f"<div class='chat-bubble'>🤖 {answer}</div>",
                unsafe_allow_html=True
            )
        else:
            st.warning("⚠️ يرجى إدخال سؤال أولًا.")

# ========================
# MAIN APP
# ========================
def app():
    data = QuranData()
    tools = QuranQATools()
    agent = QuranAgent(data, tools)
    display_ui(agent)

if __name__ == "__main__":
    app()
