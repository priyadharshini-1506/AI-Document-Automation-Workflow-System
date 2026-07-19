from database.database import get_connection
 
 
def update_ai_results(
    old_filepath,
    new_filepath,
    summary,
    category,
    priority,
    department,
    metadata
):
    conn = get_connection()
    cur = conn.cursor()
 
    cur.execute("""
        UPDATE documents
        SET
            filepath = ?,
            summary = ?,
            category = ?,
            priority = ?,
            department = ?,
            metadata = ?
        WHERE filepath = ?
    """, (
        new_filepath,
        summary,
        category,
        priority,
        department,
        metadata,
        old_filepath
    ))
 
    conn.commit()
    conn.close()
 
 
def get_user_documents(username):
 
    conn = get_connection()
    cur = conn.cursor()
 
    cur.execute(
        "SELECT * FROM documents WHERE username=? ORDER BY upload_date DESC",
        (username,)
    )
 
    rows = cur.fetchall()
 
    conn.close()
 
    return rows
 
 
def get_document_by_id(document_id):
 
    conn = get_connection()
    cur = conn.cursor()
 
    cur.execute(
        "SELECT * FROM documents WHERE id=?",
        (document_id,)
    )
 
    row = cur.fetchone()
 
    conn.close()
 
    return row
 
 
def delete_document(document_id):
 
    conn = get_connection()
    cur = conn.cursor()
 
    cur.execute(
        "DELETE FROM documents WHERE id=?",
        (document_id,)
    )
 
    conn.commit()
    conn.close()
 
 
def update_document_location(document_id, new_department, new_filepath):
 
    conn = get_connection()
    cur = conn.cursor()
 
    cur.execute("""
        UPDATE documents
        SET
            department = ?,
            filepath = ?
        WHERE id = ?
    """, (
        new_department,
        new_filepath,
        document_id
    ))
 
    conn.commit()
    conn.close()