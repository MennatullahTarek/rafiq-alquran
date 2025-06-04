import streamlit as st

st.set_page_config(page_title="رفيق القرآن", layout="wide")

st.sidebar.title("القائمة الرئيسية")
page = st.sidebar.radio("اختر الصفحة:", [
    "لوحة التحكم",
    "التلاوة"
])

if page == "لوحة التحكم":
    import safahat.dash_01 as dash
    dash.app()

elif page == "التلاوة":
    import safahat.tilawa_02 as tilawa
    tilawa.app()
