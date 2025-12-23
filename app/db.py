import psycopg2
from config import Config

def get_db_connection():
    """
    Veritabanına yeni bir bağlantı açar ve döndürür.
    Raw SQL sorguları için bu connection üzerinden cursor oluşturulacak.
    """
    conn = psycopg2.connect(
        host=Config.DB_HOST,
        database=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASS
    )
    return conn