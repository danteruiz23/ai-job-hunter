"""Theme-specific CSS for Streamlit (dark / light)."""

from typing import Dict

# Keys match __KEY__ placeholders in STYLESHEET_TEMPLATE
THEMES: Dict[str, Dict[str, str]] = {
    "dark": {
        "ACCENT": "#14B8A6",
        "ACCENT_HOVER": "#0D9488",
        "ACCENT_SOFT": "#2DD4BF",
        "UP_BG": "#172554",
        "UP_BORDER": "#3b82f6",
        "UP_TEXT": "#93c5fd",
        "UP_TEXT_STRONG": "#60a5fa",
        "UP_TEXT_MUTED": "#bfdbfe",
        "UP_PILL": "#1e3a8a",
        "UP_BTN": "#1d4ed8",
        "UP_BTN_HOVER": "#2563eb",
        "JD_BG": "#0c4a6e",
        "JD_BORDER": "#38bdf8",
        "JD_TEXT": "#bae6fd",
        "JD_PLACEHOLDER": "#7dd3fc",
        "JD_CARET": "#e0f2fe",
        "LANG_BG": "#064e3b",
        "LANG_BORDER": "#10b981",
        "LANG_TEXT": "#6ee7b7",
        "LANG_LABEL": "#34d399",
        "APP_BG": "#020817",
        "APP_FG": "#ffffff",
        "SIDEBAR_G1": "#0F172A",
        "SIDEBAR_G2": "#020617",
        "SIDEBAR_EDGE": "#1E293B",
        "SIDEBAR_MD": "#e2e8f0",
        "SIDEBAR_H": "#ffffff",
        "FIELD_BG": "#111827",
        "FIELD_FG": "#ffffff",
        "FIELD_BORDER": "#1E293B",
        "HEADING": "#ffffff",
        "BODY": "#CBD5E1",
        "CAPTION": "#94a3b8",
        "TAB_MUTED": "#CBD5E1",
        "PANEL_BG": "#111827",
        "PANEL_BORDER": "#1E293B",
        "HR": "#1E293B",
        "FU_OUT_BG": "#111827",
        "FU_OUT_BORDER": "#1E293B",
        "BLOCKQUOTE": "#1e293b",
        "CODE_BG": "#0f172a",
    },
    "light": {
        "ACCENT": "#0d9488",
        "ACCENT_HOVER": "#0f766e",
        "ACCENT_SOFT": "#5eead4",
        "UP_BG": "#eff6ff",
        "UP_BORDER": "#2563eb",
        "UP_TEXT": "#1e40af",
        "UP_TEXT_STRONG": "#1d4ed8",
        "UP_TEXT_MUTED": "#3b82f6",
        "UP_PILL": "#dbeafe",
        "UP_BTN": "#2563eb",
        "UP_BTN_HOVER": "#1d4ed8",
        "JD_BG": "#f0f9ff",
        "JD_BORDER": "#0ea5e9",
        "JD_TEXT": "#0c4a6e",
        "JD_PLACEHOLDER": "#0369a1",
        "JD_CARET": "#075985",
        "LANG_BG": "#ecfdf5",
        "LANG_BORDER": "#059669",
        "LANG_TEXT": "#065f46",
        "LANG_LABEL": "#047857",
        "APP_BG": "#f8fafc",
        "APP_FG": "#0f172a",
        "SIDEBAR_G1": "#f1f5f9",
        "SIDEBAR_G2": "#e8eef5",
        "SIDEBAR_EDGE": "#cbd5e1",
        "SIDEBAR_MD": "#334155",
        "SIDEBAR_H": "#0f172a",
        "FIELD_BG": "#ffffff",
        "FIELD_FG": "#0f172a",
        "FIELD_BORDER": "#cbd5e1",
        "HEADING": "#0f172a",
        "BODY": "#475569",
        "CAPTION": "#64748b",
        "TAB_MUTED": "#64748b",
        "PANEL_BG": "#ffffff",
        "PANEL_BORDER": "#e2e8f0",
        "HR": "#e2e8f0",
        "FU_OUT_BG": "#f1f5f9",
        "FU_OUT_BORDER": "#cbd5e1",
        "BLOCKQUOTE": "#f1f5f9",
        "CODE_BG": "#f8fafc",
    },
}


STYLESHEET_TEMPLATE = """
<style>
@import url("https://fonts.googleapis.com/css2?family=Nunito:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&display=swap");

:root {
    --accent: __ACCENT__;
    --accent-hover: __ACCENT_HOVER__;
    --accent-soft: __ACCENT_SOFT__;
    --sidebar-upload-bg: __UP_BG__;
    --sidebar-upload-border: __UP_BORDER__;
    --sidebar-upload-text: __UP_TEXT__;
    --sidebar-upload-text-strong: __UP_TEXT_STRONG__;
    --sidebar-upload-text-muted: __UP_TEXT_MUTED__;
    --sidebar-upload-pill-bg: __UP_PILL__;
    --sidebar-upload-btn: __UP_BTN__;
    --sidebar-upload-btn-hover: __UP_BTN_HOVER__;
    --jd-bg: __JD_BG__;
    --jd-border: __JD_BORDER__;
    --jd-text: __JD_TEXT__;
    --jd-placeholder: __JD_PLACEHOLDER__;
    --jd-caret: __JD_CARET__;
    --lang-select-bg: __LANG_BG__;
    --lang-select-border: __LANG_BORDER__;
    --lang-select-text: __LANG_TEXT__;
    --lang-select-label: __LANG_LABEL__;
    --font-ui: "Nunito", "Segoe UI", ui-sans-serif, system-ui, sans-serif;
    --font-mono: ui-monospace, "Cascadia Code", "Source Code Pro", Menlo, monospace;
}

html, body {
    font-family: var(--font-ui);
}

.stApp {
    background-color: __APP_BG__;
    color: __APP_FG__;
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

section[data-testid="stSidebar"] {
    width: 28vw !important;
    min-width: 260px !important;
    max-width: 420px !important;
    flex-shrink: 0 !important;
    box-sizing: border-box !important;
    background: linear-gradient(
        180deg,
        __SIDEBAR_G1__,
        __SIDEBAR_G2__
    );
    border-right: 1px solid __SIDEBAR_EDGE__;
}

section[data-testid="stSidebar"] > div:first-child {
    width: 100% !important;
}

/* Tighter vertical rhythm in sidebar */
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div {
    gap: 0.35rem !important;
}

section[data-testid="stSidebar"] .element-container {
    padding-top: 0.2rem !important;
    padding-bottom: 0.2rem !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: __SIDEBAR_H__ !important;
    font-size: 1.05rem !important;
    line-height: 1.25 !important;
    margin: 0.25rem 0 0.35rem 0 !important;
    padding-top: 0 !important;
}

section[data-testid="stSidebar"] hr {
    margin: 0.35rem 0 !important;
}

section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown span {
    color: __SIDEBAR_MD__ !important;
}

section[data-testid="stSidebar"] div:has([data-testid="stFileUploader"]) label {
    color: var(--sidebar-upload-text-strong) !important;
}

section[data-testid="stSidebar"] div:has(.stTextArea) [data-testid="stWidgetLabel"] {
    color: var(--jd-text) !important;
}

section[data-testid="stSidebar"] [data-testid="stSelectbox"]:first-of-type [data-baseweb="select"] {
    background-color: var(--lang-select-bg) !important;
    border: 2px solid var(--lang-select-border) !important;
    border-radius: 12px !important;
}

section[data-testid="stSidebar"] [data-testid="stSelectbox"]:first-of-type [data-baseweb="select"] > div {
    color: var(--lang-select-text) !important;
    -webkit-text-fill-color: var(--lang-select-text) !important;
}

section[data-testid="stSidebar"] [data-testid="stSelectbox"]:first-of-type [data-baseweb="select"] span {
    color: var(--lang-select-text) !important;
    -webkit-text-fill-color: var(--lang-select-text) !important;
}

section[data-testid="stSidebar"] [data-testid="stSelectbox"]:first-of-type svg {
    fill: var(--lang-select-border) !important;
}

section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
    color: var(--sidebar-upload-text-strong) !important;
}

section[data-testid="stSidebar"] [data-testid="stSelectbox"]:first-of-type [data-testid="stWidgetLabel"] p {
    color: var(--lang-select-label) !important;
}

section[data-testid="stSidebar"] .stTextArea textarea {
    min-height: 72px !important;
    max-height: 240px !important;
    resize: vertical !important;
    background-color: var(--jd-bg) !important;
    color: var(--jd-text) !important;
    border: 2px solid var(--jd-border) !important;
    border-radius: 10px !important;
    caret-color: var(--jd-caret) !important;
    font-size: 14px !important;
    line-height: 1.45 !important;
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
    background-color: __FIELD_BG__ !important;
    color: __FIELD_FG__ !important;
    border: 1px solid __FIELD_BORDER__ !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background-color: transparent !important;
    border: none !important;
    padding: 0 !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploader"] section {
    background-color: var(--sidebar-upload-bg) !important;
    border: 2px solid var(--sidebar-upload-border) !important;
    border-radius: 10px !important;
    padding: 6px 8px !important;
}

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
    background: linear-gradient(
        135deg,
        var(--accent),
        #8B5CF6
    ) !important;
    border: none !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploader"] button:hover {
    background: linear-gradient(
        135deg,
        var(--accent-hover),
        #7C3AED
    ) !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploader"] *:not(button) {
    color: var(--sidebar-upload-text-strong) !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploader"] small,
section[data-testid="stSidebar"] [data-testid="stFileUploader"] [class*="caption"],
section[data-testid="stSidebar"] [data-testid="stFileUploader"] [class*="Caption"] {
    color: var(--sidebar-upload-text-muted) !important;
}

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

section[data-testid="stSidebar"] [data-testid="stFileUploader"] [data-baseweb="typography"],
section[data-testid="stSidebar"] [data-testid="stFileUploader"] li,
section[data-testid="stSidebar"] [data-testid="stFileUploader"] [role="listitem"] {
    background-color: transparent !important;
    color: var(--sidebar-upload-text-strong) !important;
}

h1, h2, h3 {
    color: __HEADING__ !important;
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
    color: __BODY__;
    line-height: 1.7;
}

[data-testid="stCaptionContainer"] {
    font-family: var(--font-ui) !important;
    font-weight: 500 !important;
    font-size: 1.05rem !important;
    color: __CAPTION__ !important;
    line-height: 1.55 !important;
}

[data-testid="stCaptionContainer"] strong {
    font-weight: 700 !important;
    color: inherit !important;
}

[data-testid="stCaptionContainer"] p + p {
    font-size: 0.92rem !important;
    font-weight: 500 !important;
    margin-top: 0.2rem !important;
    opacity: 0.92 !important;
}

.stCodeBlock,
pre,
code,
.stMarkdown code {
    font-family: var(--font-mono) !important;
}

.stMarkdown blockquote {
    border-left-color: var(--accent) !important;
    background: __BLOCKQUOTE__ !important;
}

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

section[data-testid="stSidebar"] .stButton button {
    height: 40px !important;
    min-height: 40px !important;
    font-size: 14px !important;
    border-radius: 10px !important;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}

[data-testid="stFileUploader"] {
    background-color: __FU_OUT_BG__;
    border-radius: 12px;
    border: 1px solid __FU_OUT_BORDER__;
    padding: 10px;
}

textarea {
    background-color: __FIELD_BG__ !important;
    color: __FIELD_FG__ !important;
    border-radius: 12px !important;
}

.stTabs [data-baseweb="tab"] {
    color: __TAB_MUTED__;
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 0.01em;
}

.stTabs [aria-selected="true"] {
    color: var(--accent) !important;
}

.panel {
    background-color: __PANEL_BG__;
    border-radius: 18px;
    padding: 30px;
    border: 1px solid __PANEL_BORDER__;
}

hr {
    border-color: __HR__;
}

div[data-testid="stExpander"] details {
    background-color: __PANEL_BG__ !important;
    border: 1px solid __PANEL_BORDER__ !important;
    border-radius: 12px !important;
}

.stDownloadButton button {
    background: linear-gradient(
        135deg,
        var(--accent),
        #8B5CF6
    ) !important;
    color: white !important;
}

.stDownloadButton button:hover {
    background: linear-gradient(
        135deg,
        var(--accent-hover),
        #7C3AED
    ) !important;
}

/* Alerts / info boxes — closer to theme */
[data-testid="stAlert"] {
    background-color: __PANEL_BG__ !important;
    border: 1px solid __PANEL_BORDER__ !important;
    color: __BODY__ !important;
}

[data-testid="stAlert"] * {
    color: inherit !important;
}

section[data-testid="stSidebar"] [data-testid="stAlert"] {
    padding: 0.45rem 0.65rem !important;
    font-size: 0.88rem !important;
    margin-top: 0.15rem !important;
    margin-bottom: 0.15rem !important;
}

/* Code block surface */
.stCodeBlock {
    background-color: __CODE_BG__ !important;
    border: 1px solid __PANEL_BORDER__ !important;
}

</style>
"""


def build_stylesheet(theme: str) -> str:

    tokens = THEMES.get(
        theme,
        THEMES["dark"],
    )

    out = STYLESHEET_TEMPLATE

    for key, val in tokens.items():

        out = out.replace(
            f"__{key}__",
            val,
        )

    return out
