import streamlit as st
import openai
import pandas as pd
from fpdf import FPDF
from io import BytesIO
import json

openai.api_key = st.secrets["openai_api_key"]

def app():
    st.title("🧠📖 مٌخطط حفظ القرآن")

    st.markdown("خطط حفظك بناءً على قدراتك وعدد الأيام، وسيقوم رفيق القرآن بتقسيم الحفظ لك بطريقة ذكية 💡.")

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
        - أرجع الخطة كـ JSON يحتوي قائمة أيام، كل يوم به:
          "day": رقم اليوم،
          "verses": الآيات التي تحفظها في ذلك اليوم كنص،
          "notes": ملاحظات إذا وجدت.

        أعطني فقط ال JSON بدون أي شرح.
        """

        with st.spinner("جاري توليد الخطة الذكية..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o",  
                    messages=[
                        {"role": "system", "content": "أنت مساعد ذكي ومهذب في تعليم القرآن."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )

                plan_json_str = response['choices'][0]['message']['content']
           
                plan_json = json.loads(plan_json_str)

            
                df = pd.DataFrame(plan_json)

              
                st.markdown("### ✨ خطة الحفظ الذكي (جدول):")
                st.dataframe(df.style.set_properties(**{'text-align': 'right'}))

    
                def create_pdf_from_df(df):
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
                    pdf.cell(0, 10, "خطة الحفظ الذكي", ln=True, align="C")
                    pdf.ln(5)

                    col_widths = [20, 100, 60]  

                    headers = ["اليوم", "الآيات", "ملاحظات"]
                    for i, header in enumerate(headers):
                        pdf.cell(col_widths[i], 10, header, border=1, align='C')
                    pdf.ln()

                 
                    for idx, row in df.iterrows():
                        pdf.cell(col_widths[0], 10, str(row['day']), border=1, align='C')
                        pdf.multi_cell(col_widths[1], 10, row['verses'], border=1, align='R', max_line_height=pdf.font_size)
                     
                        x = pdf.get_x()
                        y = pdf.get_y()
                        pdf.set_xy(x + col_widths[1], y - pdf.font_size * (row['verses'].count('\n') + 1))
                        pdf.cell(col_widths[2], 10 * (row['verses'].count('\n') + 1), row.get('notes', ''), border=1, align='R')
                        pdf.ln()

                    pdf_output = BytesIO()
                    pdf.output(pdf_output)
                    pdf_output.seek(0)
                    return pdf_output

                pdf_data = create_pdf_from_df(df)
                st.download_button("📄 تحميل الخطة كـ PDF", data=pdf_data, file_name="خطة_الحفظ.pdf")

            except Exception as e:
                st.error(f"حدث خطأ: {str(e)}")
