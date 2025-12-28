from app.db import get_db_connection
import os

def reset_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    with open('seed_data.sql', 'r') as f:
        sql = f.read()
        cur.execute(sql)
        print("Database reset successfully.")
        
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    reset_db()
