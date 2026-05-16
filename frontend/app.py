import os
import sys
import html
import time

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

    try:

        if hasattr(
            st,
            "secrets",
        ) and "API_URL" in st.secrets:

            from_secrets = (
                str(
                    st.secrets["API_URL"],
                )
                .strip()
                .rstrip("/")
            )

            if from_secrets:

                return from_secrets

    except Exception:

        pass

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

    base = _resolve_api_url()

    url = (
        path
        if path.startswith("http")
        else f"{base}{path}"
    )

    headers = kwargs.pop(
        "headers",
        None,
    ) or {}

    headers.update(_api_headers())

    kwargs["headers"] = headers

    try:

        _timeout = kwargs.pop(
            "timeout",
            None,
        )

        if _timeout is None:

            _connect = float(
                os.getenv(
                    "API_CONNECT_TIMEOUT",
                    "25",
                )
            )

            _read = float(
                os.getenv(
                    "API_READ_TIMEOUT",
                    "300",
                )
            )

            _timeout = (
                _connect,
                _read,
            )

        _gw_retries = max(
            0,
            int(
                os.getenv(
                    "API_GATEWAY_RETRIES",
                    "2",
                )
            ),
        )

        _attempt = 0

        while True:

            response = requests.post(
                url,
                timeout=_timeout,
                **kwargs,
            )

            if (
                response.status_code
                not in (
                    502,
                    503,
                    504,
                )
                or _attempt >= _gw_retries
            ):

                return response

            _attempt += 1

            time.sleep(
                2.5 + _attempt * 1.5,
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
                url=base,
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


def _looks_like_html_document(
    s: str,
) -> bool:

    if not s or not isinstance(
        s,
        str,
    ):

        return False

    low = s.lstrip()[:20000].lower()

    if "<!doctype html" in low or low.startswith("<html"):

        return True

    if "<html" not in low[:12000]:

        return False

    if "<body" in low[:24000]:

        return True

    if any(
        marker in low
        for marker in (
            "<title>502",
            "<title>503",
            "<title>504",
            "bad gateway",
            "service unavailable",
            "gateway time-out",
            "roobert",
            "render.com",
        )
    ):

        return True

    return False


def _api_error_message(
    response,
) -> str:

    code = getattr(
        response,
        "status_code",
        "?",
    )
    body = (response.text or "").strip()
    ctype = (
        response.headers.get(
            "Content-Type",
            "",
        )
        or ""
    ).lower()

    if "text/html" in ctype or _looks_like_html_document(body):

        _lang = st.session_state.get(
            "lang",
            "en",
        )

        return ui_text(
            _lang,
            "api_error_html",
        ).format(
            code=code,
        )

    if len(body) > 900:

        return body[:900] + "…"

    if body:

        return body

    return f"HTTP {code}"


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
    "job_search_results": [],
    "job_search_messages": [],
    "job_search_meta": None,
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
                st.error(
                    _api_error_message(response)
                )

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
                st.error(
                    _api_error_message(response)
                )

    st.markdown("---")

    # ==================================================
    # JOB DESCRIPTION
    # ==================================================

    _jd_key = "job_description_input"
    _jd_existing = st.session_state.get(_jd_key)

    if isinstance(
        _jd_existing,
        str,
    ) and _looks_like_html_document(_jd_existing):

        st.session_state[_jd_key] = ""
        st.session_state["has_job_description"] = False

        if not st.session_state.get("_jd_bad_html_warned"):

            st.session_state["_jd_bad_html_warned"] = True
            st.warning(
                t("jd_cleared_bad_html")
            )

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

        if _looks_like_html_document(job_description):

            st.warning(
                t("jd_reject_html")
            )

        else:

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
                st.error(
                    _api_error_message(response)
                )

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

                st.error(
                    _api_error_message(r)
                )

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

                st.error(
                    _api_error_message(r)
                )

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
            st.error(
                _api_error_message(response)
            )
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
            st.error(
                _api_error_message(response)
            )
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
            st.error(
                _api_error_message(response)
            )
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
            st.error(
                _api_error_message(response)
            )
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

    with st.expander(
        t("debug_api_expander"),
        expanded=False,
    ):

        _probe_base = _resolve_api_url()

        st.code(
            _probe_base,
            language=None,
        )

        st.caption(
            t("debug_probe_hint")
        )

        if st.button(
            t("debug_probe_health"),
            key="sidebar_health_probe",
        ):

            try:

                _hr = requests.get(
                    f"{_probe_base}/health",
                    timeout=(
                        20,
                        30,
                    ),
                )

                st.caption(
                    f"HTTP {_hr.status_code}"
                )

                st.text(
                    (_hr.text or "")[:800]
                )

            except requests.RequestException as _exc:

                st.caption(
                    str(_exc)
                )

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
# JOB CARD RENDERER
# ======================================================


def _render_job_card(
    job: dict,
    *,
    ui_theme: str = "light",
):

    _title = html.escape(
        job.get("title", "Untitled"),
    )

    _company = html.escape(
        job.get("company", ""),
    )

    _score = max(
        0,
        min(
            100,
            int(job.get("match_score", 0)),
        ),
    )

    _one_liner = html.escape(
        job.get("one_liner", ""),
    )

    _source = job.get("source", "")

    _url = job.get("url", "")

    if _score >= 85:
        _score_color = "#22C55E"
        _score_bg = "rgba(34,197,94,0.12)"
    elif _score >= 70:
        _score_color = "#EAB308"
        _score_bg = "rgba(234,179,8,0.12)"
    else:
        _score_color = "#EF4444"
        _score_bg = "rgba(239,68,68,0.12)"

    if ui_theme == "light":
        _card_bg = "#ffffff"
        _card_border = "#e2e8f0"
        _title_c = "#0f172a"
        _company_c = "#0d9488"
        _text_c = "#475569"
        _src_bg = "#f1f5f9"
        _src_c = "#64748b"
        _link_c = "#0d9488"
        _shadow = "0 1px 8px rgba(13,148,136,0.06)"
    else:
        _card_bg = "#0F172A"
        _card_border = "#1E293B"
        _title_c = "#ffffff"
        _company_c = "#14B8A6"
        _text_c = "#CBD5E1"
        _src_bg = "#1E293B"
        _src_c = "#94a3b8"
        _link_c = "#2DD4BF"
        _shadow = "0 1px 8px rgba(20,184,166,0.08)"

    _source_labels = {
        "serpapi_google_jobs": "Google Jobs",
        "user_url": "Direct URL",
        "rss": "RSS Feed",
    }

    _src_label = html.escape(
        _source_labels.get(
            _source,
            _source,
        ),
    )

    _company_html = ""

    if _company:

        _company_html = (
            f'<div style="'
            f"font-size:14px;"
            f"font-weight:600;"
            f"color:{_company_c};"
            f"margin-top:2px;"
            f'">{_company}</div>'
        )

    _link_html = ""

    if _url:

        _safe_url = html.escape(
            _url,
            quote=True,
        )

        _link_text = t(
            "job_search_apply",
        )

        _link_html = (
            f'<a href="{_safe_url}" target="_blank"'
            f' rel="noopener noreferrer" style="'
            f"display:inline-flex;"
            f"align-items:center;"
            f"gap:4px;"
            f"color:#fff;"
            f"background:{_link_c};"
            f"text-decoration:none;"
            f"font-size:13px;"
            f"font-weight:700;"
            f"padding:4px 12px;"
            f"border-radius:6px;"
            f'">{_link_text}</a>'
        )

    _card_html = (
        f'<div style="'
        f"background:{_card_bg};"
        f"border:1px solid {_card_border};"
        f"border-radius:14px;"
        f"padding:18px 20px;"
        f"margin-bottom:10px;"
        f"display:flex;"
        f"align-items:flex-start;"
        f"gap:16px;"
        f"box-shadow:{_shadow};"
        f"font-family:'Nunito',ui-sans-serif,system-ui,sans-serif;"
        f'">'
        f'<div style="'
        f"min-width:54px;"
        f"height:54px;"
        f"border-radius:12px;"
        f"background:{_score_bg};"
        f"display:flex;"
        f"align-items:center;"
        f"justify-content:center;"
        f"flex-shrink:0;"
        f'">'
        f'<span style="'
        f"color:{_score_color};"
        f"font-size:18px;"
        f"font-weight:800;"
        f"line-height:1;"
        f'">{_score}%</span>'
        f"</div>"
        f'<div style="flex:1;min-width:0;">'
        f'<div style="'
        f"font-size:16px;"
        f"font-weight:700;"
        f"color:{_title_c};"
        f"line-height:1.3;"
        f'">{_title}</div>'
        f"{_company_html}"
        f'<div style="'
        f"font-size:13.5px;"
        f"color:{_text_c};"
        f"margin-top:6px;"
        f"line-height:1.5;"
        f'">{_one_liner}</div>'
        f'<div style="'
        f"display:flex;"
        f"align-items:center;"
        f"gap:10px;"
        f"margin-top:8px;"
        f"flex-wrap:wrap;"
        f'">'
        f'<span style="'
        f"font-size:11px;"
        f"font-weight:600;"
        f"color:{_src_c};"
        f"background:{_src_bg};"
        f"padding:2px 8px;"
        f"border-radius:6px;"
        f"letter-spacing:0.02em;"
        f'">{_src_label}</span>'
        f"{_link_html}"
        f"</div>"
        f"</div>"
        f"</div>"
    )

    st.html(_card_html)


# ======================================================
# TABS
# ======================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    t("tab_profile"),
    t("tab_match"),
    t("tab_resume"),
    t("tab_cover"),
    t("tab_job_search"),
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

# JOB SEARCH

with tab5:

    st.markdown(
        '<div class="panel">',
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # PROFILE-DRIVEN SEARCH
    # --------------------------------------------------

    st.subheader(
        t("job_search_header")
    )

    st.caption(
        t("job_search_hint")
    )

    if not can_profile:

        st.warning(
            t("job_search_upload_first")
        )

    _search_clicked = st.button(
        t("job_search_run"),
        disabled=not can_profile,
        key="job_search_run_btn",
        use_container_width=True,
        type="primary",
    )

    with st.expander(
        t("job_search_advanced"),
        expanded=False,
    ):

        st.caption(
            t("job_search_advanced_hint")
        )

        _js_n = st.number_input(
            t("job_search_count"),
            min_value=1,
            max_value=10,
            value=5,
            step=1,
            key="job_search_num_input",
        )

        _js_urls = st.text_area(
            t("job_search_urls"),
            height=100,
            key="job_search_urls_input",
            placeholder="https://www.linkedin.com/jobs/view/123456\nhttps://www.indeed.com/viewjob?jk=abc123",
        )

        _js_serpapi_key = st.text_input(
            t("job_search_serpapi_key"),
            type="password",
            key="job_search_serpapi_key_input",
        )

    if _search_clicked:

        _url_list = [
            ln.strip()
            for ln in (
                st.session_state.get("job_search_urls_input") or ""
            ).splitlines()
            if ln.strip()
        ][:35]

        _payload = {
            "query": None,
            "location": None,
            "job_type": None,
            "job_urls": _url_list,
            "rss_feed_urls": [],
            "num_results": int(_js_n),
            "serpapi_api_key": (
                st.session_state.get("job_search_serpapi_key_input") or ""
            ).strip() or None,
        }

        response = api_post(
            "/job-search",
            json=_payload,
        )

        if response.status_code != 200:
            st.error(
                _api_error_message(response)
            )
            st.stop()

        data = response_json_or_none(response)

        if data is None:
            st.error(
                t("invalid_json")
            )
            st.stop()

        st.session_state["job_search_results"] = data.get(
            "results",
            [],
        ) or []

        st.session_state["job_search_messages"] = data.get(
            "messages",
            [],
        ) or []

        st.session_state["job_search_meta"] = data.get(
            "search",
        )

        st.success(
            t("job_search_done")
        )

        st.rerun()

    st.markdown("---")

    # --------------------------------------------------
    # RESULTS
    # --------------------------------------------------

    _js_rows = st.session_state.get(
        "job_search_results",
        [],
    )

    if not _js_rows:

        st.info(
            t("empty_job_search")
        )

        _msgs_empty = st.session_state.get(
            "job_search_messages",
            [],
        )

        if _msgs_empty:

            with st.expander(
                t("job_search_messages"),
                expanded=False,
            ):

                for _m in _msgs_empty:
                    st.caption(_m)

    else:

        _sort_options = [
            (
                "match_desc",
                t("job_search_sort_match_desc"),
            ),
            (
                "match_asc",
                t("job_search_sort_match_asc"),
            ),
            (
                "title_asc",
                t("job_search_sort_title"),
            ),
            (
                "company_asc",
                t("job_search_sort_company"),
            ),
        ]

        _results_hdr1, _results_hdr2 = st.columns(
            [
                2,
                1,
            ],
        )

        with _results_hdr1:

            st.caption(
                t("job_search_results_count").format(
                    count=len(_js_rows),
                )
            )

            _meta = st.session_state.get(
                "job_search_meta",
            ) or {}

            st.caption(
                t("job_search_used").format(
                    q=_meta.get(
                        "query",
                        "",
                    ),
                    loc=_meta.get(
                        "location",
                        "",
                    ),
                    serp=_meta.get(
                        "serpapi_used",
                        False,
                    ),
                )
            )

        with _results_hdr2:

            _sort_sel = st.selectbox(
                t("job_search_sort_label"),
                options=[
                    k for k, _v in _sort_options
                ],
                format_func=lambda k: dict(
                    _sort_options,
                )[k],
                key="job_search_sort",
            )

        _sorted = list(_js_rows)

        if _sort_sel == "match_desc":

            _sorted.sort(
                key=lambda r: r.get(
                    "match_score",
                    0,
                ),
                reverse=True,
            )

        elif _sort_sel == "match_asc":

            _sorted.sort(
                key=lambda r: r.get(
                    "match_score",
                    0,
                ),
            )

        elif _sort_sel == "title_asc":

            _sorted.sort(
                key=lambda r: (
                    r.get("title") or ""
                ).lower(),
            )

        elif _sort_sel == "company_asc":

            _sorted.sort(
                key=lambda r: (
                    r.get("company") or ""
                ).lower(),
            )

        for _job in _sorted:

            _render_job_card(
                _job,
                ui_theme=_ui_theme,
            )

        _msgs = st.session_state.get(
            "job_search_messages",
            [],
        )

        if _msgs:

            with st.expander(
                t("job_search_messages"),
                expanded=False,
            ):

                for _m in _msgs:
                    st.caption(_m)

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )