import os

class Config:
    # Veritabanı bağlantı bilgilerin (Kendi DB bilgilerine göre düzenle!)
    DB_HOST = "localhost"
    DB_NAME = "fitness_db"
    DB_USER = "postgres"
    DB_PASS = "12345" 
    
    # JWT ve Flask güvenlik anahtarı (Rastgele uzun bir string yaz)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cok-gizli-super-anahtar'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-icin-gizli-anahtar'