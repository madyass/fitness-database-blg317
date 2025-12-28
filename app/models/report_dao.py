from app.db import get_db_connection

def get_inactive_members_report():
    """
    Complex Query Example:
    Returns active members who have not attended any class in the last 30 days,
    along with their membership plans.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    # RAW SQL (Nested Query + JOIN)
    query = """
    SELECT 
        m.first_name, 
        m.last_name, 
        m.email, 
        p.plan_name
    FROM members m
    JOIN membership_plans p ON m.plan_id = p.plan_id
    WHERE m.status = 'Active' 
    AND m.member_id NOT IN (
        -- NESTED QUERY (Subquery)
        -- IDs of members who attended class in the last 30 days
        SELECT DISTINCT member_id 
        FROM attendance 
        WHERE attendance_date > CURRENT_DATE - INTERVAL '30 days'
    );
    """
    
    cur.execute(query)
    results = cur.fetchall()
    
    cur.close()
    conn.close()
    
    
    # Format data for JSON response
    data = []
    for row in results:
        data.append({
            "first_name": row[0],
            "last_name": row[1],
            "email": row[2],
            "plan_name": row[3]
        })
    return data

def get_coach_retention_report():
    """
    Analyzes instructor student retention rates.
    Calculates the average membership duration of students taking classes from each instructor.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    query = """
    SELECT 
        i.first_name || ' ' || i.last_name as instructor_name,
        AVG(CURRENT_DATE - m.join_date) as avg_membership_days,
        COUNT(DISTINCT m.member_id) as student_count
    FROM instructors i
    JOIN group_classes gc ON i.instructor_id = gc.instructor_id
    JOIN class_enrollments ce ON gc.class_id = ce.class_id
    JOIN members m ON ce.member_id = m.member_id
    WHERE m.status = 'Active'
    GROUP BY i.instructor_id, i.first_name, i.last_name
    ORDER BY avg_membership_days DESC;
    """
    
    cur.execute(query)
    results = cur.fetchall()
    
    cur.close()
    conn.close()
    
    data = []
    for row in results:
        data.append({
            "instructor_name": row[0],
            "avg_membership_days": round(row[1], 1) if row[1] else 0,
            "student_count": row[2]
        })
    return data