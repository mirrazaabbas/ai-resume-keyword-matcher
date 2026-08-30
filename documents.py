"""Resume/job document ingestion with optional PDF and DOCX support."""
from __future__ import annotations

from pathlib import Path


def read_document(path: str | Path) -> str:
    target = Path(path)
    if not target.is_file():
        raise ValueError(f"file not found: {target}")
    suffix = target.suffix.lower()
    if suffix in {".txt", ".md"}:
        try:
            text = target.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"file is not valid UTF-8: {target}") from exc
    elif suffix == ".pdf":
        text = _read_pdf(target)
    elif suffix == ".docx":
        text = _read_docx(target)
    else:
        raise ValueError("supported formats are .txt, .md, .pdf and .docx")
    if not text.strip():
        raise ValueError(f"document contains no extractable text: {target}")
    return text


def _read_pdf(path: Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("PDF support requires the 'documents' extra") from exc
    try:
        reader = PdfReader(str(path))
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    except Exception as exc:  # noqa: BLE001 - parser boundary normalizes provider errors
        raise ValueError(f"unable to read PDF: {path}") from exc


def _read_docx(path: Path) -> str:
    try:
        from docx import Document
    except ImportError as exc:
        raise RuntimeError("DOCX support requires the 'documents' extra") from exc
    try:
        document = Document(str(path))
        return "\n".join(paragraph.text for paragraph in document.paragraphs)
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"unable to read DOCX: {path}") from exc
