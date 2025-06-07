import streamlit as st
import json
import re
from transformers import pipeline
import nest_asyncio



nest_asyncio.apply()

PRIMARY_COLOR = "#2E7D32"  # أخضر
ACCENT_COLOR = "#FFC107"   # ذهبي
BACKGROUND_COLOR = "#fffbf2"

@st.cache_resource
def load_surah_data(filepath="surah_info.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_surah_name(question):
    match = re.search(r"سورة\s+([\w]+)", question)
    return match.group(1) if match else None

def get_context_from_surah(surah_name, surah_data):
    for surah in surah_data:
        if surah_name == surah["name_ar"]:
            return (
                f"سورة {surah['name_ar']} هي سورة {surah['revelation_place']}، "
                f"عدد آياتها {surah['verses_count']}، "
                f"نزلت في {surah['revelation_time']}، "
                f"والهدف منها: {surah['reasons']}."
            )
    return ""

@st.cache_resource
def load_llm_model():
    with st.spinner("⏳ جاري تحميل نموذج اللغة... يرجى الانتظار"):
        model = pipeline("question-answering", model="Damith/AraELECTRA-discriminator-QuranQA")
    return model

def generate_response_with_llm(question, context, llm):
    if not context:
        return "لا توجد معلومات كافية للإجابة على هذا السؤال."
    result = llm(question=question, context=context)
    return result["answer"]

def generate_response(message, surah_data, llm):
    msg = message.strip()

    if "السلام" in msg or "مرحبا" in msg:
        return "وعليكم السلام! أهلاً بك يا رفيق، كيف يمكنني مساعدتك اليوم؟ 😊"

    if "شكرا" in msg or "متشكر" in msg:
        return "على الرحب والسعة! يسعدني مساعدتك في أي وقت 🌟"

    surah_name = extract_surah_name(msg)
    if surah_name:
        context = get_context_from_surah(surah_name, surah_data)
        if context:
            return generate_response_with_llm(msg, context, llm)
        else:
            return f"لم أتمكن من العثور على معلومات عن سورة {surah_name}."

    return "لم أفهم سؤالك تمامًا 🤔، حاول تكتبه بطريقة أوضح أو اسألني عن سورة معينة."

def render_message(user_msg, bot_msg):
    message_html = f"""
    <style>
    .chat-container {{
        max-width: 700px;
        margin: 0 auto 10px auto;
        font-family:  'Cairo', sans-serif;
        background-color: {BACKGROUND_COLOR};
        padding: 10px 20px;
        border-radius: 12px;
    }}
    .message {{
        display: flex;
        margin-bottom: 12px;
        align-items: flex-start;
    }}
    .user-msg {{
        justify-content: flex-start;
    }}
    .bot-msg {{
        justify-content: flex-end;
    }}
    .bubble {{
        max-width: 70%;
        padding: 12px 18px;
        border-radius: 18px;
        font-size: 16px;
        line-height: 1.4;
        white-space: pre-wrap;
        word-wrap: break-word;
    }}
    .user-bubble {{
        background-color: #DCF8C6;
        color: #000;
        border-bottom-left-radius: 0;
    }}
    .bot-bubble {{
        background-color: {ACCENT_COLOR};
        color: #000;
        border-bottom-right-radius: 0;
    }}
    .user-icon {{
        font-weight: bold;
        margin-right: 10px;
        color: {PRIMARY_COLOR};
        min-width: 30px;
        text-align: center;
    }}
    .bot-icon {{
        font-weight: bold;
        margin-left: 10px;
        color: #5a4b00;
        min-width: 30px;
        text-align: center;
    }}
    </style>

    <div class="chat-container">
        <div class="message user-msg">
            <div class="user-icon">👤</div>
            <div class="bubble user-bubble">{user_msg}</div>
        </div>
        <div class="message bot-msg">
            <div class="bubble bot-bubble">{bot_msg}</div>
            <div class="bot-icon">🤖</div>
        </div>
    </div>
    """
    st.markdown(message_html, unsafe_allow_html=True)

def on_enter():
    user_input = st.session_state.user_input.strip()
    if user_input:
        response = generate_response(user_input, st.session_state.surah_data, st.session_state.qa_pipeline)
        st.session_state.chat_history.append((user_input, response))
        st.session_state.user_input = ""

def app():
    st.markdown(
        f"""
        <h1 style="text-align: center; color: {PRIMARY_COLOR}; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
        🤖 رفيق القرآن - شات بوت مع QA
        </h1>
        """,
        unsafe_allow_html=True,
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

    if "surah_data" not in st.session_state:
        st.session_state.surah_data = load_surah_data()
    if "qa_pipeline" not in st.session_state:
        st.session_state.qa_pipeline = load_llm_model()

    # عرض المحادثة بشكل فقاعات
    if st.session_state.chat_history:
        for user_msg, bot_msg in st.session_state.chat_history:
            render_message(user_msg, bot_msg)

    # نص الإدخال مع on_change عشان نرسل بالضغط Enter
    st.text_input(
        "💬 أكتب رسالتك هنا:",
        key="user_input",
        on_change=on_enter,
        placeholder="اكتب سؤالك واضغط Enter للإرسال...",
        label_visibility="collapsed"
    )

if __name__ == "__main__":
    app()
