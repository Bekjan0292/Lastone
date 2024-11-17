import streamlit as st

# Title for the About Page
st.markdown("<h1 style='text-align: center;'>About This Application</h1>", unsafe_allow_html=True)

# Full-width text styling
st.markdown(
    """
    <style>
    .full-width-text {
        width: 100%;
        margin: 0;
        padding: 0;
        text-align: justify;
        font-size: 18px;
        line-height: 1.6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# About Message
st.markdown(
    """
    <div class="full-width-text">
    This application was prepared for the course <strong>"Investments and Machine Learning"</strong> in 2024. It is designed specifically for beginners in the field of investments, providing an intuitive platform to learn and explore key concepts.

    Through tools for both <strong>technical analysis</strong> and <strong>fundamental analysis</strong>, this application helps users:
    - Understand essential financial metrics and indicators.
    - Make informed decisions for short-term and long-term investments.
    - Gain practical knowledge to start their investment journey with confidence.

    Thank you for using this application. We hope it serves as a helpful resource in your learning and growth as an investor!

    Nurbek, Baratov
    Gulrukh, Rakhimova
    Temur, Jurabekov
    Gulnar, Yermagambetova
    Bekjan, Jyrgalbek uulu
    </div>
    """,
    unsafe_allow_html=True
)
