import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = "database/document_system.db"


def get_connection():

    return sqlite3.connect(DB_PATH)


def admin_panel():

    st.set_page_config(
        page_title="Admin Panel",
        page_icon="👨‍💼",
        layout="wide"
    )

    st.title("👨‍💼 Admin Panel")

    conn = get_connection()

    # ==========================
    # USERS
    # ==========================

    users = pd.read_sql(
        "SELECT * FROM users",
        conn
    )

    st.subheader("👥 Registered Users")

    st.dataframe(
        users,
        use_container_width=True
    )

    st.divider()

    # ==========================
    # DOCUMENTS
    # ==========================

    docs = pd.read_sql(
        "SELECT * FROM documents ORDER BY upload_date DESC",
        conn
    )

    st.subheader("📄 Uploaded Documents")

    st.dataframe(
        docs,
        use_container_width=True
    )

    st.divider()

    # ==========================
    # DELETE DOCUMENT
    # ==========================

    if len(docs) > 0:

        document_id = st.selectbox(
            "Select Document ID",
            docs["id"]
        )

        if st.button("🗑 Delete Document"):

            cur = conn.cursor()

            cur.execute(
                "DELETE FROM documents WHERE id=?",
                (int(document_id),)
            )

            conn.commit()

            st.success(
                "Document Deleted Successfully"
            )

            st.rerun()

    st.divider()

    # ==========================
    # SYSTEM STATS
    # ==========================

    st.subheader("📊 System Statistics")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Total Users",
            len(users)
        )

        st.metric(
            "Total Documents",
            len(docs)
        )

    with col2:

        high = len(
            docs[
                docs["priority"].fillna("").str.lower() == "high"
            ]
        )

        medium = len(
            docs[
                docs["priority"].fillna("").str.lower() == "medium"
            ]
        )

        low = len(
            docs[
                docs["priority"].fillna("").str.lower() == "low"
            ]
        )

        st.metric(
            "High Priority",
            high
        )

        st.metric(
            "Medium Priority",
            medium
        )

        st.metric(
            "Low Priority",
            low
        )

    conn.close()


if __name__ == "__main__":

    admin_panel()