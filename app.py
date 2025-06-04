import streamlit as st

st.set_page_config(page_title="رفيق القرآن", layout="wide")

st.sidebar.title("📚 القائمة الرئيسية")
page = st.sidebar.radio("اختر الصفحة:", [
    "📊 لوحة التحكم",
])

if page == "📊 لوحة التحكم":
    import safahat.01_dash as dash
    dash.app()
