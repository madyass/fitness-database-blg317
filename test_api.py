import requests

BASE_URL = "http://127.0.0.1:5000/api"

# Test Kullanıcısı
USER_DATA = {"username": "postgres", "password": "12345"}

def run_full_test():
    print("🚀 FITNESS API FULL TEST BAŞLIYOR...\n")

    # 1. Kayıt Ol (Varsa geçer)
    print("--- 1. Kayıt Olunuyor ---")
    requests.post(f"{BASE_URL}/auth/register", json=USER_DATA)
    
    # 2. Giriş Yap
    print("--- 2. Giriş Yapılıyor ---")
    r = requests.post(f"{BASE_URL}/auth/login", json=USER_DATA)
    if r.status_code != 200:
        print("❌ GİRİŞ BAŞARISIZ!")
        return
    token = r.json().get('access_token')
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Token Alındı.")

    # 3. Plan Ekle
    print("\n--- 3. Plan Ekleniyor ---")
    plan_data = {"plan_name": "Platinum Pro", "monthly_fee": 200, "duration_months": 6}
    r = requests.post(f"{BASE_URL}/plans/", json=plan_data, headers=headers)
    if r.status_code == 201:
        plan_id = r.json().get('id')
        print(f"✅ Plan Eklendi (ID: {plan_id})")
    else:
        print(f"❌ Plan Hatası: {r.text}")
        return

    # 4. Üye Ekle (Plan ID ile)
    print("\n--- 4. Üye Ekleniyor ---")
    member_data = {
        "first_name": "Test", "last_name": "Ogrenci", 
        "email": "test_final@itu.edu.tr", "plan_id": plan_id
    }
    r = requests.post(f"{BASE_URL}/members/", json=member_data, headers=headers)
    if r.status_code == 201:
        print("✅ Üye Başarıyla Eklendi")
    else:
        print(f"❌ Üye Ekleme Hatası: {r.text}")

    # 5. Complex Query Raporu (Devamsızlık Yapanlar)
    print("\n--- 5. Complex Query Testi (Rapor) ---")
    r = requests.get(f"{BASE_URL}/reports/inactive-members", headers=headers)
    if r.status_code == 200:
        print("✅ Rapor Çekildi!")
        print("📊 Rapor Sonucu (JSON):")
        print(r.json()) # Burada az önce eklediğin üyeyi görmelisin
    else:
        print(f"❌ Rapor Hatası: {r.text}")

if __name__ == "__main__":
    try:
        run_full_test()
    except Exception as e:
        print(f"Bir hata oluştu: {e}")