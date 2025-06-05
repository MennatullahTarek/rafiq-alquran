import streamlit as st
import requests
import csv
from io import StringIO
from huggingface_hub import InferenceClient


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
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        try:
            return data['verses'][0]['text_uthmani']
        except (KeyError, IndexError):
            return None
    return None

def get_tafsir(surah_num, ayah_num, tafsir_id=91):  # tafsir_id 91: تفسير ابن كثير
    url = f"https://api.quran.com/api/v4/tafsirs/{tafsir_id}/by_ayah/{surah_num}:{ayah_num}"
    r = requests.get(url)
    if r.status_code == 200:
        try:
            return r.json()['tafsir']['text']
        except (KeyError, TypeError):
            return None
    return None

# --  (Agents) --

class DataAgent:
    def __init__(self, surah_name, start_ayah, end_ayah):
        self.surah_name = surah_name
        self.surah_num = surahs[surah_name]
        self.start_ayah = start_ayah
        self.end_ayah = end_ayah
        self.current_ayah = start_ayah

    def get_current_ayah(self):
        return get_ayah_text(self.surah_num, self.current_ayah)

    def get_current_tafsir(self):
        return get_tafsir(self.surah_num, self.current_ayah)

    def next_ayah(self):
        if self.current_ayah < self.end_ayah:
            self.current_ayah += 1
            return True
        return False

class MemorizationAgent:
    def __init__(self, surah_num, start_ayah, end_ayah):
        self.surah_num = surah_num
        self.start_ayah = start_ayah
        self.end_ayah = end_ayah

    def check_ayah(self, ayah_num, user_text):
        correct_text = get_ayah_text(self.surah_num, ayah_num)
        if not correct_text:
            return False, "لم أتمكن من جلب نص الآية."
        # مقارنة نص المستخدم مع النص الصحيح (ممكن تحسين المقارنة لاحقاً)
        if user_text.strip() == correct_text.strip():
            return True, "إجابتك صحيحة."
        else:
            return False, f"الإجابة غير صحيحة.\nالنص الصحيح:\n{correct_text}"

class TafsirAgent:
    def __init__(self, surah_num):
        self.surah_num = surah_num

    def check_tafsir(self, ayah_num, user_tafsir):
        correct_tafsir = get_tafsir(self.surah_num, ayah_num)
        if not correct_tafsir:
            return False, "لم أتمكن من جلب التفسير."
        # هنا ممكن نستخدم الذكاء الاصطناعي للمقارنة الذكية، لكن حالياً مقارنة نصية بسيطة:
        user_tafsir = user_tafsir.strip()
        if user_tafsir in correct_tafsir:
            return True, "تفسيرك مقبول."
        else:
            return False, "التفسير يحتاج مراجعة."

class LLMHelper:
    def __init__(self, token, model="bigscience/bloom"):
        self.client = InferenceClient(token=token)
        self.model = model

    def ask(self, prompt):
        response = self.client.text_generation(
            model=self.model,
            prompt=prompt,
            max_new_tokens=100
        )
        # response هي dict فيها key 'generated_text'
        return response.get('generated_text', '').strip()



def app():
    st.title("📖 اختبار حفظ وتفسير القرآن الكريم")

 
    if "data_agent" not in st.session_state:
        st.session_state.data_agent = None
    if "memorization_agent" not in st.session_state:
        st.session_state.memorization_agent = None
    if "tafsir_agent" not in st.session_state:
        st.session_state.tafsir_agent = None
    if "llm_helper" not in st.session_state:
        # ما تضيفش التوكن هنا مباشرة، خلي المستخدم يحط التوكن أو حط من env vars
        st.session_state.llm_helper = None

    if st.session_state.data_agent is None:
        # إدخال بيانات البداية
        surah_name = st.selectbox("اختر السورة", list(surahs.keys()))
        start_ayah = st.number_input("رقم بداية الآية", min_value=1, value=1)
        end_ayah = st.number_input("رقم نهاية الآية", min_value=start_ayah, value=start_ayah)

        token = st.text_input("أدخل Huggingface Token (لا يظهر)", type="password")

        if st.button("ابدأ الاختبار"):
            # إنشاء الوكلاء
            st.session_state.data_agent = DataAgent(surah_name, start_ayah, end_ayah)
            st.session_state.memorization_agent = MemorizationAgent(surahs[surah_name], start_ayah, end_ayah)
            st.session_state.tafsir_agent = TafsirAgent(surahs[surah_name])
            if token.strip() != "":
                st.session_state.llm_helper = LLMHelper(token.strip())
            else:
                st.warning("يُفضل إدخال توكن Huggingface للذكاء الاصطناعي")

            st.experimental_rerun()

    else:
        data_agent = st.session_state.data_agent
        mem_agent = st.session_state.memorization_agent
        tafsir_agent = st.session_state.tafsir_agent
        llm_helper = st.session_state.llm_helper

        current_ayah_num = data_agent.current_ayah
        st.markdown(f"### السورة: **{data_agent.surah_name}** - الآية رقم {current_ayah_num}")

        
        ayah_text = data_agent.get_current_ayah()
        if ayah_text:
           
            halfway = len(ayah_text) // 2
            part_ayah = ayah_text[:halfway] + "..."
            st.markdown(f"**نص الآية (جزء):** {part_ayah}")
        else:
            st.error("خطأ في جلب نص الآية")

        # اليوزر يكتب تكملة الآية
        user_memorization = st.text_area("أكمل نص الآية من عندك:", height=100)

        # اختبار الحفظ
        if st.button("تحقق من الحفظ"):
            if user_memorization.strip() == "":
                st.warning("من فضلك اكتب تكملة الآية")
            else:
                correct, feedback = mem_agent.check_ayah(current_ayah_num, user_memorization)
                st.markdown(f"**نتيجة الحفظ:** {feedback}")

                # استخدام LLM لتصحيح النص
                if llm_helper:
                    prompt = f"صحح النص التالي من القرآن: \"{user_memorization}\" وقل لي إذا كان صحيحًا أو به أخطاء."
                    correction = llm_helper.ask(prompt)
                    st.markdown(f"**تصحيح الذكاء الاصطناعي:** {correction}")

        # طلب تفسير الآية
        user_tafsir = st.text_area("اكتب تفسيرك أو شرحك للآية:", height=150)

        if st.button("تحقق من التفسير"):
            if user_tafsir.strip() == "":
                st.warning("من فضلك اكتب تفسيرًا")
            else:
                correct, feedback = tafsir_agent.check_tafsir(current_ayah_num, user_tafsir)
                st.markdown(f"**نتيجة التفسير:** {feedback}")

                if llm_helper:
                    prompt = f"قارن تفسير المستخدم التالي مع التفسير الصحيح وقل لي إذا كان صحيح أو يحتاج تصحيح:\n{user_tafsir}"
                    llm_feedback = llm_helper.ask(prompt)
                    st.markdown(f"**مراجعة الذكاء الاصطناعي:** {llm_feedback}")

        # زر الانتقال للآية التالية
        if st.button("الآية التالية"):
            if not data_agent.next_ayah():
                st.success("انتهت الآيات المحددة")
            else:
                # إعادة ضبط النصوص
                st.session_state.user_memorization = ""
                st.session_state.user_tafsir = ""
                st.experimental_rerun()

        # تسجيل النتائج
        if "results" not in st.session_state:
            st.session_state.results = []

        # حفظ الإجابات والتقييمات بعد كل تحقق (يمكن تحسين التوقيت)
        if st.button("حفظ النتيجة الحالية"):
            st.session_state.results.append({
                "ayah_number": current_ayah_num,
                "user_memorization": user_memorization,
                "memorization_feedback": feedback if 'feedback' in locals() else "",
                "user_tafsir": user_tafsir,
                "tafsir_feedback": feedback if 'feedback' in locals() else ""
            })
            st.success("تم حفظ النتيجة")

        # تنزيل الملف
        if st.session_state.results:
            csv_buffer = StringIO()
            writer = csv.DictWriter(csv_buffer, fieldnames=["ayah_number", "user_memorization", "memorization_feedback", "user_tafsir", "tafsir_feedback"])
            writer.writeheader()
            writer.writerows(st.session_state.results)
            st.download_button(
                label="تحميل نتائجك كملف CSV",
                data=csv_buffer.getvalue(),
                file_name="quran_memorization_results.csv",
                mime="text/csv"
            )


if __name__ == "__main__":
    app()
