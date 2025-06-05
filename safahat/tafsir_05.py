import streamlit as st
import requests

def get_tafsir_muyassar(surah_num, ayah_num):
    # هنا بنستخدم نسخة التفسير الميسر من AlQuran Cloud
    url = f"https://api.alquran.cloud/v1/ayah/{surah_num}:{ayah_num}/editions/quran-simple"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "data" in data and len(data["data"]) > 0:
            tafsir = data["data"][0].get("text", None)
            return tafsir
        else:
            return None
    else:
        st.error(f"❌ حدث خطأ في جلب التفسير: {response.status_code}")
        return None

def app():
    st.title("📖 التفسير الميسر باستخدام AlQuran Cloud")

    surah_list = [
        ("الفاتحة", 1),
        ("البقرة", 2),
        ("آل عمران", 3),
        ("النساء", 4),
        ("المائدة", 5),
    ]

    surah_name = st.selectbox("اختر السورة", [name for name, _ in surah_list])
    surah_number = dict(surah_list)[surah_name]
    aya_number = st.number_input("اكتب رقم الآية", min_value=1, step=1)

    if st.button("عرض التفسير الميسر"):
        st.info("جاري جلب التفسير الميسر ...")
        tafsir_text = get_tafsir_muyassar(surah_number, aya_number)

        if tafsir_text:
            st.markdown(f"### تفسير الآية {aya_number} من سورة {surah_name}")
            st.write(tafsir_text)
        else:
            st.error("❌ لم يتم العثور على تفسير لهذه الآية.")

if __name__ == "__main__":
    app()
