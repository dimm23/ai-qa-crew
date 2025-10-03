from pathlib import Path
import PyPDF2
from docx import Document

def extract_text_from_file(file_path: str) -> str:
    path = Path(file_path)
    if path.suffix.lower() == ".pdf":
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            return "\n".join(page.extract_text() for page in reader.pages)
    elif path.suffix.lower() in [".docx", ".doc"]:
        doc = Document(file_path)
        return "\n".join(paragraph.text for paragraph in doc.paragraphs)
    elif path.suffix.lower() in [".txt", ".md"]:
        return path.read_text(encoding="utf-8")
    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")