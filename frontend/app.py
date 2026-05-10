import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Job Hunter",
    layout="wide"
)

st.title("AI Job Hunter")

col1, col2 = st.columns(2)

with col1:

    st.header("Candidate Documents")

    resume_file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx", "txt"]
    )

    linkedin_file = st.file_uploader(
        "Upload LinkedIn PDF",
        type=["pdf"]
    )

with col2:

    st.header("Target Job")

    job_description = st.text_area(
        "Paste Job Description",
        height=300
    )

st.divider()

col3, col4, col5, col6 = st.columns(4)

with col3:

    if st.button("Generate Profile"):

        response = requests.post(
            f"{API_URL}/profile"
        )

        if response.status_code == 200:

            st.success(
                "Candidate profile generated"
            )

        else:

            st.error(
                response.text
            )

with col4:

    if st.button("Run Match"):

        response = requests.post(
            f"{API_URL}/match"
        )

        if response.status_code == 200:

            st.success(
                "Job match completed"
            )

            result_response = requests.get(
                f"{API_URL}/match-result"
            )

            result = result_response.json()

            st.subheader(
                "Match Score"
            )

            st.metric(
                label="Compatibility",
                value=f"{result['match_score']}%"
            )

            st.subheader(
                "Strengths"
            )

            for item in result["strengths"]:

                st.write(
                    f"✅ {item}"
                )

            st.subheader(
                "Missing Skills"
            )

            for item in result["missing_skills"]:

                st.write(
                    f"⚠️ {item}"
                )

            st.subheader(
                "Recommendations"
            )

            for item in result["recommendations"]:

                st.write(
                    f"💡 {item}"
                )

            st.subheader(
                "Executive Summary"
            )

            st.info(
                result["executive_summary"]
            )

        else:

            st.error(
                response.text
            )

with col5:

    if st.button("Generate Resume"):

        response = requests.post(
            f"{API_URL}/resume"
        )

        if response.status_code == 200:

            st.success(
                "Resume generated"
            )

            resume_response = requests.get(
                f"{API_URL}/resume-result"
            )

            result = resume_response.json()

            st.subheader(
                "Optimized Resume"
            )

            st.text_area(
                "",
                result["resume"],
                height=600
            )

            download_response = requests.get(
                f"{API_URL}/download-resume"
            )

            if download_response.status_code == 200:

                st.download_button(
                    label="Download DOCX Resume",
                    data=download_response.content,
                    file_name="optimized_resume.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

        else:

            st.error(
                response.text
            )

with col6:

    if st.button("Generate Cover Letter"):

        response = requests.post(
            f"{API_URL}/cover-letter"
        )

        if response.status_code == 200:

            st.success(
                "Cover letter generated"
            )

        else:

            st.error(
                response.text
            )