# DOC / Main Tools

Dependency expectations:
- Python 3.11+
- git
- rg
- required model path: at least one configured provider
- optional connector: at least one configured channel
- optional OpenAI / Anthropic API keys
- optional local model endpoint
- optional Tailscale reachability
- optional repo-intel adapter

Primary public-safe tool surfaces:
- materialize-pack
- doctor, privacy-check, validate-config
- context pack
- failure clinic
- baseline and scorecard
- task and delegation schemas
- ops-fabric bootstrap, validation, and summary
- health and validation surfaces

Expected future role:
- memory-first orchestration
- delegation to CODEX / PA / HK
- optional repo-intelligence coordination

Privacy contract:
- consumes templates and public-safe config only
- never depends on private operator memory or personal routing doctrine
