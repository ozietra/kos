import urllib.request
import urllib.parse
import json
import ssl
import sys

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

BASE_URL = "https://kosgeb-backend.onrender.com"
#BASE_URL = "http://localhost:8000"

def login():
    url = f"{BASE_URL}/api/auth/login"
    data = json.dumps({
        "email": "test@demo.com",
        "password": "password123"
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            res = json.loads(response.read().decode())
            return res.get("access_token")
    except urllib.error.HTTPError as e:
        print("Login failed:", e.code, e.read().decode())
        return None

def main():
    token = login()
    if not token:
        print("Sisteme test kullanıcısıyla giriş yapılamadı. Elle kayıt yapalım.")

        # Kayıt olalım
        reg_url = f"{BASE_URL}/api/auth/register"
        reg_data = json.dumps({
            "name": "Test User",
            "email": "test@demo.com",
            "password": "password123"
        }).encode("utf-8")
        req = urllib.request.Request(reg_url, data=reg_data, method="POST", headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, context=ctx) as response:
                pass
        except urllib.error.HTTPError as e:
            if e.code != 400: # email already registered vs
                print("Register error", e.code, e.read().decode())
        
        token = login()
        if not token:
            print("Register -> Login failed")
            return

    # Önce bir işletme ve başvuru id'si almalıyız
    req = urllib.request.Request(f"{BASE_URL}/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, context=ctx) as res:
            me = json.loads(res.read().decode())
            print("Logged in as", me.get("email"))
    except Exception as e:
        print("Profile fetch failed", e)
        return

    # İşletme var mı?
    req = urllib.request.Request(f"{BASE_URL}/api/businesses", headers={"Authorization": f"Bearer {token}"})
    biz_id = None
    try:
        with urllib.request.urlopen(req, context=ctx) as res:
            bizs = json.loads(res.read().decode())
            if not bizs:
                print("No business found for test user. Creating one...")
                biz_req = urllib.request.Request(f"{BASE_URL}/api/businesses", headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, method="POST")
                biz_data = json.dumps({
                  "business_name": "Demo Corporation",
                  "nace_code": "62.01",
                  "nace_description": "Yazılım",
                  "city": "Ankara"
                }).encode("utf-8")
                with urllib.request.urlopen(biz_req, data=biz_data, context=ctx) as response:
                    new_biz = json.loads(response.read().decode())
                    biz_id = new_biz["id"]
            else:
                biz_id = bizs[0]["id"]
            print("Found/Created business", biz_id)
    except Exception as e:
        print("Biz fetch/create failed", e)
        if hasattr(e, 'read'):
            print(e.read().decode())
        return

    # Başvurular?
    req = urllib.request.Request(f"{BASE_URL}/api/businesses/{biz_id}/applications", headers={"Authorization": f"Bearer {token}"})
    app_id = None
    try:
        with urllib.request.urlopen(req, context=ctx) as res:
            apps = json.loads(res.read().decode())
            if apps:
                app_id = apps[0]["id"]
                print("Found app", app_id)
            else:
                # Başvuru oluştur
                create_req = urllib.request.Request(f"{BASE_URL}/api/applications/", headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, method="POST")
                create_data = json.dumps({"business_id": biz_id, "program_type": "KOBIGEL", "application_year": 2026}).encode("utf-8")
                with urllib.request.urlopen(create_req, data=create_data, context=ctx) as cres:
                    new_app = json.loads(cres.read().decode())
                    app_id = new_app["id"]
                    print("Created app", app_id)
    except Exception as e:
        print("App fetch failed", e)
        if hasattr(e, 'read'):
            print(e.read().decode())
        return
        
    # Trigger AI generation
    trigger_req = urllib.request.Request(f"{BASE_URL}/api/applications/{app_id}/generate", headers={"Authorization": f"Bearer {token}"}, method="POST")
    try:
        with urllib.request.urlopen(trigger_req, context=ctx) as res:
            pass
    except Exception:
        pass

    # ŞİMDİ SSE TESTİ
    print(f"Testing SSE stream for app {app_id}...")
    sse_url = f"{BASE_URL}/api/applications/{app_id}/progress?token={token}"
    sse_req = urllib.request.Request(sse_url)
    try:
        with urllib.request.urlopen(sse_req, context=ctx) as response:
            print("SSE Connection Status:", response.status)
            print("Headers:", response.headers)
            # Okumaya çalışalım
            for line in response:
                print("SSE YIELD:", line.decode().strip())
                if b'done": true' in line or b'error": true' in line:
                    break
    except urllib.error.HTTPError as e:
        print("SSE HTTP Error:", e.code)
        print(e.read().decode())
    except Exception as e:
        print("SSE Other Error:", str(e))

if __name__ == "__main__":
    main()
