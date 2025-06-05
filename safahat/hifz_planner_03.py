import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from fpdf import FPDF
from io import BytesIO
import pandas as pd

def app():
    st.title("🧠📖 مٌخطط حفظ القرآن")

    st.markdown("خطط حفظك بناءً على قدراتك وعدد الأيام، وسيقوم رفيق القرآن بتقسيم الحفظ لك بطريقة ذكية 💡.")

    # إدخال بيانات المستخدم
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
        text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return text

    def parse_plan_to_df(plan_text):
        lines = plan_text.strip().split('\n')
        rows = []
        for line in lines:
            if "اليوم" in line:
                try:
                    day_part, rest = line.split(":", 1)
                    ayat_part, notes = rest.split(" - ", 1)
                    rows.append({
                        "اليوم": day_part.strip(),
                        "الآيات": ayat_part.strip(),
                        "ملاحظات": notes.strip()
                    })
                except:
                    rows.append({"اليوم": "", "الآيات": "", "ملاحظات": line})
        return pd.DataFrame(rows)

    if st.button("أنشئ الخطة الذكية ✨"):
        prompt = f"""
        أنت مساعد ذكي في تعليم القرآن الكريم. مهمتك تقسيم حفظ سورة {surah_name} من الآية {from_ayah} إلى الآية {to_ayah}
        على {total_days} يوم، مع مراعاة:
        - تقسم الآيات حسب المعنى أو الطول المناسب.
        - يكون الحمل اليومي متوازن.
        - تظهر الخطة بشكل جدول: اليوم - الآيات - ملاحظات.
        أخرج النتيجة كجدول منظم واضح باللغة العربية.
        """

        with st.spinner("جاري توليد الخطة..."):
            try:
                plan_text = generate_plan(prompt)
                st.markdown("### ✨ خطة الحفظ الذكي:")
                st.text(plan_text)

                df = parse_plan_to_df(plan_text)
                if not df.empty:
                    st.markdown("### جدول خطة الحفظ:")
                    st.dataframe(df, use_container_width=True)
                else:
                    st.warning("لم يتمكن التطبيق من استخراج جدول من الخطة، يرجى مراجعة النص الناتج.")

                def create_pdf(text):
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
                    for line in text.split('\n'):
                        pdf.cell(0, 10, txt=line, ln=True, align='R')
                    pdf_output = BytesIO()
                    pdf.output(pdf_output)
                    pdf_output.seek(0)
                    return pdf_output

                pdf_data = create_pdf(plan_text)
                st.download_button("📄 تحميل الخطة كـ PDF", data=pdf_data, file_name="خطة_الحفظ.pdf")

            except Exception as e:
                st.error(f"حدث خطأ: {str(e)}")


if __name__ == "__main__":
    app()
