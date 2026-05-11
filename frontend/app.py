import os

import requests
import streamlit as st
from dotenv import load_dotenv

from streamlit.components.v1 import html as st_html

load_dotenv()

API_URL = (
    os.getenv(
        "API_URL",
        "http://127.0.0.1:8000",
    ).rstrip("/")
)


def _api_headers():

    key = os.getenv(
        "JOB_HUNTER_API_KEY",
        "",
    ).strip()

    if key:

        return {
            "X-Api-Key": key,
        }

    return {}


def api_post(
    path: str,
    **kwargs,
):

    url = (
        path
        if path.startswith("http")
        else f"{API_URL}{path}"
    )

    headers = kwargs.pop(
        "headers",
        None,
    ) or {}

    headers.update(_api_headers())

    kwargs["headers"] = headers

    try:

        return requests.post(
            url,
            timeout=kwargs.pop(
                "timeout",
                300,
            ),
            **kwargs,
        )

    except requests.RequestException as exc:

        st.error(
            "Could not reach the API at "
            f"`{API_URL}`. Start it with: "
            "`python -m uvicorn app.api.main:app --reload`\n\n"
            f"Details: {exc}"
        )

        st.stop()


def response_json_or_none(
    response,
):

    try:

        return response.json()

    except ValueError:

        return None

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="AI Job Hunter",
    page_icon="🚀",
    layout="wide"
)

# ======================================================
# CSS
# ======================================================

st.markdown("""
<style>
@import url("https://fonts.googleapis.com/css2?family=Nunito:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&display=swap");

:root {
    --accent: #14B8A6;         /* teal */
    --accent-hover: #0D9488;   /* teal-600 */
    --accent-soft: #2DD4BF;    /* teal-400 */
    /* Upload Resume / LinkedIn PDF — blue theme */
    --sidebar-upload-bg: #172554;       /* blue-950 */
    --sidebar-upload-border: #3b82f6; /* blue-500 */
    --sidebar-upload-text: #93c5fd;    /* blue-300 — icons / secondary */
    --sidebar-upload-text-strong: #60a5fa; /* blue-400 — labels & filenames */
    --sidebar-upload-text-muted: #bfdbfe;  /* blue-200 — file size */
    --sidebar-upload-pill-bg: #1e3a8a;     /* blue-900 — selected file row */
    --sidebar-upload-btn: #1d4ed8;        /* blue-700 — Browse */
    --sidebar-upload-btn-hover: #2563eb;   /* blue-600 */
    /* Job description textarea — orange theme */
    --jd-bg: #431407;           /* orange-950 */
    --jd-border: #ea580c;       /* orange-600 */
    --jd-text: #fdba74;         /* orange-300 */
    --jd-placeholder: #fb923c;  /* orange-400 */
    --jd-caret: #fed7aa;        /* orange-200 */
    --font-ui: "Nunito", "Segoe UI", ui-sans-serif, system-ui, sans-serif;
    --font-mono: ui-monospace, "Cascadia Code", "Source Code Pro", Menlo, monospace;
}

/* Cozy, friendly base typography */
html, body {
    font-family: var(--font-ui);
}

.stApp {
    background-color: #020817;
    color: white;
    font-family: var(--font-ui) !important;
    font-size: 17px;
    line-height: 1.65;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

.stApp textarea,
.stApp input,
.stApp button,
.stApp [data-baseweb="tab"] {
    font-family: var(--font-ui) !important;
}

/* Sidebar ~1/3 of viewport for more room (job description, uploads) */
section[data-testid="stSidebar"] {
    width: 33.333vw !important;
    min-width: 280px !important;
    flex-shrink: 0 !important;
    box-sizing: border-box !important;
    background: linear-gradient(
        180deg,
        #0F172A,
        #020617
    );
    border-right: 1px solid #1E293B;
}

section[data-testid="stSidebar"] > div:first-child {
    width: 100% !important;
}

/* Sidebar copy (do NOT force white on labels/spans — breaks file upload widgets) */
section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown span {
    color: #e2e8f0 !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: white !important;
}

/* Labels next to file uploaders (Streamlit puts label outside stFileUploader) */
section[data-testid="stSidebar"] div:has([data-testid="stFileUploader"]) label {
    color: var(--sidebar-upload-text-strong) !important;
}

/* Job description label — orange to match textarea (wins over default widget label) */
section[data-testid="stSidebar"] div:has(.stTextArea) [data-testid="stWidgetLabel"] {
    color: var(--jd-text) !important;
}

/* Other sidebar widget labels (uploads) — blue */
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
    color: var(--sidebar-upload-text-strong) !important;
}

/* Job description only: orange text on dark orange panel (.stTextArea = streamlit text_area) */
section[data-testid="stSidebar"] .stTextArea textarea {
    min-height: 280px !important;
    background-color: var(--jd-bg) !important;
    color: var(--jd-text) !important;
    border: 2px solid var(--jd-border) !important;
    border-radius: 12px !important;
    caret-color: var(--jd-caret) !important;
}

section[data-testid="stSidebar"] .stTextArea textarea::placeholder {
    color: var(--jd-placeholder) !important;
    opacity: 1 !important;
}

section[data-testid="stSidebar"] .stTextArea [data-baseweb="textarea"] {
    background-color: var(--jd-bg) !important;
    border-color: var(--jd-border) !important;
}

section[data-testid="stSidebar"] input[type="text"] {
    background-color: #111827 !important;
    color: white !important;
    border: 1px solid #1E293B !important;
}

/* ---- File uploader: blue dropzones + readable text ---- */
section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background-color: transparent !important;
    border: none !important;
    padding: 0 !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploader"] section {
    background-color: var(--sidebar-upload-bg) !important;
    border: 2px solid var(--sidebar-upload-border) !important;
    border-radius: 12px !important;
}

/* Inner dropzone / rows (Streamlit + Base Web vary by version) */
section[data-testid="stSidebar"] [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"],
section[data-testid="stSidebar"] [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] > div,
section[data-testid="stSidebar"] [data-testid="stFileUploader"] [data-baseweb="file-uploader"],
section[data-testid="stSidebar"] [data-testid="stFileUploader"] [data-baseweb="file-uploader"] > div,
section[data-testid="stSidebar"] [data-testid="stFileUploader"] div[class*="fileUploader"] {
    background-color: var(--sidebar-upload-bg) !important;
    background-image: none !important;
    border-color: var(--sidebar-upload-border) !important;
    color: var(--sidebar-upload-text) !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploader"] button {
    background-color: var(--sidebar-upload-btn) !important;
    border: 1px solid var(--sidebar-upload-border) !important;
    color: #ffffff !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploader"] button:hover {
    background-color: var(--sidebar-upload-btn-hover) !important;
}

/* Uploader text: blue tones except Browse buttons */
section[data-testid="stSidebar"] [data-testid="stFileUploader"] *:not(button) {
    color: var(--sidebar-upload-text-strong) !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploader"] small,
section[data-testid="stSidebar"] [data-testid="stFileUploader"] [class*="caption"],
section[data-testid="stSidebar"] [data-testid="stFileUploader"] [class*="Caption"] {
    color: var(--sidebar-upload-text-muted) !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploader"] button {
    color: #ffffff !important;
}

/* Selected file pill / filename (Streamlit versions vary) */
section[data-testid="stSidebar"] [data-testid="stFileUploader"] [data-testid="stUploadedFile"] {
    background-color: var(--sidebar-upload-pill-bg) !important;
    border: 1px solid var(--sidebar-upload-border) !important;
    border-radius: 12px !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploader"] [data-testid="stUploadedFile"],
section[data-testid="stSidebar"] [data-testid="stFileUploader"] [data-testid="stUploadedFile"] *:not(button) {
    color: var(--sidebar-upload-text-strong) !important;
    -webkit-text-fill-color: var(--sidebar-upload-text-strong) !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploader"] [data-testid="stUploadedFile"] svg {
    fill: var(--sidebar-upload-text) !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploader"] [data-testid="stUploadedFile"] small {
    color: var(--sidebar-upload-text-muted) !important;
    -webkit-text-fill-color: var(--sidebar-upload-text-muted) !important;
}

/* Base Web / inner rows sometimes stay white — force surface */
section[data-testid="stSidebar"] [data-testid="stFileUploader"] [data-baseweb="typography"],
section[data-testid="stSidebar"] [data-testid="stFileUploader"] li,
section[data-testid="stSidebar"] [data-testid="stFileUploader"] [role="listitem"] {
    background-color: transparent !important;
    color: var(--sidebar-upload-text-strong) !important;
}

h1, h2, h3 {
    color: white !important;
    font-family: var(--font-ui) !important;
    letter-spacing: -0.02em;
}

h1 {
    font-weight: 800 !important;
    line-height: 1.15 !important;
}

h2, h3 {
    font-weight: 700 !important;
    line-height: 1.25 !important;
}

p, li {
    font-family: var(--font-ui);
    color: #CBD5E1;
    line-height: 1.7;
}

/* Caption under title — softer, friendly */
[data-testid="stCaptionContainer"] {
    font-family: var(--font-ui) !important;
    font-weight: 500 !important;
    font-size: 1.05rem !important;
    color: #94a3b8 !important;
    line-height: 1.55 !important;
}

/* Keep code readable */
.stCodeBlock,
pre,
code,
.stMarkdown code {
    font-family: var(--font-mono) !important;
}

/* BUTTONS */

.stButton button {

    background: linear-gradient(
        135deg,
        var(--accent),
        #8B5CF6
    );

    color: white !important;

    border: none;

    border-radius: 12px;

    font-weight: 700;

    letter-spacing: 0.02em;

    width: 100%;

    height: 48px;

    font-size: 16px;
}

.stButton button:hover {

    background: linear-gradient(
        135deg,
        var(--accent-hover),
        #7C3AED
    );
}

/* FILE UPLOADER */

[data-testid="stFileUploader"] {

    background-color: #111827;

    border-radius: 12px;

    border: 1px solid #1E293B;

    padding: 10px;
}

/* TEXT AREA */

textarea {

    background-color: #111827 !important;

    color: white !important;

    border-radius: 12px !important;
}

/* TABS */

.stTabs [data-baseweb="tab"] {

    color: #CBD5E1;

    font-size: 16px;

    font-weight: 700;

    letter-spacing: 0.01em;
}

.stTabs [aria-selected="true"] {

    color: var(--accent) !important;
}

/* CONTENT PANELS */

.panel {

    background-color: #111827;

    border-radius: 18px;

    padding: 30px;

    border: 1px solid #1E293B;
}

/* DIVIDER */

hr {

    border-color: #1E293B;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# SESSION STATE
# ======================================================

defaults = {
    "profile": "",
    "analysis": "",
    "resume": "",
    "cover_letter": "",
    "match_score": 0,
    "ats_score": 0,
    "missing_skills": [],
    "has_resume": False,
    "has_linkedin": False,
    "has_job_description": False,
    "resume_uploaded_name": "",
    "linkedin_uploaded_name": "",
}

for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value

# ======================================================
# HEADER
# ======================================================

st.title("🚀 AI Job Hunter")

st.caption(
    "AI-Powered Resume & Career Optimization Platform"
)

st.markdown("---")

# ======================================================
# SIDEBAR
# ======================================================

with st.sidebar:

    st.header("📂 Upload Documents")

    # ==================================================
    # RESUME
    # ==================================================

    uploaded_resume = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx", "txt"]
    )

    if uploaded_resume:
        if st.session_state.get("resume_uploaded_name") != uploaded_resume.name:
            st.session_state["resume_uploaded_name"] = uploaded_resume.name

            files = {
                "file": (
                    uploaded_resume.name,
                    uploaded_resume.getvalue()
                )
            }

            response = api_post(
                "/upload-resume",
                files=files,
            )

            if response.status_code == 200:
                st.session_state["has_resume"] = True

                st.success(
                    "Resume uploaded successfully"
                )
            else:
                st.error(response.text)

    # ==================================================
    # LINKEDIN PDF
    # ==================================================

    linkedin_pdf = st.file_uploader(
        "Upload LinkedIn PDF",
        type=["pdf"]
    )

    if linkedin_pdf:
        if st.session_state.get("linkedin_uploaded_name") != linkedin_pdf.name:
            st.session_state["linkedin_uploaded_name"] = linkedin_pdf.name

            files = {
                "file": (
                    linkedin_pdf.name,
                    linkedin_pdf.getvalue()
                )
            }

            response = api_post(
                "/upload-linkedin",
                files=files,
            )

            if response.status_code == 200:
                st.session_state["has_linkedin"] = True

                st.success(
                    "LinkedIn PDF uploaded"
                )
            else:
                st.error(response.text)

    st.markdown("---")

    # ==================================================
    # JOB DESCRIPTION
    # ==================================================

    st.header("🎯 Target Job")

    job_description = st.text_area(
        "Paste Job Description",
        height=380,
        key="job_description_input",
        label_visibility="visible",
    )

    if st.button("Save Job Description"):

        response = api_post(
            "/save-job-description",
            json={
                "job_description": job_description
            },
        )

        if response.status_code == 200:
            st.session_state["has_job_description"] = True

            st.success(
                "Job Description saved"
            )
        else:
            st.error(response.text)

    st.markdown("---")

    # ==================================================
    # AI ACTIONS
    # ==================================================

    st.header("🚀 AI Actions")

    can_profile = st.session_state.get("has_resume") or st.session_state.get("has_linkedin")
    can_with_job = can_profile and st.session_state.get("has_job_description")

    if not can_profile:
        st.warning("Upload a resume and/or LinkedIn PDF to enable AI actions.")
    elif not st.session_state.get("has_job_description"):
        st.info("Save a job description to enable Match/Resume/Cover Letter.")

    # PROFILE

    if st.button("Generate Profile", disabled=not can_profile):

        response = api_post("/profile")

        if response.status_code != 200:
            st.error(response.text)
            st.stop()

        data = response_json_or_none(response)

        if data is None:

            st.error(
                "API returned a response that is not valid JSON."
            )

            st.stop()

        st.session_state["profile"] = data.get(
            "profile",
            ""
        )

        st.success(
            "Profile generated"
        )

        st.rerun()

    # MATCH ANALYSIS

    if st.button("Analyze Job Match", disabled=not can_with_job):

        response = api_post("/match")

        if response.status_code != 200:
            st.error(response.text)
            st.stop()

        data = response_json_or_none(response)

        if data is None:

            st.error(
                "API returned a response that is not valid JSON."
            )

            st.stop()

        st.session_state["analysis"] = data.get(
            "analysis",
            ""
        )

        st.session_state["match_score"] = data.get(
            "match_score",
            0
        )

        st.session_state["ats_score"] = data.get(
            "ats_score",
            0
        )

        st.session_state["missing_skills"] = data.get(
            "missing_skills",
            []
        )

        st.success(
            "Match analysis completed"
        )

        st.rerun()

    # RESUME

    if st.button("Generate AI Resume", disabled=not can_with_job):

        response = api_post("/resume")

        if response.status_code != 200:
            st.error(response.text)
            st.stop()

        data = response_json_or_none(response)

        if data is None:

            st.error(
                "API returned a response that is not valid JSON."
            )

            st.stop()

        st.session_state["resume"] = data.get(
            "resume",
            ""
        )

        st.success(
            "AI Resume generated"
        )

        st.rerun()

    # COVER LETTER

    if st.button("Generate Cover Letter", disabled=not can_with_job):

        response = api_post("/cover-letter")

        if response.status_code != 200:
            st.error(response.text)
            st.stop()

        data = response_json_or_none(response)

        if data is None:

            st.error(
                "API returned a response that is not valid JSON."
            )

            st.stop()

        st.session_state["cover_letter"] = data.get(
            "cover_letter",
            ""
        )

        st.success(
            "Cover Letter generated"
        )

        st.rerun()

# ======================================================
# DASHBOARD DATA
# ======================================================

match_score = st.session_state.get(
    "match_score",
    0
)

ats_score = st.session_state.get(
    "ats_score",
    0
)

missing_skills = st.session_state.get(
    "missing_skills",
    []
)

# ======================================================
# SCORE STATUS
# ======================================================

def get_score_status(score):

    if score >= 85:

        return (
            "#22C55E",
            "Excellent Match"
        )

    elif score >= 70:

        return (
            "#FACC15",
            "Good Match"
        )

    return (
        "#EF4444",
        "Needs Improvement"
    )

match_color, match_status = get_score_status(
    match_score
)

ats_color, ats_status = get_score_status(
    ats_score
)

skills_color = (
    "#22C55E"
    if len(missing_skills) <= 3
    else "#EF4444"
)

skills_status = (
    "Strong Alignment"
    if len(missing_skills) <= 3
    else "Skill Gaps Detected"
)

# ======================================================
# DASHBOARD
# ======================================================

col1, col2, col3 = st.columns(3)

# ======================================================
# METRIC CARD RENDERER (HTML component avoids markdown escaping)
# ======================================================

def render_metric_card(
    title: str,
    value: str,
    value_color: str,
    subtitle: str,
    height: int = 155
):
    st_html(
        f"""
<style>
@import url("https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap");
</style>
<div style="
    font-family:'Nunito',ui-sans-serif,system-ui,sans-serif;
    background: linear-gradient(135deg,#0F172A,#111827);
    padding:22px 18px;
    border-radius:18px;
    border:1px solid #1E293B;
    text-align:center;
    box-shadow:0 0 25px rgba(20,184,166,0.12);
">
  <div style="
      color:#14B8A6;
      font-size:15px;
      font-weight:700;
      margin-bottom:10px;
      letter-spacing:0.02em;
  ">{title}</div>
  <div style="
      color:{value_color};
      font-size:42px;
      font-weight:800;
      line-height:1.05;
  ">{value}</div>
  <div style="
      color:#CBD5E1;
      margin-top:10px;
      font-size:13px;
      font-weight:600;
      line-height:1.35;
  ">{subtitle}</div>
</div>
""",
        height=height,
    )

# MATCH SCORE

with col1:
    render_metric_card(
        title="Match Score",
        value=f"{match_score}%",
        value_color=match_color,
        subtitle=match_status,
    )

# ATS SCORE

with col2:
    render_metric_card(
        title="ATS Score",
        value=f"{ats_score}%",
        value_color=ats_color,
        subtitle=ats_status,
    )

# MISSING SKILLS

with col3:
    render_metric_card(
        title="Missing Skills",
        value=str(len(missing_skills)),
        value_color=skills_color,
        subtitle=skills_status,
    )

# ======================================================
# MISSING SKILLS DETAIL
# ======================================================

if missing_skills:

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="panel">',
        unsafe_allow_html=True
    )

    st.markdown(
        """
<h3 style="
    color:var(--accent);
    margin-bottom:20px;
">
    Missing Skills Details
</h3>
""",
        unsafe_allow_html=True,
    )

    for skill in missing_skills:

        st.markdown(
            f"""
<div style="
    background:#0F172A;
    padding:12px;
    border-radius:10px;
    margin-bottom:10px;
    border-left:4px solid #EF4444;
    color:white;
    font-size:16px;
">
    {skill}
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# ======================================================
# TABS
# ======================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "👤 Profile",
    "📊 Match Analysis",
    "📄 AI Resume",
    "✉️ Cover Letter"
])

# PROFILE

with tab1:

    st.markdown(
        '<div class="panel">',
        unsafe_allow_html=True
    )

    if not st.session_state.get("profile"):
        st.info(
            "Upload your resume + LinkedIn PDF, save a job description, then click **Generate Profile** in the sidebar."
        )
    else:
        st.markdown(st.session_state["profile"])

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

# MATCH ANALYSIS

with tab2:

    st.markdown(
        '<div class="panel">',
        unsafe_allow_html=True
    )

    if not st.session_state.get("analysis"):
        st.info(
            "Click **Run Match Analysis** in the sidebar to generate the match report and scores."
        )
    else:
        st.markdown(st.session_state["analysis"])

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

# RESUME

with tab3:

    st.markdown(
        '<div class="panel">',
        unsafe_allow_html=True
    )

    if not st.session_state.get("resume"):
        st.info(
            "Click **Generate Resume** in the sidebar to create an ATS-optimized version tailored to the job."
        )
    else:
        st.code(
            st.session_state["resume"],
            language="markdown"
        )

    if st.session_state.get("resume"):

        st.download_button(
            label="⬇ Download Resume",
            data=st.session_state["resume"],
            file_name="ai_resume.txt",
            mime="text/plain"
        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

# COVER LETTER

with tab4:

    st.markdown(
        '<div class="panel">',
        unsafe_allow_html=True
    )

    if not st.session_state.get("cover_letter"):
        st.info(
            "Click **Generate Cover Letter** in the sidebar after saving a job description."
        )
    else:
        st.code(
            st.session_state["cover_letter"],
            language="markdown"
        )

    if st.session_state.get("cover_letter"):

        st.download_button(
            label="⬇ Download Cover Letter",
            data=st.session_state["cover_letter"],
            file_name="cover_letter.txt",
            mime="text/plain"
        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )