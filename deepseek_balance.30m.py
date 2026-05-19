#!/usr/bin/env python3
import subprocess, json, urllib.request, urllib.error

def get_key():
    r = subprocess.run(["/Users/demo/.config/secrets/sofia-keychain-get.sh", "deepseek-api-key", "sofia"], capture_output=True, text=True, timeout=5)
    return r.stdout.strip()

key = get_key()
try:
    req = urllib.request.Request("https://api.deepseek.com/user/balance", headers={"Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=8) as resp:
        data = json.loads(resp.read())
    total = sum(float(i["total_balance"]) for i in data["balance_infos"])
    print(f"DS: ${total:.2f}")
    print("---")
    print(f"💰 Balance: ${total:.2f}")
    print("---")
    print("🔄 Refresh | refresh=true")
except Exception as e:
    print("DS: ❌")
    print("---")
    print(f"{e}")
