"""UI strings for Streamlit (English / Spanish)."""

STRINGS = {
    "en": {
        "page_title": "🚀 AI Job Hunter",
        "page_caption": "AI-Powered Resume & Career Optimization Platform",
        "upload_documents": "📂 Upload Documents",
        "upload_resume": "Upload Resume",
        "resume_uploaded_ok": "Resume uploaded successfully",
        "upload_linkedin": "Upload LinkedIn PDF",
        "linkedin_uploaded_ok": "LinkedIn PDF uploaded",
        "target_job": "🎯 Target Job",
        "paste_job_description": "Paste Job Description",
        "save_job_description": "Save Job Description",
        "job_description_saved": "Job Description saved",
        "cleanup_expander": "🧹 Clean up files on server",
        "cleanup_caption": (
            "The API only uses fixed names: **resume.pdf|docx|txt**, "
            "**linkedin.pdf**, and **job_description.txt**. "
            "Old uploads (e.g. extra .docx names) are ignored for saving "
            "but can still be read until you remove them."
        ),
        "remove_extra_files": "Remove extra files in data/input",
        "remove_extra_help": (
            "Deletes anything that is not job description, "
            "canonical resume/LinkedIn, or .gitkeep."
        ),
        "removed_label": "Removed:",
        "no_extra_files": "No extra files to remove.",
        "clear_candidate_files": "Clear resume & LinkedIn from server",
        "clear_candidate_help": (
            "Deletes resume.pdf, resume.docx, resume.txt, "
            "and linkedin.pdf. Re-upload to run AI again."
        ),
        "cleared_label": "Cleared:",
        "nothing_on_disk": "nothing was on disk",
        "ai_actions": "🚀 AI Actions",
        "warn_upload_first": (
            "Upload a resume and/or LinkedIn PDF to enable AI actions."
        ),
        "info_save_jd": (
            "Save a job description to enable Match/Resume/Cover Letter."
        ),
        "generate_profile": "Generate Profile",
        "invalid_json": "API returned a response that is not valid JSON.",
        "profile_generated": "Profile generated",
        "analyze_match": "Analyze Job Match",
        "match_completed": "Match analysis completed",
        "generate_resume": "Generate AI Resume",
        "resume_generated": "AI Resume generated",
        "generate_cover": "Generate Cover Letter",
        "cover_generated": "Cover Letter generated",
        "score_excellent": "Excellent Match",
        "score_good": "Good Match",
        "score_needs_work": "Needs Improvement",
        "skills_strong": "Strong Alignment",
        "skills_gaps": "Skill Gaps Detected",
        "match_score": "Match Score",
        "ats_score": "ATS Score",
        "missing_skills": "Missing Skills",
        "missing_skills_heading": "Missing Skills Details",
        "tab_profile": "👤 Profile",
        "tab_match": "📊 Match Analysis",
        "tab_resume": "📄 AI Resume",
        "tab_cover": "✉️ Cover Letter",
        "empty_profile": (
            "Upload your resume + LinkedIn PDF, save a job description, "
            "then click **Generate Profile** in the sidebar."
        ),
        "empty_analysis": (
            "Click **Analyze Job Match** in the sidebar to generate the "
            "match report and scores."
        ),
        "empty_resume": (
            "Click **Generate AI Resume** in the sidebar to create an "
            "ATS-optimized version tailored to the job."
        ),
        "empty_cover": (
            "Click **Generate Cover Letter** in the sidebar after saving "
            "a job description."
        ),
        "download_resume": "⬇ Download Resume",
        "download_cover": "⬇ Download Cover Letter",
        "lang_label": "🌐 Language / Idioma",
        "theme_label": "Appearance",
        "theme_dark": "Dark",
        "theme_light": "Light",
        "api_unreachable": (
            "Could not reach the API at `{url}`. Start it with: "
            "`python -m uvicorn app.api.main:app --reload`\n\nDetails: {exc}"
        ),
    },
    "es": {
        "page_title": "🚀 Cazador de empleos IA",
        "page_caption": (
            "Plataforma de currículum y carrera asistida por IA"
        ),
        "upload_documents": "📂 Subir documentos",
        "upload_resume": "Subir currículum",
        "resume_uploaded_ok": "Currículum subido correctamente",
        "upload_linkedin": "Subir PDF de LinkedIn",
        "linkedin_uploaded_ok": "PDF de LinkedIn subido",
        "target_job": "🎯 Puesto objetivo",
        "paste_job_description": "Pegar descripción del puesto",
        "save_job_description": "Guardar descripción",
        "job_description_saved": "Descripción guardada",
        "cleanup_expander": "🧹 Limpiar archivos en el servidor",
        "cleanup_caption": (
            "La API solo usa nombres fijos: **resume.pdf|docx|txt**, "
            "**linkedin.pdf** y **job_description.txt**. "
            "Subidas antiguas (p. ej. otros .docx) ya no se guardan "
            "pero pueden seguir leyéndose hasta que las borres."
        ),
        "remove_extra_files": "Eliminar archivos extra en data/input",
        "remove_extra_help": (
            "Borra todo lo que no sea la descripción del puesto, "
            "currículum/LinkedIn canónicos o .gitkeep."
        ),
        "removed_label": "Eliminados:",
        "no_extra_files": "No hay archivos extra que eliminar.",
        "clear_candidate_files": "Borrar currículum y LinkedIn del servidor",
        "clear_candidate_help": (
            "Elimina resume.pdf, resume.docx, resume.txt y linkedin.pdf. "
            "Vuelve a subirlos para usar la IA."
        ),
        "cleared_label": "Borrado:",
        "nothing_on_disk": "no había archivos en disco",
        "ai_actions": "🚀 Acciones IA",
        "warn_upload_first": (
            "Sube un currículum y/o PDF de LinkedIn para activar las "
            "acciones de IA."
        ),
        "info_save_jd": (
            "Guarda una descripción del puesto para Coincidencia/"
            "Currículum/Carta de presentación."
        ),
        "generate_profile": "Generar perfil",
        "invalid_json": "La API devolvió una respuesta que no es JSON válido.",
        "profile_generated": "Perfil generado",
        "analyze_match": "Analizar coincidencia",
        "match_completed": "Análisis de coincidencia terminado",
        "generate_resume": "Generar currículum IA",
        "resume_generated": "Currículum IA generado",
        "generate_cover": "Generar carta de presentación",
        "cover_generated": "Carta generada",
        "score_excellent": "Excelente coincidencia",
        "score_good": "Buena coincidencia",
        "score_needs_work": "Necesita mejora",
        "skills_strong": "Buena alineación",
        "skills_gaps": "Brechas de habilidades",
        "match_score": "Coincidencia",
        "ats_score": "Puntuación ATS",
        "missing_skills": "Habilidades faltantes",
        "missing_skills_heading": "Detalle de habilidades faltantes",
        "tab_profile": "👤 Perfil",
        "tab_match": "📊 Análisis",
        "tab_resume": "📄 Currículum IA",
        "tab_cover": "✉️ Carta de presentación",
        "empty_profile": (
            "Sube currículum + PDF de LinkedIn, guarda la descripción del "
            "puesto y pulsa **Generar perfil** en la barra lateral."
        ),
        "empty_analysis": (
            "Pulsa **Analizar coincidencia** en la barra lateral para "
            "generar el informe y las puntuaciones."
        ),
        "empty_resume": (
            "Pulsa **Generar currículum IA** para crear una versión "
            "optimizada para ATS."
        ),
        "empty_cover": (
            "Pulsa **Generar carta de presentación** después de guardar "
            "la descripción del puesto."
        ),
        "download_resume": "⬇ Descargar currículum",
        "download_cover": "⬇ Descargar carta de presentación",
        "lang_label": "🌐 Language / Idioma",
        "theme_label": "Apariencia",
        "theme_dark": "Oscuro",
        "theme_light": "Claro",
        "api_unreachable": (
            "No se pudo conectar con la API en `{url}`. Inicia el servidor "
            "con: `python -m uvicorn app.api.main:app --reload`\n\n"
            "Detalle: {exc}"
        ),
    },
}


def text(
    lang: str,
    key: str,
) -> str:

    bucket = STRINGS.get(
        lang,
        STRINGS["en"],
    )

    return bucket.get(
        key,
        STRINGS["en"].get(
            key,
            key,
        ),
    )
