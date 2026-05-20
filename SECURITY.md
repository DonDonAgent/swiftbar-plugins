# Security Policy

## Reporting a Vulnerability

If you find a security issue in these plugins (API key handling, credential exposure, etc.):

**Email:** security@dondonberry.com

Do NOT open a public issue — this is about secrets management. I'll respond within 48 hours.

## Key handling

These plugins read API keys from macOS Keychain. Never hardcode keys in plugin files. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for the correct keychain setup.
