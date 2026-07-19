import bcrypt
from database.database import get_connection


def hash_password(password):
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )


def register(username, password):

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users(username,password) VALUES(?,?)",
            (
                username,
                hash_password(password)
            )
        )

        conn.commit()
        return True

    except:
        return False


def login(username, password):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    )

    user = cur.fetchone()

    if user:

        if bcrypt.checkpw(
                password.encode(),
                user["password"]
        ):
            return True

    return False