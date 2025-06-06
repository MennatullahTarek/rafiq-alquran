import streamlit as st
from transformers import pipeline
import nest_asyncio

nest_asyncio.apply()

@st.cache_resource
def load_generator():
    return pipeline(
        "text-generation",
        model="aubmindlab/aragpt2-base", 
        use_auth_token=st.secrets["huggingface_token"]
    )

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
