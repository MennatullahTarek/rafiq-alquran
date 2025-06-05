import streamlit as st


st.set_page_config(page_title="رفيق القرآن", layout="wide")

st.sidebar.title("القائمة الرئيسية")
page = st.sidebar.radio("اختر الصفحة:", [
    "لوحة التحكم",
    "الاستماع",
    "مُخطط الحفظ",
   "التفسير"
])

if page == "لوحة التحكم":
    import safahat.dash_01 as dash
    dash.app()

elif page ==  "الاستماع":
    import safahat.estimaa_02 as estimaa
    estimaa.app()

elif page == "مُخطط الحفظ":
    import safahat.hifz_planner_03 as hifz
    hifz.app()

elif page ==  "التفسير":
    import safahat.tafsir_04 as tafsir
    tafsir.app()
