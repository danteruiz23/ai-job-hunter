import json
import os

from app.agents.profile_extractor import (
    extract_candidate_data
)


def run():

    print(
        "Loading resume..."
    )

    with open(
        "data/input/resume.txt",
        "r"
    ) as file:

        resume_text = file.read()

    print(
        "Extracting candidate profile..."
    )

    candidate_profile = extract_candidate_data(
        resume_text
    )

    os.makedirs(
        "data/output",
        exist_ok=True
    )

    with open(
        "data/output/candidate_profile.json",
        "w"
    ) as file:

        json.dump(
            candidate_profile,
            file,
            indent=2
        )

    print(
        "Candidate profile saved."
    )