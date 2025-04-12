import streamlit as st
from resume_parser import extract_text_from_pdf
from utils import create_pdf
import openai, os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="AI Resume Scanner", layout="centered")
st.title("📄 AI Resume Scanner & Matcher")

uploaded_resume = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])
job_desc = st.text_area("Paste the Job Description")

if st.button("Analyze Resume"):
    if not uploaded_resume or not job_desc.strip():
        st.warning("Please upload a resume and provide the job description.")
    else:
        with st.spinner("Analyzing resume..."):
            resume_text = extract_text_from_pdf(uploaded_resume)

            prompt = f"""You are an AI recruiter. Analyze the following resume against the job description. 
Provide:
- Match percentage
- Strengths
- Missing skills or gaps
- Final recommendation

Resume:
{resume_text}

Job Description:
{job_desc}"""

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5
            )

            result = response.choices[0].message.content
            st.success("✅ Analysis Complete")
            st.markdown(result)

            create_pdf(result, "resume_feedback.pdf")
            with open("resume_feedback.pdf", "rb") as f:
                st.download_button("📥 Download Feedback as PDF", f, file_name="resume_feedback.pdf")
