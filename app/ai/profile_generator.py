from openai import OpenAI
from dotenv import load_dotenv
import os

from app.ai.prompt_engine import PROFILE_PROMPT

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def generate_profile(candidate_data):

    response = client.chat.completions.create(
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