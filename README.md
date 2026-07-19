# AI-Powered Intelligent Document Automation and Workflow Management System

An intelligent document management system that automates document processing using Optical Character Recognition (OCR), Artificial Intelligence (AI), and Natural Language Processing (NLP). The system extracts text from uploaded documents, analyzes content, classifies documents, generates summaries, predicts priority and department, and automates workflow management.

---

## Features

- Secure user authentication
- Upload PDF, DOCX, and image documents
- OCR-based text extraction
- AI-powered document summarization
- Automatic document classification
- Metadata extraction
- Department prediction
- Priority prediction (High, Medium, Low)
- AI chatbot for document queries
- Dashboard for document monitoring
- Email notification system
- Workflow tracking and management
- PDF report generation
- SQLite database integration

---

## Technology Stack

| Category | Technologies |
|----------|--------------|
| Programming Language | Python |
| Backend | Flask |
| Database | SQLite |
| OCR | Tesseract OCR |
| AI & NLP | Groq API, Large Language Models |
| Document Processing | PyPDF2, python-docx, Pillow |
| Other Libraries | OpenCV, pytesseract |

---

## Project Structure

```
AI-Document-Automation-Workflow-System/
│
├── admin/
├── ai/
├── assets/
├── dashboard/
├── database/
├── generated_reports/
├── models/
├── ocr/
├── reports/
├── upload/
├── uploads/
├── workflow/
├── app.py
├── config.py
├── requirements.txt
└── README.md
```

---

## System Workflow

1. User logs into the system.
2. Documents are uploaded (PDF, DOCX, or Image).
3. OCR extracts text from uploaded files.
4. AI analyzes the extracted content.
5. The system:
   - Generates document summaries
   - Classifies document type
   - Extracts metadata
   - Predicts department
   - Predicts priority
6. Document information is stored in the database.
7. Workflow notifications and reports are generated.
8. Users can interact with documents through the AI chatbot.

---

## Installation

Clone the repository

```bash
git clone https://github.com/priyadharshini-1506/AI-Document-Automation-Workflow-System.git
```

Navigate to the project

```bash
cd AI-Document-Automation-Workflow-System
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

---

## Results

The system successfully provides:

- OCR-based text extraction
- AI-generated document summaries
- Intelligent document classification
- Metadata extraction
- Department prediction
- Priority prediction
- AI chatbot assistance
- Secure authentication
- Automated workflow tracking
- Email notifications
- PDF report generation
- Centralized document storage

---

## Future Enhancements

- Cloud storage integration
- Multi-language OCR support
- Role-based access control
- Mobile application
- Advanced analytics dashboard
- Digital signature verification

---



