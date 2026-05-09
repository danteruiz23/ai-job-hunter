import json

from app.agents.match_engine import (
    match_candidate_to_job
)

with open(
    "data/profiles/candidate_profile.json",
    "r"
) as file:

    candidate_profile = json.load(file)

with open(
    "data/jobs/job_description.txt",
    "r"
) as file:

    job_description = file.read()

result = match_candidate_to_job(
    candidate_profile,
    job_description
)

print(result)