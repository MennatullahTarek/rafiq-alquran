import streamlit as st
import math
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

def app():
    # Theme colors
    theme = {
        "primary": "#2E7D32",
        "secondary": "#00796B",
        "accent": "#FFC107",
        "background": "#F9F9F9",
        "text": "#333333",
        "highlight": "#AED581"
    }

    # Apply custom CSS
    st.markdown(f"""
        <style>
            html, body, .main {{
                background-color: {theme['background']};
                direction: rtl;
            }}
            .title-section {{
                text-align: center;
                color: {theme['primary']};
                font-size: 2.5rem;
                font-weight: 800;
                margin-bottom: 10px;
            }}
            .subtitle {{
                text-align: center;
                color: {theme['secondary']};
                font-size: 1.1rem;
                margin-bottom: 35px;
            }}
            .form-style {{
                max-width: 600px;
                margin: auto;
                padding: 10px;
            }}
            .result-title {{
                font-size: 1.3rem;
                font-weight: 700;
                color: {theme['text']};
                margin-top: 30px;
                margin-bottom: 10px;
            }}
        </style>
    """, unsafe_allow_html=True)

    # Title & subtitle
    st.markdown('<div class="title-section">🧠📖 مُخطط الحفظ الذكي</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">اصنع خطتك بنفسك بناءً على طاقتك وعدد الأيام، وسنقسمها لك بطريقة محفزة ومنظمة 🚀</div>', unsafe_allow_html=True)

    # Input fields inside styled form
    st.markdown('<div class="form-style">', unsafe_allow_html=True)
    surah_name = st.text_input("📘 اسم السورة", "البقرة")
    from_ayah = st.number_input("✳️ من الآية", min_value=1, value=1)
    to_ayah = st.number_input("🔚 إلى الآية", min_value=from_ayah, value=7)
    total_days = st.number_input("( المدة) عدد أيام الحفظ", min_value=1, value=7)
    days_per_week = st.slider("📅 كم يوم تحفظ في الأسبوع؟", 1, 7, 5)
    st.markdown('</div>', unsafe_allow_html=True)

    # Plan logic
    def create_plan(from_ayah, to_ayah, total_days):
        total_ayahs = to_ayah - from_ayah + 1
        ayahs_per_day = math.ceil(total_ayahs / total_days)
        plan = []
        current_ayah = from_ayah

        for day in range(1, total_days + 1):
            start = current_ayah
            end = min(current_ayah + ayahs_per_day - 1, to_ayah)

            if day % 7 == 0:
                note = "🌟 مراجعة عامة"
            elif day % 5 == 0:
                note = "🔁 تثبيت الحفظ"
            elif day % 3 == 0:
                note = "🔂 راجع ما سبق"
            elif day == 1:
                note = "✨ استعن بالله وابدأ بنية صادقة"
            else:
                note = "📖 واصل الحفظ بهمة"

            plan.append({
                "اليوم": f"اليوم {day}",
                "الآيات": f"{start} - {end}",
                "ملاحظات": note
            })

            current_ayah = end + 1
            if current_ayah > to_ayah:
                break

        return pd.DataFrame(plan)

  
    def plot_table(df):
        fig, ax = plt.subplots(figsize=(7, len(df) * 0.6 + 1))
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='right')
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1.2, 1.5)
        buf = BytesIO()
        plt.savefig(buf, format="png", bbox_inches='tight')
        buf.seek(0)
        return buf

  
    if st.button("✨ أنشئ الخطة الآن"):
        plan_df = create_plan(from_ayah, to_ayah, total_days)

        st.markdown('<div class="result-title">📋 خطة الحفظ التفصيلية:</div>', unsafe_allow_html=True)
        st.table(plan_df)

        csv = plan_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 تحميل الخطة كـ CSV",
            data=csv,
            file_name="خطة_الحفظ.csv",
            mime="text/csv",
        )

        img = plot_table(plan_df)
        st.download_button(
            label="🖼️ تحميل الخطة كصورة",
            data=img,
            file_name="خطة_الحفظ.png",
            mime="image/png"
        )



if __name__ == "__main__":
    app()
