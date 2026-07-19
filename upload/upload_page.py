import streamlit as st

from database.document_repository import update_ai_results

from upload.upload import save_uploaded_file
from upload.organizer import organize_file
from upload.validator import allowed_file

from ocr.extractor import extract_text

from ai.summarizer import generate_summary
from ai.classifier import classify_document
from ai.metadata import extract_metadata
from ai.priority import detect_priority
from ai.department import assign_department

from workflow.logger import add_log
from workflow.workflow import recommend_workflow
from workflow.reminder import create_reminder
from workflow.email_sender import send_email

from reports.pdf_report import generate_pdf_report


def upload_page():

    st.title("📄 AI-Powered Intelligent Document Automation")

    st.sidebar.success(
        f"Welcome {st.session_state.user}"
    )

    uploaded_file = st.file_uploader(
        "📤 Upload Document",
        type=[
            "pdf",
            "docx",
            "jpg",
            "jpeg",
            "png"
        ]
    )

    if uploaded_file:

        if allowed_file(uploaded_file.name):

            # ==========================
            # SAVE DOCUMENT
            # ==========================

            filepath = save_uploaded_file(
                uploaded_file,
                st.session_state.user
            )

            st.success(
                "✅ Document Uploaded Successfully"
            )

            st.subheader("📁 Uploaded File")

            st.code(filepath)

            # ==========================
            # OCR TEXT EXTRACTION
            # ==========================

            with st.spinner(
                "📄 Extracting text..."
            ):

                extracted_text = extract_text(
                    filepath
                )

            # Save extracted text for chatbot

            st.session_state.document_text = extracted_text

            st.subheader(
                "📄 Extracted Text"
            )

            st.text_area(
                "OCR Output",
                extracted_text,
                height=250
            )

            # ==========================
            # AI ANALYSIS
            # ==========================

            with st.spinner(
                "🤖 AI analyzing document..."
            ):

                summary = generate_summary(
                    extracted_text
                )

                category = classify_document(
                    extracted_text
                )

                metadata = extract_metadata(
                    extracted_text
                )

                priority = detect_priority(
                    extracted_text
                )

                department = assign_department(
                    extracted_text
                )

            # Save results for chatbot

            st.session_state.summary = summary
            st.session_state.category = category
            st.session_state.priority = priority
            st.session_state.department = department
            st.session_state.metadata = metadata