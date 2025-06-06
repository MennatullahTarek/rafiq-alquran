import streamlit as st
from transformers import pipeline
import nest_asyncio

# لحل مشكلة event loop مع Streamlit
nest_asyncio.apply()

# تحميل النموذج
@st.cache_resource
def load_model():
    return pipeline(
        "question-answering",
        model="ZeyadAhmed/AraElectra-Arabic-SQuADv2-QA",
        tokenizer="ZeyadAhmed/AraElectra-Arabic-SQuADv2-QA"
    )

def app():
    qa_pipeline = load_model()

    st.title("💬 اسأل عن القرآن")
    st.markdown("أكتب أي سؤال له علاقة بالقرآن الكريم وسنحاول مساعدتك في الإجابة عليه ✨")

    question = st.text_input("❓ سؤالك:", placeholder="مثال: كم عدد آيات سورة البقرة؟")
    context = st.text_area("📚 أضف سياقًا (اختياري):", placeholder="مثال: سورة البقرة تحتوي على ...")

    if question:
        with st.spinner("⏳ جاري توليد الإجابة..."):
            try:
                result = qa_pipeline(question=question, context=context)
                st.success(f"✅ الإجابة: {result['answer']}")
            except Exception as e:
                st.error(f"حدث خطأ أثناء محاولة الإجابة على سؤالك: {e}")

if __name__ == "__main__":
    app()
