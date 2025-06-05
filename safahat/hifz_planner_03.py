import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

st.title("مُخطط حفظ القرآن  ")

model_name = "aubmindlab/aragpt2-base"

@st.cache_resource(show_spinner=False)
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_model()

surah_name = st.text_input("اسم السورة", "البقرة")
from_ayah = st.number_input("من الآية", min_value=1, value=1)
to_ayah = st.number_input("إلى الآية", min_value=from_ayah, value=7)
total_days = st.number_input("عدد أيام الحفظ", min_value=1, value=7)

if st.button("أنشئ الخطة"):
    prompt = f"قسم سورة {surah_name} من الآية {from_ayah} إلى الآية {to_ayah} على {total_days} يوم، مع خطة حفظ يومية واضحة باللغة العربية."
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(
        inputs,
        max_length=150,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        do_sample=True,
        temperature=0.7,
    )
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    st.markdown("### خطة الحفظ المقترحة:")
    st.write(result)
