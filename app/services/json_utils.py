import json
import re


def extract_json(content):

    # Remove markdown fences
    content = re.sub(
        r"```json|```",
        "",
        content
    ).strip()

    # Find first JSON object
    start = content.find("{")

    if start == -1:
        raise ValueError(
            "No JSON object found"
        )

    decoder = json.JSONDecoder()

    obj, _ = decoder.raw_decode(
        content[start:]
    )

    return obj