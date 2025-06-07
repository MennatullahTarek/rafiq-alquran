import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
from io import StringIO
import csv

# === Agentic Persona ===
AGENT_NAME = "👳‍♂️ رفيق القرآن"
GREETING = f"{AGENT_NAME} هنا ليساعدك تتدبر في آيات القرآن الكريم وتتعلم من تفسيرها 🌙✨"

# === Surah Mapping ===
surahs = {
    "الفاتحة": 1, "البقرة": 2, "آل عمران": 3, "النساء": 4, "المائدة": 5,
    # truncated for brevity; keep full list from original code
    "الناس": 114
}

# === Agent Task 1: Fetch Tafsir ===
def get_tafsir(surah, ayah, tafsir_id=91):
    url = f"https://api.quran.com/api/v4/tafsirs/{tafsir_id}/by_ayah/{surah}:{ayah}"
    response = requests.get(url)
    if response.ok:
        return response.json().get('tafsir', {}).get('text', "⚠️ لم يتم العثور على التفسير.")
    return "❌ فشل الاتصال بجلب التفسير."

# === Agent Task 2: Fetch Ayah Text ===
def get_ayah(surah, ayah):
    url = f"https://api.quran.com/api/v4/quran/verses/uthmani?verse_key={surah}:{ayah}"
    response = requests.get(url)
    if response.ok:
        return response.json()['verses'][0].get('text_uthmani', "⚠️ لم يتم العثور على نص الآية.")
    return "❌ فشل الاتصال بجلب نص الآية."

# === Agent Task 3: Render as Image ===
def text_to_image(text, tafsir, font_path="arial.ttf", font_size=28, tafsir_font_size=18):
    width, height = 800, 600
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(font_path, font_size)
        tafsir_font = ImageFont.truetype(font_path, tafsir_font_size)
    except IOError:
        font = ImageFont.load_default()
        tafsir_font = ImageFont.load_default()
    draw.text((width - 50, 50), text, fill="black", font=font, anchor="ra", direction="rtl")
    words = tafsir.split()
    lines, line = [], ""
    for word in words:
        test = (line + " " + word).strip()
        if draw.textlength(test, font=tafsir_font) < width - 100:
            line = test
        else:
            lines.append(line)
            line = word
    lines.append(line)
    y = 150
    for l in lines:
        draw.text((50, y), l.strip(), fill="black", font=tafsir_font)
        y += tafsir_font_size + 8
    return img

# === Main App (Agent Interface) ===
def app():
    st.set_page_config(page_title="تفسير القرآن - رفيق القرآن", layout="centered", initial_sidebar_state="collapsed")
    st.title("📖 رفيق القرآن - مساعد التفسير الذكي")
    st.markdown(f"🌟 {GREETING}", unsafe_allow_html=True)

    with st.form("tafsir_form"):
        surah_name = st.selectbox("🔍 اختر السورة", list(surahs.keys()))
        ayah = st.number_input("🔢 رقم الآية", min_value=1, value=1)
        submit = st.form_submit_button("استخرج التفسير")

    if submit:
        st.info("⏳ جاري جلب التفسير والنص...")
        surah_num = surahs[surah_name]
        ayah_text = get_ayah(surah_num, ayah)
        tafsir = get_tafsir(surah_num, ayah)

        st.success("✅ تم جلب النتائج!")
        st.markdown("### 📖 نص الآية:")
        st.markdown(f"<div style='font-size:28px; direction: rtl; text-align: right;'>{ayah_text}</div>", unsafe_allow_html=True)

        st.markdown("### 📗 التفسير:")
        st.markdown(f"<div style='direction: rtl; text-align: right;'>{tafsir}</div>", unsafe_allow_html=True)

        # Optional export
        csv_buffer = StringIO()
        csv_writer = csv.writer(csv_buffer)
        csv_writer.writerow(["السورة", "رقم الآية", "نص الآية", "التفسير"])
        csv_writer.writerow([surah_name, ayah, ayah_text, tafsir])

        st.download_button("💾 تحميل بصيغة CSV", data=csv_buffer.getvalue(), file_name=f"{surah_name}_{ayah}.csv", mime="text/csv")

        # Optional image rendering
        with st.expander("🖼️ عرض التفسير كصورة"):
            img = text_to_image(ayah_text, tafsir)
            st.image(img, caption=f"تفسير الآية {ayah} - {surah_name}")

# Run app
if __name__ == "__main__":
    app()
