from app.db import get_db_connection as get_db

def get_all_classes():
    conn = get_db()
    cur = conn.cursor()
    # Join with Instructors table to get instructor name
    query = """
        SELECT gc.class_id, gc.class_name, gc.start_time, gc.capacity,
               i.first_name || ' ' || i.last_name as instructor_name,
               r.room_name
        FROM group_classes gc
        JOIN instructors i ON gc.instructor_id = i.instructor_id
        JOIN rooms r ON gc.room_id = r.room_id
    """
    cur.execute(query)
    return cur.fetchall()

def create_group_class(class_name, instructor_id, room_id, start_time, capacity=20):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO group_classes (class_name, instructor_id, room_id, start_time, capacity)
        VALUES (%s, %s, %s, %s, %s) RETURNING class_id
    """, (class_name, instructor_id, room_id, start_time, capacity))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return new_id
