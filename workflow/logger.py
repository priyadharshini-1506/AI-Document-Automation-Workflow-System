from datetime import datetime
from database.database import get_connection
 
 
def create_log_table():
 
    conn = get_connection()
 
    cur = conn.cursor()
 
    cur.execute("""
    CREATE TABLE IF NOT EXISTS activity_log(
 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
 
        username TEXT,
 
        filename TEXT,
 
        action TEXT,
 
        time TIMESTAMP
 
    )
    """)
 
    conn.commit()
 
    conn.close()
 
 
def add_log(
    username,
    filename,
    action
):
 
    conn = get_connection()
 
    cur = conn.cursor()
 
    cur.execute("""
    INSERT INTO activity_log
    (
        username,
        filename,
        action,
        time
    )
 
    VALUES(?,?,?,?)
 
    """,
    (
        username,
        filename,
        action,
        datetime.now()
    ))
 
    conn.commit()
 
    conn.close()
 
 
# Ensure table exists on import
create_log_table()