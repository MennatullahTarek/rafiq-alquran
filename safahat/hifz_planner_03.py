import streamlit as st
import math

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
            note = "راجع جيدًا" if day % 7 == 0 else ""
            plan.append({
                "اليوم": f"اليوم {day}",
                "الآيات": f"{start} - {end}",
                "ملاحظات": note
            })
            current_ayah = end + 1
            if current_ayah > to_ayah:
                break
    
        return plan
    
    
    if st.button("أنشئ الخطة الذكية ✨"):
        plan = create_plan(from_ayah, to_ayah, total_days)
        st.markdown("### ✨ خطة الحفظ الذكي:")
        st.table(plan)



if __name__ == "__main__":
    app()
