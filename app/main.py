from fastapi import FastAPI
import json

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


@app.post("/cover-letter")
def cover_letter():

    run_cover_letter()

    return {
        "status": "cover letter generated"
    }