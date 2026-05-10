import json
import os

from app.agents.match_engine import (
    match_candidate_to_job
)


def run():

    print("Loading candidate profile...")

    with open(
        "data/profiles/candidate_profile.json",
        "r"
    ) as file:

        candidate_profile = json.load(file)

    print("Loading job description...")

    with open(
        "data/jobs/job_description.txt",
        "r"
    ) as file:

        job_description = file.read()

    print("Running AI match engine...")

    result = match_candidate_to_job(
        candidate_profile,
        job_description
    )

    print("\nMATCH RESULT:\n")
    print(result)

    os.makedirs(
        "data/output",
        exist_ok=True
    )

    with open(
        "data/output/match_result.json",
        "w"
    ) as file:

        json.dump(
            result,
            file,
            indent=4
        )

    print("\nMatch result saved.")


if __name__ == "__main__":

    run()