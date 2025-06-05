import streamlit as st
import safahat.hifz_planner_03 as hifz

st.set_page_config(page_title="رفيق القرآن", layout="wide")

st.sidebar.title("القائمة الرئيسية")
page = st.sidebar.radio("اختر الصفحة:", [
    "لوحة التحكم",
    "التلاوة",
    "مُخطط الحفظ"
])

if page == "لوحة التحكم":
    import safahat.dash_01 as dash
    dash.app()

elif page == "التلاوة":
    import safahat.tilawa_02 as tilawa
    tilawa.app()

elif page == "مُخطط الحفظ":
    hifz.app()
