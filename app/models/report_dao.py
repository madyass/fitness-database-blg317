from app.db import get_db_connection

def get_inactive_members_report():
    """
    Complex Query Örneği:
    Son 30 gündür 'Attendance' tablosunda kaydı olmayan
    ama üyeliği 'Active' olan kullanıcıları ve planlarını getirir.
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
        -- NESTED QUERY (Alt Sorgu)
        -- Son 30 gündür derse gelenlerin ID'leri
        SELECT DISTINCT member_id 
        FROM attendance 
        WHERE attendance_date > CURRENT_DATE - INTERVAL '30 days'
    );
    """
    
    cur.execute(query)
    results = cur.fetchall()
    
    cur.close()
    conn.close()
    
    # Veriyi JSON formatına uygun hale getirelim
    data = []
    for row in results:
        data.append({
            "first_name": row[0],
            "last_name": row[1],
            "email": row[2],
            "plan_name": row[3]
        })
    return data