import streamlit as st
import PyPDF2
import io
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load the API key from .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Configure Gemini API
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-pro")

# Streamlit UI
st.set_page_config(page_title="Resume Critiquer", page_icon="📄", layout="centered")
st.markdown("<h1 style='color: navy;'>📄 AI Resume Critiquer</h1>", unsafe_allow_html=True)
st.markdown("Upload your resume (PDF) and get AI-powered feedback!")

uploaded_file = st.file_uploader("Upload your resume", type=["pdf"])
job_role = st.text_input("Enter the job role you are targeting")
analyse = st.button("Analyze Resume")

# PDF text extraction
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")

# Analyze resume using Gemini
if analyse and uploaded_file:
    try:
        file_content = extract_text_from_file(uploaded_file)

        if not file_content.strip():
            st.error("File does not have any content.")
            st.stop()

        # Build prompt for Gemini
        prompt = f"""
Please analyze this resume and provide constructive feedback.
Focus on the following aspects:
1. Content clarity and impact
2. Skills presentation
3. Experience descriptions
4. Specific improvements for the job role: {job_role if job_role else 'general job applications'}

Resume content:
{file_content}

Please give your feedback in a structured and clear format.
"""

        response = model.generate_content(prompt)
        st.markdown("### 📝 Analysis Results")
        st.markdown(response.text)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
