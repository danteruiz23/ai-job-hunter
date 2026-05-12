from dotenv import load_dotenv

from app.ai.openai_client import get_openai_client
from app.ai.prompt_engine import PROFILE_PROMPT

load_dotenv()


def generate_profile(candidate_data):

    response = get_openai_client().chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.7,
        messages=[
            {
                "role": "system",
                "content": PROFILE_PROMPT
            },
            {
                "role": "user",
                "content": candidate_data
            }
        ]
    )

    return response.choices[0].message.content