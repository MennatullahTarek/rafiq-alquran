import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import pandas as pd
from fpdf import FPDF
from io import BytesIO
import re

def app():
    st.title("مُخطط حفظ القرآن على Streamlit Cloud")

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
        prompt = f"قسم سورة {surah_name} من الآية {from_ayah} إلى الآية {to_ayah} على {total_days} يوم، مع خطة حفظ يومية واضحة باللغة العربية بشكل جدول: اليوم - الآيات - ملاحظات."
        inputs = tokenizer.encode(prompt, return_tensors="pt")
        outputs = model.generate(
            inputs,
            max_length=300,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            do_sample=True,
            temperature=0.7,
        )
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)


        rows = []
        for line in result.split('\n'):

            match = re.match(r'اليوم\s*(\d+)\s*:\s*آيات\s*([\d\-،]+)\s*(.*)', line)
            if match:
                day = match.group(1)
                ayat = match.group(2)
                notes = match.group(3).strip()
                rows.append({"اليوم": day, "الآيات": ayat, "ملاحظات": notes})

        if rows:
            df = pd.DataFrame(rows)
            st.markdown("### خطة الحفظ في جدول:")
            st.dataframe(df)

            def create_pdf(dataframe):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=14)
                pdf.cell(0, 10, f"خطة حفظ سورة {surah_name}", ln=True, align='C')
                pdf.ln(10)
                pdf.set_font("Arial", size=12)

                # عرض الجدول
                col_widths = [30, 50, 110]
                headers = ["اليوم", "الآيات", "ملاحظات"]
                for i, header in enumerate(headers):
                    pdf.cell(col_widths[i], 10, header, border=1, align='C')
                pdf.ln()

                for _, row in dataframe.iterrows():
                    pdf.cell(col_widths[0], 10, str(row["اليوم"]), border=1, align='C')
                    pdf.cell(col_widths[1], 10, str(row["الآيات"]), border=1, align='C')
                    pdf.cell(col_widths[2], 10, str(row["ملاحظات"]), border=1, align='R')
                    pdf.ln()

                pdf_output = BytesIO()
                pdf.output(pdf_output)
                pdf_output.seek(0)
                return pdf_output

            pdf_file = create_pdf(df)
            st.download_button(
                label="📄 تحميل الخطة كملف PDF",
                data=pdf_file,
                file_name="خطة_الحفظ.pdf",
                mime="application/pdf"
            )
        else:
            st.markdown("### خطة الحفظ:")
            st.write(result)
