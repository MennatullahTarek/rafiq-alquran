import streamlit as st
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch

# تحميل النموذج مرة واحدة (كفاءة أعلى)
@st.cache_resource
def load_quran_qa_model():
    tokenizer = AutoTokenizer.from_pretrained("mohammed-elkomy/quran-qa")
    model = AutoModelForQuestionAnswering.from_pretrained("mohammed-elkomy/quran-qa")
    return tokenizer, model

tokenizer, model = load_quran_qa_model()

# صفحة اسأل عن القرآن
def app():
    st.title("📖 اسأل عن القرآن")

    st.markdown("🕌 **اكتب أي سؤال متعلق بالقرآن الكريم** مثل:\n- كم عدد آيات سورة البقرة؟\n- هل سورة التكاثر مكية أم مدنية؟\n- لما نزلت سورة الطلاق؟")

    question = st.text_input("✍️ سؤالك هنا:")
    
    # يمكنك تحميل نص القرآن أو جزء منه لاستخدامه كسياق
    # هنا سنضع مثال مبسط فقط، ممكن تحسينه لاحقًا
    default_context = """
        الم (1) ذَٰلِكَ الْكِتَابُ لَا رَيْبَ ۛ فِيهِ ۛ هُدًى لِّلْمُتَّقِينَ (2) الَّذِينَ يُؤْمِنُونَ بِالْغَيْبِ وَيُقِيمُونَ الصَّلَاةَ...
    """

    context = st.text_area("📜 السياق (يمكن تركه فارغ لاستخدام جزء من القرآن):", value=default_context, height=150)

    if st.button("🔍 احصل على الإجابة"):
        if not question.strip():
            st.warning("من فضلك أدخل سؤال.")
        else:
            inputs = tokenizer.encode_plus(question, context, return_tensors="pt", truncation=True)
            with torch.no_grad():
                outputs = model(**inputs)
                answer_start = torch.argmax(outputs.start_logits)
                answer_end = torch.argmax(outputs.end_logits) + 1
                answer_ids = inputs["input_ids"][0][answer_start:answer_end]
                answer = tokenizer.decode(answer_ids, skip_special_tokens=True)
            st.success(f"💡 **الإجابة:** {answer}")
