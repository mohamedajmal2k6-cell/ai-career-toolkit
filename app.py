import streamlit as st
import pandas as pd
from prompt_generator import generate_prompt
from resume_analyzer import extract_text, analyze_resume

# --- Page Config ---
st.set_page_config(page_title="AI Career Toolkit", layout="wide", page_icon="💼")

# --- CSS Styling ---
st.markdown("""
<style>
body {
    background-color: #f5f5f5;
}
.card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
h2 {
    color: #8A2BE2;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1 style='color:#8A2BE2;text-align:center;'>💼 AI Career Toolkit</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Generate career prompts & analyze your resume easily!</p>", unsafe_allow_html=True)
st.write("---")

# --- Sidebar ---
st.sidebar.header("💡 Tips & Tricks")
st.sidebar.write("""
- Upload your resume as **PDF or Image**
- Enter your **career goal** for relevant prompts
- Download prompts or resume feedback easily
""")

# --- Tabs ---
tab1, tab2 = st.tabs(["🧠 Smart Prompt Generator", "📄 AI Resume Analyzer"])

# --- Tab 1: Prompt Generator ---
with tab1:
    with st.container():
        st.subheader("Generate Career Prompts")
        career_goal = st.text_input("Enter your career goal (e.g., Frontend Developer, AI Engineer, Data Analyst):")
        number = st.slider("Number of prompts:", 1, 5, 3)

        if st.button("Generate Prompts"):
            if career_goal:
                result = generate_prompt(career_goal, number)
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.text_area("Generated Prompts:", "\n".join(result), height=200)
                st.download_button("📥 Download Prompts", "\n".join(result), file_name="prompts.txt")
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning("Please enter a career goal first.")

# --- Tab 2: Resume Analyzer ---
with tab2:
    with st.container():
        st.subheader("Upload & Analyze Resume")
        uploaded_file = st.file_uploader("Upload your resume (PDF, PNG, JPG, JPEG):", type=["pdf", "png", "jpg", "jpeg"])

        if uploaded_file:
            with st.spinner("🔍 Extracting text and analyzing resume..."):
                text = extract_text(uploaded_file)
                if text:
                    feedback, ats_score = analyze_resume(text)

                    # Display extracted text
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.text_area("📜 Extracted Text:", text, height=150)
                    st.markdown("</div>", unsafe_allow_html=True)

                    # Display feedback
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.text_area("💬 Feedback:", feedback, height=150)
                    st.markdown("</div>", unsafe_allow_html=True)

                    # ATS Score with color coding
                    if ats_score >= 80:
                        st.success(f"🌟 ATS Score: {ats_score}%")
                    elif ats_score >= 50:
                        st.warning(f"📈 ATS Score: {ats_score}%")
                    else:
                        st.error(f"⚠️ ATS Score: {ats_score}%")

                    st.download_button("📥 Download Feedback", feedback, file_name="resume_feedback.txt")

                    # Optional: Visualize found vs missing skills
                    text_lower = text.lower()
                    frontend_skills = ["html", "css", "javascript", "react", "tailwind", "bootstrap", "typescript"]
                    prompt_skills = ["prompt engineering", "openai", "llm", "langchain", "vertex ai", "gpt"]
                    general_skills = ["python", "git", "teamwork", "machine learning", "data analysis", "streamlit"]
                    all_skills = frontend_skills + prompt_skills + general_skills
                    found_skills = [s for s in all_skills if s in text_lower]
                    missing_skills = [s for s in all_skills if s not in text_lower]

                    df = pd.DataFrame({
                        'Skills': ['Found', 'Missing'],
                        'Count': [len(found_skills), len(missing_skills)]
                    })
                    st.bar_chart(df.set_index('Skills'))

                else:
                    st.error("Couldn't extract any text. Try uploading a typed resume or clearer image.")
