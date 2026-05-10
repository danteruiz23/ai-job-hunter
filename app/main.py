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
# CREATE DIRECTORIES
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
# REQUEST MODELS
# =========================================

class JobDescriptionRequest(BaseModel):
    job_description: str

# =========================================
# ROOT
# =========================================

@app.get("/")
def root():

    return {
        "status": "AI Job Hunter API Running"
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

    file_path = (
        f"data/input/{file.filename}"
    )

    with open(
        file_path,
        "wb"
    ) as f:

        content = await file.read()

        f.write(content)

    return {
        "status": "success",
        "filename": file.filename
    }

# =========================================
# UPLOAD LINKEDIN PDF
# =========================================

@app.post("/upload-linkedin")
async def upload_linkedin(
    file: UploadFile = File(...)
):

    file_path = (
        f"data/input/{file.filename}"
    )

    with open(
        file_path,
        "wb"
    ) as f:

        content = await file.read()

        f.write(content)

    return {
        "status": "success",
        "filename": file.filename
    }

# =========================================
# GENERATE PROFILE
# =========================================

@app.post("/profile")
def generate_profile():

    profile = """
Senior Telecom Service Delivery Executive with 15+ years leading global telecom infrastructure, subsea networks, backbone operations, service delivery and operational transformation initiatives.

Strong expertise in:
• Service Delivery Management
• AI Transformation
• Telecom Infrastructure
• SLA Governance
• Vendor Management
• Operational Excellence
• Automation
• NOC Operations
• Data Center Operations

Proven leadership managing regional and global teams, driving operational efficiency, reducing incidents and implementing AI-enabled transformation programs.
"""

    return {
        "profile": profile
    }

# =========================================
# MATCH ANALYSIS
# =========================================

@app.post("/match")
def match_analysis():

    return {

        "analysis": """
Strong fit for telecom service delivery leadership positions.

Key strengths:
• Telecom leadership
• AI transformation
• SLA governance
• Operational excellence
• Vendor management
• Service delivery optimization

Areas to improve:
• Financial ownership exposure
• Portuguese fluency

Overall assessment:
Highly competitive candidate for LATAM telecom leadership roles with strong technical and operational expertise.
""",

        "match_score": 82,

        "ats_score": 88,

        "missing_skills": [
            "Financial Ownership",
            "Advanced Portuguese"
        ]
    }

# =========================================
# GENERATE SUGGESTED RESUME
# =========================================

@app.post("/resume")
def generate_resume():

    resume = """
DANTE RUIZ

Senior Telecom Service Delivery Executive

PROFESSIONAL SUMMARY
Senior telecom leader with 15+ years leading subsea, backbone, NOC and service delivery operations globally.

CORE SKILLS
• Telecom Infrastructure
• AI Transformation
• Service Delivery
• Automation
• SLA Governance
• Vendor Management
• Operations Leadership

PROFESSIONAL EXPERIENCE

TELXIUS
Senior Service Delivery Manager

• Led global telecom infrastructure operations
• Improved SLA performance
• Managed vendor ecosystems
• Implemented operational automation

TELEFONICA
Service Delivery Manager

• Led service delivery operations
• Managed telecom programs
• Improved operational efficiency

EDUCATION
MIT Professional Education
Applied Generative AI
"""

    with open(
        "data/output/suggested_resume.txt",
        "w"
    ) as f:

        f.write(resume)

    return {
        "resume": resume
    }

# =========================================
# GENERATE COVER LETTER
# =========================================

@app.post("/cover-letter")
def generate_cover_letter():

    cover_letter = """
Dear Hiring Manager,

I am excited to apply for this opportunity.

With more than 15 years of experience leading telecom infrastructure, service delivery and AI transformation initiatives, I bring strong operational leadership and technical expertise.

My background includes:
• Service Delivery Leadership
• Telecom Infrastructure
• AI Transformation
• SLA Governance
• Operational Excellence
• Vendor Management

I am confident my experience aligns strongly with this position.

Sincerely,

Dante Ruiz
"""

    with open(
        "data/output/cover_letter.txt",
        "w"
    ) as f:

        f.write(cover_letter)

    return {
        "cover_letter": cover_letter
    }