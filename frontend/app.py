import os
import sys

from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv

from streamlit.components.v1 import html as st_html

load_dotenv()

_frontend_dir = Path(
    __file__,
).resolve().parent

if str(_frontend_dir) not in sys.path:

    sys.path.insert(
        0,
        str(_frontend_dir),
    )

from i18n import text as ui_text

from theme_styles import build_stylesheet


def _resolve_api_url() -> str:

    explicit = (
        os.getenv(
            "API_URL",
            "",
        )
        .strip()
        .rstrip("/")
    )

    if explicit:

        return explicit

    hp = (
        os.getenv(
            "API_INTERNAL_HOSTPORT",
            "",
        )
        .strip()
    )

    if hp:

        if hp.startswith(
            (
                "http://",
                "https://",
            ),
        ):

            return hp.rstrip("/")

        return f"http://{hp}".rstrip("/")

    return "http://127.0.0.1:8000"


def t(
    key,
):

    return ui_text(
        st.session_state.get(
            "lang",
            "en",
        ),
        key,
    )


API_URL = _resolve_api_url()


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

        _lang = st.session_state.get(
            "lang",
            "en",
        )

        st.error(
            ui_text(
                _lang,
                "api_unreachable",
            ).format(
                url=API_URL,
                exc=exc,
            )
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
    layout="wide",
)

# ======================================================
# SESSION STATE DEFAULTS (language before UI strings)
# ======================================================

_defaults = {
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
    "lang": "en",
    "theme": "light",
}

for _key, _value in _defaults.items():

    if _key not in st.session_state:

        st.session_state[_key] = _value

# ======================================================
# CSS (dark / light via session theme)
# ======================================================

st.markdown(
    build_stylesheet(
        st.session_state.get(
            "theme",
            "light",
        ),
    ),
    unsafe_allow_html=True,
)

# ======================================================
# SESSION STATE
# ======================================================

# ======================================================
# HEADER (title left, language + theme top-right)
# ======================================================

_header_left, _header_right = st.columns(
    [
        4,
        1.2,
    ],
)

with _header_left:

    st.title(
        t("page_title")
    )

    st.caption(
        t("page_caption")
    )

with _header_right:

    _lang_idx = (
        0
        if st.session_state.get(
            "lang",
            "en",
        )
        == "en"
        else 1
    )

    _lang_sel = st.selectbox(
        t("lang_label"),
        options=[
            "en",
            "es",
        ],
        index=_lang_idx,
        format_func=lambda c: (
            "English"
            if c == "en"
            else "Español"
        ),
        key="header_lang_select",
    )

    if _lang_sel != st.session_state.get(
        "lang",
        "en",
    ):

        st.session_state["lang"] = _lang_sel

        st.rerun()

    _theme_idx = (
        0
        if st.session_state.get(
            "theme",
            "light",
        )
        == "dark"
        else 1
    )

    _theme_sel = st.selectbox(
        t("theme_label"),
        options=[
            "dark",
            "light",
        ],
        index=_theme_idx,
        format_func=lambda x: (
            t("theme_dark")
            if x == "dark"
            else t("theme_light")
        ),
        key="header_theme_select",
    )

    if _theme_sel != st.session_state.get(
        "theme",
        "light",
    ):

        st.session_state["theme"] = _theme_sel

        st.rerun()

st.markdown("---")

# ======================================================
# SIDEBAR
# ======================================================

with st.sidebar:

    st.subheader(
        t("upload_documents")
    )

    # ==================================================
    # RESUME
    # ==================================================

    uploaded_resume = st.file_uploader(
        t("upload_resume"),
        type=["pdf", "docx", "txt"],
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
                    t("resume_uploaded_ok")
                )
            else:
                st.error(response.text)

    # ==================================================
    # LINKEDIN PDF
    # ==================================================

    linkedin_pdf = st.file_uploader(
        t("upload_linkedin"),
        type=["pdf"],
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
                    t("linkedin_uploaded_ok")
                )
            else:
                st.error(response.text)

    st.markdown("---")

    # ==================================================
    # JOB DESCRIPTION
    # ==================================================

    st.subheader(
        t("target_job")
    )

    job_description = st.text_area(
        t("paste_job_description"),
        height=320,
        key="job_description_input",
        label_visibility="visible",
    )

    if st.button(
        t("save_job_description"),
    ):

        response = api_post(
            "/save-job-description",
            json={
                "job_description": job_description
            },
        )

        if response.status_code == 200:
            st.session_state["has_job_description"] = True

            st.success(
                t("job_description_saved")
            )
        else:
            st.error(response.text)

    with st.expander(
        t("cleanup_expander"),
        expanded=False,
    ):

        st.caption(
            t("cleanup_caption")
        )

        if st.button(
            t("remove_extra_files"),
            help=t("remove_extra_help"),
        ):

            r = api_post("/cleanup-input-extras")

            if r.status_code != 200:

                st.error(r.text)

            else:

                data = response_json_or_none(r) or {}

                removed = data.get(
                    "removed",
                    [],
                )

                if removed:

                    st.success(
                        t("removed_label")
                        + " "
                        + ", ".join(removed)
                    )

                else:

                    st.info(
                        t("no_extra_files")
                    )

        if st.button(
            t("clear_candidate_files"),
            help=t("clear_candidate_help"),
        ):

            r = api_post("/clear-candidate-files")

            if r.status_code != 200:

                st.error(r.text)

            else:

                st.session_state["has_resume"] = False
                st.session_state["has_linkedin"] = False
                st.session_state["resume_uploaded_name"] = ""
                st.session_state["linkedin_uploaded_name"] = ""

                data = response_json_or_none(r) or {}

                removed = data.get(
                    "removed",
                    [],
                )

                st.success(
                    t("cleared_label")
                    + " "
                    + (
                        ", ".join(removed)
                        if removed
                        else t("nothing_on_disk")
                    )
                )

                st.rerun()

    st.markdown("---")

    # ==================================================
    # AI ACTIONS
    # ==================================================

    st.subheader(
        t("ai_actions")
    )

    can_profile = st.session_state.get("has_resume") or st.session_state.get("has_linkedin")
    can_with_job = can_profile and st.session_state.get("has_job_description")

    if not can_profile:
        st.warning(
            t("warn_upload_first")
        )
    elif not st.session_state.get("has_job_description"):
        st.info(
            t("info_save_jd")
        )

    # PROFILE

    if st.button(
        t("generate_profile"),
        disabled=not can_profile,
    ):

        response = api_post("/profile")

        if response.status_code != 200:
            st.error(response.text)
            st.stop()

        data = response_json_or_none(response)

        if data is None:

            st.error(
                t("invalid_json")
            )

            st.stop()

        st.session_state["profile"] = data.get(
            "profile",
            ""
        )

        st.success(
            t("profile_generated")
        )

        st.rerun()

    # MATCH ANALYSIS

    if st.button(
        t("analyze_match"),
        disabled=not can_with_job,
    ):

        response = api_post("/match")

        if response.status_code != 200:
            st.error(response.text)
            st.stop()

        data = response_json_or_none(response)

        if data is None:

            st.error(
                t("invalid_json")
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
            t("match_completed")
        )

        st.rerun()

    # RESUME

    if st.button(
        t("generate_resume"),
        disabled=not can_with_job,
    ):

        response = api_post("/resume")

        if response.status_code != 200:
            st.error(response.text)
            st.stop()

        data = response_json_or_none(response)

        if data is None:

            st.error(
                t("invalid_json")
            )

            st.stop()

        st.session_state["resume"] = data.get(
            "resume",
            ""
        )

        st.success(
            t("resume_generated")
        )

        st.rerun()

    # COVER LETTER

    if st.button(
        t("generate_cover"),
        disabled=not can_with_job,
    ):

        response = api_post("/cover-letter")

        if response.status_code != 200:
            st.error(response.text)
            st.stop()

        data = response_json_or_none(response)

        if data is None:

            st.error(
                t("invalid_json")
            )

            st.stop()

        st.session_state["cover_letter"] = data.get(
            "cover_letter",
            ""
        )

        st.success(
            t("cover_generated")
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
            t("score_excellent"),
        )

    elif score >= 70:

        return (
            "#FACC15",
            t("score_good"),
        )

    return (
        "#EF4444",
        t("score_needs_work"),
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
    t("skills_strong")
    if len(missing_skills) <= 3
    else t("skills_gaps")
)

# ======================================================
# DASHBOARD
# ======================================================

_ui_theme = st.session_state.get(
    "theme",
    "light",
)

col1, col2, col3 = st.columns(3)

# ======================================================
# METRIC CARD RENDERER (HTML component avoids markdown escaping)
# ======================================================

def render_metric_card(
    title: str,
    value: str,
    value_color: str,
    subtitle: str,
    height: int = 155,
    *,
    ui_theme: str = "light",
):
    if ui_theme == "light":
        _bg = "linear-gradient(135deg,#ffffff,#f8fafc)"
        _border = "#e2e8f0"
        _shadow = "rgba(13,148,136,0.07)"
        _title_c = "#0d9488"
        _sub_c = "#64748b"
    else:
        _bg = "linear-gradient(135deg,#0F172A,#111827)"
        _border = "#1E293B"
        _shadow = "rgba(20,184,166,0.12)"
        _title_c = "#14B8A6"
        _sub_c = "#CBD5E1"

    st_html(
        f"""
<style>
@import url("https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap");
</style>
<div style="
    font-family:'Nunito',ui-sans-serif,system-ui,sans-serif;
    background:{_bg};
    padding:22px 18px;
    border-radius:18px;
    border:1px solid {_border};
    text-align:center;
    box-shadow:0 0 25px {_shadow};
">
  <div style="
      color:{_title_c};
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
      color:{_sub_c};
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
        title=t("match_score"),
        value=f"{match_score}%",
        value_color=match_color,
        subtitle=match_status,
        ui_theme=_ui_theme,
    )

# ATS SCORE

with col2:
    render_metric_card(
        title=t("ats_score"),
        value=f"{ats_score}%",
        value_color=ats_color,
        subtitle=ats_status,
        ui_theme=_ui_theme,
    )

# MISSING SKILLS

with col3:
    render_metric_card(
        title=t("missing_skills"),
        value=str(len(missing_skills)),
        value_color=skills_color,
        subtitle=skills_status,
        ui_theme=_ui_theme,
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
    """
        + t("missing_skills_heading")
        + """
</h3>
""",
        unsafe_allow_html=True,
    )

    _skill_bg = (
        "#f8fafc"
        if _ui_theme == "light"
        else "#0F172A"
    )

    _skill_fg = (
        "#0f172a"
        if _ui_theme == "light"
        else "white"
    )

    for skill in missing_skills:

        st.markdown(
            f"""
<div style="
    background:{_skill_bg};
    padding:12px;
    border-radius:10px;
    margin-bottom:10px;
    border-left:4px solid #EF4444;
    color:{_skill_fg};
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
    t("tab_profile"),
    t("tab_match"),
    t("tab_resume"),
    t("tab_cover"),
])

# PROFILE

with tab1:

    st.markdown(
        '<div class="panel">',
        unsafe_allow_html=True
    )

    if not st.session_state.get("profile"):
        st.info(
            t("empty_profile")
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
            t("empty_analysis")
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
            t("empty_resume")
        )
    else:
        st.code(
            st.session_state["resume"],
            language="markdown"
        )

    if st.session_state.get("resume"):

        st.download_button(
            label=t("download_resume"),
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
            t("empty_cover")
        )
    else:
        st.code(
            st.session_state["cover_letter"],
            language="markdown"
        )

    if st.session_state.get("cover_letter"):

        st.download_button(
            label=t("download_cover"),
            data=st.session_state["cover_letter"],
            file_name="cover_letter.txt",
            mime="text/plain"
        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )