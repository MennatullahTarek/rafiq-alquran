import streamlit as st

def app():
    theme = {
        "primary": "#2E7D32",
        "secondary": "#009688",
        "accent": "#FFC107",
        "background": "#EDE7D9"
    }
    
    st.markdown(f"""
    <style>
        .fade-in {{
            animation: fadeIn 0.8s ease-in-out;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .app-title {{
            color: {theme['primary']};
            font-size: 38px;
            font-weight: bold;
            text-align: center;
            margin-top: 70px;
            margin-bottom: 20px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        .app-subtitle {{
            font-size: 20px;
            color: {theme['secondary']};
            text-align: center;
            margin-bottom: 40px;
            font-style: italic;
        }}
        .features-list {{
            font-size: 18px;
            line-height: 1.8;
            max-width: 650px;
            margin: auto;
            color: #444;
        }}
        .features-list li {{
            margin-bottom: 12px;
            padding-left: 24px;
            position: relative;
        }}
        .features-list li::before {{
            content: "🌟";
            position: absolute;
            left: 0;
            top: 0;
        }}
        .contact {{
            margin-top: 50px;
            text-align: center;
            font-size: 18px;
            color: {theme['primary']};
            font-weight: 600;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        .contact a {{
            color: {theme['accent']};
            text-decoration: none;
            font-weight: bold;
        }}
        .contact a:hover {{
            text-decoration: underline;
        }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    st.markdown('<div class="app-title">عن التطبيق</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">مرحبًا بك في <strong>رفيق القرآن</strong> 🌟</div>', unsafe_allow_html=True)

    st.markdown("""
    <ul class="features-list">
        <li>🕋 تطبيق شامل لمساعدتك في حفظ القرآن الكريم</li>
        <li>📖 تحسين التلاوة والتجويد</li>
        <li>🕯️ التدبر والتفسير اليومي</li>
        <li>🧠 مراجعة ذكية وتفاعلية</li>
        <li>📊 تصدير تقارير التقدم والملاحظات</li>
    </ul>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="contact">
        للمزيد من المعلومات تواصل معنا عبر: 
        <a href="mailto:menatarek04@gmail.com">menatarek04@gmail.com</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
