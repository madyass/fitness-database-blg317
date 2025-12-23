from app.db import get_db_connection

def create_member(first_name, last_name, email, plan_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    query = """
    INSERT INTO members (first_name, last_name, email, plan_id, join_date)
    VALUES (%s, %s, %s, %s, CURRENT_DATE)
    RETURNING member_id;
    """
    
    cur.execute(query, (first_name, last_name, email, plan_id))
    new_id = cur.fetchone()[0]
    
    conn.commit()
    cur.close()
    conn.close()
    return new_id

def get_all_members():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT member_id, first_name, last_name, email, status FROM members ORDER BY member_id DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    # List of Dicts döndürelim
    members = []
    for row in rows:
        members.append({
            "id": row[0], "first_name": row[1], "last_name": row[2], 
            "email": row[3], "status": row[4]
        })
    return members

def update_member(member_id, phone, address):
    conn = get_db_connection()
    cur = conn.cursor()
    query = "UPDATE members SET phone = %s, address = %s WHERE member_id = %s"
    cur.execute(query, (phone, address, member_id))
    conn.commit()
    cur.close()
    conn.close()

def delete_member(member_id):
    conn = get_db_connection()
    cur = conn.cursor()
    query = "DELETE FROM members WHERE member_id = %s"
    cur.execute(query, (member_id,))
    conn.commit()
    cur.close()
    conn.close()