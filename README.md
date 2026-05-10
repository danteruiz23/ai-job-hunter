# AI Job Hunter Agent

AI-powered career copilot that analyzes candidates, matches jobs, optimizes resumes, generates cover letters, and prepares executive-level application assets using OpenAI.

---

# Features

- Multi-format resume ingestion (TXT, PDF, DOCX)
- LinkedIn profile parsing
- AI-powered candidate intelligence extraction
- ATS match scoring engine
- Executive resume optimization
- Tailored cover letter generation
- DOCX export support
- CLI-driven workflow orchestration

---

# Architecture

```text
app/
│
├── agents/        # AI reasoning agents
├── services/      # Shared infrastructure/services
├── cli/           # CLI entrypoints
├── data/          # Inputs and outputs