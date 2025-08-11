import json
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

class CoverLetterGenerator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.7,  # Higher creativity for cover letters
            google_api_key=api_key
        )
        self.output_parser = StrOutputParser()

    def generate_cover_letter(self, job_analysis: dict, resume_analysis: dict, match_analysis: dict,
                              tone: str = "professional") -> str:
        prompt_template = """
        Generate a compelling cover letter using this information:

        Job Details:
        {job}

        Candidate Details:
        {resume}

        Match Analysis:  
        {match}

        Tone: {tone}

        Requirements:
        1. Make it personal and specific to the job
        2. Highlight the strongest skill matches
        3. Address potential gaps professionally  
        4. Keep it concise but impactful (3-4 paragraphs)
        5. Use the specified tone: {tone}
        6. Include specific examples from the resume
        7. Make it ATS-friendly with relevant keywords
        8. Add a strong call to action
        9. Format as a proper business letter
        10. Don't exceed 400 words

        Generate a professional cover letter that will impress hiring managers.
        """

        try:
            # Create the chain
            prompt = PromptTemplate(
                template=prompt_template,
                input_variables=["job", "resume", "match", "tone"]
            )
            chain = prompt | self.llm | self.output_parser
            
            # Generate cover letter
            response = chain.invoke({
                "job": json.dumps(job_analysis, indent=2),
                "resume": json.dumps(resume_analysis, indent=2),
                "match": json.dumps(match_analysis, indent=2),
                "tone": tone
            })
            
            return response.strip()
            
        except Exception as e:
            st.error(f"Error generating cover letter: {str(e)}")
            return "Error generating cover letter. Please try again."

    def generate_custom_cover_letter(self, resume_text: str, job_description: str, 
                                   company_name: str = "", position_title: str = "", 
                                   tone: str = "professional") -> str:
        """Generate cover letter directly from resume and job description"""
        prompt_template = """
        Create a personalized cover letter based on:

        Resume:
        {resume_text}

        Job Description:
        {job_description}

        Company Name: {company_name}
        Position: {position_title}
        Tone: {tone}

        Instructions:
        1. Write a compelling opening that mentions the specific position
        2. Highlight 2-3 key qualifications that match the job requirements
        3. Include specific achievements from the resume with metrics
        4. Show enthusiasm for the company and role
        5. Address any potential concerns proactively
        6. End with a strong call to action
        7. Keep it professional and under 350 words
        8. Use {tone} tone throughout

        Format as a proper business letter with clear paragraphs.
        """

        try:
            # Create the chain
            prompt = PromptTemplate(
                template=prompt_template,
                input_variables=["resume_text", "job_description", "company_name", 
                               "position_title", "tone"]
            )
            chain = prompt | self.llm | self.output_parser
            
            # Generate cover letter
            response = chain.invoke({
                "resume_text": resume_text,
                "job_description": job_description,
                "company_name": company_name or "the company",
                "position_title": position_title or "this position",
                "tone": tone
            })
            
            return response.strip()
            
        except Exception as e:
            st.error(f"Error generating custom cover letter: {str(e)}")
            return "Error generating cover letter. Please try again."

    def get_cover_letter_tips(self, tone: str = "professional") -> str:
        """Generate cover letter writing tips"""
        prompt_template = """
        Provide 8-10 actionable tips for writing an excellent cover letter with a {tone} tone.
        
        Include tips about:
        1. Opening statements
        2. Body paragraph structure
        3. Closing statements
        4. Formatting and length
        5. Common mistakes to avoid
        6. ATS optimization
        7. Personalization techniques
        8. Industry-specific advice

        Format as a numbered list with brief explanations.
        """

        try:
            prompt = PromptTemplate(
                template=prompt_template,
                input_variables=["tone"]
            )
            chain = prompt | self.llm | self.output_parser
            
            response = chain.invoke({"tone": tone})
            return response.strip()
            
        except Exception as e:
            st.error(f"Error generating tips: {str(e)}")
            return "Error generating tips. Please try again."