# 🚀 HireReady – AI-Powered Job Application Assistant  
**Make your job applications smarter, faster, and interview-ready**  

---

## 📝 Overview  
Applying for jobs can be time-consuming — tailoring your resume and writing a personalized cover letter for each posting is hard work.  

**HireReady** automates the process:  
- **Analyzes job descriptions** to understand exactly what the employer needs  
- **Matches your resume** to those requirements  
- **Identifies missing skills** and suggests improvements  
- **Generates a tailored cover letter instantly**  
- **Optimizes your resume for the job role**  

---

## ✨ Features  
- **Job Description Analysis** – Understand employer requirements  
- **Resume Matching** – Get a match percentage and skill breakdown  
- **ATS Optimization Tips** – Pass Applicant Tracking Systems  
- **Skill Gap Insights** – See missing skills with suggestions  
- **Cover Letter Generator** – Unique AI-written letters  
- **Updated Resume Creation** – AI-optimized resume tailored to the job  
- **Interactive Visual Dashboards** – Skill matches displayed clearly  

---

## 🛠 Tech Stack  
- **Frontend/UI:** [Streamlit](https://streamlit.io/)  
- **AI Model:** [Google Gemini AI](https://ai.google/) via `langchain_google_genai`  
- **AI Orchestration:** [LangChain](https://www.langchain.com/)  
- **Visualization:** Plotly Express  
- **Data Processing:** Pandas  
- **Document Handling:** PyPDF2, python-docx  
- **PDF Generation:** ReportLab  
- **Environment Management:** Conda, python-dotenv  

---

## 🔍 How It Works (Simple Terms)  
1. **User enters API key** – Connect the app to Google Gemini AI  
2. **Paste the job description** – The AI breaks it down into key skill requirements  
3. **Upload resume** – Extracts and processes your resume’s text  
4. **AI compares both** – Finds matches, highlights gaps, and produces a score  
5. **Suggestions provided** – Offers ATS optimization and recommended changes  
6. **Document generation** – Creates a custom resume and cover letter  

---

## 📂 Project Structure  
┣ 📜 app.py                 # Main Streamlit app UI
┣ 📜 resume_optimizer.py    # Reads resumes, analyzes, generates updated resume
┣ 📜 job_analyzer.py        # Analyzes job descriptions and matches with resume
┣ 📜 coverletter.py         # Generates tailored cover letters & email-ready text
┣ 📜 requirements.txt       # Python dependencies
┣ 📜 .env                   # API keys and environment variables
┗ 📂 data / tests / etc.

## ⚙️ Setup & Installation  

### 1️⃣ Create Python Environment  
```bash
conda create -p env python==3.10 -y
conda activate env/

### Install dependencies
pip install -r requirements.txt

##Create project modules

##Set up environment variables
Create .env file:

#Run the application
streamlit run app.py