# Applicant_Tracking_system

## Overview
The **Applicant Tracking System (ATS)** is a resume analysis tool that leverages **Streamlit** for the UI, follows an **MVC architecture**, and utilizes **LLM (via Groq API)** to score resumes. It provides three main functionalities:

1. **Single Resume Analyzer** - Evaluates a single resume and provides:
   - **Format Score**
   - **ATS Score**
   - **Missing Skills**
   - **Links in Resume**
   
2. **Multiple Resume Analyzer** - Processes multiple resumes and extracts:
   - **Name**
   - **Email**
   - **Phone Number**
   - **Skills in Resume**
   - **ATS Score** (Displayed in a tabular format)
3. **Dashboard** - Displays analysis like:
   - **most knwon skills**
   - **Average ATS score**
   - **Weekly submission**

## Tech Stack
- **Frontend**: Streamlit (for UI)
- **Backend**: Python with MVC architecture
- **Database**: SQLite (for storing candidate details)
- **AI Model**: LLM via **Groq API** (for resume scoring)
- **Other**: Spacy, Pandas, PyPDF2, docx, requests, Plotly

## Features
### 1. **Single Resume Analyzer**
- Upload a single resume (PDF/DOCX format)
- The system analyzes the resume and provides:
  - **Format Score** - Checks formatting quality
  - **ATS Score** - Evaluates compatibility with Applicant Tracking Systems
  - **Missing Skills** - Identifies essential skills missing from the resume
  - **Links in Resume** - Detects and verifies external links (e.g., LinkedIn, portfolios)

### 2. **Multiple Resume Analyzer**
- Upload multiple resumes at once
- Extracts and presents:
  - **Candidate Name**
  - **Email Address**
  - **Phone Number**
  - **Skills Found in Resume**
  - **ATS Score**
- Results displayed in a tabular format

## Database (SQLite)
Stores applicant details, including:
- Candidate Name
- Email
- Phone Number
- ATS Score
- Format Score
- Extracted Skills
- Applied Position
- Other relevant information

## Installation & Setup
### Prerequisites:
- Python 3.8+
- Virtual environment (recommended)

### Steps:
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/applicant-tracking-system.git
   cd applicant-tracking-system
   ```
2. Create a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # For macOS/Linux
   venv\Scripts\activate  # For Windows
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the application:
   ```sh
   streamlit run main.py
   ```

## Usage
1. **Upload a resume** (single or multiple)
2. **View analysis results** in the Streamlit interface
3. **Store or export results** as needed

## Future Enhancements
- Integration with job portals for real-time applicant tracking
- AI-based recommendations for resume improvements
- Enhanced data visualization for resume analytics

## Contributing
Contributions are welcome! Feel free to open issues and submit pull requests.

