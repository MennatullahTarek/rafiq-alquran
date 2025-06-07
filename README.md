

# 📖 Rafiq Al-Quran: Your Intelligent Quran Companion

**Rafiq Al-Quran** is a cutting-edge, multi-agent AI system crafted to enrich your Quranic learning experience. Combining powerful language models with trusted Quranic APIs, it offers interactive memorization tools, high-quality audio playback, detailed tafsir (exegesis), and an intelligent Q\&A chatbot — all accessible via a sleek, Arabic-optimized interface built on Streamlit.

---
### 📱 App Screenshot  
![Rafiq Al-Quran Homepage](https://drive.google.com/uc?export=view&id=1C6XylFOiZKNhMkBCZE_XtRsM2nF0f14C)
 

---

## 🌟 Features at a Glance

### Multi-Agent Architecture

* **QuranAudioAgent**: Stream recitations from multiple renowned Qaris.
* **HifzAgent**: Personalized memorization tracking and progress logging.
* **TafsirAgent**: Access authentic verse explanations via Quran.com API.
* **Q\&A Agent**: AI-powered chatbot answering Quranic queries using the `AraELECTRA` LLM.

### Core Functionalities

* 🎧 Listen to any Ayah with your choice of reciter.
* 📝 Plan and monitor your memorization journey with customizable Hifz schedules.
* 🔍 Dive deep into verse-by-verse tafsir with trusted sources.
* 🤖 Engage with an intelligent Quranic chatbot supporting Arabic and English.
* 📊 Export progress and tafsir notes for offline review.


### Tech Stack
* **Python** + **Streamlit** (GUI)
* **Hugging Face Transformers** (`AraELECTRA` model)
* **Quran APIs**: MP3Quran, Alquran.cloud, Quran.com
* **Pandas** (Data logging) | **Matplotlib** (Visualization)
  

## Featured UI Elements: 

1. **Title & Quote**:  
   - "خيركم من تعلّم القرآن وعلمه" - النبي محمد ﷺ  
   - Sets the spiritual tone for the app.  

2. **Navigation Menu**:  
   - 📖 **تفسير** (Tafsir)  
   - 🎧 **استماع** (Audio Playback)  
   - 🗓️ **مخطط الحفظ** (Hifz Planner)  
   - 🤖 **سؤال قرآني** (Q&A Chatbot)  
   - 🏠 **الرئيسية** (Home)  

3. **Daily Ayah**:  
   - Rotates inspirational verses (e.g., "إن مع العسر يسرا").  

---

---

## 🚀 Getting Started

## 🖥️ Live Demo & Interface  
Experience Rafiq Al-Quran instantly:  
🔗 **[Try the Live Demo](https://rafiq-alquran-bhrre6ptt6ke4bt3jhr25e.streamlit.app/)**  

### Navigation

Use the intuitive bottom menu to explore:

* **🏠 Home:** Daily inspirational Ayah and quick links
* **🎧 Audio:** Select Surah and Qari for recitation
* **📖 Tafsir:** Explore verse explanations
* **🤖 Q\&A:** Chat with the Quranic AI assistant
* **📝 Hifz Planner:** Create and manage your memorization plan

### Export Data
* Download memorization logs (`hifz_helper.py`).
* Save tafsir notes as CSV (`tafsir.py`).

---

## 📂 Project Structure

```
rafiq-alquran/
├── app.py                # Main Streamlit application
├── estimaa.py            # QuranAudioAgent implementation
├── hifz_helper.py        # HifzAgent for memorization tracking
├── hifz_planner.py       # Memorization schedule planner
├── morajaa.py            # Interactive review game
├── tafsir.py             # TafsirAgent accessing Quran.com API
├── ask_quran.py          # Q&A Agent with AraELECTRA LLM integration
├── data/                 # Exported logs and user data
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## 🌐 APIs & Models

* **Audio Sources:** [MP3Quran.net API](https://mp3quran.net/api)
* **Tafsir & Verse Data:** [Quran.com API](https://quran.api-docs.io/)
* **Verse Lookup:** [Alquran.cloud API](https://alquran.cloud/api)
* **Language Model:** Hugging Face `AraELECTRA` for Arabic NLP

---

## 🎯 Why Rafiq Al-Quran?

This project bridges technology and spirituality by providing a comprehensive, AI-enhanced toolkit for Quran learners. Its multi-agent design ensures modular, scalable, and responsive interactions — empowering users to engage deeply with the Quran in a personalized and meaningful way.

---

## 📧 Contact

For questions, feedback, or collaboration:
**Email:** [menatarek04@gmail.com](mailto:menatarek04@gmail.com)

---





