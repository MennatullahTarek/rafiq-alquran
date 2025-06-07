import streamlit as st
import json
import re
from transformers import pipeline
import nest_asyncio



nest_asyncio.apply()

# ألوان الثيم حسب طلبك
PRIMARY_COLOR = "#2E7D32"  # أخضر
SECONDARY_COLOR = "#009688"
ACCENT_COLOR = "#FFC107"   # ذهبي
BACKGROUND_COLOR = "#fffbf2"

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
    message_html = f"""
    <style>
    .chat-container {{
        max-width: 700px;
        margin: 0 auto;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
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

def app():
    st.markdown(
        f"""
        <h1 style="text-align: center; color: {PRIMARY_COLOR}; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
        🤖 رفيق القرآن - شات بوت مع QA
        </h1>
        """,
        unsafe_allow_html=True,
    )

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

    # خانة الإدخال بدون زر - نرسل بالضغط Enter فقط
    user_input = st.text_input("💬 أكتب رسالتك هنا:", value=st.session_state.user_input, key="input_box", on_change=None)

    # زر افتراضي لإرسال عند الضغط Enter
    if user_input.strip() and st.session_state.user_input != user_input:
        # حدث عند التغيير فقط لمنع إعادة إرسال تلقائي
        st.session_state.user_input = user_input

    # طريقة معالجة إرسال Enter:
    # لأن streamlit لا يدعم التعرف مباشرة على زر Enter في text_input بدون زر، الحل:
    # نستخدم زر مخفي أو زر إرسال صغير لكن نختفيه، ونشجع المستخدم على الضغط Enter ثم الضغط زر إرسال (بس انت قلت لا زر إرسال)
    # بالتالي، الطريقة الأفضل هي إرسال فور الضغط على زر Enter عن طريق on_change مع استدعاء دالة. لكن Streamlit محدود في هذا.
    # لهذا، ممكن نعتمد على زر إرسال خفي أو زر بجانب الإدخال ولكن صغير جدًا.
    # أو نستعمل st.form مع submit_on_enter=True.

    # الحل الأفضل هنا هو استخدام st.form مع submit_on_enter=True

def app_with_form():
    st.markdown(
        f"""
        <h1 style="text-align: center; color: {PRIMARY_COLOR}; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
        🤖 رفيق القرآن - شات بوت مع QA
        </h1>
        """,
        unsafe_allow_html=True,
    )

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

    # هنا نستخدم form ليدعم الضغط على Enter للإرسال
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("💬 أكتب رسالتك هنا:", value="", key="input_box")
        submit_button = st.form_submit_button(label="")

        if submit_button and user_input.strip():
            response = generate_response(user_input, surah_data, qa_pipeline)
            st.session_state.chat_history.append((user_input, response))
            st.rerun()

if __name__ == "__main__":
    app_with_form()
