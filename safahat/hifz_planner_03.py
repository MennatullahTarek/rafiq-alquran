import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

tokenizer = AutoTokenizer.from_pretrained("gemini/gemini-2.0-flash")
model = AutoModelForCausalLM.from_pretrained("gemini/gemini-2.0-flash")

def generate_plan(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=500)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def app():
    st.title("🧠📖 مُخطط حفظ القرآن")

    surah_name = st.text_input("اسم السورة", "البقرة")
    from_ayah = st.number_input("من الآية", min_value=1, value=1)
    to_ayah = st.number_input("إلى الآية", min_value=from_ayah, value=7)
    total_days = st.number_input("عدد أيام الحفظ", min_value=1, value=7)
    days_per_week = st.slider("كم يوم تحفظ في الأسبوع؟", 1, 7, 5)

    if st.button("أنشئ الخطة الذكية ✨"):
        prompt = f"""
        أنت مساعد ذكي في تعليم القرآن الكريم. مهمتك تقسيم حفظ سورة {surah_name} من الآية {from_ayah} إلى الآية {to_ayah}
        على {total_days} يوم، مع مراعاة:
        - تقسم الآيات حسب المعنى أو الطول المناسب.
        - يكون الحمل اليومي متوازن.
        - تظهر الخطة بشكل جدول: اليوم - الآيات - ملاحظات.

        أخرج النتيجة كجدول منظم واضح باللغة العربية.
        """

        with st.spinner("جاري توليد الخطة الذكية..."):
            try:
                plan_text = generate_plan(prompt)
                st.markdown("### ✨ خطة الحفظ الذكي:")
                st.markdown(plan_text)
            except Exception as e:
                st.error(f"حدث خطأ: {str(e)}")
