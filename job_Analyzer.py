import json
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

class JobAnalyzer:
    def __init__(self, api_key: str):
        self.api_key = api_key
        try:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                temperature=0.1,  # Lower temperature like your working version
                google_api_key=api_key
            )
            print("✅ JobAnalyzer initialized successfully with gemini-1.5-flash")
        except Exception as e:
            print(f"❌ Error initializing JobAnalyzer: {e}")
            raise e

    def analyze_job(self, job_description: str) -> dict:
        """Analyze job description - improved prompting based on your working version"""
        print(f"🔍 Starting job analysis...")
        
        prompt = """
        Analyze this job description and provide a detailed JSON with:
        1. Key technical skills required  
        2. Soft skills required
        3. Years of experience required
        4. Education requirements
        5. Key responsibilities
        6. Company culture indicators
        7. Required certifications
        8. Industry type
        9. Job level (entry, mid, senior)  
        10. Key technologies mentioned

        IMPORTANT: Respond ONLY with valid JSON format, no additional text.

        Format the response as this EXACT JSON structure:
        {{
            "technical_skills": ["skill1", "skill2", "skill3"],
            "soft_skills": ["communication", "teamwork"],
            "years_experience": "3-5 years",
            "education_requirements": ["Bachelor's in Computer Science"],
            "key_responsibilities": ["responsibility1", "responsibility2"],
            "company_culture": "collaborative, innovative environment",
            "certifications": ["AWS", "PMP"],
            "industry_type": "Technology",
            "job_level": "mid-level",
            "key_technologies": ["Python", "AWS", "Docker"]
        }}

        Job Description:
        {description}
        """

        try:
            # Fixed: Extract content from AIMessage object
            response = self.llm.invoke(prompt.format(description=job_description[:3000]))
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            print(f"📥 Job analysis response received: {response_text[:200]}...")
            
            # Clean response
            response_text = response_text.strip()
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            parsed_response = json.loads(response_text)
            print("✅ Job analysis successful!")
            return parsed_response
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            print(f"Debug - Response content: {response_text}")
            st.error("Error parsing job analysis response. Please check the job description format.")
            return {}
        except Exception as e:
            print(f"❌ Error analyzing job: {str(e)}")
            st.error(f"Error analyzing job description: {str(e)}")
            return {}

    def analyze_resume(self, resume_text: str) -> dict:
        """Analyze resume - improved prompting based on your working version"""
        print(f"🔍 Starting resume analysis...")
        
        prompt = """
        Analyze this resume and provide a detailed JSON with:
        1. Technical skills
        2. Soft skills
        3. Years of experience
        4. Education details
        5. Key achievements
        6. Core competencies  
        7. Industry experience
        8. Leadership experience
        9. Technologies used
        10. Projects completed

        IMPORTANT: Respond ONLY with valid JSON format, no additional text.

        Format the response as this EXACT JSON structure:
        {{
            "technical_skills": ["Python", "JavaScript", "AWS"],
            "soft_skills": ["leadership", "communication"],
            "years_experience": "5 years",
            "education": [{{"degree": "Bachelor's", "field": "Computer Science", "institution": "XYZ University"}}],
            "key_achievements": ["achievement1", "achievement2"],
            "core_competencies": ["competency1", "competency2"],
            "industry_experience": ["Technology", "Finance"],
            "leadership_experience": ["Led team of 5 developers"],
            "technologies_used": ["React", "Node.js", "MongoDB"],
            "projects": ["Project 1: Description", "Project 2: Description"]
        }}

        Resume:
        {resume}
        """

        try:
            # Fixed: Extract content from AIMessage object
            response = self.llm.invoke(prompt.format(resume=resume_text[:4000]))
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            print(f"📥 Resume analysis response received: {response_text[:200]}...")
            
            # Clean response
            response_text = response_text.strip()
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            parsed_response = json.loads(response_text)
            print("✅ Resume analysis successful!")
            return parsed_response
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            print(f"Debug - Response content: {response_text}")
            st.error("Error parsing resume analysis response. Please check the resume text for any formatting issues.")
            return {}
        except Exception as e:
            print(f"❌ Error analyzing resume: {str(e)}")
            st.error(f"Error analyzing resume: {str(e)}")
            return {}

    def analyze_match(self, job_analysis: dict, resume_analysis: dict) -> dict:
        """Compare job and resume - using your exact working prompt structure"""
        print("🔍 Starting match analysis...")
        
        if not job_analysis or not resume_analysis:
            print("❌ Missing job or resume analysis data")
            return {}
        
        prompt = """You are a professional resume analyzer. Compare the provided job requirements and resume to generate a detailed analysis in valid JSON format.

IMPORTANT: Respond ONLY with a valid JSON object and NO additional text or formatting.

Job Requirements:
{job}

Resume Details:
{resume}

Generate a response following this EXACT structure:
{{
"overall_match_percentage":"85%",
"matching_skills":[{{"skill_name":"Python","is_match":true}},{{"skill_name":"AWS","is_match":true}}],
"missing_skills":[{{"skill_name":"Docker","is_match":false,"suggestion":"Consider obtaining Docker certification"}}],
"skills_gap_analysis":{{"technical_skills":"Specific technical gap analysis","soft_skills":"Specific soft skills gap analysis"}},
"experience_match_analysis":"Detailed experience match analysis",
"education_match_analysis":"Detailed education match analysis",
"recommendations_for_improvement":[{{"recommendation":"Add metrics","section":"Experience","guidance":"Quantify achievements with specific numbers"}}],
"ats_optimization_suggestions":[{{"section":"Skills","current_content":"Current format","suggested_change":"Specific change needed","keywords_to_add":["keyword1","keyword2"],"formatting_suggestion":"Specific format change","reason":"Detailed reason"}}],
"key_strengths":"Specific key strengths",
"areas_of_improvement":"Specific areas to improve"
}}

Focus on providing detailed, actionable insights for each field. Keep the JSON structure exact but replace the example content with detailed analysis based on the provided job and resume."""

        try:
            # Fixed: Extract content from AIMessage object
            response = self.llm.invoke(prompt.format(
                job=json.dumps(job_analysis, indent=2)[:2000],
                resume=json.dumps(resume_analysis, indent=2)[:2000]
            ))
            response_content = response.content if hasattr(response, 'content') else str(response)
            
            print(f"📥 Match analysis response received: {response_content[:200]}...")
            
            # Clean up the response content - using your exact approach
            response_content = response_content.strip()
            response_content = response_content.strip('"\'')
            
            # Remove code blocks if present
            if response_content.startswith('```json'):
                response_content = response_content.replace('```json', '').replace('```', '').strip()
            
            parsed_response = json.loads(response_content)
            print(f"✅ Match analysis successful! Overall match: {parsed_response.get('overall_match_percentage', 'Unknown')}")
            return parsed_response
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            print(f"Debug - Response content: {response_content}")
            st.error("Error parsing match analysis response. Please try again.")
            return {}
        except Exception as e:
            print(f"❌ Error analyzing match: {str(e)}")
            st.error(f"Error analyzing match: {str(e)}")
            return {}