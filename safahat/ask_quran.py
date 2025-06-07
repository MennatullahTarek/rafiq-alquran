import streamlit as st
import json
import re
from transformers import pipeline
import nest_asyncio

nest_asyncio.apply()

# تحميل بيانات السور
@st.cache_resource
def load_surah_data(filepath="surah_info.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

# استخراج اسم السورة من السؤال
def extract_surah_name(question):
    match = re.search(r"سورة\s+([\w]+)", question)
    return match.group(1) if match else None

# توليد السياق من البيانات
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

# تحميل موديل LLM (QA model)
@st.cache_resource
def load_llm_model():
    with st.spinner("⏳ جاري تحميل نموذج اللغة... يرجى الانتظار"):
        model = pipeline("question-answering", model="Damith/AraELECTRA-discriminator-QuranQA")
    return model

# توليد الرد من الموديل والسياق
def generate_response_with_llm(question, context, llm):
    if not context:
        return "لا توجد معلومات كافية للإجابة على هذا السؤال."
    result = llm(question=question, context=context)
    return result["answer"]

# شات بوت
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

# تصميم فقاعات الرسائل (HTML + CSS)
def render_message(user_msg, bot_msg):
    # استخدام HTML وCSS لترتيب الفقاعات بشكل جميل
    message_html = f"""
    <style>
    .chat-container {{
        max-width: 700px;
        margin: 0 auto;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
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
        background-color: #2F80ED;
        color: white;
        border-bottom-right-radius: 0;
    }}
    .user-icon {{
        font-weight: bold;
        margin-right: 10px;
        color: #34B7F1;
        min-width: 30px;
        text-align: center;
    }}
    .bot-icon {{
        font-weight: bold;
        margin-left: 10px;
        color: #E2E2E2;
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

# تطبيق Streamlit
def app():

    st.title("🤖 رفيق القرآن - شات بوت مع QA")

    surah_data = load_surah_data()
    qa_pipeline = load_llm_model()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

    # عرض المحادثة بشكل فقاعات
    if st.session_state.chat_history:
        for user_msg, bot_msg in st.session_state.chat_history:
            render_message(user_msg, bot_msg)

    # إدخال المستخدم مع زر إرسال بجانب بعض
    col1, col2 = st.columns([8,1])
    with col1:
        user_input = st.text_input("💬 أكتب رسالتك هنا:", value=st.session_state.user_input, key="input_box")
    with col2:
        send_button = st.button("▶️")

    if send_button and user_input.strip():
        response = generate_response(user_input, surah_data, qa_pipeline)
        st.session_state.chat_history.append((user_input, response))
        st.session_state.user_input = ""
        st.rerun()  # إعادة تشغيل التطبيق لإظهار الرسالة الجديدة

    else:
        st.session_state.user_input = user_input  # الحفاظ على نص الإدخال لو لم يُرسل

if __name__ == "__main__":
    app()
