import requests
import time

BASE_URL = "http://127.0.0.1:5001/api"
USER_DATA = {"username": "admin", "password": "123"}

def run_tests():
    print("🚀 FITNESS API COMPREHENSIVE TEST STARTED...\n")
    
    # 1. AUTHENTICATION
    print("--- 1. Authentication ---")
    requests.post(f"{BASE_URL}/auth/register", json=USER_DATA) # ignore error if exists
    r = requests.post(f"{BASE_URL}/auth/login", json=USER_DATA)
    if r.status_code != 200:
        print(f"❌ Login Failed: {r.text}")
        return
    token = r.json().get('access_token')
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Login Successful & Token Acquired")

    # 2. INSTRUCTORS (NEW)
    print("\n--- 2. Instructors ---")
    inst_data = {"first_name": "Test", "last_name": "Instructor", "specialization": "Pilates"}
    r = requests.post(f"{BASE_URL}/instructors/", json=inst_data, headers=headers)
    if r.status_code == 201:
        inst_id = r.json().get('id')
        print(f"✅ Instructor Created (ID: {inst_id})")
    else:
        print(f"❌ Create Instructor Failed: {r.text}")
        inst_id = 1 # Fallback for next steps

    r = requests.get(f"{BASE_URL}/instructors/", headers=headers)
    if r.status_code == 200:
        print(f"✅ List Instructors: Found {len(r.json())} instructors")
    
    # 3. PLANS
    print("\n--- 3. Membership Plans ---")
    plan_data = {"plan_name": "Gold 2025", "monthly_fee": 199, "duration_months": 12}
    r = requests.post(f"{BASE_URL}/plans/", json=plan_data, headers=headers)
    if r.status_code == 201:
        plan_id = r.json().get('id')
        print(f"✅ Plan Created (ID: {plan_id})")
    else:
         # use existing plan if fails
        plan_id = 1
        print(f"⚠️ Plan Creation Skipped/Failed: {r.text}")

    # 4. ROOMS (Using Seed Data for now as no API yet)
    room_id = 1 # Assuming seeded

    # 5. CLASSES (NEW)
    print("\n--- 5. Group Classes ---")
    class_data = {
        "class_name": "Advanced Pilates",
        "instructor_id": inst_id,
        "room_id": room_id,
        "start_time": "2025-06-01 10:00:00"
    }
    r = requests.post(f"{BASE_URL}/classes/", json=class_data, headers=headers)
    if r.status_code == 201:
        print(f"✅ Class Scheduled (ID: {r.json().get('id')})")
    else:
        print(f"❌ Schedule Class Failed: {r.text}")

    r = requests.get(f"{BASE_URL}/classes/", headers=headers)
    if r.status_code == 200:
        print(f"✅ List Classes: Found {len(r.json())} classes")

    # 6. MEMBERS
    print("\n--- 6. Members ---")
    member_data = {
        "first_name": "New", "last_name": "Member", 
        "email": f"new.member.{int(time.time())}@test.com", "plan_id": plan_id
    }
    r = requests.post(f"{BASE_URL}/members/", json=member_data, headers=headers)
    if r.status_code == 201:
        member_id = r.json().get('member_id')
        print(f"✅ Member Created (ID: {member_id})")
    else:
        print(f"❌ Member Create Failed: {r.text}")

    # 7. REPORTS
    print("\n--- 7. Reports ---")
    
    # Inactive Members
    r = requests.get(f"{BASE_URL}/reports/inactive-members", headers=headers)
    if r.status_code == 200:
         print(f"✅ Inactive Members Report: {len(r.json())} members found")
    else:
         print(f"❌ Inactive Report Failed: {r.text}")

    # Coach Analysis (NEW)
    r = requests.get(f"{BASE_URL}/reports/coach-analysis", headers=headers)
    if r.status_code == 200:
        print("✅ Coach Retention Analysis Report:")
        for item in r.json():
            print(f"   - Coach: {item['instructor_name']}, Avg Days: {item['avg_membership_days']}, Students: {item['student_count']}")
    else:
        print(f"❌ Coach Analysis Failed: {r.status_code} {r.text}")

if __name__ == "__main__":
    try:
        run_tests()
    except Exception as e:
        print(f"FATAL ERROR: {e}")