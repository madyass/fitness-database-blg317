from app.db import get_db_connection

def create_user(username, password, role='member'):
    """Yeni kullanıcı oluşturur (Register)"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # RAW SQL KULLANIMI
    # Güvenlik için %s kullanarak parametreli sorgu atıyoruz (SQL Injection önlemi)
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
    """Login kontrolü için kullanıcıyı çeker"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    query = "SELECT id, username, password, role FROM users WHERE username = %s;"
    
    cur.execute(query, (username,))
    user = cur.fetchone() # (id, username, password, role) döner ya da None
    
    cur.close()
    conn.close()
    
    if user:
        # Tuple'ı dictionary'e çevirip dönelim, kullanımı kolay olsun
        return {"id": user[0], "username": user[1], "password": user[2], "role": user[3]}
    return None