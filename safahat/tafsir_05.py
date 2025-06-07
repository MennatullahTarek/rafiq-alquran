import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
import csv
from io import StringIO

# ------------------ Agent 1: Data Fetcher ------------------

class QuranDataFetcher:
    def __init__(self, tafsir_id=91):
        self.tafsir_id = tafsir_id
        self.surahs = {
            "الفاتحة": 1, "البقرة": 2, "آل عمران": 3, "النساء": 4, "المائدة": 5, "الأنعام": 6,
            "الأعراف": 7, "الأنفال": 8, "التوبة": 9, "يونس": 10, "هود": 11, "يوسف": 12,
            "الرعد": 13, "إبراهيم": 14, "الحجر": 15, "النحل": 16, "الإسراء": 17, "الكهف": 18,
            "مريم": 19, "طه": 20, "الأنبياء": 21, "الحج": 22, "المؤمنون": 23, "النور": 24,
            "الفرقان": 25, "الشعراء": 26, "النمل": 27, "القصص": 28, "العنكبوت": 29, "الروم": 30,
            "لقمان": 31, "السجدة": 32, "الأحزاب": 33, "سبأ": 34, "فاطر": 35, "يس": 36,
            "الصافات": 37, "ص": 38, "الزمر": 39, "غافر": 40, "فصلت": 41, "الشورى": 42,
            "الزخرف": 43, "الدخان": 44, "الجاثية": 45, "الأحقاف": 46, "محمد": 47, "الفتح": 48,
            "الحجرات": 49, "ق": 50, "الذاريات": 51, "الطور": 52, "النجم": 53, "القمر": 54,
            "الرحمن": 55, "الواقعة": 56, "الحديد": 57, "المجادلة": 58, "الحشر": 59,
            "الممتحنة": 60, "الصف": 61, "الجمعة": 62, "المنافقون": 63, "التغابن": 64,
            "الطلاق": 65, "التحريم": 66, "الملك": 67, "القلم": 68, "الحاقة": 69,
            "المعارج": 70, "نوح": 71, "الجن": 72, "المزّمّل": 73, "المدّثر": 74, "القيامة": 75,
            "الإنسان": 76, "المرسلات": 77, "النبأ": 78, "النازعات": 79, "عبس": 80,
            "التكوير": 81, "الإنفطار": 82, "المطفّفين": 83, "الإنشقاق": 84, "البروج": 85,
            "الطارق": 86, "الأعلى": 87, "الغاشية": 88, "الفجر": 89, "البلد": 90,
            "الشمس": 91, "الليل": 92, "الضحى": 93, "الشرح": 94, "التين": 95, "العلق": 96,
            "القدر": 97, "البينة": 98, "الزلزلة": 99, "العاديات": 100, "القارعة": 101,
            "التكاثر": 102, "العصر": 103, "الهمزة": 104, "الفيل": 105, "قريش": 106,
            "الماعون": 107, "الكوثر": 108, "الكافرون": 109, "النصر": 110, "المسد": 111,
            "الإخلاص": 112, "الفلق": 113, "الناس": 114
        }

    def get_tafsir(self, surah_num, ayah):
        url = f"https://api.quran.com/api/v4/tafsirs/{self.tafsir_id}/by_ayah/{surah_num}:{ayah}"
        response = requests.get(url)
        if response.status_code == 200:
            try:
                return response.json()['tafsir']['text']
            except (KeyError, TypeError):
                return "⚠️ لم يتم العثور على التفسير."
        else:
            return "❌ فشل في الاتصال بالـ API."

    def get_ayah_text(self, surah_num, ayah):
        url = f"https://api.quran.com/api/v4/quran/verses/uthmani?verse_key={surah_num}:{ayah}"
        response = requests.get(url)
        if response.status_code == 200:
            try:
                return response.json()['verses'][0]['text_uthmani']
            except (KeyError, IndexError):
                return "⚠️ لم يتم العثور على نص الآية."
        else:
            return "❌ فشل في الاتصال بجلب نص الآية."


# ------------------ Agent 2: Image Renderer ------------------

class ImageRenderer:
    def __init__(self, font_path="arial.ttf", font_size=28, tafsir_font_size=18):
        self.font_path = font_path
        self.font_size = font_size
        self.tafsir_font_size = tafsir_font_size

    def text_to_image(self, text, tafsir):
        width, height = 800, 600
        img = Image.new("RGB", (width, height), color="white")
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype(self.font_path, self.font_size)
            tafsir_font = ImageFont.truetype(self.font_path, self.tafsir_font_size)
        except IOError:
            font = ImageFont.load_default()
            tafsir_font = ImageFont.load_default()

        draw.text((width - 50, 50), text, fill="black", font=font, anchor="ra", direction="rtl")

        lines = []
        words = tafsir.split()
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
            y_text += self.tafsir_font_size + 8

        return img


# ------------------ Agent 3: UI Manager ------------------

class QuranAppUI:
    def __init__(self):
        self.data_fetcher = QuranDataFetcher()
        self.image_renderer = ImageRenderer()

    def run(self):
        st.set_page_config(page_title="📖 رفيق القرآن - مساعد التفسير الذكي", layout="centered")

        st.title("📖 تفسير القرآن الكريم ")
        st.markdown(
            "📖 هنا تقدر تختار السورة والآية اللي عايز تعرف تفسيرها، ورفيق القرآن هيجيب لك التفسير بطريقة واضحة وسهلة، "
            "وكمان تقدر تحفظ التفسير بصيغة CSV . استمتع بالمعرفة والتدبر✨",
            unsafe_allow_html=True
        )

        surah_name = st.selectbox("اختر السورة", list(self.data_fetcher.surahs.keys()))
        ayah = st.number_input("🔢 رقم الآية", min_value=1, value=1)

        if st.button("📚 عرض التفسير"):
            st.info("⏳ جاري جلب نص الآية والتفسير من API...")
            surah_num = self.data_fetcher.surahs[surah_name]
            ayah_text = self.data_fetcher.get_ayah_text(surah_num, ayah)
            tafsir = self.data_fetcher.get_tafsir(surah_num, ayah)

            st.subheader("📖 نص الآية:")
            st.markdown(f"<div style='font-size:28px; direction: rtl; text-align: right;'>{ayah_text}</div>", unsafe_allow_html=True)

            st.subheader("📗 التفسير:")
            st.markdown(tafsir, unsafe_allow_html=True)

            # Render image (optional)
            # img = self.image_renderer.text_to_image(ayah_text, tafsir)
            # st.image(img)

            # Prepare CSV
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


# ------------------ Main ------------------

def app():
    ui = QuranAppUI()
    ui.run()


if __name__ == "__main__":
    app()
