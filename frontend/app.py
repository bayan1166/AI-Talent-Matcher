import streamlit as st
import requests

# Page setup
st.set_page_config(
    page_title="TalentMatch AI | Talent Intelligence", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

BACKEND_URL = "http://127.0.0.1:8000/match"

# Theme styling & layout adjustments
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

<style>
:root {
    --bg-deep: #090B0E;         
    --bg-panel: #12161B;        
    --bg-raised: #1A1F26;       
    --border-line: #272E38;     
    --brand-red: #E3352B;       
    --brand-red-soft: rgba(227, 53, 43, 0.12);
    --brand-red-glow: rgba(227, 53, 43, 0.25);
    --text-primary: #FFFFFF;
    --text-muted: #8E9BAE;
}

/* Hide Streamlit default badges, Deploy button, and footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {background-color: transparent !important;}
.stDeployButton {display: none !important;}
[data-testid="stAppDeployButton"] {display: none !important;}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: 
        radial-gradient(circle at 50% 0%, var(--brand-red-glow) 0%, transparent 40%),
        var(--bg-deep);
    color: var(--text-primary);
}

/* Hero section */
.hero { 
    max-width: 720px; 
    margin: 25px auto 10px auto; 
    text-align: center; 
}
.hero-badge {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--brand-red);
    background: var(--brand-red-soft);
    padding: 6px 14px;
    border-radius: 20px;
    border: 1px solid rgba(227, 53, 43, 0.3);
    margin-bottom: 16px;
}
.hero h1 {
    font-family: 'Outfit', sans-serif;
    font-weight: 700;
    font-size: 2.5rem;
    color: var(--text-primary);
    margin: 0 0 12px 0;
    letter-spacing: -0.02em;
}
.hero h1 span {
    color: var(--brand-red);
}
.hero p {
    color: var(--text-muted);
    font-size: 1.05rem;
    line-height: 1.6;
    margin: 0 auto;
}

/* Search container */
.search-wrapper {
    max-width: 680px;
    margin: 30px auto 0 auto;
    background: var(--bg-panel);
    border: 1px solid var(--border-line);
    border-radius: 14px;
    padding: 24px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
}
.search-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--brand-red);
    margin-bottom: 10px;
    display: block;
}

/* Input field adjustments */
.stTextInput > div > div > input {
    background: var(--bg-raised) !important;
    border: 1px solid var(--border-line) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-size: 0.95rem !important;
    padding: 14px 16px !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--brand-red) !important;
    box-shadow: 0 0 0 1px var(--brand-red) !important;
}
.stTextInput input::placeholder { 
    color: var(--text-muted) !important; 
    opacity: 0.65; 
}

/* Action button */
.stButton > button {
    width: 100%;
    border-radius: 8px;
    height: 3.2em;
    margin-top: 12px;
    background: var(--brand-red);
    color: white;
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
    font-size: 1rem;
    letter-spacing: 0.02em;
    border: none;
    transition: all 0.2s ease;
}
.stButton > button:hover { 
    background-color: #FA3E33; 
    transform: translateY(-1px); 
    box-shadow: 0 4px 14px var(--brand-red-glow); 
    color: white;
}

/* Result brief card */
.brief-card {
    max-width: 680px;
    margin: 28px auto 0 auto;
    background: var(--bg-panel);
    border: 1px solid var(--border-line);
    border-radius: 14px;
    padding: 0;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    animation: fadeIn 0.3s ease-out;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
.brief-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 24px;
    background: var(--brand-red-soft);
    border-bottom: 1px solid rgba(227, 53, 43, 0.2);
}
.brief-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--brand-red);
    font-weight: 600;
}
.brief-body { 
    padding: 24px; 
}
.brief-grid {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
    padding-bottom: 18px;
    border-bottom: 1px solid var(--border-line);
}
.field-label {
    font-size: 11px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 6px;
}
.field-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.3rem;
    color: var(--text-primary);
    font-weight: 600;
}
.major-tag {
    display: inline-block;
    background: var(--brand-red-soft);
    border: 1px solid rgba(227, 53, 43, 0.3);
    color: #FF8F88;
    padding: 5px 14px;
    border-radius: 6px;
    font-size: 0.9rem;
}
.assessment { 
    margin-top: 20px; 
}
.assessment-text {
    font-size: 0.98rem;
    line-height: 1.65;
    color: #D1D8E0;
    border-left: 3px solid var(--brand-red);
    padding: 4px 0 4px 16px;
    background: linear-gradient(90deg, rgba(227,53,43,0.04), transparent);
}

/* Footer note */
.footer-note {
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.12em;
    color: var(--text-muted);
    margin-top: 50px;
    padding-bottom: 30px;
}
.footer-note span { color: var(--brand-red); }
</style>
""", unsafe_allow_html=True)

# Sidebar setup
with st.sidebar:
    st.markdown("""
    <div style="font-family:'Outfit',sans-serif; font-size:1.6rem; font-weight:700; color:#FFF; margin-bottom:4px;">
        TalentMatch<span style="color:#E3352B;">.ai</span>
    </div>
    <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:#E3352B; letter-spacing:0.12em; text-transform:uppercase; margin-bottom:20px;">
        Neural Talent Search
    </div>
    <div style="font-size:13px; color:#8E9BAE; line-height:1.6;">
        Evaluates skill prerequisites against employee profile records using vector embeddings to match semantic intent beyond exact keywords.
    </div>
    <hr style="border-color:#272E38; margin:20px 0;">
    
    <div style="font-size:11px; color:#8E9BAE; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:10px;">
        System Architecture
    </div>
    <div style="font-family:'JetBrains Mono',monospace; font-size:12px; color:#D1D8E0; line-height:2.0;">
        FastAPI <span style="color:#E3352B;">→</span> Service Layer<br>
        ChromaDB <span style="color:#E3352B;">→</span> Vector Index<br>
        PostgreSQL <span style="color:#E3352B;">→</span> Relational Store
    </div>
    """, unsafe_allow_html=True)

# Hero Header
st.markdown("""
<div class="hero">
    <div class="hero-badge">Autonomous Talent Scout</div>
    <h1>Skill-Driven <span>Talent Intelligence</span></h1>
    <p>Specify the technical stack and requirements to find the best candidate profile ranked by semantic similarity.</p>
</div>
""", unsafe_allow_html=True)

# Main Query Section
with st.container():
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.markdown('<span class="search-label">Required Technical Competencies</span>', unsafe_allow_html=True)
        skills_query = st.text_input(
            "Required Skills",
            placeholder="e.g., Python, Docker, PostgreSQL, Machine Learning...",
            label_visibility="collapsed"
        )
        search_btn = st.button("Find Matching Talent")

# Query Execution & Results Display
if search_btn:
    if skills_query.strip():
        with st.spinner("Processing vector similarity scores..."):
            try:
                response = requests.get(BACKEND_URL, params={"skills": skills_query.strip()}, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") == "success":
                        st.markdown(f"""
                        <div class="brief-card">
                            <div class="brief-header">
                                <span class="brief-title">Optimal Candidate Profile</span>
                                <span style="color:var(--brand-red); font-size:14px;">●</span>
                            </div>
                            <div class="brief-body">
                                <div class="brief-grid">
                                    <div>
                                        <div class="field-label">Candidate Identifier</div>
                                        <div class="field-value">{data['top_candidate']}</div>
                                    </div>
                                    <div>
                                        <div class="field-label">Field of Study</div>
                                        <span class="major-tag">{data['major']}</span>
                                    </div>
                                </div>
                                <div class="assessment">
                                    <div class="field-label">Alignment Evaluation</div>
                                    <div class="assessment-text">{data['ai_reasoning']}</div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error(f"Engine Error: {data.get('message')}")
                else:
                    st.error("Backend unreachable. Ensure FastAPI server is running on port 8000.")
            except Exception as e:
                st.error("Connection failed. Please check if the local server process is active.")
    else:
        st.warning("Please specify at least one skill requirement.")

# Footer
st.markdown("""
<div class="footer-note"><span>TALENTMATCH AI</span> &nbsp;·&nbsp; VECTOR RETRIEVAL ENGINE</div>
""", unsafe_allow_html=True)