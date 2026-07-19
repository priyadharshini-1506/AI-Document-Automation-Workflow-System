
import streamlit as st
import os
 
from database.auth import register, login
from database.document_repository import (
    update_ai_results,
    get_user_documents,
    delete_document,
    update_document_location
)
 
from upload.upload import save_uploaded_file
from upload.organizer import organize_file
from upload.validator import allowed_file
 
from ocr.extractor import extract_text
 
from ai.summarizer import generate_summary
from ai.classifier import classify_document
from ai.metadata import extract_metadata
from ai.priority import detect_priority
from ai.department import assign_department
 
# Workflow modules
from workflow.logger import add_log
from workflow.workflow import recommend_workflow
from workflow.reminder import create_reminder
from workflow.email_sender import send_email
 
from reports.pdf_report import generate_pdf_report
from ai.chatbot import chatbot
 
 
 
# ==========================================
# PAGE CONFIG
# ==========================================
 
st.set_page_config(
    page_title="AI Document Automation",
    page_icon="📄",
    layout="wide"
)
 
 
 
# ==========================================
# SESSION
# ==========================================
 
if "login" not in st.session_state:
    st.session_state.login = False
 
if "user" not in st.session_state:
    st.session_state.user = ""
 
if "processed_file" not in st.session_state:
    st.session_state.processed_file = None
 
if "chat_open" not in st.session_state:
    st.session_state.chat_open = False
 
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
 
 
 
# ==========================================
# FLOATING CHAT WIDGET (bottom-right corner)
# ==========================================
# Uses a CSS "anchor + adjacent sibling" trick: the empty div
# with id="floating-chat-anchor" is rendered right before the
# container below in the page's HTML. The CSS rule targets the
# very next element after that anchor and pins it to the corner
# of the screen, regardless of where it sits in the normal page
# flow.
 
def render_chat_bubble(role, text):
 
    if role == "user":
 
        st.markdown(
            f"""
            <div class="chat-row chat-row-user">
                <div class="chat-bubble chat-bubble-user">{text}</div>
                <div class="chat-avatar chat-avatar-user">🙂</div>
            </div>
            """,
            unsafe_allow_html=True
        )
 
    else:
 
        st.markdown(
            f"""
            <div class="chat-row chat-row-bot">
                <div class="chat-avatar chat-avatar-bot">🤖</div>
                <div class="chat-bubble chat-bubble-bot">{text}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
 
 
def render_floating_chat():
 
    st.markdown(
        '<div id="floating-chat-anchor"></div>',
        unsafe_allow_html=True
    )
 
    with st.container():
 
        if not st.session_state.chat_open:
 
            if st.button("💬 Chatbot", key="chat_toggle_open"):
                st.session_state.chat_open = True
                st.rerun()
 
        else:
 
            st.markdown(
                """
                <div class="chat-header">
                    <div class="chat-header-avatar">🤖</div>
                    <div class="chat-header-text">
                        <div class="chat-header-title">Document AI Assistant</div>
                        <div class="chat-header-status">● Online</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
 
            if st.button("✖", key="chat_toggle_close"):
                st.session_state.chat_open = False
                st.rerun()
 
            if not st.session_state.processed_file:
 
                st.info("Upload and process a document first.")
 
            else:
 
                chat_box = st.container(height=280)
 
                with chat_box:
 
                    if not st.session_state.chat_history:
 
                        render_chat_bubble(
                            "bot",
                            "Hi! Ask me anything about your uploaded document."
                        )
 
                    for q, a in st.session_state.chat_history:
 
                        render_chat_bubble("user", q)
                        render_chat_bubble("bot", a)
 
                input_col, send_col = st.columns([5, 1])
 
                with input_col:
 
                    question = st.text_input(
                        "Ask about your document",
                        key="chat_input_box",
                        label_visibility="collapsed",
                        placeholder="Type your question..."
                    )
 
                with send_col:
 
                    send_clicked = st.button("➤", key="chat_send_btn")
 
                if send_clicked:
 
                    if question.strip():
 
                        with st.spinner("Thinking..."):
 
                            answer = chatbot(
                                st.session_state.extracted_text,
                                question
                            )
 
                        st.session_state.chat_history.append(
                            (question, answer)
                        )
 
                        st.rerun()
 
                    else:
 
                        st.warning("Enter a question.")
 
    st.markdown(
        """
        <style>
        #floating-chat-anchor + div {
            position: fixed;
            bottom: 24px;
            right: 24px;
            z-index: 9999;
            background: #ffffff;
            border-radius: 16px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.25);
            padding: 0;
            width: 350px;
            overflow: hidden;
            border: 1px solid #e5e7eb;
        }
 
        /* Collapsed floating icon+label button (WhatsApp-style pill) */
        #floating-chat-anchor + div button[kind="secondary"] {
            border-radius: 24px;
            padding: 10px 18px;
            font-size: 15px;
            font-weight: 600;
            background: #25D366;
            color: white;
            border: none;
            box-shadow: 0 4px 14px rgba(37,211,102,0.5);
        }
 
        /* Header bar */
        .chat-header {
            display: flex;
            align-items: center;
            gap: 10px;
            background: #075E54;
            padding: 14px 16px;
            margin: -1px -1px 0 -1px;
        }
 
        .chat-header-avatar {
            font-size: 26px;
            background: rgba(255,255,255,0.2);
            border-radius: 50%;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
 
        .chat-header-title {
            color: white;
            font-weight: 600;
            font-size: 15px;
        }
 
        .chat-header-status {
            color: #b6f2c9;
            font-size: 12px;
        }
 
        /* Chat area background - WhatsApp's light green/beige pattern feel */
        #floating-chat-anchor + div div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #e5ddd5;
        }
 
        /* Chat bubbles */
        .chat-row {
            display: flex;
            align-items: flex-end;
            gap: 8px;
            margin: 6px 0;
        }
 
        .chat-row-user {
            justify-content: flex-end;
        }
 
        .chat-row-bot {
            justify-content: flex-start;
        }
 
        .chat-avatar {
            font-size: 14px;
            width: 22px;
            height: 22px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }
 
        .chat-avatar-user {
            background: #25D366;
        }
 
        .chat-avatar-bot {
            background: #ffffff;
            border: 1px solid #d1d7db;
        }
 
        .chat-bubble {
            max-width: 75%;
            padding: 6px 10px;
            border-radius: 8px;
            font-size: 13px;
            line-height: 1.4;
            word-wrap: break-word;
            box-shadow: 0 1px 1px rgba(0,0,0,0.1);
        }
 
        .chat-bubble-user {
            background: #DCF8C6;
            color: #111b21;
            border-top-right-radius: 0;
        }
 
        .chat-bubble-bot {
            background: #ffffff;
            color: #111b21;
            border-top-left-radius: 0;
        }
 
        /* Send button */
        #floating-chat-anchor + div .stButton button {
            border-radius: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
 
 
 
# ==========================================
# MY DOCUMENTS PAGE
# ==========================================
 
DEPARTMENT_OPTIONS = [
    "HR",
    "Finance",
    "Legal",
    "Administration",
    "Technical",
    "Medical",
    "Other"
]
 
 
def render_my_documents():
 
    st.title("📁 My Documents")
 
    docs = get_user_documents(st.session_state.user)
 
    if len(docs) == 0:
 
        st.info("You haven't uploaded any documents yet.")
 
        return
 
    # ==========================
    # SEARCH
    # ==========================
 
    search = st.text_input("🔍 Search by filename, category, or department")
 
    filtered_docs = []
 
    for doc in docs:
 
        haystack = " ".join([
            str(doc["filename"] or ""),
            str(doc["category"] or ""),
            str(doc["department"] or ""),
            str(doc["priority"] or "")
        ]).lower()
 
        if not search or search.lower() in haystack:
 
            filtered_docs.append(doc)
 
    st.caption(f"{len(filtered_docs)} document(s) found")
 
    st.divider()
 
    # ==========================
    # DOCUMENT LIST
    # ==========================
 
    for doc in filtered_docs:
 
        with st.expander(f"📄 {doc['filename']}  —  {doc['category'] or 'Uncategorized'}"):
 
            col1, col2 = st.columns(2)
 
            with col1:
 
                st.write(f"**Department:** {doc['department'] or 'Not set'}")
                st.write(f"**Priority:** {doc['priority'] or 'Not set'}")
                st.write(f"**Uploaded:** {doc['upload_date']}")
 
            with col2:
 
                st.write(f"**Category:** {doc['category'] or 'Not set'}")
                st.write(f"**File type:** {doc['filetype']}")
 
            if doc["summary"]:
 
                st.write("**Summary:**")
                st.write(doc["summary"])
 
            st.divider()
 
            # ==========================
            # DOWNLOAD
            # ==========================
 
            if doc["filepath"] and os.path.exists(doc["filepath"]):
 
                with open(doc["filepath"], "rb") as f:
 
                    st.download_button(
                        "⬇ Download File",
                        f,
                        file_name=doc["filename"],
                        key=f"download_{doc['id']}"
                    )
 
            else:
 
                st.warning("File not found on disk.")
 
            # ==========================
            # RE-ORGANIZE (move to different department folder)
            # ==========================
 
            move_col, move_btn_col = st.columns([3, 1])
 
            with move_col:
 
                current_dept = doc["department"] if doc["department"] in DEPARTMENT_OPTIONS else "Other"
 
                new_department = st.selectbox(
                    "Move to department",
                    DEPARTMENT_OPTIONS,
                    index=DEPARTMENT_OPTIONS.index(current_dept),
                    key=f"dept_select_{doc['id']}"
                )
 
            with move_btn_col:
 
                st.write("")
                st.write("")
 
                if st.button("📂 Move", key=f"move_{doc['id']}"):
 
                    if new_department == doc["department"]:
 
                        st.info("Already in this department.")
 
                    elif not doc["filepath"] or not os.path.exists(doc["filepath"]):
 
                        st.error("Cannot move - file not found on disk.")
 
                    else:
 
                        new_path = organize_file(doc["filepath"], new_department)
 
                        update_document_location(
                            doc["id"],
                            new_department,
                            new_path
                        )
 
                        st.success(f"Moved to {new_department}")
 
                        st.rerun()
 
            # ==========================
            # DELETE
            # ==========================
 
            if st.button("🗑 Delete Document", key=f"delete_{doc['id']}"):
 
                if doc["filepath"] and os.path.exists(doc["filepath"]):
 
                    try:
                        os.remove(doc["filepath"])
                    except Exception:
                        pass
 
                delete_document(doc["id"])
 
                st.success("Document deleted.")
 
                st.rerun()
 
 
 
# ==========================================
# AFTER LOGIN
# ==========================================
 
if st.session_state.login:
 
 
    page = st.sidebar.radio(
        "Navigate",
        ["📤 Upload Document", "📁 My Documents"]
    )
 
    st.sidebar.success(
        f"Welcome {st.session_state.user}"
    )
 
    if page == "📁 My Documents":
 
        render_my_documents()
 
        render_floating_chat()
 
        st.sidebar.divider()
 
        if st.sidebar.button("Logout"):
 
            st.session_state.clear()
 
            st.rerun()
 
        st.stop()
 
 
    st.title(
        "📄 AI-Powered Intelligent Document Automation and Workflow Management System"
    )
 
 
    uploaded_file = st.file_uploader(
 
        "Upload Document",
 
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
 
 
            if st.session_state.processed_file != uploaded_file.name:
 
 
 
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
 
 
 
                # ==========================
                # OCR EXTRACTION
                # ==========================
 
                with st.spinner(
                    "📄 Extracting text..."
                ):
 
 
                    extracted_text = extract_text(filepath)
 
 
 
 
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
 
 
                # Guard against None/empty priority (e.g. if the AI call failed)
                # so nothing downstream crashes on priority.lower()
                if not priority:
                    priority = "Low"
 
 
                # ==========================
                # ORGANIZE FILE
                # ==========================
 
                organized_path = organize_file(
 
                    filepath,
 
                    department
 
                )
 
 
 
 
                # ==========================
                # DATABASE SAVE
                # ==========================
 
                # NOTE: must pass the ORIGINAL filepath (before the move)
                # as old_filepath so the WHERE clause can find the row,
                # and organized_path as new_filepath so the DB is updated
                # to match the file's actual location on disk.
                update_ai_results(
 
                    filepath,
 
                    organized_path,
 
                    summary,
 
                    category,
 
                    priority,
 
                    department,
 
                    metadata
 
                )
 
 
 
 
                # ==========================
                # WORKFLOW
                # ==========================
 
                add_log(
 
                    st.session_state.user,
 
                    uploaded_file.name,
 
                    "Document uploaded, analyzed and organized"
 
                )
 
 
 
                workflow = recommend_workflow(
 
                    priority,
 
                    department
 
                )
 
 
 
                reminder = create_reminder(
 
                    priority
 
                )
 
 
                # ==========================
                # PDF REPORT GENERATION
                # ==========================
                pdf_path = generate_pdf_report(
 
                    st.session_state.user,
 
                    uploaded_file.name,
 
                    category,
 
                    summary,
 
                    metadata,
 
                    priority,
 
                    department,
 
                    workflow,
 
                    reminder
 
                )
 
 
 
 
                # ==========================
                # EMAIL NOTIFICATION
                # ==========================
 
                priority_text = priority.lower()
 
                email_status = ""
 
                # Send email for HIGH and MEDIUM priority
                if "high" in priority_text or "medium" in priority_text:
 
                    subject = f"{priority} Priority Document Notification"
 
                    message = f"""
Hello,
 
A new document has been processed by the AI-Powered Intelligent Document Automation System.
 
----------------------------------------
Document Name : {uploaded_file.name}
Category      : {category}
Department    : {department}
Priority      : {priority}
----------------------------------------
 
AI Summary:
 
{summary}
 
Please review the document as soon as possible.
 
Regards,
AI Document Automation System
"""
 
                    # TODO: replace with a real recipient address (or read
                    # one from config/.env) before this goes live - emails
                    # will silently fail to reach anyone until this is set.
                    email_sent = send_email(
                        "YOUR_EMAIL@gmail.com",   # Replace with your Gmail
                        subject,
                        message
                    )
 
                    if email_sent:
                        email_status = "📧 Email Notification Sent Successfully"
                    else:
                        email_status = "❌ Email Notification Failed"
 
                else:
 
                    email_status = "ℹ️ Low Priority Document - Email Not Required"
 
 
                # ==========================
                # PERSIST EVERYTHING TO SESSION STATE
                # ==========================
                # Results are stored here so they survive Streamlit
                # reruns (e.g. clicking the chat button below triggers
                # a full script rerun - without this, all of the
                # analysis results and chat history would vanish).
 
                st.session_state.processed_file = uploaded_file.name
                st.session_state.extracted_text = extracted_text
                st.session_state.summary = summary
                st.session_state.category = category
                st.session_state.priority = priority
                st.session_state.priority_text = priority_text
                st.session_state.department = department
                st.session_state.metadata = metadata
                st.session_state.workflow = workflow
                st.session_state.reminder = reminder
                st.session_state.organized_path = organized_path
                st.session_state.pdf_path = pdf_path
                st.session_state.email_status = email_status
                st.session_state.uploaded_file_name = uploaded_file.name
 
                # Fresh document -> fresh chat history
                st.session_state.chat_history = []
 
 
            else:
 
                st.info(
                    "Document already processed"
                )
 
 
        else:
 
            st.error(
                "❌ Unsupported File Type"
            )
 
 
    # ==========================================
    # RESULT DISPLAY (runs on every rerun as long
    # as a document has been processed)
    # ==========================================
 
    if st.session_state.processed_file:
 
        st.subheader(
            "📄 Extracted Text"
        )
 
        st.text_area(
 
            "OCR Output",
 
            st.session_state.extracted_text,
 
            height=250
 
        )
 
        st.subheader(
            "📂 Organized File Location"
        )
 
        st.code(
            st.session_state.organized_path
        )
 
        if st.session_state.email_status:
 
            if "Sent" in st.session_state.email_status:
                st.success(st.session_state.email_status)
            elif "Failed" in st.session_state.email_status:
                st.error(st.session_state.email_status)
            else:
                st.info(st.session_state.email_status)
 
        st.success(
            "✅ AI Analysis Completed Successfully"
        )
 
        st.divider()
 
 
        col1, col2 = st.columns(2)
 
 
        with col1:
 
            st.subheader(
                "📑 AI Summary"
            )
 
            st.write(st.session_state.summary)
 
            st.subheader(
                "📂 Document Category"
            )
 
            st.success(st.session_state.category)
 
            st.subheader(
                "⚠ Priority"
            )
 
            if st.session_state.priority_text == "high":
 
                st.error(st.session_state.priority)
 
            elif st.session_state.priority_text == "medium":
 
                st.warning(st.session_state.priority)
 
            else:
 
                st.success(st.session_state.priority)
 
 
        with col2:
 
            st.subheader(
                "🏢 Department"
            )
 
            st.info(st.session_state.department)
 
            st.subheader(
                "📝 Metadata"
            )
 
            st.text(st.session_state.metadata)
 
 
        # ==========================
        # WORKFLOW DISPLAY
        # ==========================
 
        st.divider()
 
        st.subheader(
            "⚙️ Recommended Workflow"
        )
 
        st.write(st.session_state.workflow)
 
        st.subheader(
            "⏰ Reminder"
        )
 
        st.info(st.session_state.reminder)
 
        st.divider()
 
        st.subheader("📄 AI Report")
 
        st.success("PDF Report Generated Successfully")
 
        with open(st.session_state.pdf_path, "rb") as pdf_file:
 
            st.download_button(
 
                label="📥 Download PDF Report",
 
                data=pdf_file,
 
                file_name=f"{st.session_state.uploaded_file_name}_Report.pdf",
 
                mime="application/pdf"
 
            )
 
 
    # ==========================
    # FLOATING CHAT WIDGET
    # ==========================
 
    render_floating_chat()
 
 
    st.sidebar.divider()
 
 
    if st.sidebar.button("Logout"):
 
        st.session_state.clear()
 
        st.rerun()
 
 
    st.stop()
 
 
 
 
 
# ==========================================
# LOGIN / REGISTER
# ==========================================
 
st.title(
    "📄 AI-Powered Intelligent Document Automation and Workflow Management System"
)
 
 
 
menu = st.sidebar.radio(
 
    "Select",
 
    [
        "Login",
        "Register"
    ]
 
)
 
 
 
 
# ==========================================
# REGISTER
# ==========================================
 
if menu == "Register":
 
 
    st.subheader(
        "Create Account"
    )
 
 
    username = st.text_input(
        "Username"
    )
 
 
    password = st.text_input(
 
        "Password",
 
        type="password"
 
    )
 
 
 
    if st.button("Register"):
 
 
        if register(username,password):
 
            st.success(
                "✅ Registration Successful"
            )
 
 
        else:
 
            st.error(
                "❌ Username Already Exists"
            )
 
 
 
 
# ==========================================
# LOGIN
# ==========================================
 
else:
 
 
    st.subheader(
        "Login"
    )
 
 
    username = st.text_input(
        "Username"
    )
 
 
    password = st.text_input(
 
        "Password",
 
        type="password"
 
    )
 
 
 
    if st.button("Login"):
 
 
        if login(username,password):
 
 
            st.session_state.login = True
 
            st.session_state.user = username
 
 
            st.success(
                "✅ Login Successful"
            )
 
 
            st.rerun()
 
 
 
        else:
 
 
            st.error(
                "❌ Invalid Username or Password"
            )