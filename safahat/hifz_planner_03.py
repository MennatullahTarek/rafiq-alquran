import streamlit as st
from openai import OpenAI
from fpdf import FPDF
from io import BytesIO


def app():
    client = OpenAI()

    st.title("🧠📖 مٌخطط حفظ القرآن")

    st.markdown("خطط حفظك بناءً على قدراتك وعدد الأيام، وسيقوم رفيق القرآن بتقسيم الحفظ لك بطريقة ذكية 💡.")

    surah_name = st.text_input("اسم السورة", "البقرة")
    from_ayah = st.number_input("من الآية", min_value=1, value=1)
    to_ayah = st.number_input("إلى الآية", min_value=from_ayah, value=7)
    total_days = st.number_input(" المدة ", min_value=1, value=7)
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
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "أنت مساعد ذكي ومهذب في تعليم القرآن."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )

                plan_text = response.choices[0].message.content
                st.markdown("### ✨ خطة الحفظ الذكي:")
                st.markdown(plan_text)

                def create_pdf(text):
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
                    for line in text.split('\n'):
                        pdf.cell(200, 10, txt=line, ln=True, align='R')
                    pdf_output = BytesIO()
                    pdf.output(pdf_output)
                    pdf_output.seek(0)
                    return pdf_output

                pdf_data = create_pdf(plan_text)
                st.download_button("📄 تحميل الخطة كـ PDF", data=pdf_data, file_name="خطة_الحفظ.pdf")

            except Exception as e:
                st.error(f"حدث خطأ: {str(e)}")
