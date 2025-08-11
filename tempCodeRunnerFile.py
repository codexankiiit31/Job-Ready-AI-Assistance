import os
import json
import docx
import PyPDF2
import streamlit as st
from dotenv import load_dotenv
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyMuPDFLoader


# Load API key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

## utilities functions
def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text



def read_docx(file):
    """Read DOCX file"""
    try:
        doc = docx.Document(file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading DOCX: {str(e)}")
        return None

def load_resume(uploaded_file):
    """Load resume from uploaded file"""
    if not uploaded_file:
        return None
        
    try:
        if uploaded_file.name.lower().endswith('.pdf'):
            return read_pdf(uploaded_file)
        elif uploaded_file.name.lower().endswith('.docx'):
            return read_docx(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload PDF or DOCX files.")
            return None
    except Exception as e:
        st.error(f"Error loading resume: {str(e)}")
        return None

# LangChain + Gemini function for ATS match analysis
def get_match_analysis(resume_text, job_description):
    """Get ATS optimization suggestions"""
    if not GEMINI_API_KEY:
        st.error("Please set GOOGLE_API_KEY or GEMINI_API_KEY in your environment variables.")
        return {"ats_optimization_suggestions": []}
    
    prompt_template = """
    You are an ATS resume optimization assistant.
    Compare the following resume with the given job description
    and return JSON in this format:
    {{
        "ats_optimization_suggestions": [
            {{
                "section": "Section Name",
                "current_content": "Current text",
                "suggested_change": "Improved version",
                "keywords_to_add": ["keyword1", "keyword2"],
                "formatting_suggestion": "Any format improvements",
                "reason": "Why this change helps"
            }}
        ]
    }}

    Resume:
    {resume_text}

    Job Description:
    {job_description}
    
    Focus on:
    1. Keyword optimization for ATS systems
    2. Skills alignment with job requirements
    3. Action verb improvements
    4. Quantifiable achievements
    5. Industry-specific terminology
    """

    try:
        # Initialize the LLM
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash", 
            temperature=0.2, 
            google_api_key=GEMINI_API_KEY
        )
        
        # Create prompt template
        prompt = PromptTemplate(
            template=prompt_template, 
            input_variables=["resume_text", "job_description"]
        )
        
        # Create the chain using the new syntax
        chain = prompt | llm | StrOutputParser()
        
        # Invoke the chain
        response = chain.invoke({
            "resume_text": resume_text[:4000],  # Limit text length
            "job_description": job_description[:2000]
        })

        return json.loads(response)
    except json.JSONDecodeError:
        st.warning("Could not parse AI response. Returning empty suggestions.")
        return {"ats_optimization_suggestions": []}
    except Exception as e:
        st.error(f"Error getting match analysis: {str(e)}")
        return {"ats_optimization_suggestions": []}

# Generate updated resume function
def generate_updated_resume(resume_text, match_analysis):
    """Generate updated resume PDF with recommendations"""
    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                                rightMargin=40, leftMargin=40,
                                topMargin=60, bottomMargin=40)
        styles = getSampleStyleSheet()

        # Custom styles
        header_style = ParagraphStyle(
            name='CustomHeader',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=18,
            textColor=colors.HexColor('#1a1a1a'),
            alignment=1  # Center alignment
        )

        section_header_style = ParagraphStyle(
            name='SectionHeader',
            parent=styles['Heading2'],
            fontSize=13,
            spaceAfter=12,
            spaceBefore=16,
            textColor=colors.HexColor('#0d47a1'),
            borderWidth=1,
            borderColor=colors.HexColor('#0d47a1'),
            borderPadding=5
        )

        normal_style = ParagraphStyle(
            name='NormalText',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            spaceAfter=6,
        )

        bullet_style = ParagraphStyle(
            name='BulletStyle',
            parent=normal_style,
            bulletFontName='Helvetica',
            bulletFontSize=8,
            bulletIndent=10,
            leftIndent=20
        )

        recommendation_style = ParagraphStyle(
            name='RecommendationStyle',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#00695c'),
            leftIndent=25,
            spaceAfter=4,
            borderWidth=0.5,
            borderColor=colors.lightgrey,
            borderPadding=3
        )

        content = []
        content.append(Paragraph("Optimized Resume", header_style))
        content.append(Spacer(1, 12))

        # Process resume text
        resume_parts = resume_text.split("\n")
        current_section = ""
        bullets = []

        def flush_bullets():
            for bullet in bullets:
                if bullet.strip():
                    content.append(Paragraph(f"• {bullet.strip()}", bullet_style))
            bullets.clear()

        # Common section identifiers
        common_sections = [
            'EXPERIENCE', 'EDUCATION', 'SKILLS', 'PROJECTS', 'CERTIFICATIONS', 
            'SUMMARY', 'OBJECTIVE', 'WORK EXPERIENCE', 'PROFESSIONAL EXPERIENCE',
            'TECHNICAL SKILLS', 'ACHIEVEMENTS', 'AWARDS'
        ]

        # Process resume content
        for line in resume_parts:
            line = line.strip()
            if not line:
                continue

            # Check if line is a section header
            is_section = (line.isupper() and len(line) > 3) or \
                        any(section in line.upper() for section in common_sections)

            if is_section:
                flush_bullets()
                current_section = line
                content.append(Spacer(1, 12))
                content.append(Paragraph(current_section, section_header_style))
            else:
                bullets.append(line)

        flush_bullets()

        # Add optimization recommendations
        ats_suggestions = match_analysis.get('ats_optimization_suggestions', [])
        if ats_suggestions:
            content.append(Spacer(1, 20))
            content.append(Paragraph("ATS Optimization Recommendations", section_header_style))
            content.append(Spacer(1, 10))

            for i, suggestion in enumerate(ats_suggestions, 1):
                section = suggestion.get('section', 'General')
                current = suggestion.get('current_content', '')
                suggested = suggestion.get('suggested_change', '')
                keywords = ', '.join(suggestion.get('keywords_to_add', []))
                formatting = suggestion.get('formatting_suggestion', '')
                reason = suggestion.get('reason', '')

                content.append(Paragraph(f"<b>Recommendation {i}: {section}</b>", recommendation_style))
                
                if current:
                    content.append(Paragraph(f"Current: {current[:100]}{'...' if len(current) > 100 else ''}", recommendation_style))
                
                if suggested:
                    content.append(Paragraph(f"Suggestion: {suggested}", recommendation_style))
                
                if keywords:
                    content.append(Paragraph(f"Keywords to Add: {keywords}", recommendation_style))
                
                if formatting:
                    content.append(Paragraph(f"Formatting: {formatting}", recommendation_style))
                
                if reason:
                    content.append(Paragraph(f"Why: {reason}", recommendation_style))
                
                content.append(Spacer(1, 8))

        # Build the PDF
        doc.build(content)
        buffer.seek(0)
        return buffer
    
    except Exception as e:
        st.error(f"Error generating updated resume: {str(e)}")
        # Return empty buffer on error
        empty_buffer = BytesIO()
        return empty_buffer