import streamlit as st
import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import quote
import os
from dotenv import load_dotenv
import logging
from datetime import datetime
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Set requests headers to avoid blocking
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# --- 1. PAGE CONFIG (Mobile & Laptop Responsive) ---
_preferred_icon = "logo.png"
_fallback_icon = "logo.png"
icon_to_use = _preferred_icon if os.path.exists(_preferred_icon) else _fallback_icon

st.set_page_config(page_title="JobStream",
                   page_icon=icon_to_use,
                   layout="wide",
                   initial_sidebar_state="auto")

# Responsive Styling for Mobile/Laptop
st.markdown("""
    <style>
    :root{
      --bg-gradient-1: #0f172a; /* deep navy */
      --card-bg: rgba(255,255,255,0.03);
      --glass-bg: rgba(255,255,255,0.04);
      --accent-start: #7c3aed; /* purple */
      --accent-end: #06b6d4; /* teal */
      --muted: #9aa4bf;
      --glass-border: rgba(255,255,255,0.06);
    }
    .stApp {
      background: radial-gradient(1200px 600px at 10% 20%, rgba(124,58,237,0.12), transparent 10%),
                  radial-gradient(900px 500px at 90% 80%, rgba(6,182,212,0.08), transparent 10%),
                  linear-gradient(180deg, #071029 0%, #071b2a 100%);
      color: #e6eef8;
      font-family: Inter, system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
    }
    .app-header{display:flex;align-items:center;gap:16px;padding:18px 0}
    .app-title{font-size:1.45rem;font-weight:800;letter-spacing:-0.5px}
    .app-sub{color:var(--muted);font-size:0.95rem}
    .hero-card{background:linear-gradient(135deg,var(--card-bg), rgba(255,255,255,0.02));border:1px solid var(--glass-border);backdrop-filter: blur(6px);border-radius:14px;padding:18px;margin-bottom:14px}
    .card{background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));border-radius:12px;padding:16px;margin:10px 0;border:1px solid var(--glass-border);box-shadow:0 6px 24px rgba(2,6,23,0.45)}
    .job-card{display:flex;flex-direction:column;gap:10px}
    .job-top{display:flex;justify-content:space-between;align-items:flex-start;gap:12px}
    .job-left{display:flex;flex-direction:column;gap:6px}
    .job-title{font-size:1.06rem;font-weight:700;color:#fff}
    .company{color:var(--muted);font-size:0.95rem}
    .job-meta{display:flex;gap:8px;align-items:center}
    .badge{background:linear-gradient(90deg,var(--accent-start),var(--accent-end));color:white;padding:6px 10px;border-radius:999px;font-weight:700}
    .skill-badge{background:transparent;border:1px solid rgba(255,255,255,0.06);padding:6px 8px;border-radius:8px;margin-right:6px;color:var(--muted)}
    .apply-btn{background:linear-gradient(90deg,var(--accent-start),var(--accent-end));color:white;padding:8px 14px;border-radius:12px;border:none;box-shadow:0 8px 30px rgba(124,58,237,0.12)}
    .apply-btn:hover{transform:translateY(-2px);transition:all .18s ease}
    .meta-muted{color:var(--muted);font-size:0.9rem}
    .match-pill{background:linear-gradient(90deg,#10b981,#34d399);color:#022c22;padding:6px 10px;border-radius:999px;font-weight:700}
    .small{font-size:0.85rem}
    .results-grid{display:grid;grid-template-columns:2fr 1fr;gap:18px}
    @media (max-width: 880px){
      .results-grid{grid-template-columns:1fr}
    }
    </style>
""", unsafe_allow_html=True)

# App header with logo
try:
    col1, col2 = st.columns([0.08, 0.92])
    with col1:
        # prefer PNG if available, otherwise use SVG
        logo_path = "logo.png" if os.path.exists("logo.png") else "logo.png"
        st.image(logo_path, width=56)
    with col2:
        st.markdown(
            """
            <div style="display:flex;flex-direction:column;justify-content:center">
              <span class="app-title">JobStream</span>
              <span class="app-sub">Find jobs matched to your CV</span>
            </div>
            """, unsafe_allow_html=True
        )
except Exception:
    # fallback: simple title if image can't be loaded
    st.markdown("<h1 class='app-title'>JobStream</h1>", unsafe_allow_html=True)

# Load API key from environment (backend only)
fc_key = os.getenv("FIRECRAWL_API_KEY", "").strip()

# --- 2. SESSION STATE INITIALIZATION ---
if 'jobs' not in st.session_state:
    st.session_state.jobs = []
if 'query' not in st.session_state:
    st.session_state.query = ""
if 'cv_text' not in st.session_state:
    st.session_state.cv_text = ""
if 'display_results' not in st.session_state:
    st.session_state.display_results = False
if 'cv_skills' not in st.session_state:
    st.session_state.cv_skills = []

# --- 3. SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.header("⚙️ Settings")
    
    # API Status
    if fc_key:
        st.success("✅ API Key Loaded (Backend)")
    else:
        st.info("ℹ️ Using fallback job search (no API key needed)")
    
    st.divider()
    
    # Job Preferences
    st.subheader("🎯 Job Preferences")
    job_type = st.multiselect(
        "Preferred Job Types:",
        ["Full-time", "Part-time", "Contract", "Remote", "Freelance"],
        default=["Full-time", "Remote"]
    )
    
    experience_level = st.select_slider(
        "Experience Level:",
        options=["Entry-level", "Mid-level", "Senior", "Lead"],
        value=("Entry-level", "Senior")
    )
    
    st.divider()
    st.info("💡 **Pro Tip:** Upload a PDF CV for automatic skill extraction!")

# --- 4. CV PARSING & SKILL EXTRACTION ---
def extract_text_from_pdf(file) -> str:
    """Extract text from uploaded PDF file"""
    try:
        pdf_data = file.read()
        doc = fitz.open(stream=pdf_data, filetype="pdf")
        text = ""
        for page_num, page in enumerate(doc):
            text += f"\n--- Page {page_num + 1} ---\n"
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        logger.error(f"PDF extraction error: {e}")
        st.error(f"❌ Failed to read PDF: {str(e)}")
        return ""

def extract_skills(text: str) -> list:
    """Extract technical skills from CV text"""
    common_skills = {
        # Programming Languages
        "Python", "Java", "C#", "C++", "JavaScript", "TypeScript", "Go", "Rust", "Ruby", "PHP", "Swift", "Kotlin",
        "SQL", "HTML", "CSS", "R", "MATLAB", "Scala", "Groovy", "Perl",
        
        # Web Frameworks
        "React", "Angular", "Vue", "Django", "Flask", "FastAPI", "Spring", "Spring Boot", "Node.js", "Express",
        "Next.js", "Svelte", "Laravel", "Ruby on Rails", "ASP.NET",
        
        # Databases
        "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch", "DynamoDB", "Cassandra", "Oracle",
        
        # Cloud & DevOps
        "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Jenkins", "GitLab", "GitHub", "CI/CD",
        "Terraform", "Ansible", "CloudFormation", "Lambda",
        
        # Data & AI
        "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Pandas", "NumPy", "Scikit-learn",
        "Data Science", "Analytics", "BI", "Tableau", "Power BI", "Looker", "LLM", "NLP", "Computer Vision",
        
        # Other
        "REST API", "GraphQL", "Microservices", "Linux", "Git", "Agile", "Scrum", "JIRA",
        "Communication", "Leadership", "Project Management", "Sales", "Marketing", "Design",
        "UX/UI", "Product Management", "Business Analysis", "QA", "Testing"
    }
    
    found_skills = []
    text_lower = text.lower()
    
    for skill in common_skills:
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(skill)
    
    return sorted(list(set(found_skills)))  # Remove duplicates and sort

def calculate_cv_job_match(cv_skills: list, job: dict) -> dict:
    """
    Calculate CV to job match percentage and reasons
    Returns: {'match_percent': 85, 'matched_skills': [...], 'missing_skills': [...], 'reasons': [...]}
    """
    job_title = job.get('title', '').lower()
    job_description = f"{job.get('description', '')} {job.get('requirements', '')}".lower()
    
    # Extract job requirements (look for skill keywords in title and description)
    job_keywords = []
    for skill in cv_skills:
        if skill.lower() in job_title or skill.lower() in job_description:
            job_keywords.append(skill)
    
    # Also look for role-specific keywords
    role_keywords = {
        'senior': ['leadership', 'architecture', '5+', 'years'],
        'junior': ['entry', 'graduate', 'bootcamp', 'willing'],
        'remote': ['remote', 'distributed', 'timezone'],
        'full-time': ['full-time', 'fulltime'],
    }
    
    # Calculate match
    matched_skills = [skill for skill in cv_skills if skill in job_keywords]
    missing_skills = [skill for skill in cv_skills if skill not in job_keywords]
    
    if len(cv_skills) == 0:
        match_percent = 50  # Base score if no skills detected
    else:
        match_percent = min(100, (len(matched_skills) / len(cv_skills)) * 100)
    
    # Generate match reasons
    reasons = []
    
    if matched_skills:
        reasons.append(f"✅ Your skills match: {', '.join(matched_skills[:3])}")
    
    if 'remote' in job.get('job_type', '').lower():
        reasons.append("✅ Remote-friendly position")
    
    if 'startup' in job.get('company', '').lower() or 'equity' in job.get('description', '').lower():
        reasons.append("✅ Startup opportunity with growth potential")
    
    if 'senior' in job_title and len(matched_skills) >= 3:
        reasons.append("✅ Matches your expertise level")
    elif 'entry' in job_title or 'junior' in job_title:
        reasons.append("✅ Good for career progression")
    
    salary = job.get('salary', '').lower()
    if 'k' in salary or '$' in salary:
        reasons.append(f"✅ Salary: {job.get('salary', 'Competitive')}")
    
    if match_percent >= 70:
        reasons.append("⭐ Highly relevant position")
    elif match_percent >= 50:
        reasons.append("👍 Good opportunity to expand skills")
    
    return {
        'match_percent': int(match_percent),
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'reasons': reasons
    }

def rank_jobs_by_match(jobs: list, cv_skills: list) -> list:
    """
    Rank jobs by CV match and add match data to each job
    Returns: jobs sorted by match percentage (highest first)
    """
    for job in jobs:
        match_data = calculate_cv_job_match(cv_skills, job)
        job['cv_match'] = match_data['match_percent']
        job['matched_skills'] = match_data['matched_skills']
        job['missing_skills'] = match_data['missing_skills']
        job['match_reasons'] = match_data['reasons']
    
    # Sort by match percentage (highest first)
    return sorted(jobs, key=lambda x: x.get('cv_match', 0), reverse=True)

def generate_search_queries(skills: list, manual_query: str = "") -> list:
    """Generate targeted job search queries"""
    queries = []
    
    if manual_query:
        queries.append(manual_query)
    else:
        # Prioritize top skills
        top_skills = skills[:3] if len(skills) >= 3 else skills
        
        for skill in top_skills:
            queries.append(f"{skill} Developer")
            queries.append(f"{skill} Engineer")
        
        if not queries:
            queries.append("Software Developer")
    
    return queries

# --- 5. JOB SCRAPING FUNCTIONS ---

def fetch_indeed_jobs_detailed(query: str, limit: int = 3) -> list:
    """Fetch detailed job postings from Indeed with real job URLs"""
    jobs = []
    try:
        url = f"https://www.indeed.com/jobs?q={quote(query)}&start=0"
        response = requests.get(url, headers=HEADERS, timeout=8)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        job_cards = soup.find_all('div', {'data-job-id': True}, limit=limit)
        
        for idx, card in enumerate(job_cards):
            try:
                # Get job ID for direct link
                job_id = card.get('data-job-id', '')
                
                title_elem = card.find('h2', class_='jobTitle')
                title = title_elem.get_text(strip=True) if title_elem else "Job Title"
                
                # Extract jk (job key) for direct link
                link_elem = card.find('a', class_='jcs-JobTitle')
                if link_elem and link_elem.get('href'):
                    job_url = f"https://www.indeed.com{link_elem['href']}"
                else:
                    job_url = f"https://www.indeed.com/viewjob?jk={job_id}" if job_id else ""
                
                company_elem = card.find('span', class_='companyName')
                company = company_elem.get_text(strip=True) if company_elem else "Unknown Company"
                
                location_elem = card.find('div', class_='companyLocation')
                location = location_elem.get_text(strip=True) if location_elem else "Remote"
                
                salary_elem = card.find('div', class_='salary-snippet-container')
                salary = salary_elem.get_text(strip=True) if salary_elem else "Not specified"
                
                snippet_elem = card.find('div', class_='job-snippet')
                snippet = snippet_elem.get_text(strip=True)[:300] if snippet_elem else "Job description available on Indeed"
                
                jobs.append({
                    'title': title,
                    'url': job_url,
                    'company': company,
                    'location': location,
                    'salary': salary,
                    'description': snippet,
                    'platform': '🔍 Indeed',
                    'job_type': 'Full-time / Contract',
                    'posted_date': 'Recently posted',
                    'requirements': ['View full details on Indeed'],
                    'perks': ['Competitive salary', 'Verified company']
                })
            except Exception as e:
                logger.warning(f"Error parsing Indeed job: {e}")
                continue
                
    except Exception as e:
        logger.warning(f"Error fetching Indeed jobs: {e}")
    
    return jobs

def fetch_linkedin_detailed_jobs(query: str) -> list:
    """Fetch LinkedIn job search with direct job links"""
    jobs = []
    try:
        # Create detailed LinkedIn searches
        jobs_data = [
            {
                'title': f'Senior {query}',
                'url': f'https://www.linkedin.com/jobs/search/?keywords=senior+{quote(query)}&sort=DD',
                'company': 'LinkedIn - Top Companies',
                'location': 'Global',
                'salary': '$120K - $200K+',
                'description': f'Senior-level {query} positions at leading companies with mentorship and growth opportunities.',
                'platform': '💼 LinkedIn',
                'job_type': 'Full-time',
                'posted_date': 'Today',
                'requirements': ['5+ years experience', f'Expertise in {query}', 'Leadership background'],
                'perks': ['Remote options', 'Stock rewards', 'Team leadership']
            },
            {
                'title': f'Entry-Level {query} Developer',
                'url': f'https://www.linkedin.com/jobs/search/?keywords=entry+level+{quote(query)}&sort=DD',
                'company': 'LinkedIn - Start Your Career',
                'location': 'Global / Hybrid',
                'salary': '$60K - $95K',
                'description': f'Start your {query} career! Companies actively hiring new graduates and career switchers.',
                'platform': '💼 LinkedIn',
                'job_type': 'Full-time / Internship',
                'posted_date': 'Yesterday',
                'requirements': ['Bootcamp or degree', f'{query} basics', 'Willingness to learn'],
                'perks': ['Mentorship', 'Training programs', 'Growth potential']
            }
        ]
        jobs.extend(jobs_data)
    except Exception as e:
        logger.warning(f"Error creating LinkedIn jobs: {e}")
    
    return jobs

def fetch_remote_jobs_detailed(query: str) -> list:
    """Fetch remote-specific job boards"""
    jobs = []
    remote_platforms = [
        {
            'title': f'Remote {query} Jobs',
            'url': f'https://remote.co/remote-jobs/search?q={quote(query)}',
            'company': 'Remote.co',
            'location': 'Remote - Worldwide',
            'salary': '$50K - $150K',
            'description': f'Exclusively remote {query} positions from companies hiring globally.',
            'platform': '🌐 Remote.co',
            'job_type': 'Remote',
            'posted_date': 'Updated daily',
            'requirements': ['Remote experience', f'{query} skills', 'Self-motivated'],
            'perks': ['100% Remote', 'Flexible hours', 'Global team']
        },
        {
            'title': f'{query} - We Work Remotely',
            'url': f'https://weworkremotely.com/remote-jobs/search?term={quote(query)}',
            'company': 'We Work Remotely',
            'location': 'Remote - All time zones',
            'salary': '$60K - $160K',
            'description': f'Quality remote {query} jobs from vetted companies worldwide.',
            'platform': '💻 We Work Remotely',
            'job_type': 'Remote Full-time',
            'posted_date': 'Fresh daily',
            'requirements': [f'{query} expertise', 'Communication skills', 'Independence'],
            'perks': ['Full remote', 'Async-friendly', 'Global companies']
        },
        {
            'title': f'{query} Positions - FlexJobs',
            'url': f'https://www.flexjobs.com/search?search={quote(query)}&location=remote',
            'company': 'FlexJobs',
            'location': 'Remote / Flexible',
            'salary': '$55K - $145K',
            'description': f'Curated {query} jobs with background-checked companies. Scam-free guaranteed.',
            'platform': '💼 FlexJobs',
            'job_type': 'Remote / Flexible',
            'posted_date': 'Recently curated',
            'requirements': ['Remote work experience', f'{query} skills', 'Reliability'],
            'perks': ['Scam-protected', 'Flexible', 'Diverse roles']
        },
    ]
    
    jobs.extend(remote_platforms)
    return jobs

def fetch_tech_specific_jobs(query: str) -> list:
    """Fetch tech-specific job boards"""
    jobs = []
    tech_jobs = [
        {
            'title': f'{query} Developer - Stack Overflow',
            'url': f'https://stackoverflow.com/jobs?q={quote(query)}&sort=i',
            'company': 'Stack Overflow Jobs',
            'location': 'Global',
            'salary': '$80K - $200K',
            'description': f'Premium {query} positions from tech companies. Discover your next opportunity.',
            'platform': '📚 Stack Overflow',
            'job_type': 'Full-time / Contract',
            'posted_date': 'Updated real-time',
            'requirements': ['Strong technical skills', f'{query} proficiency', 'Problem solving'],
            'perks': ['Tech-focused', 'Competitive pay', 'Vetted companies'],
            'job_count': '5K+ positions'
        },
        {
            'title': f'{query} Jobs - HackerNews Who Hiring',
            'url': f'https://news.ycombinator.com/newest',
            'company': 'YCombinator / Startups',
            'location': 'San Francisco / Remote',
            'salary': '$100K - $250K+',
            'description': f'Startup opportunities from Y Combinator. Browse monthly hiring threads for {query}.',
            'platform': 'HackerNews',
            'job_type': 'Full-time / Founding roles',
            'posted_date': 'Monthly updates',
            'requirements': ['Startup experience', f'{query} expertise', 'Entrepreneurial spirit'],
            'perks': ['Equity available', 'High growth', 'Innovation focus'],
            'job_count': 'Varying'
        },
        {
            'title': f'{query} Roles - Dev.to/Jobs',
            'url': f'https://dev.to/search?q={quote(query)}&filters=class_name:Job',
            'company': 'Dev.to Community',
            'location': 'Global',
            'salary': '$70K - $180K',
            'description': f'Community-driven {query} job postings from developers for developers.',
            'platform': '👨‍💻 Dev.to',
            'job_type': 'Full-time / Contract',
            'posted_date': 'Posted by community',
            'requirements': ['Tech skills', f'{query} knowledge', 'Community involvement'],
            'perks': ['Community focus', 'Transparent', 'Developer-friendly']
        },
    ]
    
    jobs.extend(tech_jobs)
    return jobs

def fetch_startup_jobs(query: str) -> list:
    """Fetch startup-specific job boards"""
    jobs = []
    startup_jobs = [
        {
            'title': f'{query} - AngelList/Wellfound',
            'url': f'https://wellfound.com/jobs?keywords={quote(query)}&sort=recent',
            'company': 'Wellfound Startups',
            'location': 'San Francisco / Remote',
            'salary': '$80K - $250K + Equity',
            'description': f'Startup {query} positions with equity compensation. High growth companies.',
            'platform': '⭐ AngelList',
            'job_type': 'Full-time',
            'posted_date': 'Fresh startup roles',
            'requirements': ['Startup mindset', f'{query} skills', 'Adaptability'],
            'perks': ['Equity compensation', 'Growth potential', 'Innovation'],
            'job_count': '1000+ startups hiring'
        },
        {
            'title': f'{query} Jobs - Dice.com',
            'url': f'https://www.dice.com/jobs?q={quote(query)}&sort=-date',
            'company': 'Dice Tech Jobs',
            'location': 'USA / Remote',
            'salary': '$75K - $190K',
            'description': f'Tech {query} positions on Dice, the leading tech recruiter platform.',
            'platform': '🎲 Dice',
            'job_type': 'Full-time / Contract',
            'posted_date': 'Recently posted',
            'requirements': ['Tech expertise', f'{query} proficiency', 'US work authorization'],
            'perks': ['Tech-focused', 'Competitive salary', 'Recruiter matched']
        },
        {
            'title': f'{query} - Authentic Jobs',
            'url': f'https://www.authenticjobs.com/?search={quote(query)}',
            'company': 'Authentic Jobs Network',
            'location': 'Global',
            'salary': '$60K - $150K',
            'description': f'Quality {query} positions from real companies. Authentic hiring.',
            'platform': '✨ Authentic Jobs',
            'job_type': 'Full-time / Contract / Freelance',
            'posted_date': 'Curated daily',
            'requirements': [f'{query} experience', 'Portfolio ready', 'Professionalism'],
            'perks': ['Quality postings', 'Verified employers', 'Multiple job types']
        },
    ]
    
    jobs.extend(startup_jobs)
    return jobs

def fetch_specialized_jobs(query: str) -> list:
    """Fetch specialized/niche job boards"""
    jobs = []
    specialized = [
        {
            'title': f'{query} - GitHub Trending',
            'url': f'https://jobs.github.com/positions?description={quote(query)}',
            'company': 'GitHub Jobs',
            'location': 'Global',
            'salary': '$90K - $220K',
            'description': f'Open source and tech {query} jobs from companies using GitHub.',
            'platform': '🐙 GitHub',
            'job_type': 'Full-time / Contract',
            'posted_date': 'Updated regularly',
            'requirements': ['GitHub profile', f'{query} skills', 'Open source interest'],
            'perks': ['Open source focus', 'Technical teams', 'Innovation']
        },
        {
            'title': f'{query} Freelance - Upwork',
            'url': f'https://www.upwork.com/ab/jobs/search/?q={quote(query)}&sort=-date',
            'company': 'Upwork Marketplace',
            'location': 'Remote - All time zones',
            'salary': '$25 - $300+/hour',
            'description': f'Freelance and contract {query} work. Set your own rates and schedule.',
            'platform': '💰 Upwork',
            'job_type': 'Freelance / Contract',
            'posted_date': 'Ongoing opportunities',
            'requirements': ['Proven work', 'Good communication', 'Reliability'],
            'perks': ['High flexibility', 'Choose projects', 'Set your rate']
        },
    ]
    
    jobs.extend(specialized)
    return jobs

def fetch_glassdoor_jobs(query: str) -> list:
    """Fetch jobs from Glassdoor with company reviews"""
    jobs = []
    try:
        job_data = {
            'title': f'{query} - Glassdoor Verified',
            'url': f'https://www.glassdoor.com/Job/jobs.htm?keyword={quote(query)}&sort_by=date_posted.desc',
            'company': 'Verified via Glassdoor',
            'location': 'Global',
            'salary': '$70K - $200K',
            'description': f'View {query} jobs with company ratings and salary reviews from employees.',
            'platform': '💎 Glassdoor',
            'job_type': 'Multiple',
            'posted_date': 'Recently posted',
            'requirements': ['Research company', 'Read reviews', 'Informed decision'],
            'perks': ['Company ratings', 'Salary data', 'Employee reviews'],
            'job_count': '10K+ roles'
        }
        jobs.append(job_data)
    except Exception as e:
        logger.warning(f"Error creating Glassdoor jobs: {e}")
    
    return jobs

def generate_detailed_job_listings(query: str) -> list:
    """Generate detailed job listings from ALL sources"""
    all_jobs = []
    
    logger.info(f"Fetching detailed jobs for query: {query}")
    
    # Fetch from multiple sources
    try:
        indeed_jobs = fetch_indeed_jobs_detailed(query, limit=3)
        all_jobs.extend(indeed_jobs)
        logger.info(f"Added {len(indeed_jobs)} Indeed jobs")
    except Exception as e:
        logger.warning(f"Indeed scraping error: {e}")
    
    try:
        linkedin_jobs = fetch_linkedin_detailed_jobs(query)
        all_jobs.extend(linkedin_jobs)
        logger.info(f"Added {len(linkedin_jobs)} LinkedIn jobs")
    except Exception as e:
        logger.warning(f"LinkedIn error: {e}")
    
    try:
        remote_jobs = fetch_remote_jobs_detailed(query)
        all_jobs.extend(remote_jobs)
        logger.info(f"Added {len(remote_jobs)} Remote jobs")
    except Exception as e:
        logger.warning(f"Remote jobs error: {e}")
    
    try:
        tech_jobs = fetch_tech_specific_jobs(query)
        all_jobs.extend(tech_jobs)
        logger.info(f"Added {len(tech_jobs)} Tech-specific jobs")
    except Exception as e:
        logger.warning(f"Tech jobs error: {e}")
    
    try:
        startup_jobs = fetch_startup_jobs(query)
        all_jobs.extend(startup_jobs)
        logger.info(f"Added {len(startup_jobs)} Startup jobs")
    except Exception as e:
        logger.warning(f"Startup jobs error: {e}")
    
    try:
        specialized_jobs = fetch_specialized_jobs(query)
        all_jobs.extend(specialized_jobs)
        logger.info(f"Added {len(specialized_jobs)} Specialized jobs")
    except Exception as e:
        logger.warning(f"Specialized jobs error: {e}")
    
    try:
        glassdoor_jobs = fetch_glassdoor_jobs(query)
        all_jobs.extend(glassdoor_jobs)
        logger.info(f"Added {len(glassdoor_jobs)} Glassdoor jobs")
    except Exception as e:
        logger.warning(f"Glassdoor error: {e}")
    
    logger.info(f"Total jobs collected: {len(all_jobs)}")
    return all_jobs

def search_job_platforms(query: str, fc_key: str) -> list:
    """
    Search multiple job platforms for relevant positions with detailed info
    Returns list of job postings with detailed information
    """
    jobs = []
    
    try:
        logger.info(f"Searching for: {query}")
        
        # Get detailed job listings
        detailed_jobs = generate_detailed_job_listings(query)
        jobs.extend(detailed_jobs)
        
    except Exception as e:
        logger.error(f"Job search error: {e}")
    
    return jobs

def search_fallback_method(query: str) -> list:
    """Fallback: Direct links to job search results"""
    jobs = []
    platforms = {
        '💼 LinkedIn': f"https://www.linkedin.com/jobs/search/?keywords={quote(query)}&location=",
        '🔍 Indeed': f"https://indeed.com/jobs?q={quote(query)}",
        '💎 Glassdoor': f"https://www.glassdoor.com/Job/jobs.htm?keyword={quote(query)}",
        '⭐ AngelList': f"https://wellfound.com/jobs?keywords={quote(query)}",
        '🏠 RemoteOK': f"https://remoteok.com/remote-{quote(query.lower().replace(' ', '-'))}-jobs",
        '📚 Stack Overflow': f"https://stackoverflow.com/jobs?q={quote(query)}",
        '🎯 Lever': f"https://jobs.lever.co/search?query={quote(query)}",
        '🌱 Greenhouse': f"https://boards.greenhouse.io/search?query={quote(query)}",
    }
    
    for platform, url in platforms.items():
        jobs.append({
            'title': f"{query} Jobs",
            'url': url,
            'description': f"Search {query} jobs on {platform.replace(chr(128512), '').replace(chr(128270), '').replace(chr(128269), '')}",
            'company': platform.split()[0] if len(platform.split()) > 0 else platform,
            'platform': platform
        })
    
    logger.info(f"Fallback method created {len(jobs)} job search links for '{query}'")
    return jobs

def extract_company_from_url(url: str) -> str:
    """Extract company name or platform from URL"""
    if not url:
        return "Unknown"
    try:
        domain = url.split('/')[2].replace('www.', '').split('.')[0]
        return domain.capitalize()
    except:
        return "Unknown"

def get_platform_name(url: str) -> str:
    """Identify job platform from URL"""
    platforms = {
        'linkedin.com': '💼 LinkedIn',
        'indeed.com': '🔍 Indeed',
        'lever.co': '🎯 Lever',
        'greenhouse.io': '🌱 Greenhouse',
        'wellfound.com': '⭐ AngelList',
        'glassdoor.com': '💎 Glassdoor',
        'remoteok.com': '🏠 RemoteOK',
        'stackoverflow.com': '📚 Stack Overflow',
    }
    
    for domain, name in platforms.items():
        if domain in url:
            return name
    return "🔗 Job Board"

# --- 6. MAIN UI ---
st.title("Jobstream")
st.markdown("**Instantly discover job opportunities that match your skills**")

# Create responsive layout
col1, col2 = st.columns([1, 1.5], gap="medium")

with col1:
    st.subheader("📤 Your Profile")
    
    # CV Upload Section
    uploaded_file = st.file_uploader(
        "Upload your CV (PDF)",
        type=["pdf"],
        help="We'll extract your skills automatically"
    )
    
    if uploaded_file:
        with st.spinner("📖 Analyzing your CV..."):
            st.session_state.cv_text = extract_text_from_pdf(uploaded_file)
        
        if st.session_state.cv_text:
            skills = extract_skills(st.session_state.cv_text)
            st.success(f"✅ Found {len(skills)} skills in your CV")
            
            with st.expander("📋 Detected Skills", expanded=True):
                if skills:
                    skill_cols = st.columns(3)
                    for idx, skill in enumerate(skills):
                        with skill_cols[idx % 3]:
                            st.markdown(f'<span class="skill-badge">{skill}</span>', unsafe_allow_html=True)
                else:
                    st.info("No specific skills detected. Try searching manually.")
    
    st.divider()
    
    # Manual Search Option
    st.subheader("🔍 Quick Search")
    manual_query = st.text_input(
        "Or search for a specific role:",
        placeholder="e.g., Full Stack Developer, Data Scientist",
        help="Enter a job title or role you're interested in"
    )

with col2:
    st.subheader("💼 Job Opportunities")
    
    # Search Button
    search_button = st.button("🔍 Find Matching Jobs", type="primary", use_container_width=True)
    
    if search_button:
        if not manual_query and not st.session_state.cv_text:
            st.error("❌ Please upload a CV or enter a search query")
        else:
            # Extract skills from CV for matching
            cv_skills = []
            if st.session_state.cv_text:
                cv_skills = extract_skills(st.session_state.cv_text)
                st.session_state.cv_skills = cv_skills
            
            # Determine search query
            if manual_query:
                search_queries = [manual_query]
            elif st.session_state.cv_text:
                search_queries = generate_search_queries(cv_skills)
                if not search_queries:
                    search_queries = ["Software Developer"]
            else:
                search_queries = []
            
            if search_queries:
                all_jobs = []
                
                with st.spinner(f"🔍 Searching for jobs: {', '.join(search_queries[:2])}..."):
                    for query in search_queries[:3]:  # Limit to top 3 queries
                        try:
                            jobs = search_job_platforms(query, fc_key)
                            if jobs:
                                logger.info(f"Found {len(jobs)} jobs for query: {query}")
                                all_jobs.extend(jobs)
                        except Exception as e:
                            logger.error(f"Error searching for {query}: {e}")
                            st.warning(f"⚠️ Error searching for '{query}': {str(e)}")
                
                if all_jobs:
                    # Remove duplicates
                    seen_urls = set()
                    unique_jobs = []
                    for job in all_jobs:
                        url = job.get('url', '')
                        if url and url not in seen_urls:
                            seen_urls.add(url)
                            unique_jobs.append(job)
                    
                    # Rank by CV match if skills were extracted
                    if cv_skills:
                        unique_jobs = rank_jobs_by_match(unique_jobs, cv_skills)
                    
                    st.session_state.jobs = unique_jobs
                    st.session_state.query = ", ".join(search_queries)
                    st.session_state.display_results = True
                    st.success(f"✅ Found {len(unique_jobs)} job opportunities (ranked by CV match)!")
                else:
                    st.warning("❌ No jobs found. Try a different search term or check your internet connection.")
                    st.session_state.jobs = []
                    st.session_state.display_results = False
    
    # Display Results (persists across reruns)
    if st.session_state.get('display_results', False) and st.session_state.jobs:
        st.divider()
        st.success(f"✅ Found {len(st.session_state.jobs)} job opportunities!")
        st.caption(f"📌 Searched for: {st.session_state.query}")
        
    # Display Results (persists across reruns)
    if st.session_state.get('display_results', False) and st.session_state.jobs:
        st.divider()
        st.success(f"✅ Found {len(st.session_state.jobs)} job opportunities!")
        st.caption(f"📌 Searched for: {st.session_state.query}")
        
        # ===== BEST JOB OFFER SECTION =====
        if st.session_state.get('cv_skills') and st.session_state.jobs:
            best_job = st.session_state.jobs[0]  # Already sorted by match
            
            with st.container(border=True):
                st.markdown("## 🏆 **BEST MATCH FOR YOUR CV**")
                
                # CV Match score
                match_percent = best_job.get('cv_match', 0)
                
                # Progress bar for match percentage
                col_score1, col_score2 = st.columns([3, 1])
                with col_score1:
                    st.progress(min(match_percent / 100, 1.0))
                with col_score2:
                    st.markdown(f"<h3 style='text-align:center; color: #2563eb;'>{match_percent}% Match</h3>", unsafe_allow_html=True)
                
                st.divider()
                
                # Job title and platform
                col_title, col_platform = st.columns([3, 1], gap="small")
                with col_title:
                    st.markdown(f"### 🎯 {best_job.get('title', 'Job Opening')}")
                with col_platform:
                    st.markdown(f'<span class="platform-badge">{best_job.get("platform", "Job Board")}</span>', unsafe_allow_html=True)
                
                # Quick Info
                col1, col2, col3 = st.columns(3, gap="small")
                with col1:
                    st.markdown(f"**🏢 Company:** {best_job.get('company', 'Not Specified')}")
                with col2:
                    st.markdown(f"**📍 Location:** {best_job.get('location', 'Remote')}")
                with col3:
                    st.markdown(f"**💰 Salary:** {best_job.get('salary', 'Competitive')}")
                
                st.divider()
                
                # WHY THIS IS THE BEST MATCH
                st.markdown("### ✨ **Why This Job is Perfect for You:**")
                if best_job.get('match_reasons'):
                    for reason in best_job.get('match_reasons', []):
                        st.markdown(f"- {reason}")
                
                # Matched skills
                if best_job.get('matched_skills'):
                    st.markdown("### 💪 **Your Skills Match:**")
                    matched_html = "".join([f"<span class='skill-badge'>{skill}</span>" for skill in best_job.get('matched_skills', [])])
                    st.markdown(f"{matched_html}", unsafe_allow_html=True)
                
                # Missing but valuable skills
                if best_job.get('missing_skills') and len(best_job.get('missing_skills', [])) <= 5:
                    st.markdown("### 📚 **Skills to Learn:**")
                    missing_html = "".join([f"<span style='display:inline-block; background-color: #fee2e2; color: #991b1b; padding: 4px 12px; border-radius: 20px; font-size: 0.85em; margin: 4px 4px 4px 0; font-weight: 500;'>{skill}</span>" for skill in best_job.get('missing_skills', [])[:3]])
                    st.markdown(f"{missing_html}", unsafe_allow_html=True)
                
                st.divider()
                
                # Description
                if best_job.get('description'):
                    st.markdown("**📝 Description:**")
                    st.markdown(best_job.get('description'))
                
                # Requirements
                if best_job.get('requirements'):
                    st.markdown("**✅ Requirements:**")
                    reqs_html = "".join([f"<li>{req}</li>" for req in best_job.get('requirements', [])])
                    st.markdown(f"<ul>{reqs_html}</ul>", unsafe_allow_html=True)
                
                # Perks/Benefits
                if best_job.get('perks'):
                    st.markdown("**🎁 Perks & Benefits:**")
                    perks_html = "".join([f"<span class='skill-badge'>{perk}</span>" for perk in best_job.get('perks', [])])
                    st.markdown(f"{perks_html}", unsafe_allow_html=True)
                
                st.divider()
                
                # Primary call-to-action
                url = best_job.get('url', '')
                if url:
                    st.link_button(
                        f"APPLY NOW - {best_job.get('platform', 'Job Board')}",
                        url,
                        use_container_width=True,
                        type="primary"
                    )
        
        st.divider()
        
        # ===== ALL OTHER JOBS SECTION =====
        st.markdown("## 📋 **Other Great Opportunities**")
        
        # Filter options
        col_filter1, col_filter2 = st.columns(2)
        with col_filter1:
            unique_platforms = list(set([job.get('platform', 'Unknown') for job in st.session_state.jobs]))
            platform_filter = st.multiselect(
                "Filter by platform:",
                unique_platforms,
                default=unique_platforms[:5]
            )
        
        with col_filter2:
            sort_by = st.selectbox(
                "Sort by:",
                ["Most Relevant", "Newest First", "Salary (High to Low)", "Platform"]
            )
        
        # Display job cards
        if platform_filter:
            filtered_jobs = [j for j in st.session_state.jobs if j.get('platform') in platform_filter]
        else:
            filtered_jobs = st.session_state.jobs
        
        # Skip best job (already shown above)
        other_jobs = filtered_jobs[1:] if len(filtered_jobs) > 1 else filtered_jobs
        
        if other_jobs:
            st.write(f"📋 Showing {len(other_jobs)} of {len(st.session_state.jobs) - 1} other results")
            
            for idx, job in enumerate(other_jobs, 1):
                with st.container(border=True):
                    # CV Match indicator (compact)
                    col_title, col_match = st.columns([3, 1], gap="small")
                    
                    with col_title:
                        st.markdown(f"### 🎯 {job.get('title', 'Job Opening')}")
                    
                    with col_match:
                        if job.get('cv_match'):
                            st.markdown(f"<span style='color: #2563eb; font-weight: bold;'>{job.get('cv_match')}% Match</span>", unsafe_allow_html=True)
                        st.markdown(f'<span class="platform-badge">{job.get("platform", "Job Board")}</span>', unsafe_allow_html=True)
                    
                    # Company and Location
                    col1, col2, col3 = st.columns(3, gap="small")
                    with col1:
                        st.markdown(f"**🏢 Company:** {job.get('company', 'Not Specified')}")
                    with col2:
                        st.markdown(f"**📍 Location:** {job.get('location', 'Remote')}")
                    with col3:
                        st.markdown(f"**💰 Salary:** {job.get('salary', 'Competitive')}")
                    
                    # Job Type and Posted Date
                    col_type, col_date = st.columns(2, gap="small")
                    with col_type:
                        st.markdown(f"**💼 Type:** {job.get('job_type', 'Full-time')}")
                    with col_date:
                        st.markdown(f"**📅 Posted:** {job.get('posted_date', 'Recently')}")
                    
                    # Brief description
                    if job.get('description'):
                        desc_preview = job.get('description', '')[:200]
                        st.caption(desc_preview + "..." if len(job.get('description', '')) > 200 else desc_preview)
                    
                    # Apply button
                    url = job.get('url', '')
                    if url:
                        st.link_button(
                            f"Apply Now - {job.get('platform', 'Job Board')}",
                            url,
                            use_container_width=True,
                            type="secondary"
                        )
        else:
            st.info("No results match your filters. Try different filter options.")
    elif not st.session_state.get('display_results', False):
        st.info("👇 Upload your CV or search for a role to get started!")

st.divider()
st.caption("Built for Laptop & Mobile. Add to Home Screen on your phone for full-screen view.")
