"""
Smart Resume AI - Main Application
"""
import streamlit as st

# Set page config at the very beginning
st.set_page_config(
    page_title="Smart Resume AI",
    page_icon="🚀",
    layout="wide"
)

import json
import pandas as pd
import plotly.express as px
# import traceback
# from utils.resume_analyzer import ResumeAnalyzer
# from utils.resume_builder import ResumeBuilder
# from config.database import (
#     get_database_connection, save_resume_data, save_analysis_data, 
#     init_database, verify_admin, log_admin_action
# )
# from config.job_roles import JOB_ROLES # not using from .py but from .json
import requests
from streamlit_lottie import st_lottie
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import base64
import io
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime
# from jobs.job_search import render_job_search
# from PIL import Image
# import utils.resume_analyzer as resume_analyzer
# # from resume_analyser import extract_links_from_pdf, extract_links_from_docx, check_url_status
# from utils.resume_analyzer import extract_links_from_pdf, extract_links_from_docx, check_url_status
# from utils.multipleResumeAnalyzer import MultipleResumeAnalyzer



# webpages
from webpages.ui_components import (
    apply_modern_styles, hero_section, feature_card, about_section, 
    page_header, render_analytics_section, render_activity_section, 
    render_suggestions_section, load_lottie_url
)
import webpages.homeView as hv
import webpages.resumeAnalyzerView as rav
import webpages.dashboardView as dbv
import webpages.multiple_resume_analyzer_view as mrav

class ResumeAppMain:
    def __init__(self):
        """Initialize the application"""
        if 'form_data' not in st.session_state:
            st.session_state.form_data = {
                'personal_info': {
                    'full_name': '',
                    'email': '',
                    'phone': '',
                    'location': '',
                    'linkedin': '',
                    'portfolio': ''
                },
                'summary': '',
                'experiences': [],
                'education': [],
                'projects': [],
                'skills_categories': {
                    'technical': [],
                    'soft': [],
                    'languages': [],
                    'tools': []
                }
            }
        
        # Initialize navigation state
        if 'page' not in st.session_state:
            st.session_state.page = 'home'
            
        # Initialize admin state
        if 'is_admin' not in st.session_state:
            st.session_state.is_admin = False
        
        self.pages = {
            "🏠 HOME": self.render_home,
            "🔍 RESUME ANALYZER": self.render_analyzer,
            "MULTIPLE RESUME ANALYZER": self.render_multipleResumeAnalyzer,
            "📊 DASHBOARD": self.render_dashboard,
            "ℹ️ ABOUT": self.render_about
        }
        
        # Initialize dashboard manager
        # self.dashboard_manager = DashboardManager()
        
        self.analyzer = rav.ResumeAnalyzerView()

        # Initialize session state
        if 'user_id' not in st.session_state:
            st.session_state.user_id = 'default_user'
        if 'selected_role' not in st.session_state:
            st.session_state.selected_role = None
        
        # Initialize database
        # init_database()
        
        # Load external CSS
        with open('style/style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        
        # Load Google Fonts
        st.markdown("""
            <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
        """, unsafe_allow_html=True)

    def render_home(self):
        home = hv.HomeView()
        home.homePage()

    def render_analyzer(self):
        self.analyzer.resumeAnalyzerPage()

    def render_multipleResumeAnalyzer(self):
        mulResumeAnalyzerView = mrav.MultipleResumeAnalyzerView()
        mulResumeAnalyzerView.main()

    def render_dashboard(self):
        dashboardView = dbv.DashboardManager()
        dashboardView.render_dashboard()

    def render_about(self):
        pass

    def main(self):
        # Admin login/logout in sidebar
        with st.sidebar:
            st_lottie(load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_xyadoh9h.json"), height=200, key="sidebar_animation")
            st.title("Smart Resume AI")
            st.markdown("---")
            
            # Navigation buttons
            for page_name in self.pages.keys():
                if st.button(page_name, use_container_width=True):
                    cleaned_name = page_name.lower().replace(" ", "_").replace("🏠", "").replace("🔍", "").replace("📝", "").replace("📊", "").replace("🎯", "").replace("💬", "").replace("ℹ️", "").strip()
                    st.session_state.page = cleaned_name
                    st.rerun()

            # Add some space before admin login
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("---")

        # Force home page on first load
        if 'initial_load' not in st.session_state:
            st.session_state.initial_load = True
            st.session_state.page = 'home'
            st.rerun()
        
        # Get current page and render it
        current_page = st.session_state.get('page', 'home')

        # Create a mapping of cleaned page names to original names
        page_mapping = {name.lower().replace(" ", "_").replace("🏠", "").replace("🔍", "").replace("📝", "").replace("📊", "").replace("🎯", "").replace("💬", "").replace("ℹ️", "").strip(): name 
                       for name in self.pages.keys()}
        
        # Render the appropriate page
        if current_page in page_mapping:
            self.pages[page_mapping[current_page]]()
        else:
            # Default to home page if invalid page
            self.render_home()





if __name__ == "__main__":
    app = ResumeAppMain()
    app.main()