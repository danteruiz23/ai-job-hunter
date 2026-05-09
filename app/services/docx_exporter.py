from docx import Document


def export_resume_to_docx(
    resume_text,
    output_path
):

    doc = Document()

    lines = resume_text.split("\n")

    for line in lines:

        clean_line = line.strip()

        if clean_line:

            doc.add_paragraph(
                clean_line
            )

    doc.save(output_path)