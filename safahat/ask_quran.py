import streamlit as st
from transformers import pipeline
import nest_asyncio

# لحل مشكلة event loop مع Streamlit
nest_asyncio.apply()

# تحميل النموذج من Hugging Face باستخدام التوكن
@st.cache_resource
def load_qa_pipeline():
    return pipeline(
        "question-answering",
        model="NeginShams/mbert-Quran_QA",
        tokenizer="NeginShams/mbert-Quran_QA",
        use_auth_token=st.secrets["huggingface_token"]
    )

def app():
    qa_pipeline = load_qa_pipeline()

    st.title("💬 اسأل عن القرآن")
    st.markdown("أكتب أي سؤال له علاقة بالقرآن الكريم وسنحاول مساعدتك في الإجابة عليه ✨")

    # مدخل السؤال من المستخدم
    question = st.text_input("❓ سؤالك:", placeholder="مثال: كم عدد آيات سورة البقرة؟")

    # سياق مبدئي بسيط (ممكن تطوره أو تحذفه)
    default_context = (
        "القرآن الكريم هو كتاب الله المنزل على النبي محمد صلى الله عليه وسلم، ويتكون من 114 سورة. "
        "منها سور مكية ومدنية، وتحتوي السور على آيات تتحدث عن العقيدة، والعبادات، والمعاملات، "
        "وقصص الأنبياء، والحكم، والمواعظ."
    )

    if question:
        with st.spinner("⏳ جاري البحث عن الإجابة..."):
            try:
                result = qa_pipeline(question=question, context=default_context)
                st.success(f"✅ الإجابة: {result['answer']}")
            except Exception as e:
                st.error(f"حدث خطأ أثناء محاولة الإجابة على سؤالك: {e}")

if __name__ == "__main__":
    app()
