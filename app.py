from flask import Flask, render_template, request
from text_summarizer import summarizer
import os
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from docx import Document

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        rawtext = request.form.get('rawtext', '')
        uploaded_file = request.files.get('uploaded_file')
        extracted_text = ""

        # Handle uploaded file
        if uploaded_file:
            filename = secure_filename(uploaded_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(file_path)

            # Extract text based on file type
            if filename.endswith('.pdf'):
                extracted_text = extract_text_from_pdf(file_path)
            elif filename.endswith('.docx'):
                extracted_text = extract_text_from_docx(file_path)
            elif filename.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    extracted_text = f.read()

        # Use either uploaded text or raw text from the form
        input_text = extracted_text if extracted_text else rawtext
        if not input_text.strip():
            return "No text provided for summarization!", 400

        # Summarize the text
        summary, original_txt, len_orig_txt, len_summary = summarizer(input_text)
        return render_template('summary.html', summary=summary, original_txt=original_txt, len_orig_txt=len_orig_txt, len_summary=len_summary)

    return render_template('index.html')

def extract_text_from_pdf(filepath):
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(filepath):
    doc = Document(filepath)
    return "\n".join([para.text for para in doc.paragraphs])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)