import streamlit as st
from webpages.ui_components import (apply_modern_styles, page_header)
import json
import utils.resume_analyzer_controller as resumeAnalyzerController
from config.database import (save_resume_data, save_analysis_data, 
                             init_database)

class ResumeAnalyzerView:
    def __init__(self):
        # Open and load JSON file
        with open("config\\job_roles.json", "r") as file:
            JOB_ROLES = json.load(file)

        self.job_roles = JOB_ROLES

        if "editing" not in st.session_state:
            st.session_state.editing = False

        self.rac = resumeAnalyzerController.ResumeAnalyzer()

    def render_empty_state(self, icon, message):
        """Render an empty state with icon and message"""
        return f"""
            <div style='text-align: center; padding: 2rem; color: #666;'>
                <i class='{icon}' style='font-size: 2rem; margin-bottom: 1rem; color: #00bfa5;'></i>
                <p style='margin: 0;'>{message}</p>
            </div>
        """

    def save_job_roles(self, job_roles):
        # print("@ save_jobs")
        try:
            # print(job_roles)
            with open("config\\job_roles.json", "w") as file:
                json.dump(job_roles, file, indent=4)
            st.success("Job role information updated successfully!")
            # st.rerun()  # Refresh Streamlit app after saving
        except Exception as e:
            st.error(f"Error saving job roles: {e}")

    def resumeAnalyzerPage(self):
        """Render the resume analyzer page"""
        apply_modern_styles()
        
        # Page Header
        page_header(
            "Resume Analyzer",
            "Get instant AI-powered feedback to optimize your resume"
        )
        
        # Job Role Selection with dynamically applied styles
        categories = list(self.job_roles.keys())
        selected_category = st.selectbox("Job Category", categories)
        
        roles = list(self.job_roles[selected_category].keys())
        selected_role = st.selectbox("Specific Role", roles)
        
        role_info = self.job_roles[selected_category][selected_role]

        # Editing Mode
        if st.button("Update Role Info"):
            st.session_state.editing = True

        if st.session_state.editing:
            new_description = st.text_area("Update Job Description", role_info["description"])
            new_required_skills = st.text_area("Update Required Skills (comma-separated)", ", ".join(role_info["required_skills"]))
            new_technical_skills = st.text_area("Update Recommended Technical Skills (comma-separated)", ", ".join(role_info["recommended_skills"]["technical"]))
            new_soft_skills = st.text_area("Update Recommended Soft Skills (comma-separated)", ", ".join(role_info["recommended_skills"]["soft"]))

            save_button, cancel_button = st.columns(2)

            with save_button:
                # print("hello")
                if st.button("Save"):
                    # Update job roles dictionary
                    role_info["description"] = new_description
                    role_info["required_skills"] = [skill.strip() for skill in new_required_skills.split(",")]
                    role_info["recommended_skills"]["technical"] = [skill.strip() for skill in new_technical_skills.split(",")]
                    role_info["recommended_skills"]["soft"] = [skill.strip() for skill in new_soft_skills.split(",")]
                    self.save_job_roles(self.job_roles)
                    st.success("Job role information updated!")
                    st.session_state.editing = False
                    st.rerun()

            with cancel_button:
                if st.button("Cancel"):
                    st.warning("Changes discarded.")
                    st.session_state.editing = False
                    st.rerun()  # Refresh to discard changes
        
        # Display role information
        if not st.session_state.editing:
            self.display_role_information(selected_role, role_info)
        
        # File Upload
        uploaded_file = st.file_uploader("Upload your resume", type=['pdf', 'docx'])
        
        st.markdown(
            self.render_empty_state(
            "fas fa-cloud-upload-alt",
            "Upload your resume to get started with AI-powered analysis"
            ),
            unsafe_allow_html=True
        )
        if uploaded_file:
            with st.spinner("Analyzing your document..."):
                text = ""
                # Links and text are extracted here
                if uploaded_file:
                    text = self.text_extraction(uploaded_file)
                    skills = self.rac.extract_skills(text)
                    # st.write(skills)
                    # if text is null return
                    if text == "":
                        return
                    
                    self.links_extraction(uploaded_file)
               
                # Analyze the document
                analysis = self.rac.analyze_resume({'raw_text': text}, role_info)
                
                # Save resume data to database
                resume_data = {
                    'personal_info': {
                        'name': analysis.get('name', 'N/A'),
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
                    'total_experience': analysis.get('total_experience',''),
                    'projects': analysis.get('projects', []),
                    'skills': analysis.get('skills', []),
                    'template': ''
                }
                # self.rac.extract_skills(text)
                # self.rac.extract_education_experience_projects(text)
                print(resume_data)
                # Save to database
                try:
                    init_database()
                    resume_id = save_resume_data(resume_data)
                    
                    # Save analysis data
                    analysis_data = {
                        'resume_id': resume_id,
                        'ats_score': analysis['ats_score'],
                        'keyword_match_score': analysis['keyword_match']['score'],
                        'format_score': analysis['format_score'],
                        'section_score': analysis['section_score'],
                        'missing_skills': ','.join(analysis['keyword_match']['missing_skills']),
                        'recommendations': ','.join(analysis['suggestions'])
                    }
                    save_analysis_data(resume_id, analysis_data)
                    st.success("Resume data saved successfully!")
                except Exception as e:
                    st.error(f"Error saving to database: {str(e)}")
                    print(f"Database error: {e}")
                
                # Show results based on document type
                if analysis.get('document_type') != 'resume':
                    st.error(f"⚠️ This appears to be a {analysis['document_type']} document, not a resume!")
                    st.warning("Please upload a proper resume for ATS analysis.")
                    return                
                # Display results in a modern card layout
                col1, col2 = st.columns(2)
                
                with col1:
                    # displaying ATS score card
                    self.ats_score_card_display(analysis)
                                        
                    # self.display_analysis_results(analysis_results)

                    # Skills Match Card
                    st.markdown("""
                    <div class="feature-card">
                        <h2>Skills Match</h2>
                    """, unsafe_allow_html=True)
                    
                    st.metric("Keyword Match", f"{int(analysis.get('keyword_match', {}).get('score', 0))}%")
                    
                    if analysis['keyword_match']['missing_skills']:
                        st.markdown("#### Missing Skills:")
                        for skill in analysis['keyword_match']['missing_skills']:
                            st.markdown(f"- {skill}")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col2:
                    # Format Score Card
                    st.markdown("""
                    <div class="feature-card">
                        <h2>Format Analysis</h2>
                    """, unsafe_allow_html=True)
                    
                    st.metric("Format Score", f"{int(analysis.get('format_score', 0))}%")
                    st.metric("Section Score", f"{int(analysis.get('section_score', 0))}%")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
    
    def display_role_information(self, selected_role, role_info):
        st.markdown(f"""
            <div style='background-color: #1e1e1e; padding: 20px; border-radius: 10px; margin: 10px 0;'>
                <h3>{selected_role}</h3>
                <p>{role_info['description']}</p>
                <h4>Required Skills:</h4>
                <p>{', '.join(role_info['required_skills'])}</p>
            </div>
            """, unsafe_allow_html=True)
        
    def ats_score_card_display(self, analysis):
        # ATS Score Card with circular progress
        st.markdown("""
            <div class="feature-card">
            <h2>ATS Score</h2>
                <div style="position: relative; width: 150px; height: 150px; margin: 0 auto;">
                    <div style="
                        position: absolute;
                        width: 150px;
                        height: 150px;
                        border-radius: 50%;
                        background: conic-gradient(
                        #4CAF50 0% {score}%,
                        #2c2c2c {score}% 100%
                        );
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    ">
                        <div style="
                            width: 120px;
                            height: 120px;
                            background: #1a1a1a;
                            border-radius: 50%;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-size: 24px;
                            font-weight: bold;
                            color: {color};
                        ">{score}
                        </div>
                    </div>
                </div>
                <div style="text-align: center; margin-top: 10px;">
                    <span style="
                        font-size: 1.2em;
                        color: {color};
                        font-weight: bold;
                     ">{status}
                    </span>
                </div>
            """.format(
                    score=analysis['ats_score'],
                    color='#4CAF50' if analysis['ats_score'] >= 80 else '#FFA500' if analysis['ats_score'] >= 60 else '#FF4444',
                    status='Excellent' if analysis['ats_score'] >= 80 else 'Good' if analysis['ats_score'] >= 60 else 'Needs Improvement'
                    ), unsafe_allow_html=True)
                    
        st.markdown("</div>", unsafe_allow_html=True)

    def links_extraction(self, uploaded_file):
        if uploaded_file.name.endswith(".pdf"):
            links = self.rac.extract_links_from_pdf(uploaded_file)
        else:
            links = self.rac.extract_links_from_docx(uploaded_file)
                    
        if links:
            st.subheader("🔗 Extracted Links")
            for link in links:
                status = self.rac.check_url_status(link)
                st.write(f"[{link}]({link}) - {'✅ Valid' if status else '❌ Invalid'}")
        else:
            st.warning("No hyperlinks found in the resume!")
    
    def text_extraction(self, uploaded_file):
        text = ""
        try:
            if uploaded_file.type == "application/pdf":
                text = self.rac.extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                text = self.rac.extract_text_from_docx(uploaded_file)
            else:
                text = uploaded_file.getvalue().decode()
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
        return text
    
    