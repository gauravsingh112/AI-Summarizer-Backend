from transformers import pipeline
from PyPDF2 import PdfReader
import docx

# Load summarization pipeline
summarizer = pipeline("summarization")

def read_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.strip()
    except Exception as e:
        raise RuntimeError(f"Error reading PDF file: {str(e)}")

def read_docx(file_path):
    try:
        doc = docx.Document(file_path)
        text = [paragraph.text for paragraph in doc.paragraphs]
        return '\n'.join(text).strip()
    except Exception as e:
        raise RuntimeError(f"Error reading DOCX file: {str(e)}")

def read_txt(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except Exception as e:
        raise RuntimeError(f"Error reading TXT file: {str(e)}")

def summarize_text(file_path):
    try:
        if file_path.endswith('.pdf'):
            text = read_pdf(file_path)
        elif file_path.endswith('.docx'):
            text = read_docx(file_path)
        elif file_path.endswith('.txt'):
            text = read_txt(file_path)
        else:
            return "Unsupported file format"

        if not text:
            return "No content found in the file"

        # Summarize the text
        if len(text) > 1000:
            try:
                summaries = summarizer(text, max_length=400, min_length=100, do_sample=False)
                summary = " ".join([summ['summary_text'] for summ in summaries])
            except Exception as e:
                return f"Error summarizing text: {str(e)}"
        else:
            summary = text  # For small text, don't summarize

        return summary
    except Exception as e:
        return f"Error processing file: {str(e)}"
