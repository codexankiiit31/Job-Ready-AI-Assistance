#### 🚀 HireReady – AI-Powered Job Application Assistant  
Make your job applications smarter, faster, and interview-ready.

## 🚀 Live Demo
You can try the live app here:https://job-ready-ai-assistance.streamlit.app/

## 📄 Overview  
Applying for jobs can be time-consuming — tailoring your resume and writing a personalized cover letter for each posting is hard work.  

**HireReady automates the process** to save you time and help you stand out.

---

## ✨ Features  
- **Job Description Analysis** – Understand exactly what employers are looking for.  
- **Resume Matching** – Get a match percentage and detailed skill breakdown.  
- **ATS Optimization Tips** – Improve your chances of passing Applicant Tracking Systems.  
- **Skill Gap Insights** – Identify missing skills and get actionable suggestions.  
- **Cover Letter Generator** – Unique, AI-written cover letters.  
- **Updated Resume Creation** – AI-tailored resumes based on job requirements.  
- **Interactive Dashboards** – Visualize your skill matches.  

---

## 🛠 Tech Stack  
- **Frontend/UI**: Streamlit  
- **AI Model**: Google Gemini AI (via `langchain_google_genai`)  
- **AI Orchestration**: LangChain  
- **Visualization**: Plotly Express  
- **Data Processing**: Pandas  
- **Document Handling**: PyPDF2, python-docx  
- **PDF Generation**: ReportLab  
- **Environment Management**: Conda, python-dotenv  

---

## 🔍 How It Works  
1. **Enter API Key** – Connect the app to Google Gemini AI.  
2. **Paste Job Description** – The AI analyzes and extracts key skill requirements.  
3. **Upload Resume** – The app compares your resume to the job description.  
4. **Get Feedback** – See matches, missing skills, and ATS optimization tips.  
5. **Generate Documents** – Create an updated resume and cover letter instantly.  

---
## ⚙️ Setup & Installation  

1- Create Python Environment  
   conda create -p env python==3.10 -y
   conda activate env/

2-Install dependencies
   pip install -r requirements.txt

3-Create project modules

4-Set up environment variables
 Create .env file:

5-Run the application
 streamlit run app.py 
