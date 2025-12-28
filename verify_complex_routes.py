from app import create_app
import json

app = create_app()

def verify_routes():
    client = app.test_client()
    
    routes = [
        '/api/complex/popular-classes',
        '/api/complex/peak-hours',
        '/api/complex/revenue-by-plan',
        '/api/complex/instructor-performance',
        '/api/complex/maintenance-costs'
    ]
    
    print("Verifying Complex Routes...")
    
    for route in routes:
        print(f"\nTesting {route}...")
        try:
            response = client.get(route)
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                data = json.loads(response.data)
                print(f"Data: {json.dumps(data, indent=2)}")
                if isinstance(data, list):
                     print(f"Success: Received {len(data)} items.")
                else:
                    print("Success: Received data.")
            else:
                print(f"Error: {response.data.decode('utf-8')}")
        except Exception as e:
            print(f"Exception: {str(e)}")

if __name__ == "__main__":
    verify_routes()
