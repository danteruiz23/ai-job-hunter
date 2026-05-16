"""UI strings for Streamlit (English / Spanish)."""

STRINGS = {
    "en": {
        "page_title": "🚀 AI Job Hunter",
        "page_caption": (
            "**AI-Powered Resume & Career Optimization Platform**  \n"
            "(By Dante Ruiz)"
        ),
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
        "debug_api_expander": "API & connectivity (debug)",
        "debug_probe_health": "Test GET /health",
        "debug_probe_hint": (
            "Uses the same base URL as uploads and Save. "
            "200 + JSON here means the API is reachable from Streamlit."
        ),
        "api_error_html": (
            "The server returned an HTML error page (HTTP {code}), not API "
            "data. On Render, set **API_URL** in the Streamlit service to your "
            "**FastAPI** URL (not this Streamlit URL) and ensure the API "
            "service is running and healthy."
        ),
        "jd_cleared_bad_html": (
            "The job description field contained an HTML error page (for "
            "example a 502 page) and was cleared. Paste the real job text "
            "and click **Save Job Description** again."
        ),
        "jd_reject_html": (
            "That text looks like an HTML error page (not a job description). "
            "Paste the job posting text only, then save."
        ),
        "job_search_header": "🔎 Job search",
        "job_search_hint": (
            "Finds jobs that match your resume and LinkedIn expertise. "
            "Upload your documents, then click the button below."
        ),
        "job_search_upload_first": (
            "Upload your resume or LinkedIn PDF first "
            "so we can find jobs based on your expertise."
        ),
        "job_search_urls": "Job posting URLs (one per line)",
        "job_search_serpapi_key": "SerpApi API Key",
        "job_search_count": "Max listings from Google Jobs",
        "job_search_run": "🔍 Find Jobs Based on My Profile",
        "job_search_done": "Job search finished",
        "job_search_used": "Search used: query=`{q}`, location=`{loc}`, SerpApi={serp}",
        "job_search_messages": "Notes",
        "empty_job_search": (
            "Click **Find Jobs Based on My Profile** above "
            "to discover positions that match your expertise."
        ),
        "tab_job_search": "🔎 Job search",
        "job_search_advanced": "⚙️ Advanced options",
        "job_search_advanced_hint": (
            "Add specific job posting URLs or your SerpApi key "
            "for broader results."
        ),
        "job_search_sort_label": "Sort by",
        "job_search_sort_match_desc": "Match Score (High → Low)",
        "job_search_sort_match_asc": "Match Score (Low → High)",
        "job_search_sort_title": "Title (A → Z)",
        "job_search_sort_company": "Company (A → Z)",
        "job_search_results_count": "{count} jobs found",
        "job_search_apply": "Apply →",
    },
    "es": {
        "page_title": "🚀 Cazador de empleos IA",
        "page_caption": (
            "**Plataforma de currículum y carrera asistida por IA**  \n"
            "(Por Dante Ruiz)"
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
        "debug_api_expander": "API y conectividad (depuración)",
        "debug_probe_health": "Probar GET /health",
        "debug_probe_hint": (
            "Usa la misma URL base que las subidas y Guardar. "
            "200 + JSON indica que Streamlit alcanza la API."
        ),
        "api_error_html": (
            "El servidor devolvió una página HTML de error (HTTP {code}), no "
            "datos de la API. En Render, configura **API_URL** en el servicio "
            "Streamlit con la URL de **FastAPI** (no la de Streamlit) y "
            "comprueba que la API esté en marcha."
        ),
        "jd_cleared_bad_html": (
            "La descripción del puesto contenía una página HTML de error "
            "(p. ej. 502) y se vació. Pega el texto real del puesto y pulsa "
            "**Guardar descripción** de nuevo."
        ),
        "jd_reject_html": (
            "Ese texto parece una página HTML de error, no la descripción "
            "del puesto. Pega solo el texto del anuncio y guarda."
        ),
        "job_search_header": "🔎 Búsqueda de empleos",
        "job_search_hint": (
            "Encuentra empleos que coincidan con tu currículum y "
            "experiencia de LinkedIn. Sube tus documentos y pulsa el botón."
        ),
        "job_search_upload_first": (
            "Sube tu currículum o PDF de LinkedIn primero "
            "para buscar empleos según tu experiencia."
        ),
        "job_search_urls": "URLs de anuncios (una por línea)",
        "job_search_serpapi_key": "Clave API de SerpApi",
        "job_search_count": "Máximo de resultados Google Jobs",
        "job_search_run": "🔍 Buscar empleos según mi perfil",
        "job_search_done": "Búsqueda terminada",
        "job_search_used": "Búsqueda: consulta=`{q}`, ubicación=`{loc}`, SerpApi={serp}",
        "job_search_messages": "Notas",
        "empty_job_search": (
            "Pulsa **Buscar empleos según mi perfil** arriba "
            "para descubrir posiciones que coincidan con tu experiencia."
        ),
        "tab_job_search": "🔎 Búsqueda",
        "job_search_advanced": "⚙️ Opciones avanzadas",
        "job_search_advanced_hint": (
            "Añade URLs de anuncios específicos o tu clave SerpApi "
            "para resultados más amplios."
        ),
        "job_search_sort_label": "Ordenar por",
        "job_search_sort_match_desc": "Puntuación (Mayor → Menor)",
        "job_search_sort_match_asc": "Puntuación (Menor → Mayor)",
        "job_search_sort_title": "Título (A → Z)",
        "job_search_sort_company": "Empresa (A → Z)",
        "job_search_results_count": "{count} empleos encontrados",
        "job_search_apply": "Aplicar →",
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
