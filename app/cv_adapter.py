from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Leer CV automáticamente
with open("data/resumes/dante_cv.txt", "r") as file:
    cv_text = file.read()

# Job description
job_description = """
We are looking for a Telecom Service Delivery Manager with experience in:

- Tier-1 carriers
- Network deployment
- SLA management
- Cross-functional leadership
- Customer escalations
- Vendor management
- Telecom infrastructure
""" 

prompt = f"""
You are an expert telecom recruiter and ATS optimizer.

Analyze this candidate CV against the telecom job description.

Provide:

1. Match percentage
2. Missing keywords
3. Strong matching experience
4. Resume improvement recommendations
5. ATS optimization suggestions
6. Improved professional summary

CANDIDATE CV:
{cv_text}

JOB DESCRIPTION:
{job_description}
"""

response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print("\n")
print("CV MATCH ANALYSIS")
print("=================")
print("\n")

print(response.choices[0].message.content)