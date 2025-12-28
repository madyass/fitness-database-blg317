from app.db import get_db_connection

def create_user(username, password, role='member'):
    """Creates a new user (Register)"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # USING RAW SQL
    # Using parameterized queries with %s for security (SQL Injection prevention)
    query = """
    INSERT INTO users (username, password, role)
    VALUES (%s, %s, %s)
    RETURNING id;
    """
    
    try:
        cur.execute(query, (username, password, role))
        user_id = cur.fetchone()[0]
        conn.commit()
        return user_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

def get_user_by_username(username):
    """Fetches user for login check"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    query = "SELECT id, username, password, role FROM users WHERE username = %s;"
    
    cur.execute(query, (username,))
    user = cur.fetchone() # Returns (id, username, password, role) or None
    
    cur.close()
    conn.close()
    
    if user:
        # Convert Tuple to dictionary for easier usage
        return {"id": user[0], "username": user[1], "password": user[2], "role": user[3]}
    return None