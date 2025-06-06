import streamlit as st
from transformers import pipeline
import nest_asyncio

# لحل مشكلة event loop مع Streamlit
nest_asyncio.apply()

# تحميل النموذج من Hugging Face
@st.cache_resource
def load_model():
    return pipeline(
        "text-generation",
        model="riotu-lab/ArabianGPT-1.5B",
        tokenizer="riotu-lab/ArabianGPT-1.5B"
    )

def app():
    generator = load_model()

    st.title("💬 اسأل عن القرآن")
    st.markdown("أكتب أي سؤال له علاقة بالقرآن الكريم وسنحاول مساعدتك في الإجابة عليه ✨")

    # مدخل السؤال من المستخدم
    question = st.text_input("❓ سؤالك:", placeholder="مثال: كم عدد آيات سورة البقرة؟")

    if question:
        with st.spinner("⏳ جاري توليد الإجابة..."):
            try:
                prompt = f"سؤال: {question}\nإجابة:"
                result = generator(prompt, max_new_tokens=100, do_sample=True, top_k=50, top_p=0.95)
                answer = result[0]['generated_text'].split("إجابة:")[1].strip()
                st.success(f"✅ الإجابة: {answer}")
            except Exception as e:
                st.error(f"حدث خطأ أثناء محاولة الإجابة على سؤالك: {e}")

if __name__ == "__main__":
    app()
