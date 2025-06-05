import streamlit as st
import requests

def get_tafsirs_list():
    url = "https://api.quran.com/api/v4/tafsirs"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        tafsirs = data.get("tafsirs", [])
        if not tafsirs:
            st.error("❌ قائمة التفسيرات فارغة! الرجاء التأكد من الاتصال بالإنترنت أو صحة API.")
        return tafsirs
    else:
        st.error(f"❌ حدث خطأ في جلب قائمة التفسيرات: {response.status_code}")
        return []

def get_tafsir(surah_num, ayah_num, tafsir_id):
    url = f"https://api.quran.com/api/v4/verses/by_key/{surah_num}:{ayah_num}?language=ar&tafsirs={tafsir_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        try:
            tafsir_text = data["verse"]["tafsirs"][0]["text"]
            return tafsir_text
        except (KeyError, IndexError):
            return None
    else:
        st.error(f"❌ حدث خطأ في جلب التفسير: {response.status_code}")
        return None

def app():
    st.title("📖 تفسير الميسر للقرآن الكريم")

    tafsirs = get_tafsirs_list()
    if not tafsirs:
        st.stop()  # توقف التنفيذ إذا القائمة فاضية

    # خليه يجيب التفسير الميسر فقط (tafsir2)
    tafsir_muyassar = next((t for t in tafsirs if t["id"] == 2), None)
    if tafsir_muyassar is None:
        st.error("❌ تفسير الميسر غير موجود في القائمة.")
        st.stop()

    surah_list = [
        ("الفاتحة", 1),
        ("البقرة", 2),
        ("آل عمران", 3),
        ("النساء", 4),
        ("المائدة", 5),
        # ممكن تضيف المزيد من السور حسب الحاجة
    ]

    surah_name = st.selectbox("اختر السورة", [name for name, _ in surah_list])
    surah_number = dict(surah_list)[surah_name]
    aya_number = st.number_input("اكتب رقم الآية", min_value=1, step=1)

    if st.button("عرض التفسير الميسر"):
        st.info("جاري جلب التفسير الميسر ...")
        tafsir_text = get_tafsir(surah_number, aya_number, tafsir_muyassar["id"])

        if tafsir_text:
            st.markdown(f"### تفسير الآية {aya_number} من سورة {surah_name}")
            st.write(tafsir_text)
        else:
            st.error("❌ لم يتم العثور على تفسير لهذه الآية.")

if __name__ == "__main__":
    app()
