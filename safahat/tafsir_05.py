import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
import io

# قاموس السور مع أرقامها
surahs = {
    "الفاتحة": 1,
    "البقرة": 2,
    "آل عمران": 3,
    "النساء": 4,
    "المائدة": 5,
    # ... أكمل باقي السور حسب الحاجة
}

def get_tafsir_quran_api(surah, ayah, tafsir_id=91):  
    url = f"https://api.quran.com/api/v4/tafsirs/{tafsir_id}/by_ayah/{surah}:{ayah}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()['tafsir']['text']
        except (KeyError, TypeError):
            return "⚠️ لم يتم العثور على التفسير."
    else:
        return "❌ فشل في الاتصال بالـ API."

def get_ayah_text(surah, ayah):
    url = f"https://api.quran.com/api/v4/quran/verses/uthmani?verse_key={surah}:{ayah}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()['verses'][0]['text_uthmani']
        except (KeyError, IndexError):
            return "⚠️ لم يتم العثور على نص الآية."
    else:
        return "❌ فشل في الاتصال بجلب نص الآية."

def text_to_image(text, tafsir, font_path="arial.ttf", font_size=24, tafsir_font_size=18):
    # إعداد صورة بيضاء كبيرة
    width, height = 800, 600
    img = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype(font_path, font_size)
        tafsir_font = ImageFont.truetype(font_path, tafsir_font_size)
    except IOError:
        font = ImageFont.load_default()
        tafsir_font = ImageFont.load_default()

    # رسم نص الآية في الأعلى (يمين لليسار)
    draw.text((width - 50, 50), text, fill="black", font=font, anchor="ra", direction="rtl")

    # رسم التفسير أسفل الآية
    # نحتاج تقسيم النص الطويل لأسطر متعددة
    lines = []
    words = tafsir.split()
    line = ""
    for word in words:
        if draw.textlength(line + " " + word, font=tafsir_font) < width - 100:
            line += " " + word
        else:
            lines.append(line)
            line = word
    lines.append(line)

    y_text = 150
    for line in lines:
        draw.text((50, y_text), line.strip(), fill="black", font=tafsir_font)
        y_text += tafsir_font_size + 5

    return img

def app():
    st.title("📖 تفسير آية من القرآن الكريم مع حفظ الصورة")
    
    surah_name = st.selectbox("اختر السورة", list(surahs.keys()))
    ayah = st.number_input("🔢 رقم الآية", min_value=1, value=1)
    
    if st.button("📚 عرض التفسير"):
        st.info("⏳ جاري جلب نص الآية والتفسير من API...")
        surah_num = surahs[surah_name]
        ayah_text = get_ayah_text(surah_num, ayah)
        tafsir = get_tafsir_quran_api(surah_num, ayah)

        st.subheader("📖 نص الآية:")
        st.markdown(f"<div style='font-size:28px; direction: rtl; text-align: right;'>{ayah_text}</div>", unsafe_allow_html=True)

        st.subheader("📗 التفسير:")
        st.markdown(tafsir, unsafe_allow_html=True)

        if st.button("💾 حفظ الصورة"):
            img = text_to_image(ayah_text, tafsir)
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            byte_im = buf.getvalue()
            st.image(img)
            st.download_button(label="⬇️ تحميل الصورة", data=byte_im, file_name=f"{surah_name}_{ayah}.png", mime="image/png")

if __name__ == "__main__":
    app()
