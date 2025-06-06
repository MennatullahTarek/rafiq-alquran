import streamlit as st
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
import nest_asyncio

# لحل مشكلة event loop مع Streamlit
nest_asyncio.apply()

# تحميل النموذج والمحول
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("tempdas/QuranGPT")
    model = AutoModelForCausalLM.from_pretrained("tempdas/QuranGPT")
    return tokenizer, model

def generate_answer(question, tokenizer, model):
    input_ids = tokenizer.encode(question, return_tensors="pt")
    output = model.generate(
        input_ids,
        max_length=200,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        early_stopping=True
    )
    answer = tokenizer.decode(output[0], skip_special_tokens=True)
    return answer

def app():
    tokenizer, model = load_model()

    st.title("💬 اسأل عن القرآن")
    st.markdown("أكتب أي سؤال له علاقة بالقرآن الكريم وسنحاول مساعدتك في الإجابة عليه ✨")

    # مدخل السؤال من المستخدم
    question = st.text_input("❓ سؤالك:", placeholder="مثال: كم عدد آيات سورة البقرة؟")

    if question:
        with st.spinner("⏳ جاري توليد الإجابة..."):
            try:
                answer = generate_answer(question, tokenizer, model)
                st.success(f"✅ الإجابة: {answer}")
            except Exception as e:
                st.error(f"حدث خطأ أثناء محاولة الإجابة على سؤالك: {e}")

if __name__ == "__main__":
    app()
