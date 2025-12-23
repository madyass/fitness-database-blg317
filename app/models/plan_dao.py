from app.db import get_db_connection

def create_plan(plan_name, monthly_fee, duration_months):
    conn = get_db_connection()
    cur = conn.cursor()
    query = """
    INSERT INTO membership_plans (plan_name, monthly_fee, duration_months)
    VALUES (%s, %s, %s)
    RETURNING plan_id;
    """
    cur.execute(query, (plan_name, monthly_fee, duration_months))
    plan_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return plan_id

def get_all_plans():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT plan_id, plan_name, monthly_fee FROM membership_plans")
    rows = cur.fetchall()
    conn.close()
    
    plans = []
    for row in rows:
        plans.append({"id": row[0], "name": row[1], "price": row[2]})
    return plans