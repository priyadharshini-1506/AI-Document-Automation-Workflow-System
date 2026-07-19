
import os
import uuid
from database.database import get_connection
 
UPLOAD_FOLDER = "uploads"
 
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
 
 
def save_uploaded_file(uploaded_file, username):
 
    # Generate a unique filename to avoid overwriting
    # files when two uploads share the same original name
    unique_name = f"{uuid.uuid4().hex}_{uploaded_file.name}"
 
    filepath = os.path.join(
        UPLOAD_FOLDER,
        unique_name
    )
 
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
 
    conn = get_connection()
    cur = conn.cursor()
 
    cur.execute("""
    INSERT INTO documents
    (
        username,
        filename,
        filetype,
        filepath
    )
    VALUES(?,?,?,?)
    """,
    (
        username,
        uploaded_file.name,
        uploaded_file.type,
        filepath
    ))
 
    conn.commit()
    conn.close()
 
    return filepath