from pathlib import Path
def extract_text(path):
    p=Path(path); ext=p.suffix.lower()
    if ext in {".txt",".md"}: return p.read_text(encoding="utf-8",errors="ignore")
    if ext==".pdf":
        from pypdf import PdfReader
        return "\n\n".join(f"[Page {i+1}]\n{page.extract_text() or ''}" for i,page in enumerate(PdfReader(str(p)).pages))
    if ext==".docx":
        from docx import Document
        d=Document(str(p)); return "\n".join(x.text for x in d.paragraphs)
    raise ValueError("Supported knowledge documents: PDF, DOCX, TXT, Markdown.")
def chunk_text(text,chunk_chars=1800,overlap=250):
    text=text.strip(); out=[]; start=0
    while start<len(text):
        end=min(len(text),start+chunk_chars)
        out.append(text[start:end])
        if end==len(text): break
        start=max(start+1,end-overlap)
    return out
