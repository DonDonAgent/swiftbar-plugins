#!/usr/bin/env python3
"""DeepSeek API balance widget for SwiftBar. Refreshes every 30 minutes.
Loads API key from private GitHub repo sofia-memory/.swiftbar.json
Works on both server and personal laptop — just requires `gh` CLI auth."""

import json, subprocess, os, tempfile

REPO = "DonDonAgent/sofia-memory"
CONFIG_PATH = ".swiftbar.json"

def get_config():
    """Fetch config from private GitHub repo via gh CLI (works on both laptops)."""
    try:
        r = subprocess.run(
            ["gh", "api", f"repos/{REPO}/contents/{CONFIG_PATH}",
             "--jq", ".content"],
            capture_output=True, text=True, timeout=15,
            env={**os.environ, "GH_NO_UPDATE_NOTIFIER": "1"}
        )
        if r.returncode != 0:
            # Fallback: local keychain
            return _fallback_keychain()
        import base64
        return json.loads(base64.b64decode(r.stdout.strip()).decode())
    except Exception:
        return _fallback_keychain()

def _fallback_keychain():
    """Last resort — read directly from keychain."""
    try:
        r = subprocess.run(
            ["/Users/demo/.config/secrets/sofia-keychain-get.sh", "deepseek-api-key", "sofia"],
            capture_output=True, text=True, timeout=5
        )
        return {"deepseek_api_key": r.stdout.strip()}
    except Exception:
        return {}

config = get_config()
API_KEY = config.get("deepseek_api_key", "")
API_URL = "https://api.deepseek.com/user/balance"

try:
    import urllib.request, urllib.error
    req = urllib.request.Request(API_URL, headers={"Authorization": f"Bearer {API_KEY}"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())

    if not data.get("is_available"):
        print("DS: ⚠️")
        print("---")
        print("API недоступен")
        exit(0)

    infos = data["balance_infos"]
    total = sum(float(i["total_balance"]) for i in infos)

    if total > 2.0:
        print(f"DS: ${total:.2f}")
    elif total > 1.0:
        print(f"DS: ${total:.2f} | color=orange")
    else:
        print(f"DS: ${total:.2f} | color=red")

    print("---")
    print(f"💰 Balance: ${total:.2f}")
    print("---")
    for info in infos:
        currency = info["currency"]
        print(f"💳 {currency}:")
        print(f"   Total:     ${float(info['total_balance']):.2f}")
        print(f"   Topped up: ${float(info['topped_up_balance']):.2f}")
        if float(info.get("granted_balance", 0)) > 0:
            print(f"   Granted:   ${float(info['granted_balance']):.2f}")
    print("---")
    print("🔄 Refresh | refresh=true")
    print("🌐 DeepSeek Platform | href=https://platform.deepseek.com")

except urllib.error.HTTPError as e:
    print(f"DS: ❌ {e.code}")
    print("---")
    print(f"HTTP Error: {e.code}")
except Exception as e:
    print("DS: ❌")
    print("---")
    print(f"Error: {e}")
