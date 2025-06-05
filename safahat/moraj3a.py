import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
from io import StringIO
import csv
from huggingface_hub import InferenceClient


import os
HF_TOKEN = os.getenv("HF_TOKEN")  

HF_MODEL = "gpt2"  


client = InferenceClient(model=HF_MODEL, token=HF_TOKEN)



surahs = {
    "الفاتحة": 1,
    "البقرة": 2,
    "آل عمران": 3,
    "النساء": 4,
    "المائدة": 5,
    "الأنعام": 6,
    "الأعراف": 7,
    "الأنفال": 8,
    "التوبة": 9,
    "يونس": 10,
    "هود": 11,
    "يوسف": 12,
    "الرعد": 13,
    "إبراهيم": 14,
    "الحجر": 15,
    "النحل": 16,
    "الإسراء": 17,
    "الكهف": 18,
    "مريم": 19,
    "طه": 20,
    "الأنبياء": 21,
    "الحج": 22,
    "المؤمنون": 23,
    "النور": 24,
    "الفرقان": 25,
    "الشعراء": 26,
    "النمل": 27,
    "القصص": 28,
    "العنكبوت": 29,
    "الروم": 30,
    "لقمان": 31,
    "السجدة": 32,
    "الأحزاب": 33,
    "سبأ": 34,
    "فاطر": 35,
    "يس": 36,
    "الصافات": 37,
    "ص": 38,
    "الزمر": 39,
    "غافر": 40,
    "فصلت": 41,
    "الشورى": 42,
    "الزخرف": 43,
    "الدخان": 44,
    "الجاثية": 45,
    "الأحقاف": 46,
    "محمد": 47,
    "الفتح": 48,
    "الحجرات": 49,
    "ق": 50,
    "الذاريات": 51,
    "الطور": 52,
    "النجم": 53,
    "القمر": 54,
    "الرحمن": 55,
    "الواقعة": 56,
    "الحديد": 57,
    "المجادلة": 58,
    "الحشر": 59,
    "الممتحنة": 60,
    "الصف": 61,
    "الجمعة": 62,
    "المنافقون": 63,
    "التغابن": 64,
    "الطلاق": 65,
    "التحريم": 66,
    "الملك": 67,
    "القلم": 68,
    "الحاقة": 69,
    "المعارج": 70,
    "نوح": 71,
    "الجن": 72,
    "المزّمّل": 73,
    "المدّثر": 74,
    "القيامة": 75,
    "الإنسان": 76,
    "المرسلات": 77,
    "النبأ": 78,
    "النازعات": 79,
    "عبس": 80,
    "التكوير": 81,
    "الإنفطار": 82,
    "المطفّفين": 83,
    "الإنشقاق": 84,
    "البروج": 85,
    "الطارق": 86,
    "الأعلى": 87,
    "الغاشية": 88,
    "الفجر": 89,
    "البلد": 90,
    "الشمس": 91,
    "الليل": 92,
    "الضحى": 93,
    "الشرح": 94,
    "التين": 95,
    "العلق": 96,
    "القدر": 97,
    "البينة": 98,
    "الزلزلة": 99,
    "العاديات": 100,
    "القارعة": 101,
    "التكاثر": 102,
    "العصر": 103,
    "الهمزة": 104,
    "الفيل": 105,
    "قريش": 106,
    "الماعون": 107,
    "الكوثر": 108,
    "الكافرون": 109,
    "النصر": 110,
    "المسد": 111,
    "الإخلاص": 112,
    "الفلق": 113,
    "الناس": 114
}


def get_ayah_text(surah_num, ayah_num):
    url = f"https://api.quran.com/api/v4/quran/verses/uthmani?verse_key={surah_num}:{ayah_num}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()['verses'][0]['text_uthmani']
        except Exception:
            return "⚠️ لم يتم العثور على نص الآية."
    else:
        return "❌ فشل في الاتصال بجلب نص الآية."

def get_tafsir(surah_num, ayah_num, tafsir_id=91):
    url = f"https://api.quran.com/api/v4/tafsirs/{tafsir_id}/by_ayah/{surah_num}:{ayah_num}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()['tafsir']['text']
        except Exception:
            return "⚠️ لم يتم العثور على التفسير."
    else:
        return "❌ فشل في الاتصال بجلب التفسير."

# 6- دالة لتحويل النص والصورة (اختياري - ممكن تستخدم للعرض بصيغة صورة)
def text_to_image(text, tafsir, font_path="arial.ttf", font_size=28, tafsir_font_size=18):
    width, height = 800, 600
    img = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype(font_path, font_size)
        tafsir_font = ImageFont.truetype(font_path, tafsir_font_size)
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
        y_text += tafsir_font_size + 8  

    return img


class HuggingFaceLLM:
    def __init__(self, model_name=HF_MODEL, token=HF_TOKEN):
        self.model_name = model_name
        self.token = token
        self.client = InferenceClient(model=self.model_name, token=self.token)

    def generate_text(self, prompt, max_tokens=200):
        # استدعاء API
        response = self.client.text_generation(
            inputs=prompt,
            max_new_tokens=max_tokens,
            do_sample=True,
            temperature=0.7,
        )
        # response هي dict بها 'generated_text'
        return response.generated_text if hasattr(response, 'generated_text') else response[0]['generated_text']


class MemorizationAgent:
    def __init__(self, llm: HuggingFaceLLM):
        self.llm = llm
        self.memory = []

    def memorize(self, text):
        self.memory.append(text)
        return f"تم حفظ: {text}"

class InferenceAgent:
    def __init__(self, llm: HuggingFaceLLM):
        self.llm = llm

    def infer(self, prompt):
        return self.llm.generate_text(prompt)

class InteractionAgent:
    def __init__(self, llm: HuggingFaceLLM):
        self.llm = llm

    def interact(self, prompt):
        return self.llm.generate_text(prompt)


llm = HuggingFaceLLM()
memorization_agent = MemorizationAgent(llm)
inference_agent = InferenceAgent(llm)
interaction_agent = InteractionAgent(llm)


def app():
    st.title("📖 تفسير القرآن الكريم مع دعم LLM")


    surah_name = st.selectbox("اختر السورة", list(surahs.keys()))

  
    ayah_num = st.number_input("رقم الآية", min_value=1, value=1)

    if "memory" not in st.session_state:
        st.session_state.memory = []

    if st.button("📚 عرض التفسير والنص"):
        surah_num = surahs[surah_name]
        ayah_text = get_ayah_text(surah_num, ayah_num)
        tafsir = get_tafsir(surah_num, ayah_num)

        st.subheader("📖 نص الآية:")
        st.markdown(f"<div style='font-size:28px; direction: rtl; text-align: right;'>{ayah_text}</div>", unsafe_allow_html=True)

        st.subheader("📗 التفسير:")
        st.markdown(tafsir, unsafe_allow_html=True)

        # حفظ الذاكرة في session state (مثلاً تقدر تستخدم لحفظ الحوارات أو التفسيرات)
        st.session_state.memory.append({"surah": surah_name, "ayah": ayah_num, "text": ayah_text, "tafsir": tafsir})

        # عرض الذاكرة
        st.write("🧠 ذاكرة التفسير (جلسة المستخدم):")
        for i, mem in enumerate(st.session_state.memory):
            st.write(f"{i+1}. سورة {mem['surah']} آية {mem['ayah']}: {mem['text']}")

        # تحميل ملف CSV
        csv_buffer = StringIO()
        csv_writer = csv.writer(csv_buffer)
        csv_writer.writerow(["السورة", "رقم الآية", "نص الآية", "التفسير"])
        for mem in st.session_state.memory:
            csv_writer.writerow([mem['surah'], mem['ayah'], mem['text'], mem['tafsir']])

        st.download_button(
            label="💾 تحميل كل التفسيرات كملف CSV",
            data=csv_buffer.getvalue(),
            file_name=f"tafsir_all.csv",
            mime="text/csv"
        )

    # استخدام الـ agents
    st.markdown("---")
    st.subheader("🧠 استخدام الذاكرة - حفظ نص")
    text_to_memorize = st.text_input("اكتب نص للحفظ:")
    if st.button("حفظ النص"):
        result = memorization_agent.memorize(text_to_memorize)
        st.success(result)

    st.subheader("🤖 الاستنتاج من خلال LLM")
    prompt = st.text_area("ادخل نص للاستنتاج:")
    if st.button("استنتج"):
        answer = inference_agent.infer(prompt)
        st.markdown(f"**النتيجة:** {answer}")

    st.subheader("💬 التفاعل مع LLM")
    interaction_prompt = st.text_area("ادخل نص للتفاعل:")
    if st.button("تفاعل"):
        response = interaction_agent.interact(interaction_prompt)
        st.markdown(f"**الرد:** {response}")



if __name__ == "__main__":
    app()
