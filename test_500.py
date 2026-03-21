import urllib.request
import urllib.error
import urllib.parse
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# API base URL
url = "https://kosgeb-backend.onrender.com/api/eligibility/caaa1a2d-79de-4052-9cd8-5b06b31dbafe"

# Assuming we need auth token, but let's try just getting the 500 if it doesn't check auth first, 
# or wait, auth is required:
req = urllib.request.Request(url, headers={"Authorization": "Bearer fake_token_just_to_see_if_it_fails_auth_or_500"})

try:
    with urllib.request.urlopen(req, context=ctx) as response:
        print(response.read().decode())
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code}")
    print(e.read().decode())
    
