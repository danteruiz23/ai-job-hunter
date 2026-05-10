from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path

app = FastAPI()

# =========================================
# CORS
# =========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

class JobDescriptionRequest(BaseModel):
    job_description: str

# =========================================
# ROOT
# =========================================

@app.get("/")
def root():

    return {
        "status": "AI Job Hunter API running"
    }

# =========================================
# SAVE JOB DESCRIPTION
# =========================================

@app.post("/save-job-description")
def save_job_description(
    request: JobDescriptionRequest
):

    with open(
        "data/input/job_description.txt",
        "w"
    ) as f:

        f.write(
            request.job_description
        )

    return {
        "status": "success"
    }

# =========================================
# UPLOAD RESUME
# =========================================

@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...)
):

    with open(
        f"data/input/{file.filename}",
        "wb"
    ) as f:

        f.write(
            await file.read()
        )

    return {
        "status": "success"
    }

# =========================================
# UPLOAD LINKEDIN
# =========================================

@app.post("/upload-linkedin")
async def upload_linkedin(
    file: UploadFile = File(...)
):

    with open(
        f"data/input/{file.filename}",
        "wb"
    ) as f:

        f.write(
            await file.read()
        )

    return {
        "status": "success"
    }

# =========================================
# PROFILE
# =========================================

@app.post("/profile")
def generate_profile():

    return {

        "profile": """
Senior Telecom Service Delivery Executive

15+ years leading:
• Telecom Infrastructure
• Service Delivery
• AI Transformation
• SLA Governance
• NOC Operations
• Vendor Management

Strong background managing global telecom operations and AI-driven transformation initiatives.
"""
    }

# =========================================
# MATCH
# =========================================

@app.post("/match")
def generate_match():

    return {

        "analysis": """
Strong candidate for telecom leadership positions.

Strengths:
• Service Delivery
• AI Transformation
• Telecom Operations
• Vendor Management
• SLA Governance

Areas to improve:
• Financial ownership
• Portuguese fluency
""",

        "match_score": 82,

        "ats_score": 88,

        "missing_skills": [
            "Financial Ownership",
            "Advanced Portuguese"
        ]
    }

# =========================================
# RESUME
# =========================================

@app.post("/resume")
def generate_resume():

    resume = """
DANTE RUIZ

Senior Telecom Service Delivery Executive

SUMMARY
15+ years leading telecom infrastructure and AI transformation programs.

SKILLS
• Telecom
• AI
• Automation
• SLA
• NOC
• Leadership

EXPERIENCE
• Telxius
• Telefonica
"""

    return {
        "resume": resume
    }

# =========================================
# COVER LETTER
# =========================================

@app.post("/cover-letter")
def generate_cover_letter():

    cover_letter = """
Dear Hiring Manager,

I am excited to apply for this position.

My experience leading telecom operations and AI transformation initiatives makes me a strong fit.

Sincerely,

Dante Ruiz
"""

    return {
        "cover_letter": cover_letter
    }