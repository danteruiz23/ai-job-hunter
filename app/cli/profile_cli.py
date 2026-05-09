from app.agents.profile_builder import (
    build_candidate_profile
)

from app.agents.profile_extractor import (
    extract_candidate_data
)

import json


def run():

    profile = build_candidate_profile()

    candidate_data = extract_candidate_data(
        profile
    )

    print(candidate_data)

    with open(
        "data/profiles/candidate_profile.json",
        "w"
    ) as file:

        json.dump(
            candidate_data,
            file,
            indent=4
        )

    print(
        "\nCandidate profile saved."
    )


if __name__ == "__main__":
    run()