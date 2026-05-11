import os

from contextlib import asynccontextmanager

from fastapi import Depends
from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
from fastapi import HTTPException

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from pathlib import Path

from app.services.file_parser import (
    extract_text
)

from app.api.deps import (
    read_upload_with_limit,
    require_openai_key,
)

from app.api.middleware_api_key import (
    ApiKeyMiddleware,
)

# =========================================
# AI GENERATORS
# =========================================

from app.ai.profile_generator import (
    generate_profile
)

from app.ai.match_engine import (
    generate_match_analysis
)

from app.ai.resume_generator import (
    generate_resume
)

from app.ai.cover_letter_generator import (
    generate_cover_letter
)

# =========================================
# APP
# =========================================


@asynccontextmanager
async def lifespan(
    _app: FastAPI,
):

    _env = os.getenv(
        "ENVIRONMENT",
        "",
    ).strip().lower()

    _force_key = os.getenv(
        "REQUIRE_JOB_HUNTER_API_KEY",
        "",
    ).strip().lower() in (
        "1",
        "true",
        "yes",
    )

    if _env == "production" or _force_key:

        if not os.getenv(
            "JOB_HUNTER_API_KEY",
            "",
        ).strip():

            raise RuntimeError(
                "JOB_HUNTER_API_KEY must be set when "
                "ENVIRONMENT=production or "
                "REQUIRE_JOB_HUNTER_API_KEY=1. "
                "Set a shared secret in .env for the API and Streamlit."
            )

    _openai = (
        "set"
        if os.getenv(
            "OPENAI_API_KEY",
            "",
        ).strip()
        else "missing"
    )

    _api_key = (
        "required"
        if os.getenv(
            "JOB_HUNTER_API_KEY",
            "",
        ).strip()
        else "open"
    )

    print(
        "[ai-job-hunter] "
        f"OPENAI_API_KEY: {_openai}; "
        f"JOB_HUNTER_API_KEY: {_api_key}",
        flush=True,
    )

    yield


app = FastAPI(
    lifespan=lifespan,
)

# =========================================
# CORS (local Streamlit by default)
# =========================================

_cors_raw = os.getenv(
    "CORS_ORIGINS",
    "http://127.0.0.1:8501,http://localhost:8501",
)

_cors_origins = [
    o.strip()
    for o in _cors_raw.split(",")
    if o.strip()
]

if not _cors_origins:

    _cors_origins = ["http://127.0.0.1:8501"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================
# Optional API key (set JOB_HUNTER_API_KEY in .env)
# =========================================

app.add_middleware(ApiKeyMiddleware)

# =========================================
# FOLDERS
# =========================================

Path("data/input").mkdir(
    parents=True,
    exist_ok=True
)

Path("data/output").mkdir(
    parents=True,
    exist_ok=True
)

# =========================================
# REQUEST MODEL
# =========================================

class JobDescriptionRequest(
    BaseModel
):
    job_description: str

# =========================================
# HELPERS
# =========================================

def _require_non_empty(
    value: str,
    *,
    field_name: str,
    message: str,
):
    if not (value or "").strip():
        raise HTTPException(
            status_code=400,
            detail=f"{field_name}: {message}",
        )

def _save_upload_path(
    file: UploadFile,
    *,
    base_name: str,
    allowed_suffixes: set[str],
) -> Path:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in allowed_suffixes:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{suffix}'. Allowed: {sorted(allowed_suffixes)}",
        )

    # Ignore user-provided filenames entirely (prevents path traversal and messy names).
    return Path("data/input") / f"{base_name}{suffix}"


ALLOWED_INPUT_NAMES = frozenset(
    {
        "job_description.txt",
        "resume.pdf",
        "resume.docx",
        "resume.txt",
        "linkedin.pdf",
        ".gitkeep",
    }
)

CANDIDATE_UPLOAD_NAMES = (
    "resume.pdf",
    "resume.docx",
    "resume.txt",
    "linkedin.pdf",
)


def load_candidate_data():

    input_folder = Path("data/input")

    parts: list[str] = []

    for file in sorted(input_folder.iterdir()):
        if not file.is_file():
            continue

        if file.name == "job_description.txt":
            continue

        if file.suffix.lower() not in {".txt", ".pdf", ".docx"}:
            continue

        try:
            extracted = extract_text(str(file))
        except Exception:
            continue

        extracted = (extracted or "").strip()
        if not extracted:
            continue

        parts.append(f"{file.name}\n{extracted}")

    return "\n\n---\n\n".join(parts).strip()

def load_job_description():

    try:

        with open(
            "data/input/job_description.txt",
            "r",
            encoding="utf-8"
        ) as f:

            return f.read()

    except:

        return ""

# =========================================
# ROOT
# =========================================

@app.get("/")
def root():

    return {
        "status": "AI Job Hunter API running"
    }


@app.get("/health")
def health():

    return {
        "status": "ok"
    }

# =========================================
# SAVE JOB DESCRIPTION
# =========================================

@app.post("/save-job-description")
def save_job_description(
    request: JobDescriptionRequest
):
    _require_non_empty(
        request.job_description,
        field_name="job_description",
        message="Please provide a job description before saving.",
    )

    with open(
        "data/input/job_description.txt",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            request.job_description
        )

    return {
        "status": "success"
    }


@app.post("/cleanup-input-extras")
def cleanup_input_extras():
    """Remove files in data/input that are not the canonical uploads or job description."""

    input_dir = Path("data/input")
    input_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    removed: list[str] = []

    for path in sorted(input_dir.iterdir()):

        if not path.is_file():

            continue

        if path.name in ALLOWED_INPUT_NAMES:

            continue

        path.unlink()
        removed.append(path.name)

    return {
        "status": "success",
        "removed": removed,
    }


@app.post("/clear-candidate-files")
def clear_candidate_files():
    """Delete resume.* and linkedin.pdf only (keeps job_description.txt and .gitkeep)."""

    input_dir = Path("data/input")
    removed: list[str] = []

    for name in CANDIDATE_UPLOAD_NAMES:

        p = input_dir / name

        if p.is_file():

            p.unlink()
            removed.append(name)

    return {
        "status": "success",
        "removed": removed,
    }


# =========================================
# UPLOAD RESUME
# =========================================

@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...)
):

    out_path = _save_upload_path(
        file,
        base_name="resume",
        allowed_suffixes={".pdf", ".docx", ".txt"},
    )

    payload = await read_upload_with_limit(file)

    with open(
        out_path,
        "wb"
    ) as f:

        f.write(payload)

    return {
        "status": "success",
        "filename": out_path.name,
    }

# =========================================
# UPLOAD LINKEDIN
# =========================================

@app.post("/upload-linkedin")
async def upload_linkedin(
    file: UploadFile = File(...)
):

    out_path = _save_upload_path(
        file,
        base_name="linkedin",
        allowed_suffixes={".pdf"},
    )

    payload = await read_upload_with_limit(file)

    with open(
        out_path,
        "wb"
    ) as f:

        f.write(payload)

    return {
        "status": "success",
        "filename": out_path.name,
    }

# =========================================
# PROFILE
# =========================================

@app.post("/profile")
def profile(
    _openai: None = Depends(require_openai_key),
):

    candidate_data = (
        load_candidate_data()
    )

    _require_non_empty(
        candidate_data,
        field_name="candidate_data",
        message="Upload your resume and/or LinkedIn PDF first.",
    )

    result = generate_profile(
        candidate_data
    )

    return {
        "profile": result
    }

# =========================================
# MATCH ANALYSIS
# =========================================

@app.post("/match")
def match(
    _openai: None = Depends(require_openai_key),
):

    candidate_data = (
        load_candidate_data()
    )

    job_description = (
        load_job_description()
    )

    _require_non_empty(
        candidate_data,
        field_name="candidate_data",
        message="Upload your resume and/or LinkedIn PDF first.",
    )

    _require_non_empty(
        job_description,
        field_name="job_description",
        message="Save a job description first.",
    )

    try:
        result = generate_match_analysis(
            candidate_data,
            job_description
        )
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Match analysis failed: {e}"
        )

    return {
        "analysis": result["analysis"],
        "match_score": result["match_score"],
        "ats_score": result["ats_score"],
        "missing_skills": result["missing_skills"]
    }

# =========================================
# RESUME
# =========================================

@app.post("/resume")
def resume(
    _openai: None = Depends(require_openai_key),
):

    candidate_data = (
        load_candidate_data()
    )

    job_description = (
        load_job_description()
    )

    _require_non_empty(
        candidate_data,
        field_name="candidate_data",
        message="Upload your resume and/or LinkedIn PDF first.",
    )

    _require_non_empty(
        job_description,
        field_name="job_description",
        message="Save a job description first.",
    )

    result = generate_resume(
        candidate_data,
        job_description
    )

    return {
        "resume": result
    }

# =========================================
# COVER LETTER
# =========================================

@app.post("/cover-letter")
def cover_letter(
    _openai: None = Depends(require_openai_key),
):

    candidate_data = (
        load_candidate_data()
    )

    job_description = (
        load_job_description()
    )

    _require_non_empty(
        candidate_data,
        field_name="candidate_data",
        message="Upload your resume and/or LinkedIn PDF first.",
    )

    _require_non_empty(
        job_description,
        field_name="job_description",
        message="Save a job description first.",
    )

    result = generate_cover_letter(
        candidate_data,
        job_description
    )

    return {
        "cover_letter": result
    }