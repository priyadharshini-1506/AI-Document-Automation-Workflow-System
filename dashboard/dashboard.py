
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
 
DB_PATH = "database/document_system.db"
 
 
# ==========================
# LOAD DATA
# ==========================
 
def load_data():
 
    conn = sqlite3.connect(DB_PATH)
 
    df = pd.read_sql_query(
        "SELECT * FROM documents ORDER BY upload_date DESC",
        conn
    )
 
    conn.close()
 
    return df
 
 
# ==========================
# DASHBOARD
# ==========================
 
def dashboard():
 
    st.set_page_config(
        page_title="Dashboard",
        page_icon="📊",
        layout="wide"
    )
 
    st.title("📊 AI Document Analytics Dashboard")
 
    df = load_data()
 
    if df.empty:
 
        st.warning("No uploaded documents found.")
 
        return
 
    # ==========================
    # SEARCH
    # ==========================
 
    search = st.text_input(
        "🔍 Search Document"
    )
 
    if search:
 
        df = df[
            df["filename"].str.contains(search, case=False, na=False)
            |
            df["category"].str.contains(search, case=False, na=False)
            |
            df["department"].str.contains(search, case=False, na=False)
            |
            df["username"].str.contains(search, case=False, na=False)
        ]
 
    # ==========================
    # KPI
    # ==========================
 
    total_docs = len(df)
 
    high = len(
        df[df["priority"].fillna("").str.lower() == "high"]
    )
 
    medium = len(
        df[df["priority"].fillna("").str.lower() == "medium"]
    )
 
    low = len(
        df[df["priority"].fillna("").str.lower() == "low"]
    )
 
    c1, c2, c3, c4 = st.columns(4)
 
    c1.metric("📄 Documents", total_docs)
 
    c2.metric("🔴 High", high)
 
    c3.metric("🟠 Medium", medium)
 
    c4.metric("🟢 Low", low)
 
    st.divider()
 
    # ==========================
    # CATEGORY
    # ==========================
 
    st.subheader("📂 Document Categories")
 
    fig = px.histogram(
        df,
        x="category",
        color="category"
    )
 
    st.plotly_chart(
        fig,
        use_container_width=True
    )
 
    # ==========================
    # DEPARTMENT
    # ==========================
 
    st.subheader("🏢 Department Distribution")
 
    fig = px.pie(
        df,
        names="department"
    )
 
    st.plotly_chart(
        fig,
        use_container_width=True
    )
 
    # ==========================
    # PRIORITY
    # ==========================
 
    st.subheader("⚠ Priority Distribution")
 
    priority_df = (
        df["priority"]
        .fillna("Unknown")
        .value_counts()
        .rename_axis("Priority")
        .reset_index(name="Documents")
    )
 
    fig = px.bar(
        priority_df,
        x="Priority",
        y="Documents",
        color="Priority"
    )
 
    st.plotly_chart(
        fig,
        use_container_width=True
    )
 
    # ==========================
    # RECENT DOCUMENTS
    # ==========================
 
    st.subheader("📋 Uploaded Documents")
 
    st.dataframe(
        df,
        use_container_width=True
    )
 
    # ==========================
    # DOWNLOAD
    # ==========================
 
    csv = df.to_csv(index=False)
 
    st.download_button(
        "⬇ Download Dashboard Report",
        csv,
        file_name="dashboard_report.csv",
        mime="text/csv"
    )
 
 
if __name__ == "__main__":
 
    dashboard()