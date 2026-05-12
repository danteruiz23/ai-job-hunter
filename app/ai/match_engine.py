from dotenv import load_dotenv

import json

from app.ai.openai_client import get_openai_client
from app.ai.prompt_engine import MATCH_PROMPT
from app.ai.industry_detector import detect_industry
from app.ai.skill_extractor import extract_skills
from app.ai.job_parser import extract_target_role

# ======================================================
# LOAD ENV
# ======================================================

load_dotenv()

# ======================================================
# JSON RETRY REMINDER
# ======================================================

_JSON_RETRY_REMINDER = """
Return ONLY valid JSON.

No markdown.
No code fences.
No explanations.
""".strip()

# ======================================================
# JSON PARSER
# ======================================================

def _coerce_match_json(text: str):

    if not text:

        raise ValueError(
            "Empty model response"
        )

    text = text.strip()

    # Attempt extraction if model adds extra text

    if not text.startswith("{"):

        start = text.find("{")
        end = text.rfind("}")

        if (
            start != -1
            and end != -1
            and end > start
        ):

            text = text[start:end + 1]

    data = json.loads(text)

    analysis = str(
        data.get("analysis", "")
    ).strip()

    match_score = int(
        data.get("match_score", 0)
    )

    ats_score = int(
        data.get("ats_score", 0)
    )

    missing_skills = data.get(
        "missing_skills",
        []
    )

    if not isinstance(
        missing_skills,
        list
    ):

        missing_skills = []

    missing_skills = [

        str(skill).strip()

        for skill in missing_skills

        if str(skill).strip()

    ][:20]

    match_score = max(
        0,
        min(100, match_score)
    )

    ats_score = max(
        0,
        min(100, ats_score)
    )

    return {

        "analysis": analysis,

        "match_score": match_score,

        "ats_score": ats_score,

        "missing_skills": missing_skills,
    }

# ======================================================
# MODEL CALL
# ======================================================

def _call_match_model(
    prompt: str,
    *,
    temperature: float,
):

    response = get_openai_client().chat.completions.create(

        model="gpt-4.1-mini",

        temperature=temperature,

        max_tokens=3000,

        messages=[

            {
                "role": "system",
                "content": MATCH_PROMPT,
            },

            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return response.choices[0].message.content

# ======================================================
# MAIN MATCH ENGINE
# ======================================================

def generate_match_analysis(

    candidate_data,
    job_description
):

    # ==================================================
    # TARGET ROLE
    # ==================================================

    target_role = extract_target_role(
        job_description
    )

    # ==================================================
    # INDUSTRY DETECTION
    # ==================================================

    combined_text = (
        candidate_data
        + "\n"
        + job_description
    )

    industry = detect_industry(
        combined_text
    )

    # ==================================================
    # SKILL EXTRACTION
    # ==================================================

    candidate_skills = extract_skills(
        candidate_data
    )

    job_skills = extract_skills(
        job_description
    )

    # ==================================================
    # STRICT MISSING SKILLS
    # ==================================================

    missing_skills = []

    for skill in job_skills:

        if skill not in candidate_skills:

            missing_skills.append(skill)

    # ==================================================
    # PROMPT
    # ==================================================

    prompt = f"""
TARGET ROLE:
{target_role}

==================================================

INDUSTRY:
{industry}

==================================================

CANDIDATE SKILLS:
{candidate_skills}

==================================================

JOB REQUIRED SKILLS:
{job_skills}

==================================================

INITIAL MISSING SKILLS:
{missing_skills}

==================================================

CANDIDATE PROFILE:

{candidate_data}

==================================================

JOB DESCRIPTION:

{job_description}

==================================================

You are a world-class executive recruiter,
ATS optimization specialist,
career strategist,
and enterprise hiring advisor.

Your task is to evaluate the candidate specifically
for the TARGET ROLE.

Analyze the compatibility between the candidate
and the target role.

==================================================

IMPORTANT REQUIREMENTS

- Be STRICT identifying missing skills
- Infer strategic capability gaps
- Infer missing executive capabilities
- Evaluate ATS compatibility
- Evaluate technical alignment
- Evaluate leadership alignment
- Evaluate operational maturity
- Evaluate financial accountability
- Evaluate transformation experience
- Evaluate industry relevance
- Evaluate seniority alignment
- Evaluate role readiness

If the role requires capabilities like:
- P&L ownership
- executive leadership
- AI transformation
- regional leadership
- commercial accountability
- enterprise contracting
- operational leadership
- revenue ownership
- cross-functional leadership
- cloud transformation
- cybersecurity governance

and they are NOT clearly demonstrated,
include them in missing_skills.

Infer missing competencies even when
they are indirectly referenced.

==================================================

SCORING RULES

MATCH SCORE:
- overall hiring fit
- leadership fit
- technical fit
- industry fit
- strategic fit

ATS SCORE:
- keyword alignment
- ATS optimization
- terminology alignment
- role targeting
- measurable achievements

==================================================

RESPONSE REQUIREMENTS

The analysis must be:
- executive-level
- highly detailed
- strategic
- recruiter-grade
- realistic
- actionable
- role-specific

Avoid generic language.

==================================================

RETURN STRICT JSON ONLY

{{
    "analysis": "Detailed recruiter-grade analysis here",
    "match_score": 82,
    "ats_score": 78,
    "missing_skills": [
        "P&L Management",
        "Regional Leadership"
    ]
}}

NO MARKDOWN.
NO CODE BLOCKS.
NO EXTRA TEXT.
"""

    # ==================================================
    # FIRST ATTEMPT
    # ==================================================

    content = _call_match_model(
        prompt,
        temperature=0.4,
    )

    try:

        result = _coerce_match_json(
            content
        )

        # Deterministic overwrite

        if missing_skills:

            result["missing_skills"] = (
                missing_skills
            )

        return result

    # ==================================================
    # RETRY ATTEMPT
    # ==================================================

    except Exception:

        retry_content = _call_match_model(

            f"""
{prompt}

{_JSON_RETRY_REMINDER}
""",

            temperature=0.0,
        )

        result = _coerce_match_json(
            retry_content
        )

        if missing_skills:

            result["missing_skills"] = (
                missing_skills
            )

        return result