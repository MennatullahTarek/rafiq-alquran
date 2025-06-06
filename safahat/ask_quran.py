import streamlit as st
import json
import re
from transformers import pipeline
import nest_asyncio


nest_asyncio.apply()


@st.cache_resource
def load_surah_data(filepath="surah_info.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

# استخراج اسم السورة من السؤال
def extract_surah_name(question):
    match = re.search(r"سورة\s+([\w]+)", question)
    return match.group(1) if match else None

# توليد السياق من البيانات (نص مختصر عن السورة)
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

# تحميل موديل LLM من Hugging Face (موديل توليد نص عربي)
@st.cache_resource
def load_llm_model():
    return pipeline(
    "question-answering",
    model="Elgeish/bert-base-arabic-qa",
    tokenizer="Elgeish/bert-base-arabic-qa"
)

# توليد الرد باستخدام الموديل مع السياق
def generate_response_with_llm(question, context, llm):
    prompt = f"السؤال: {question}\nالمعلومات: {context}\nالإجابة:"
    result = llm(prompt, max_length=150, do_sample=True, num_return_sequences=1)
    # ناخد النص بعد "الإجابة:"
    answer = result[0]['generated_text'].split("الإجابة:")[-1].strip()
    return answer

# الشات بوت (دمج كل حاجة)
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

# واجهة Streamlit
def app():
    st.title("🤖 رفيق القرآن - شات بوت مع LLM")

    # تحميل بيانات السور
    surah_data = load_surah_data()

    # تحميل الموديل
    llm = load_llm_model()

    # محادثة المستخدم والردود مخزنة في الجلسة
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # عرض المحادثة
    for user_msg, bot_msg in st.session_state.chat_history:
        st.markdown(f"👤 **أنت**: {user_msg}")
        st.markdown(f"🤖 **رفيق**: {bot_msg}")

    # إدخال المستخدم
    user_input = st.text_input("💬 أكتب رسالتك هنا:")

    if user_input:
        response = generate_response(user_input, surah_data, llm)
        st.session_state.chat_history.append((user_input, response))
        st.rerun()

if __name__ == "__main__":
    app()
