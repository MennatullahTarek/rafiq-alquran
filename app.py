import streamlit as st


st.set_page_config(page_title="رفيق القرآن", layout="wide")

st.sidebar.title("القائمة الرئيسية")
page = st.sidebar.radio("اختر الصفحة:", [
    "لوحة التحكم",
    "الاستماع",
    "مُخطط الحفظ",
   "مُساعد الحفظ (تكرار)",
    "تفسير",
    "لعبة المراجعة"
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

elif page ==  "مُساعد الحفظ (تكرار)":
    import safahat.hifz_helper_04 as helper
    helper.app()

elif page ==  "تفسير":
    import safahat.tafsir_05 as tafsir
    tafsir.app()

elif page =="لعبة المراجعة":
    import safahat.moraj3a as memory
    memory.app()
