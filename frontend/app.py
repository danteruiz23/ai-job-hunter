import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="AI Job Hunter",
    page_icon="🤖",
    layout="wide"
)

# =========================================
# CUSTOM CSS
# =========================================

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.metric-card {
    background-color: #1E1E1E;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    border: 1px solid #333;
}

.big-font {
    font-size: 40px;
    font-weight: bold;
}

.green {
    color: #00FF99;
}

.yellow {
    color: #FFD700;
}

.red {
    color: #FF4B4B;
}

.section-card {
    background-color: #1A1A1A;
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #333;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# SESSION STATE
# =========================================

defaults = {
    "profile": "",
    "analysis": "",
    "resume": "",
    "cover_letter": "",
    "match_score": 0,
    "ats_score": 0,
    "missing_skills": []
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value

# =========================================
# HEADER
# =========================================

st.title("🤖 AI Job Hunter")

st.caption(
    "AI-Powered Resume Optimization Platform"
)

st.markdown("---")

# =========================================
# SIDEBAR
# =========================================

with st.sidebar:

    st.header("📂 Upload Documents")

    uploaded_resume = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx", "txt"]
    )

    if uploaded_resume:

        files = {
            "file": (
                uploaded_resume.name,
                uploaded_resume.getvalue()
            )
        }

        response = requests.post(
            f"{API_URL}/upload-resume",
            files=files
        )

        if response.status_code == 200:

            st.success(
                "Resume uploaded"
            )

    linkedin_pdf = st.file_uploader(
        "Upload LinkedIn PDF",
        type=["pdf"]
    )

    if linkedin_pdf:

        files = {
            "file": (
                linkedin_pdf.name,
                linkedin_pdf.getvalue()
            )
        }

        response = requests.post(
            f"{API_URL}/upload-linkedin",
            files=files
        )

        if response.status_code == 200:

            st.success(
                "LinkedIn PDF uploaded"
            )

    st.markdown("---")

    st.header("📄 Job Description")

    job_description = st.text_area(
        "Paste Job Description",
        height=250
    )

    if st.button("Save Job Description"):

        response = requests.post(
            f"{API_URL}/save-job-description",
            json={
                "job_description": job_description
            }
        )

        if response.status_code == 200:

            st.success(
                "Job Description saved"
            )

    st.markdown("---")

    st.header("🚀 AI Actions")

    if st.button("Generate Profile"):

        response = requests.post(
            f"{API_URL}/profile"
        )

        data = response.json()

        st.session_state.profile = data.get(
            "profile",
            ""
        )

    if st.button("Run Match Analysis"):

        response = requests.post(
            f"{API_URL}/match"
        )

        data = response.json()

        st.session_state.analysis = data.get(
            "analysis",
            ""
        )

        st.session_state.match_score = data.get(
            "match_score",
            0
        )

        st.session_state.ats_score = data.get(
            "ats_score",
            0
        )

        st.session_state.missing_skills = data.get(
            "missing_skills",
            []
        )

    if st.button("Generate Suggested Resume"):

        response = requests.post(
            f"{API_URL}/resume"
        )

        data = response.json()

        st.session_state.resume = data.get(
            "resume",
            ""
        )

    if st.button("Generate Cover Letter"):

        response = requests.post(
            f"{API_URL}/cover-letter"
        )

        data = response.json()

        st.session_state.cover_letter = data.get(
            "cover_letter",
            ""
        )

# =========================================
# SCORE COLORS
# =========================================

def score_color(score):

    if score >= 80:
        return "green"

    elif score >= 60:
        return "yellow"

    return "red"

# =========================================
# DASHBOARD
# =========================================

col1, col2, col3 = st.columns(3)

match_color = score_color(
    st.session_state.match_score
)

ats_color = score_color(
    st.session_state.ats_score
)

with col1:

    st.markdown(f"""
    <div class="metric-card">
        <div>Match Score</div>
        <div class="big-font {match_color}">
            {st.session_state.match_score}%
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <div class="metric-card">
        <div>ATS Score</div>
        <div class="big-font {ats_color}">
            {st.session_state.ats_score}%
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown(f"""
    <div class="metric-card">
        <div>Missing Skills</div>
        <div class="big-font red">
            {len(st.session_state.missing_skills)}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =========================================
# TABS
# =========================================

tab1, tab2, tab3, tab4 = st.tabs([
    "👤 Profile",
    "📊 Match Analysis",
    "📄 Suggested Resume",
    "✉️ Cover Letter"
])

# =========================================
# PROFILE
# =========================================

with tab1:

    st.markdown("""
    <div class="section-card">
    """, unsafe_allow_html=True)

    st.subheader("Professional Profile")

    st.markdown(
        st.session_state.profile
    )

    st.markdown("</div>",
    unsafe_allow_html=True)

# =========================================
# MATCH ANALYSIS
# =========================================

with tab2:

    st.markdown("""
    <div class="section-card">
    """, unsafe_allow_html=True)

    st.subheader("AI Match Analysis")

    st.markdown(
        st.session_state.analysis
    )

    if st.session_state.missing_skills:

        st.subheader("Missing Skills")

        for skill in st.session_state.missing_skills:

            st.write(f"• {skill}")

    st.markdown("</div>",
    unsafe_allow_html=True)

# =========================================
# RESUME
# =========================================

with tab3:

    st.markdown("""
    <div class="section-card">
    """, unsafe_allow_html=True)

    st.subheader("Suggested Resume")

    st.markdown(
        st.session_state.resume
    )

    if st.session_state.resume:

        st.download_button(
            label="⬇ Download Resume",
            data=st.session_state.resume,
            file_name="suggested_resume.txt",
            mime="text/plain"
        )

    st.markdown("</div>",
    unsafe_allow_html=True)

# =========================================
# COVER LETTER
# =========================================

with tab4:

    st.markdown("""
    <div class="section-card">
    """, unsafe_allow_html=True)

    st.subheader("Cover Letter")

    st.markdown(
        st.session_state.cover_letter
    )

    if st.session_state.cover_letter:

        st.download_button(
            label="⬇ Download Cover Letter",
            data=st.session_state.cover_letter,
            file_name="cover_letter.txt",
            mime="text/plain"
        )

    st.markdown("</div>",
    unsafe_allow_html=True)