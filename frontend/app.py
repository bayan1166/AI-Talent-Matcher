import streamlit as st
import requests

st.set_page_config(
    page_title="TalentMatch AI | Enterprise Hub",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_URL = "https://ai-talent-matcher-0bvk.onrender.com"

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

div[data-testid="stSidebarNav"] {display: none;}
footer {visibility: hidden;}
header {background-color: transparent !important;}
.stDeployButton {display: none !important;}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp {
    background: radial-gradient(circle at 50% 0%, var(--brand-red-glow) 0%, transparent 40%), var(--bg-deep);
    color: var(--text-primary);
}

.glass-card {
    background: var(--bg-panel);
    border: 1px solid var(--border-line);
    border-radius: 14px;
    padding: 24px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    margin-bottom: 20px;
}
.hero { margin-bottom: 30px; }
.hero h1 { font-family: 'Outfit', sans-serif; font-weight: 700; color: var(--text-primary); font-size: 2.2rem; margin-bottom: 8px;}
.hero h1 span { color: var(--brand-red); }
.hero p { color: var(--text-muted); font-size: 1.1rem; }
.tag {
    display: inline-block; background: var(--brand-red-soft); border: 1px solid rgba(227,53,43,0.3);
    color: #FF8F88; padding: 6px 12px; border-radius: 6px; font-size: 0.85rem; margin-right: 8px; margin-bottom: 8px;
}
.metric-value { font-family: 'JetBrains Mono', monospace; font-size: 1.4rem; font-weight: 700; color: white; margin-bottom: 4px; }
.stChatMessage { background-color: transparent !important; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="font-family:'Outfit',sans-serif; font-size:1.8rem; font-weight:700; color:#FFF; margin-bottom:4px;">
        TalentMatch<span style="color:#E3352B;">.ai</span>
    </div>
    <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:#E3352B; letter-spacing:0.12em; text-transform:uppercase; margin-bottom:30px;">
        Enterprise Hub v2.0
    </div>
    """, unsafe_allow_html=True)
    
    view = st.radio(
        "Navigation", 
        ["Talent Scout", "Team Builder", "Skill Gap Analysis", "AI Agent Chat"],
        label_visibility="collapsed"
    )
    
    st.markdown("<hr style='border-color:#272E38; margin:20px 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:11px; color:#8E9BAE; text-transform:uppercase;'>System Status: <span style='color:#00E676;'>Online</span></div>", unsafe_allow_html=True)

if view == "Talent Scout":
    st.markdown("<div class='hero'><h1>Skill-Driven <span>Talent Intelligence</span></h1><p>Search the vector index for optimal candidate alignment.</p></div>", unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            skills_query = st.text_input("Required Technical Competencies", placeholder="e.g., Python, Docker, Machine Learning...")
            if st.button("Find Matching Talent", use_container_width=True):
                if skills_query:
                    with st.spinner("Processing vector similarity scores..."):
                        try:
                            res = requests.get(f"{BASE_URL}/match", params={"skills": skills_query})
                            if res.status_code == 200:
                                data = res.json()
                                st.success("Match Found")
                                st.markdown(f"""
                                <div style="margin-top:15px; border-left: 3px solid var(--brand-red); padding-left: 15px;">
                                    <h3 style="margin:0; font-family:'JetBrains Mono';">{data['top_candidate']}</h3>
                                    <span class="tag">{data['major']}</span>
                                    <p style="margin-top:10px; color:#D1D8E0;">{data['ai_reasoning']}</p>
                                </div>
                                """, unsafe_allow_html=True)
                        except Exception:
                            st.error("Connection failed.")
            st.markdown("</div>", unsafe_allow_html=True)

elif view == "Team Builder":
    st.markdown("<div class='hero'><h1>Autonomous <span>Team Assembly</span></h1><p>Form highly synergistic project teams based on skill coverage.</p></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        brief = st.text_area("Project Brief and Required Capabilities", placeholder="Describe the project and the technical stack required...")
    with col2:
        team_size = st.slider("Team Size", min_value=2, max_value=8, value=4)
        
    if st.button("Assemble Team", use_container_width=True, type="primary"):
        if brief:
            with st.spinner("Assembling team..."):
                res = requests.post(f"{BASE_URL}/team-builder", json={"project_brief": brief, "team_size": team_size})
                if res.status_code == 200:
                    data = res.json()
                    st.markdown(f"### Team Skill Coverage: <span style='color:var(--brand-red);'>{data['combined_skill_coverage']}</span>", unsafe_allow_html=True)
                    
                    cols = st.columns(min(team_size, 4))
                    for idx, member in enumerate(data['proposed_team']):
                        with cols[idx % 4]:
                            st.markdown(f"""
                            <div class="glass-card" style="text-align:center; padding:15px;">
                                <div class="metric-value">{member['employee_id']}</div>
                                <div style="color:var(--brand-red); margin-bottom:10px; font-weight:bold;">{member['match_score']} Match</div>
                                <div class="tag" style="font-size:0.75rem; display:block;">{member['primary_skills']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    st.info(data['actionable_recommendation'])

elif view == "Skill Gap Analysis":
    st.markdown("<div class='hero'><h1>Skill Gap <span>Analysis</span></h1><p>Identify capability deficits and auto-recommend training.</p></div>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        emp_id = st.text_input("Employee ID", value="EEID-105")
    with c2:
        target_role = st.selectbox("Target Role", ["Senior Data Engineer", "NLP Engineer", "Cloud Architect"])
        
    if st.button("Analyze Profile", use_container_width=True):
        with st.spinner("Analyzing profile..."):
            res = requests.post(f"{BASE_URL}/skill-gap", json={"employee_id": emp_id, "target_role": target_role})
            if res.status_code == 200:
                data = res.json()
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("<h4 style='margin-bottom:15px;'>Analysis Results</h4>", unsafe_allow_html=True)
                st.write(f"**Current Skills:** {', '.join(data['current_skills'])}")
                
                if data['missing_skills']:
                    st.warning(data['gap_analysis'])
                    st.write("**Missing Capabilities:**")
                    for skill in data['missing_skills']:
                        st.markdown(f"<span class='tag' style='background:rgba(255,152,0,0.1); color:#FF9800; border-color:#FF9800;'>{skill}</span>", unsafe_allow_html=True)
                    
                    st.write("")
                    st.write("**Recommended Training:**")
                    for rec in data['training_recommendations']:
                        st.success(rec)
                else:
                    st.success(data['gap_analysis'])
                st.markdown("</div>", unsafe_allow_html=True)

elif view == "AI Agent Chat":
    st.markdown("<div class='hero'><h1>Talent <span>AI Agent</span></h1><p>Ask complex workforce questions in natural language.</p></div>", unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello. I am the TalentMatch AI. Ask me to build a team, find a candidate, or check skill gaps."}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                try:
                    payload = {"messages": [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]}
                    res = requests.post(f"{BASE_URL}/ask", json=payload)
                    
                    if res.status_code == 200:
                        data = res.json()
                        st.markdown(data["answer"])
                        
                        with st.expander("View AI Execution Trace"):
                            for trace in data["tool_trace"]:
                                st.code(trace, language="log")
                            if data["cited_records"]:
                                st.write("**Cited Records:**", ", ".join(data["cited_records"]))
                                
                        st.session_state.messages.append({"role": "assistant", "content": data["answer"]})
                    else:
                        st.error("Agent encountered an error.")
                except Exception:
                    st.error("Failed to connect to AI Agent.")