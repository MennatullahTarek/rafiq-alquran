import streamlit as st
import math
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

def app():
   
    st.title("🧠📖 مٌخطط حفظ القرآن")
    st.markdown("خطط حفظك بناءً على قدراتك وعدد الأيام، وسيقوم رفيق القرآن بتقسيم الحفظ لك بطريقة ذكية 💡.")
    
    
    surah_name = st.text_input("اسم السورة", "البقرة")
    from_ayah = st.number_input("من الآية", min_value=1, value=1)
    to_ayah = st.number_input("إلى الآية", min_value=from_ayah, value=7)
    total_days = st.number_input("عدد أيام الحفظ", min_value=1, value=7)
    days_per_week = st.slider("كم يوم تحفظ في الأسبوع؟", 1, 7, 5)
    
    
    def create_plan(from_ayah, to_ayah, total_days):
        total_ayahs = to_ayah - from_ayah + 1
        ayahs_per_day = math.ceil(total_ayahs / total_days)
        plan = []
        current_ayah = from_ayah
    
        for day in range(1, total_days + 1):
            start = current_ayah
            end = min(current_ayah + ayahs_per_day - 1, to_ayah)
    
            if day % 7 == 0:
                note = "مراجعة عامة"
            elif day % 5 == 0:
                note = "يوم تثبيت الحفظ"
            elif day % 3 == 0:
                note = "راجع ما سبق"
            elif day == 1:
                note = "استعن بالله وجدد النية"
            else:
                note = "استمر بالحفظ"
    
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
    
    if st.button("أنشئ الخطة الذكية ✨"):
        plan_df = create_plan(from_ayah, to_ayah, total_days)
        st.markdown("### ✨ خطة الحفظ الذكي:")
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
