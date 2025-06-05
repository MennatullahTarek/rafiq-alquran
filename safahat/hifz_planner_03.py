import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def app():
    st.title("🧠📖 مٌخطط حفظ القرآن")
    st.markdown("خطط حفظك بناءً على قدراتك وعدد الأيام، وسيقوم رفيق القرآن بتقسيم الحفظ لك بطريقة ذكية 💡.")
    
    surah_name = st.text_input("اسم السورة", "البقرة")
    from_ayah = st.number_input("من الآية", min_value=1, value=1)
    to_ayah = st.number_input("إلى الآية", min_value=from_ayah, value=7)
    total_days = st.number_input("عدد أيام الحفظ", min_value=1, value=7)
    days_per_week = st.slider("كم يوم تحفظ في الأسبوع؟", 1, 7, 5)
    
    @st.cache_resource(show_spinner=False)
    def load_model():
        model_name = "aubmindlab/aragpt2-base"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        return tokenizer, model
    
    tokenizer, model = load_model()
    
    def generate_plan(prompt):
        inputs = tokenizer.encode(prompt, return_tensors="pt")
        outputs = model.generate(
            inputs,
            max_length=300,
            num_return_sequences=1,
            do_sample=True,
            top_p=0.9,
            temperature=0.7,
            pad_token_id=tokenizer.eos_token_id,
        )
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    def parse_to_table(plan_text):
        data = []
        for line in plan_text.split("\n"):
            if "اليوم" in line and "-" in line:
                parts = line.split("-")
                if len(parts) >= 2:
                    day = parts[0].strip()
                    verses = parts[1].strip()
                    note = parts[2].strip() if len(parts) > 2 else ""
                    data.append({"اليوم": day, "الآيات": verses, "ملاحظات": note})
        return data
    
    if st.button("أنشئ الخطة الذكية ✨"):
        with st.spinner("جاري توليد الخطة..."):
            try:
                prompt = f"""
                أنت مساعد ذكي في تعليم القرآن الكريم. مهمتك تقسيم حفظ سورة {surah_name} من الآية {from_ayah} إلى الآية {to_ayah}
                على {total_days} يوم، مع مراعاة:
                - تقسم الآيات حسب المعنى أو الطول المناسب.
                - يكون الحمل اليومي متوازن.
                - تظهر الخطة بشكل جدول: اليوم - الآيات - ملاحظات.
                أخرج النتيجة كجدول منظم واضح باللغة العربية.
                """
                plan_text = generate_plan(prompt)
                st.markdown("### ✨ خطة الحفظ الذكي:")
                st.text(plan_text)
    
                table_data = parse_to_table(plan_text)
                if table_data:
                    st.table(table_data)
                else:
                    st.info("لم أتمكن من تحويل الخطة إلى جدول. ربما تحتاج تعديل التنسيق قليلاً.")
    
            except Exception as e:
                st.error(f"حدث خطأ: {str(e)}")



if __name__ == "__main__":
    app()
