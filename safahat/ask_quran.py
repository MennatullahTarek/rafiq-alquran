import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import nest_asyncio

# لحل مشكلة event loop مع Streamlit
nest_asyncio.apply()

# تحميل النموذج
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("Elgeish/t5-small-arabic-qa")
    model = AutoModelForSeq2SeqLM.from_pretrained("Elgeish/t5-small-arabic-qa")
    return pipeline("text2text-generation", model=model, tokenizer=tokenizer)

def app():
    qa_pipeline = load_model()

    st.title("💬 اسأل عن القرآن")
    st.markdown("أكتب أي سؤال له علاقة بالقرآن الكريم وسنحاول مساعدتك في الإجابة عليه ✨")

    question = st.text_input("❓ سؤالك:", placeholder="مثال: كم عدد آيات سورة البقرة؟")
    context = st.text_area("📚 أضف سياقًا (اختياري):", placeholder="مثال: سورة البقرة تحتوي على ...")

    if question:
        with st.spinner("⏳ جاري توليد الإجابة..."):
            try:
                # صيغة T5 للسؤال: سؤال: <السؤال>  سياق: <السياق>
                input_text = f"سؤال: {question}  سياق: {context}"
                result = qa_pipeline(input_text, max_new_tokens=50)[0]["generated_text"]
                st.success(f"✅ الإجابة: {result}")
            except Exception as e:
                st.error(f"حدث خطأ أثناء محاولة الإجابة على سؤالك: {e}")

if __name__ == "__main__":
    app()
