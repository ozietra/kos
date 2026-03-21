import urllib.request
import urllib.error
import json

url = "https://kosgeb-backend.onrender.com/api/auth/register"
data = json.dumps({
    "email": "test3@kosgebhibe.com",
    "name": "Test",
    "password": "TestPassword123!"
}).encode('utf-8')

req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req) as response:
        print(response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code}")
    print(e.read().decode('utf-8'))
except Exception as e:
    print(f"Error: {e}")
