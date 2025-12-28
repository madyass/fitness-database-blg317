from app.db import get_db_connection as get_db

def get_all_instructors():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM instructors")
    return cur.fetchall()

def create_instructor(first_name, last_name, specialization):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO instructors (first_name, last_name, specialization)
        VALUES (%s, %s, %s) RETURNING instructor_id
    """, (first_name, last_name, specialization))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return new_id
