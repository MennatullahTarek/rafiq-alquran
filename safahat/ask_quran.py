import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import nest_asyncio

nest_asyncio.apply()

model_name = "aubmindlab/aragpt2-base"
token = st.secrets["huggingface_token"]

@st.cache_resource
def load_generator():
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=token)
    model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=token)
    return pipeline("text-generation", model=model, tokenizer=tokenizer)

def app():
    generator = load_generator()

    st.title("💬 اسأل عن القرآن")
    st.markdown("أكتب أي سؤال له علاقة بالقرآن الكريم وسنحاول مساعدتك في الإجابة عليه ✨")

    question = st.text_input("❓ سؤالك:", placeholder="مثال: كم عدد آيات سورة البقرة؟")

    if question:
        with st.spinner("⏳ جاري توليد الإجابة..."):
            try:
                result = generator(question, max_length=100, num_return_sequences=1)
                answer = result[0]['generated_text']
                st.success(f"✅ الإجابة: {answer}")
            except Exception as e:
                st.error(f"حدث خطأ أثناء محاولة الإجابة على سؤالك: {e}")

if __name__ == "__main__":
    app()
