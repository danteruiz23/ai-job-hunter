from fastapi import FastAPI
from fastapi.responses import FileResponse

import json
import os

from app.cli.profile_cli import (
    run as run_profile
)

from app.cli.match_cli import (
    run as run_match
)

from app.cli.resume_cli import (
    run as run_resume
)

from app.cli.cover_letter_cli import (
    run as run_cover_letter
)

app = FastAPI(
    title="AI Job Hunter API"
)


@app.get("/")
def root():

    return {
        "message": "AI Job Hunter API running"
    }


@app.get("/health")
def health():

    return {
        "status": "ok"
    }


@app.post("/profile")
def profile():

    run_profile()

    return {
        "status": "candidate profile generated"
    }


@app.post("/match")
def match():

    run_match()

    return {
        "status": "job match completed"
    }


@app.get("/match-result")
def get_match_result():

    with open(
        "data/output/match_result.json",
        "r"
    ) as file:

        result = json.load(file)

    return result


@app.post("/resume")
def resume():

    run_resume()

    return {
        "status": "resume generated"
    }


@app.get("/resume-result")
def get_resume_result():

    with open(
        "data/output/optimized_resume.txt",
        "r"
    ) as file:

        resume = file.read()

    return {
        "resume": resume
    }


@app.get("/download-resume")
def download_resume():

    path = "data/output/optimized_resume.docx"

    if os.path.exists(path):

        return FileResponse(
            path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename="optimized_resume.docx"
        )

    return {
        "error": "Resume DOCX not found"
    }


@app.post("/cover-letter")
def cover_letter():

    run_cover_letter()

    return {
        "status": "cover letter generated"
    }