import streamlit as st

def app():
    theme = {
        "primary": "#2E7D32",
        "secondary": "#00796B",
        "accent": "#FFC107",
        "background": "#F9F9F9",
        "text": "#333333",
        "highlight": "#AED581"
    }
    
    st.markdown(f"""
    <style>
        .fade-in {{
            animation: fadeIn 0.9s ease-in-out;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(25px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .container {{
            max-width: 720px;
            margin: 80px auto 60px auto;
            background-color: white;
            padding: 40px 50px 50px 50px;
            border-radius: 15px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.12);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: {theme['text']};
            line-height: 1.65;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .title {{
            color: {theme['primary']};
            font-size: 3rem;
            font-weight: 900;
            margin-bottom: 5px;
            text-align: center;
            letter-spacing: 1.1px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .title img {{
            width: 48px;
            height: 48px;
        }}
        .subtitle {{
            color: {theme['secondary']};
            font-size: 1.2rem;
            font-style: italic;
            text-align: center;
            margin-bottom: 40px;
            max-width: 600px;
        }}
        .features {{
            list-style: none;
            padding: 0;
            max-width: 600px;
        }}
        .features li {{
            background: {theme['highlight']};
            color: {theme['primary']};
            font-weight: 600;
            font-size: 1.15rem;
            margin: 14px 0;
            padding: 14px 22px 14px 50px;
            border-radius: 10px;
            box-shadow: 0 3px 8px rgba(46, 125, 50, 0.15);
            position: relative;
            transition: background-color 0.3s ease;
        }}
        .features li:hover {{
            background-color: {theme['accent']};
            color: #222;
            cursor: default;
            box-shadow: 0 5px 15px rgba(255, 193, 7, 0.3);
        }}
        .features li::before {{
            content: "✔";
            position: absolute;
            left: 18px;
            top: 50%;
            transform: translateY(-50%);
            font-weight: 900;
            font-size: 1.3rem;
            color: {theme['primary']};
        }}
        .image-section {{
            margin: 30px 0 45px 0;
            max-width: 400px;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }}
        .image-section img {{
            width: 100%;
            height: auto;
            display: block;
            filter: drop-shadow(0 0 8px {theme['primary']});
            transition: transform 0.4s ease;
        }}
        .image-section img:hover {{
            transform: scale(1.05);
        }}
        .why-choose {{
            max-width: 650px;
            margin-bottom: 40px;
            text-align: center;
        }}
        .why-choose h3 {{
            color: {theme['primary']};
            font-size: 2rem;
            margin-bottom: 20px;
            font-weight: 800;
        }}
        .why-choose p {{
            font-size: 1.1rem;
            color: {theme['secondary']};
            line-height: 1.6;
        }}
        .contact {{
            margin-top: 30px;
            text-align: center;
            font-size: 1.2rem;
            font-weight: 600;
            color: {theme['secondary']};
            letter-spacing: 0.05em;
        }}
        .contact a {{
            color: {theme['accent']};
            text-decoration: none;
            font-weight: 700;
            transition: color 0.3s ease;
        }}
        .contact a:hover {{
            color: {theme['primary']};
            text-decoration: underline;
            cursor: pointer;
        }}
        @media (max-width: 768px) {{
            .container {{
                margin: 60px 20px 40px 20px;
                padding: 30px 20px 30px 20px;
            }}
            .title {{
                font-size: 2.2rem;
            }}
            .subtitle {{
                font-size: 1rem;
                margin-bottom: 28px;
            }}
            .features li {{
                font-size: 1rem;
                padding: 12px 18px 12px 45px;
            }}
            .why-choose h3 {{
                font-size: 1.5rem;
            }}
            .why-choose p {{
                font-size: 1rem;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="fade-in container">', unsafe_allow_html=True)

    # Title with Quran icon
    st.markdown("""
    <h1 class="title">
        <img src="https://cdn-icons-png.flaticon.com/512/3448/3448143.png" alt="Quran Icon"/>
        رفيق القرآن
    </h1>
    """, unsafe_allow_html=True)

    st.markdown('<p class="subtitle">رحلتك السهلة والممتعة لحفظ وتدبر كتاب الله</p>', unsafe_allow_html=True)

    # Features list
    st.markdown("""
    <ul class="features">
        <li>حفظ القرآن الكريم بأساليب مبسطة تناسب جميع المستويات</li>
        <li>تعلم التلاوة والتجويد بدقة مع تحسين الصوت</li>
        <li>تفسير مبسط يساعدك على فهم المعاني بوضوح</li>
        <li>مراجعة ذكية تضمن ثبات الحفظ وتثبيته</li>
        <li>تقارير متقدمة توضح تقدمك وتساعدك على الاستمرارية</li>
    </ul>
    """, unsafe_allow_html=True)

    # Image section
    st.markdown("""
    <div class="image-section">
        <img src="https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80" alt="Reading Quran" />
    </div>
    """, unsafe_allow_html=True)

    # Why choose section
    st.markdown("""
    <div class="why-choose">
        <h3>لماذا تختار رفيق القرآن؟</h3>
        <p>لأنه يجمع بين التكنولوجيا والروحانية، ليقدم لك تجربة حفظ وتعلم القرآن بشكل مبتكر، سهل، وفعال. مع دعم مستمر وأدوات متطورة تناسب إيقاع حياتك.</p>
    </div>
    """, unsafe_allow_html=True)

    # Contact info
    st.markdown("""
    <div class="contact">
        للمزيد من المعلومات والتواصل: 
        <a href="mailto:menatarek04@gmail.com">menatarek04@gmail.com</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
