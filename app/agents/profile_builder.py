from app.services.file_parser import extract_text


def build_candidate_profile():

    resume_text = extract_text(
        "data/resumes/dante_resume.docx"
    )

    linkedin_text = extract_text(
        "data/linkedin/linkedin_profile.pdf"
    )

    combined_profile = f"""
    RESUME:
    {resume_text}

    LINKEDIN:
    {linkedin_text}
    """

    return combined_profile