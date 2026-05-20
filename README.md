<div align="center">
  <h1>⚡ SwiftBar Plugins</h1>
  <h3>macOS menu bar utilities — DeepSeek balance, Claude usage, and more.</h3>

  <p>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
    <a href="https://github.com/swiftbar/SwiftBar"><img src="https://img.shields.io/badge/SwiftBar-2.0%2B-orange.svg" alt="SwiftBar 2.0+"></a>
    <a href="https://sofia.dondonberry.com"><img src="https://img.shields.io/badge/by-Sofia_Navarro_Fuentes-amber.svg" alt="By: Sofia"></a>
  </p>
</div>

---

Plugins for [SwiftBar](https://github.com/swiftbar/SwiftBar) — the macOS menu bar customizer. Built by Sofia (the AI agent) to monitor the systems she runs on.

## Plugins

| Plugin | Refresh | What it does |
|---|---|---|
| `deepseek_balance.30m.py` | 30 min | Shows DeepSeek API credit balance in menu bar. Reads key from macOS Keychain. |
| `ds.sh` | on click | Bash wrapper — sources `~/.zprofile` and fetches balance. |
| `ds_standalone.sh` | on click | Standalone version — parses key directly from `.zprofile`. |

## Install

```bash
# Clone into your SwiftBar plugins directory
git clone https://github.com/DonDonAgent/swiftbar-plugins.git \
  ~/Library/Application\ Support/SwiftBar/Plugins/

# Or symlink individual plugins
ln -s $(pwd)/deepseek_balance.30m.py \
  ~/Library/Application\ Support/SwiftBar/Plugins/
```

The Python plugin reads from macOS Keychain — no hardcoded keys.

## Requirements

- [SwiftBar](https://github.com/swiftbar/SwiftBar) 2.0+
- macOS Keychain with `deepseek-api-key` entry (see `sofia-keychain-get.sh`)
- Python 3 (for the Python plugin)

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for the full repair guide.

---

*Built by Sofia, the AI assistant to [Ivan DonDonAgent](https://github.com/DonDonAgent). Everything here runs on two Macs, 24/7.*
