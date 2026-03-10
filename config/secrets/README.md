# Secrets Boundary

No real secrets belong in this staging tree.

Expected public-distro approach:
- use env vars
- use user-supplied OAuth flows
- use setup scripts that write local private files after install

Never commit:
- bot tokens
- OAuth client secrets
- WhatsApp session material
- allowlists with real user ids
- private API keys
