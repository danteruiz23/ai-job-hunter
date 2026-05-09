import json

from app.agents.resume_generator import (
    generate_resume
)

from app.services.docx_exporter import (
    export_resume_to_docx
)


def run():

    print("Loading candidate profile...")

    with open(
        "data/profiles/candidate_profile.json",
        "r"
    ) as file:

        candidate_profile = json.load(file)

    print("Loading match analysis...")

    with open(
        "data/output/match_result.json",
        "r"
    ) as file:

        match_result = json.load(file)

    print("Loading job description...")

    with open(
        "data/jobs/job_description.txt",
        "r"
    ) as file:

        job_description = file.read()

    print("Generating optimized resume...")

    optimized_resume = generate_resume(
        candidate_profile,
        match_result,
        job_description
    )

    print("\nOPTIMIZED RESUME:\n")

    print(optimized_resume)

    with open(
        "data/output/optimized_resume.txt",
        "w"
    ) as file:

        file.write(
            optimized_resume
        )

    export_resume_to_docx(
        optimized_resume,
        "data/output/optimized_resume.docx"
    )

    print(
        "\nOptimized resume saved."
    )

    print(
        "DOCX resume exported."
    )


if __name__ == "__main__":
    run()