from PyPDF2 import PdfReader
from docx import Document
import streamlit as st
import docx
from utils.resume_analyzer_controller import ResumeAnalyzer
import json
import pandas as pd
import numpy as np
import time

class MultipleResumeAnalyzerView:
    def __init__(self):
        pass

    def read_pdf(self, file):
        pdf_reader = PdfReader(file)
        text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
        return text

    def read_docx(self, file):
        doc = docx.Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    
    def main(self):
        with open("config\\job_roles.json", "r") as file:
            job_roles = json.load(file)

        st.title("Multi-File Uploader in Streamlit")
        categories = list(job_roles.keys())
        selected_category = st.selectbox("Job Category", categories)
            
        roles = list(job_roles[selected_category].keys())
        selected_role = st.selectbox("Specific Role", roles)
            
        role_info = job_roles[selected_category][selected_role]

        uploaded_files = st.file_uploader("Upload multiple files", type=["pdf", "docx"], accept_multiple_files=True)

        results = []
        if uploaded_files:
            st.write(f"You uploaded {len(uploaded_files)} file(s)")
            ra = ResumeAnalyzer()
        if st.button("Submit"):
            st.success("Files uploaded successfully")
            with st.spinner("Analyzing Documents..."):
                for uploaded_file in uploaded_files:
                    # st.write(f"### {uploaded_file.name}")
                    try:
                        if uploaded_file.type == "application/pdf":
                            content = self.read_pdf(uploaded_file)
                        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                            content = self.read_docx(uploaded_file)
                        else:
                            content = "Unsupported file format"
                        
                        # st.text_area("File content:", content, height=200)
                    except Exception as e:
                        st.write("Could not read file content.")
                        st.write(e)
                    
                    analysis = ra.analyze_resume({'raw_text': content}, role_info)  

                    resume_data = {
                            'personal_info': {
                                'name': analysis.get('name', ''),
                                'email': analysis.get('email', ''),
                                'phone': analysis.get('phone', ''),
                                'linkedin': analysis.get('linkedin', ''),
                                'github': analysis.get('github', ''),
                                'portfolio': analysis.get('portfolio', '')
                            },
                            'summary': analysis.get('summary', ''),
                            'target_role': selected_role,
                            'target_category': selected_category,
                            'education': analysis.get('education', []),
                            'experience': analysis.get('experience', []),
                            'projects': analysis.get('projects', []),
                            'skills': analysis.get('skills', []),
                            'template': ''
                        }   
                    # Save analysis data
                    analysis_data = {
                                'resume_id': analysis,
                                'ats_score': analysis['ats_score'],
                                'keyword_match_score': analysis['keyword_match']['score'],
                                'format_score': analysis['format_score'],
                                'section_score': analysis['section_score'],
                                'missing_skills': ','.join(analysis['keyword_match']['missing_skills']),
                                'recommendations': ','.join(analysis['suggestions'])
                            }
                    results.append(analysis)
                    time.sleep(20)

            data = []
            for analysis in results:
                data.append({
                    "Name": analysis.get('name', ''),
                    "Email": analysis.get('email', ''),
                    "Phone": analysis.get('phone', ''),
                    "Skills": ', '.join(analysis.get('skills', [])),
                    "Total Experience": analysis.get('total_experience', ''),  # Count of experiences
                    "Ats_score": analysis.get('ats_score', '')
                })


            df = pd.DataFrame(data)            
            #     if st.button("Submit"):
            #     st.success("Files uploaded successfully")
                
                # Analysis Table
            excel_data = ra.to_excel(df)
            st.title("Resume Analysis Table")
            st.write("### Resume Analysis Results")
            st.dataframe(df)
            st.download_button(
                label="Download Excel File",
                data=excel_data,
                file_name="exported_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

