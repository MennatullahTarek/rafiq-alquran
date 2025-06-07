import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
import io
import csv
from io import StringIO

import arabic_reshaper
from bidi.algorithm import get_display

# Mapping for surah names to numbers
surahs = {
    "الفاتحة": 1,
    # ... باقي السور ...
    "الناس": 114
}

### Agent 1: Fetcher - جلب بيانات الآية والتفسير
class QuranDataFetcher:
    def __init__(self, tafsir_id=91):
        self.tafsir_id = tafsir_id

    def get_ayah_text(self, surah, ayah):
        url = f"https://api.quran.com/api/v4/quran/verses/uthmani?verse_key={surah}:{ayah}"
        response = requests.get(url)
        if response.status_code == 200:
            try:
                return response.json()['verses'][0]['text_uthmani']
            except (KeyError, IndexError):
                return "⚠️ لم يتم العثور على نص الآية."
        else:
            return "❌ فشل في الاتصال بجلب نص الآية."

    def get_tafsir(self, surah, ayah):
        url = f"https://api.quran.com/api/v4/tafsirs/{self.tafsir_id}/by_ayah/{surah}:{ayah}"
        response = requests.get(url)
        if response.status_code == 200:
            try:
                return response.json()['tafsir']['text']
            except (KeyError, TypeError):
                return "⚠️ لم يتم العثور على التفسير."
        else:
            return "❌ فشل في الاتصال بالـ API."

### Agent 2: Renderer - تجهيز الصورة من النص
class ImageRenderer:
    def __init__(self, font_path="fonts/Amiri-Regular.ttf"):
        self.font_path = font_path

    def reshape_arabic_text(self, text):
        reshaped_text = arabic_reshaper.reshape(text)
        return get_display(reshaped_text)

    def text_to_image(self, text, tafsir, font_size=28, tafsir_font_size=18):
        width, height = 800, 600
        img = Image.new("RGB", (width, height), color="white")
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype(self.font_path, font_size)
            tafsir_font = ImageFont.truetype(self.font_path, tafsir_font_size)
        except IOError:
            font = ImageFont.load_default()
            tafsir_font = ImageFont.load_default()

        reshaped_text = self.reshape_arabic_text(text)
        reshaped_tafsir = self.reshape_arabic_text(tafsir)

        # كتابة نص الآية من اليمين لليسار
        draw.text((width - 50, 50), reshaped_text, fill="black", font=font, anchor="ra")

        # تقسيم التفسير إلى أسطر مناسبة للعرض
        lines = []
        words = reshaped_tafsir.split()
        line = ""
        for word in words:
            test_line = (line + " " + word).strip()
            if draw.textlength(test_line, font=tafsir_font) < width - 100:
                line = test_line
            else:
                lines.append(line)
                line = word
        lines.append(line)

        y_text = 150
        for line in lines:
            draw.text((50, y_text), line.strip(), fill="black", font=tafsir_font)
            y_text += tafsir_font_size + 8

        return img

### Agent 3: UI Manager - واجهة المستخدم وتفاعلها
class QuranAppUI:
    def __init__(self):
        self.fetcher = QuranDataFetcher()
        self.renderer = ImageRenderer()

    def run(self):
        st.title("📖 رفيق القرآن - مساعد التفسير الذكي")

        surah_name = st.selectbox("اختر السورة", list(surahs.keys()))
        ayah = st.number_input("🔢 رقم الآية", min_value=1, value=1)

        if st.button("📚 عرض التفسير"):
            st.info("⏳ جاري جلب نص الآية والتفسير من API...")
            surah_num = surahs[surah_name]
            ayah_text = self.fetcher.get_ayah_text(surah_num, ayah)
            tafsir = self.fetcher.get_tafsir(surah_num, ayah)

            st.subheader("📖 نص الآية:")
            st.markdown(f"<div style='font-size:28px; direction: rtl; text-align: right;'>{ayah_text}</div>", unsafe_allow_html=True)

            st.subheader("📗 التفسير:")
            st.markdown(tafsir, unsafe_allow_html=True)

            with st.expander("🖼️ عرض التفسير كصورة"):
                img = self.renderer.text_to_image(ayah_text, tafsir)
                st.image(img, caption=f"تفسير الآية {ayah} - {surah_name}")

            # توفير تحميل ملف CSV
            csv_buffer = StringIO()
            csv_writer = csv.writer(csv_buffer)
            csv_writer.writerow(["السورة", "رقم الآية", "نص الآية", "التفسير"])
            csv_writer.writerow([surah_name, ayah, ayah_text, tafsir])

            st.download_button(
                label="💾 تحميل التفسير كملف CSV",
                data=csv_buffer.getvalue(),
                file_name=f"tafsir_{surah_name}_{ayah}.csv",
                mime="text/csv"
            )

### Agent 4: (اختياري) StorageManager - لو حبيت توسع
# مثال: لحفظ التاريخ أو التفضيلات أو إدارة ملفات أكثر تعقيداً

if __name__ == "__main__":
    app = QuranAppUI()
    app.run()
