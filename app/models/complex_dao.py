from app.db import get_db_connection

def get_popular_classes():
    """
    Returns classes ordered by enrollment count.
    Complex Query: Joins group_classes with class_enrollments, aggregates count.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    query = """
    SELECT 
        gc.class_name,
        COUNT(ce.member_id) as enrollment_count,
        gc.capacity
    FROM group_classes gc
    LEFT JOIN class_enrollments ce ON gc.class_id = ce.class_id
    GROUP BY gc.class_id, gc.class_name, gc.capacity
    ORDER BY enrollment_count DESC;
    """
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    conn.close()
    
    return [
        {"class_name": row[0], "enrollment_count": row[1], "capacity": row[2]} 
        for row in results
    ]

def get_peak_hours():
    """
    Returns busy hours based on class start times and attendance.
    Complex Query: Extracts hour from start_time, counts attendees.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    query = """
    SELECT 
        EXTRACT(HOUR FROM gc.start_time) as hour_of_day,
        COUNT(a.attendance_id) as total_attendance
    FROM group_classes gc
    JOIN attendance a ON gc.class_id = a.class_id
    WHERE a.status = 'Present'
    GROUP BY hour_of_day
    ORDER BY total_attendance DESC;
    """
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    conn.close()
    
    return [
        {"hour": int(row[0]), "attendance_count": row[1]} 
        for row in results
    ]

def get_revenue_by_plan():
    """
    Calculates total revenue generated, grouped by membership plan.
    Complex Query: Joins payments -> members -> membership_plans.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    query = """
    SELECT 
        mp.plan_name,
        SUM(p.amount) as total_revenue
    FROM payments p
    JOIN members m ON p.member_id = m.member_id
    JOIN membership_plans mp ON m.plan_id = mp.plan_id
    WHERE p.status = 'Paid'
    GROUP BY mp.plan_id, mp.plan_name
    ORDER BY total_revenue DESC;
    """
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    conn.close()
    
    return [
        {"plan_name": row[0], "total_revenue": float(row[1]) if row[1] else 0.0} 
        for row in results
    ]

def get_instructor_performance():
    """
    Combines group class student count and private session count for each instructor.
    Complex Query: CTEs or Subqueries to aggregate both sources.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    query = """
    WITH ClassStats AS (
        SELECT 
            i.instructor_id, 
            COUNT(DISTINCT ce.member_id) as class_students
        FROM instructors i
        LEFT JOIN group_classes gc ON i.instructor_id = gc.instructor_id
        LEFT JOIN class_enrollments ce ON gc.class_id = ce.class_id
        GROUP BY i.instructor_id
    ),
    PrivateStats AS (
        SELECT 
            i.instructor_id, 
            COUNT(ps.session_id) as private_sessions_count
        FROM instructors i
        LEFT JOIN private_sessions ps ON i.instructor_id = ps.instructor_id
        WHERE ps.status = 'Completed' OR ps.status = 'Scheduled'
        GROUP BY i.instructor_id
    )
    SELECT 
        i.first_name || ' ' || i.last_name as instructor_name,
        COALESCE(cs.class_students, 0) as total_class_students,
        COALESCE(ps.private_sessions_count, 0) as total_private_sessions
    FROM instructors i
    LEFT JOIN ClassStats cs ON i.instructor_id = cs.instructor_id
    LEFT JOIN PrivateStats ps ON i.instructor_id = ps.instructor_id;
    """
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    conn.close()
    
    return [
        {
            "instructor_name": row[0], 
            "total_class_students": row[1], 
            "total_private_sessions": row[2]
        } 
        for row in results
    ]

def get_maintenance_costs():
    """
    Total maintenance cost per equipment category.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    query = """
    SELECT 
        e.category,
        SUM(em.cost) as total_cost
    FROM equipment e
    JOIN equipment_maintenance em ON e.equipment_id = em.equipment_id
    GROUP BY e.category
    ORDER BY total_cost DESC;
    """
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    conn.close()
    
    return [
        {"category": row[0], "total_cost": float(row[1]) if row[1] else 0.0} 
        for row in results
    ]
