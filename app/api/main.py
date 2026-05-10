from fastapi import FastAPI

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
    title="AI Job Hunter API",
    version="1.0.0"
)


@app.get("/")
def root():

    return {
        "message": "AI Job Hunter API"
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


@app.post("/resume")
def resume():

    run_resume()

    return {
        "status": "resume generated"
    }


@app.post("/cover-letter")
def cover_letter():

    run_cover_letter()

    return {
        "status": "cover letter generated"
    }


@app.get("/health")
def health():

    return {
        "status": "ok"
    }