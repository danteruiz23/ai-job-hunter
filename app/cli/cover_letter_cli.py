import json

from app.agents.cover_letter_generator import (
    generate_cover_letter
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

    print("Generating cover letter...")

    cover_letter = generate_cover_letter(
        candidate_profile,
        match_result,
        job_description
    )

    print("\nCOVER LETTER:\n")

    print(cover_letter)

    with open(
        "data/output/cover_letter.txt",
        "w"
    ) as file:

        file.write(
            cover_letter
        )

    print(
        "\nCover letter saved."
    )


if __name__ == "__main__":
    run()