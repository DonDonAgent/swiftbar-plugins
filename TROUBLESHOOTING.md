# SwiftBar DeepSeek Plugin — Repair Guide

## When to use

- SwiftBar shows `DS: 401` or `DS: ❌` in menu bar
- DeepSeek API key was changed/revoked/renewed
- After any API key rotation

## Prerequisites

This guide assumes:
- `~/.config/secrets/sofia-keychain-get.sh` exists (reads from `~/Library/Keychains/sofia.keychain-db`)
- `~/.config/secrets/sofia-keychain-pw.txt` contains the keychain password
- `python3` available on PATH
- `gh` CLI or web access to download plugin from GitHub

If keychain files are missing, copy them from another machine or recreate.

## Root cause patterns

| Symptom | Root cause |
|---------|-----------|
| 401 error | Old/hardcoded API key in plugin file |
| `DS: ?` or blank | Key not reachable (keychain locked, env missing) |
| Plugin not showing | Plugin in wrong directory or ghost directory |
| Ghost directories | SwiftBar recreates empty dirs for remembered plugins |

## Architecture

SwiftBar looks for plugins in TWO places:

1. **Default:** `~/Library/Application Support/SwiftBar/Plugins/`
2. **Custom:** whatever is set in `defaults read com.ameba.SwiftBar PluginDirectory`

The custom directory takes precedence if set.

## Step-by-step repair

### Step 1: Find where SwiftBar actually reads plugins

```bash
defaults read com.ameba.SwiftBar PluginDirectory
```

If empty — uses default `~/Library/Application Support/SwiftBar/Plugins/`.
If set — that's the REAL directory.

### Step 2: Check ALL plugin directories for old keys

```bash
# Check default dir
grep -r "sk-" ~/Library/Application\ Support/SwiftBar/Plugins/

# Check custom dir (if exists)
DIR=$(defaults read com.ameba.SwiftBar PluginDirectory 2>/dev/null)
[ -n "$DIR" ] && grep -r "sk-" "$DIR"
```

Any `sk-25ee7348...` (old leaked key) = replace with `sk-2cf127ace34045d2987eb019d7bbf47a`.

### Step 3: Replace the plugin

Copy the working plugin from GitHub:

```bash
# For the default directory:
curl -o ~/Library/Application\ Support/SwiftBar/Plugins/deepseek_balance.30m.py \
  https://raw.githubusercontent.com/DonDonAgent/swiftbar-plugins/main/deepseek_balance.30m.py
chmod +x ~/Library/Application\ Support/SwiftBar/Plugins/deepseek_balance.30m.py

# For custom directory (replace PATH with actual):
DIR=$(defaults read com.ameba.SwiftBar PluginDirectory 2>/dev/null)
[ -n "$DIR" ] && curl -o "$DIR/deepseek_balance.30m.py" \
  https://raw.githubusercontent.com/DonDonAgent/swiftbar-plugins/main/deepseek_balance.30m.py
```

### Step 4: Remove ghost directories

SwiftBar recreates empty directories for plugins it remembers. Clean them:

```bash
# Remove empty dirs (SwiftBar recreates them as ghosts)
PLUGIN_DIR=~/Library/Application\ Support/SwiftBar/Plugins
find "$PLUGIN_DIR" -type d -empty -delete
```

### Step 5: Test the plugin manually

```bash
python3 ~/Library/Application\ Support/SwiftBar/Plugins/deepseek_balance.30m.py
```

Should output: `DS: $X.XX`

### Step 6: Clear caches and restart

```bash
pkill -x SwiftBar
sleep 1
rm -rf ~/Library/Caches/com.ameba.SwiftBar
rm -rf ~/Library/HTTPStorages/com.ameba.SwiftBar
open -a SwiftBar
```

### If still broken — hard reset

```bash
pkill -x SwiftBar
sleep 1
rm -rf ~/Library/Caches/com.ameba.SwiftBar
rm -rf ~/Library/HTTPStorages/com.ameba.SwiftBar
rm -f ~/Library/Preferences/com.ameba.SwiftBar.plist
open -a SwiftBar
# SwiftBar will ask for plugin folder — select:
# ~/Library/Application Support/SwiftBar/Plugins
# Or set via CLI:
defaults write com.ameba.SwiftBar PluginDirectory "~/Library/Application Support/SwiftBar/Plugins"
```

## How the plugin reads the key

The plugin uses `sofia-keychain-get.sh` subprocess (NOT hardcoded, NOT shell env).
This script is machine-specific — it must exist at `~/.config/secrets/sofia-keychain-get.sh`
with access to `~/Library/Keychains/sofia.keychain-db`.

```python
def get_key():
    r = subprocess.run(["/Users/demo/.config/secrets/sofia-keychain-get.sh",
        "deepseek-api-key", "sofia"], capture_output=True, text=True, timeout=5)
    return r.stdout.strip()
```

This works because:
- `sofia-keychain-get.sh` reads from `~/Library/Keychains/sofia.keychain-db`
- The keychain password is stored at `~/.config/secrets/sofia-keychain-pw.txt`
- No env vars, no shell sourcing needed

## How to update the key (future rotation)

```bash
# 1. Add new key to keychain
security add-generic-password -a "sofia" -s "deepseek-api-key" \
  -w "sk-NEW-KEY-HERE" -U ~/Library/Keychains/sofia.keychain-db

# 2. Verify
python3 ~/Library/Application\ Support/SwiftBar/Plugins/deepseek_balance.30m.py

# 3. Restart SwiftBar
pkill -x SwiftBar && sleep 1 && open -a SwiftBar
```

No code changes needed — plugin reads from keychain.

## Verification checklist

- [ ] `python3 path/to/deepseek_balance.30m.py` shows `DS: $X.XX`
- [ ] No old key `sk-25ee7348` anywhere: `grep -r "sk-25ee7348" ~/Library/Application\ Support/SwiftBar/`
- [ ] SwiftBar shows `DS: $X.XX` in menu bar (not 401, not ❌)
- [ ] `defaults read com.ameba.SwiftBar PluginDirectory` points to existing dir
