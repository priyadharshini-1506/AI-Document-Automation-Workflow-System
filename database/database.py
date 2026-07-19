import sqlite3
import os


DB_PATH = "database/document_system.db"


# Create database folder
os.makedirs(
    "database",
    exist_ok=True
)



def get_connection():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn



def create_tables():

    conn = get_connection()

    cur = conn.cursor()


    # ==========================
    # USERS TABLE
    # ==========================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL

    )
    """)



    # ==========================
    # DOCUMENTS TABLE
    # ==========================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS documents(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT,

        filename TEXT,

        filetype TEXT,

        filepath TEXT,

        upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        category TEXT,

        summary TEXT,

        priority TEXT,

        department TEXT,

        metadata TEXT

    )
    """)



    conn.commit()

    conn.close()



# ==========================
# ADD MISSING COLUMNS
# ==========================

def add_missing_columns():

    conn = get_connection()

    cur = conn.cursor()


    cur.execute(
        "PRAGMA table_info(documents)"
    )


    columns = [
        row["name"]
        for row in cur.fetchall()
    ]


    required_columns = {

        "category": "TEXT",

        "summary": "TEXT",

        "priority": "TEXT",

        "department": "TEXT",

        "metadata": "TEXT"

    }


    for column, datatype in required_columns.items():

        if column not in columns:

            cur.execute(
                f"""
                ALTER TABLE documents
                ADD COLUMN {column} {datatype}
                """
            )


    conn.commit()

    conn.close()



# Create database tables
create_tables()

# Update old database if needed
add_missing_columns()



