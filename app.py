
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
import os
# Importing custom classes
from job_Analyzer import JobAnalyzer
from coverletter import CoverLetterGenerator
from resume_optimizer import load_resume, generate_updated_resume

# Load environment variables
load_dotenv()

def main():
    st.set_page_config(page_title="HireReady - Job Application Assistant 📝", layout="wide")

    # ========== Sidebar ==========
    st.sidebar.title("⚙️ Settings")
    api_key = st.sidebar.text_input("Google Gemini API Key 🗝️", type="password")

    if not api_key:
        api_key = os.getenv("GOOGLE_API_KEY")

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎯 Tips for Success")
    st.sidebar.write("1️⃣ Enter your API Key")
    st.sidebar.write("2️⃣ Paste job description")  
    st.sidebar.write("3️⃣ Upload resume")
    st.sidebar.write("4️⃣ View AI analysis")
    st.sidebar.write("5️⃣ Generate documents")
    if not api_key:
        st.warning("🔑 Please enter your Google Gemini API key to continue")
        st.info("💡 Get one here: https://makersuite.google.com/app/apikey")
        return

    # ========== App Title & Intro ===========
    st.title("🚀 HireReady - Job Application Assistant")
    st.markdown("""
    Optimize your job application by **analyzing requirements**,  
    matching your resume, and **generating tailored cover letters**.

    _Powered by Google Gemini AI + LangChain ⚡_
    """)

    # ========== Initialize AI Services ==========
    try:
        job_analyzer = JobAnalyzer(api_key)
        cover_letter_gen = CoverLetterGenerator(api_key)
        st.success("✅ AI services are ready to use!")
    except Exception as e:
        st.error(f"❌ Service initialization failed: {e}")
        return

    # ========== Step 1 & Step 2: Inputs ==========
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📋 Step 1: Job Description")
        job_desc = st.text_area(
            "Paste the complete job description here:",
            height=300,
            placeholder="🔍 Include the requirements, responsibilities, and qualifications..."
        )
    with col2:
        st.subheader("📜 Step 2: Your Resume")
        resume_file = st.file_uploader(
            "Upload resume (PDF or DOCX)",
            type=['pdf', 'docx'],
            help="Ensure your file is text-based, not scanned"
        )

    # ========== Step 3: AI Analysis ==========
    if job_desc and resume_file:
        with st.spinner("🔍 Working on your analysis..."):
            resume_text = load_resume(resume_file)
            if not resume_text:
                st.error("❌ Could not read text from resume. Please check the file format.")
                return

            try:
                with st.status("Analyzing your application...") as status:
                    job_analysis = job_analyzer.analyze_job(job_desc)
                    status.update(label="Resumé analysis in progress...", state="running")
                    resume_analysis = job_analyzer.analyze_resume(resume_text)
                    status.update(label="Comparing job with resumé...", state="running")
                    match_analysis = job_analyzer.analyze_match(job_analysis, resume_analysis)
                    status.update(label="✅ Analysis complete!", state="complete")
            except Exception as e:
                st.error(f"❌ Error during analysis: {e}")
                return

        # ====== Results Metric Summary ======
        st.header("📊 Step 3: Analysis Summary")
        col1, col2, col3 = st.columns(3)
        match_percentage = match_analysis.get('overall_match_percentage', '0%')
        with col1:
            st.metric("🎯 Overall Match", match_percentage)
        with col2:
            st.metric("🧠 Matching Skills", len(match_analysis.get('matching_skills', [])))
        with col3:
            st.metric("📈 Skills to Improve", len(match_analysis.get('missing_skills', [])))

        try:
            st.progress(int(match_percentage.replace('%', '')) / 100)
        except:
            pass

        # ====== Detailed Tabs ======
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Skills Analysis",
            "🗂 Experience Match", 
            "💡 Recommendations",
            "💌 Cover Letter",
            "📝 Updated Resume"
        ])

       # Skills Tab
# Skills Tab
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("✅ Matching Skills")
                for skill in match_analysis.get('matching_skills', []):
                    st.success(f"✔ {skill.get('skill_name', skill) if isinstance(skill, dict) else skill}")
            with col2:
                st.subheader("⚠ Missing Skills")
                for skill in match_analysis.get('missing_skills', []):
                    if isinstance(skill, dict):
                        st.warning(f"⚠ {skill.get('skill_name', 'Unknown')}")
                        st.caption(f"💡 {skill.get('suggestion', '')}")
                    else:
                        st.warning(f"⚠ {skill}")

            # Pie chart instead of bar chart
            skills_data = pd.DataFrame({
                'Status': ['Matching', 'Missing'],
                'Count': [len(match_analysis.get('matching_skills', [])),
                        len(match_analysis.get('missing_skills', []))]
            })

            fig = px.pie(
                skills_data,
                names='Status',
                values='Count',
                color='Status',
                color_discrete_map={'Matching': '#5cb85c', 'Missing': '#e0403b'},
                title='Skills Overview'
            )
            fig.update_traces(textinfo='value+percent', pull=[0, 0.05])  # Slight pull for Missing slice
            st.plotly_chart(fig, use_container_width=True)

        # Experience Tab
        with tab2:
            st.subheader("Experience Match")
            st.write(match_analysis.get('experience_match_analysis', 'No data'))
            st.subheader("Education Match")
            st.write(match_analysis.get('education_match_analysis', 'No data'))
            col1, col2 = st.columns(2)
            col1.success(match_analysis.get('key_strengths', 'No strengths identified'))
            col2.info(match_analysis.get('areas_of_improvement', 'No improvements identified'))

        # Recommendations Tab
        with tab3:
            st.subheader("Key Recommendations")
            recs = match_analysis.get('recommendations_for_improvement', [])
            for i, rec in enumerate(recs, 1):
                if isinstance(rec, dict):
                    with st.expander(f"Recommendation {i}"):
                        st.write(f"**Section:** {rec.get('section', '')}")
                        st.write(f"**Guidance:** {rec.get('guidance', '')}")
                else:
                    st.info(f"{i}. {rec}")
            st.subheader("ATS Optimizations")
            ats_suggestions = match_analysis.get('ats_optimization_suggestions', [])
            for i, ats in enumerate(ats_suggestions, 1):
                with st.expander(f"ATS Suggestion {i}"):
                    st.write(ats)

        # Cover Letter Tab
        with tab4:
            st.subheader("Generate Cover Letter")
            tone = st.selectbox("Tone 🎭", ["professional", "enthusiastic", "confident", "friendly"])
            company_name = st.text_input("Company Name (optional)")
            if st.button("Generate Cover Letter ✍️"):
                with st.spinner("Creating cover letter..."):
                    letter = cover_letter_gen.generate_cover_letter(job_analysis, resume_analysis, match_analysis, tone)
                    st.text_area("Your Cover Letter", letter, height=400)
                    st.download_button("📥 Download", letter, f"cover_letter_{company_name or 'job'}.txt")

        # Updated Resume Tab
        with tab5:
            if st.button("Generate Updated Resume 📄"):
                with st.spinner("Optimizing resume..."):
                    updated_resume = generate_updated_resume(resume_text, match_analysis)
                    st.download_button("📥 Download Optimized Resume",
                                       updated_resume.getvalue(),
                                       f"optimized_resume_{company_name or 'updated'}.pdf",
                                       mime="application/pdf")

    else:
        st.info("👆 Please provide both job description and resume to start.")

if __name__ == "__main__":
    main()

