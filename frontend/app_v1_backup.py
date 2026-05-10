import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Job Hunter",
    layout="wide"
)

st.title("AI Job Hunter")

st.markdown(
    "Upload your resume and job description"
)

st.divider()

uploaded_resume = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description",
    height=300
)

col1, col2, col3 = st.columns(3)

# =========================
# GENERATE PROFILE
# =========================

with col1:

    if st.button(
        "Generate Profile"
    ):

        if uploaded_resume is None:

            st.error(
                "Please upload a resume PDF."
            )

        else:

            with st.spinner(
                "Generating candidate profile..."
            ):

                files = {
                    "file": (
                        uploaded_resume.name,
                        uploaded_resume,
                        "application/pdf"
                    )
                }

                response = requests.post(
                    f"{API_URL}/profile",
                    files=files
                )

                if response.status_code == 200:

                    st.success(
                        "Candidate profile generated"
                    )

                    profile_response = requests.get(
                        f"{API_URL}/profile-result"
                    )

                    if (
                        profile_response.status_code
                        == 200
                    ):

                        profile = (
                            profile_response.json()
                        )

                        st.subheader(
                            "Generated Candidate Profile"
                        )

                        st.json(profile)

                    else:

                        st.error(
                            "Could not load profile result."
                        )

                else:

                    st.error(
                        "Profile generation failed."
                    )

# =========================
# RUN MATCH
# =========================

with col2:

    if st.button(
        "Run Match"
    ):

        if uploaded_resume is None:

            st.error(
                "Please upload a resume PDF."
            )

        elif not job_description:

            st.error(
                "Please paste a job description."
            )

        else:

            with st.spinner(
                "Running AI match engine..."
            ):

                files = {
                    "file": (
                        uploaded_resume.name,
                        uploaded_resume,
                        "application/pdf"
                    )
                }

                data = {
                    "job_description": (
                        job_description
                    )
                }

                response = requests.post(
                    f"{API_URL}/match",
                    files=files,
                    data=data
                )

                if response.status_code == 200:

                    st.success(
                        "Job match completed"
                    )

                    match_response = requests.get(
                        f"{API_URL}/match-result"
                    )

                    if (
                        match_response.status_code
                        == 200
                    ):

                        result = (
                            match_response.json()
                        )

                        st.subheader(
                            "Match Score"
                        )

                        st.metric(
                            "Score",
                            f"{result['match_score']}%"
                        )

                        st.progress(
                            result["match_score"] / 100
                        )

                        tab1, tab2, tab3, tab4 = st.tabs(
                            [
                                "Strengths",
                                "Missing Skills",
                                "Recommendations",
                                "Executive Summary"
                            ]
                        )

                        with tab1:

                            for item in result[
                                "strengths"
                            ]:

                                st.success(item)

                        with tab2:

                            for item in result[
                                "missing_skills"
                            ]:

                                st.warning(item)

                        with tab3:

                            for item in result[
                                "recommendations"
                            ]:

                                st.info(item)

                        with tab4:

                            st.write(
                                result[
                                    "executive_summary"
                                ]
                            )

                    else:

                        st.error(
                            "Could not load match result."
                        )

                else:

                    st.error(
                        "Match process failed."
                    )

# =========================
# GENERATE COVER LETTER
# =========================

with col3:

    if st.button(
        "Generate Cover Letter"
    ):

        st.info(
            "Coming next..."
        )