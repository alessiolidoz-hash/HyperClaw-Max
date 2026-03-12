from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ALLOWED_THINKING = {"off", "minimal", "low", "medium", "high", "xhigh", "adaptive"}
REQUIRED_TOP_LEVEL_KEYS = {"gateway", "agents", "models"}
KNOWN_TOP_LEVEL_KEYS = {
    "agents",
    "auth",
    "bindings",
    "channels",
    "commands",
    "gateway",
    "hooks",
    "messages",
    "models",
    "plugins",
    "skills",
    "tools",
    "wizard",
}

KNOWN_GATEWAY_KEYS = {"auth", "bind", "http", "mode", "nodes", "port", "tailscale"}
KNOWN_AGENT_DEFAULT_KEYS = {
    "bootstrapMaxChars",
    "bootstrapTotalMaxChars",
    "compaction",
    "contextPruning",
    "heartbeat",
    "imageModel",
    "maxConcurrent",
    "memorySearch",
    "model",
    "models",
    "sandbox",
    "subagents",
    "thinkingDefault",
    "workspace",
}
KNOWN_AGENT_ENTRY_KEYS = {"botName", "heartbeat", "id", "model", "thinkingDefault", "workspace"}
KNOWN_CHANNEL_KEYS = {"telegram", "whatsapp"}
KNOWN_HOOK_KEYS = {
    "allowRequestSessionKey",
    "allowedSessionKeyPrefixes",
    "defaultSessionKey",
    "enabled",
    "gmail",
    "mappings",
    "path",
    "presets",
    "token",
    "transformsDir",
}


def issue(path: str, message: str) -> dict[str, str]:
    return {"path": path, "message": message}


def strip_jsonc_comments(text: str) -> str:
    out: list[str] = []
    in_string = False
    escape = False
    line_comment = False
    block_comment = False
    i = 0
    while i < len(text):
        ch = text[i]
        nxt = text[i + 1] if i + 1 < len(text) else ""

        if line_comment:
            if ch == "\n":
                line_comment = False
                out.append(ch)
            i += 1
            continue

        if block_comment:
            if ch == "*" and nxt == "/":
                block_comment = False
                i += 2
                continue
            if ch == "\n":
                out.append(ch)
            i += 1
            continue

        if in_string:
            out.append(ch)
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            i += 1
            continue

        if ch == '"':
            in_string = True
            out.append(ch)
            i += 1
            continue

        if ch == "/" and nxt == "/":
            line_comment = True
            i += 2
            continue

        if ch == "/" and nxt == "*":
            block_comment = True
            i += 2
            continue

        out.append(ch)
        i += 1
    return "".join(out)


def strip_trailing_commas(text: str) -> str:
    out: list[str] = []
    in_string = False
    escape = False
    i = 0
    while i < len(text):
        ch = text[i]
        if in_string:
            out.append(ch)
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            i += 1
            continue

        if ch == '"':
            in_string = True
            out.append(ch)
            i += 1
            continue

        if ch == ",":
            j = i + 1
            while j < len(text) and text[j] in " \t\r\n":
                j += 1
            if j < len(text) and text[j] in "}]":
                i += 1
                continue

        out.append(ch)
        i += 1
    return "".join(out)


def load_jsonc(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    try:
        return json.loads(strip_trailing_commas(strip_jsonc_comments(raw)))
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON parse error at line {exc.lineno} col {exc.colno}: {exc.msg}") from exc


def expect_type(value: Any, expected: type, path: str, errors: list[dict[str, str]], message: str | None = None) -> bool:
    if isinstance(value, expected):
        return True
    errors.append(issue(path, message or f"must be a {expected.__name__}"))
    return False


def warn_unknown_keys(path: str, value: dict[str, Any], known: set[str], warnings: list[dict[str, str]]) -> None:
    for key in sorted(set(value) - known):
        warnings.append(issue(f"{path}.{key}" if path else key, "unknown key"))


def validate_model_spec(path: str, value: Any, errors: list[dict[str, str]]) -> None:
    if not expect_type(value, dict, path, errors, "must be an object {primary, fallbacks}"):
        return
    primary = value.get("primary")
    if not (isinstance(primary, str) and "/" in primary and primary.strip()):
        errors.append(issue(f"{path}.primary", "must be a provider/model string"))
    fallbacks = value.get("fallbacks", [])
    if not isinstance(fallbacks, list):
        errors.append(issue(f"{path}.fallbacks", "must be a list"))
    else:
        for idx, item in enumerate(fallbacks):
            if not (isinstance(item, str) and "/" in item and item.strip()):
                errors.append(issue(f"{path}.fallbacks[{idx}]", "must be a provider/model string"))


def validate_thinking(path: str, value: Any, errors: list[dict[str, str]]) -> None:
    if value is None:
        return
    if not isinstance(value, str):
        errors.append(issue(path, "must be a string"))
        return
    if value not in ALLOWED_THINKING:
        errors.append(issue(path, f"must be one of {sorted(ALLOWED_THINKING)}"))


def validate_bool(path: str, value: Any, errors: list[dict[str, str]]) -> None:
    if not isinstance(value, bool):
        errors.append(issue(path, "must be a boolean"))


def validate_gateway(cfg: dict[str, Any], errors: list[dict[str, str]], warnings: list[dict[str, str]]) -> None:
    gateway = cfg.get("gateway")
    if gateway is None:
        errors.append(issue("gateway", "is required"))
        return
    if not expect_type(gateway, dict, "gateway", errors):
        return
    warn_unknown_keys("gateway", gateway, KNOWN_GATEWAY_KEYS, warnings)
    if not isinstance(gateway.get("mode"), str) or not gateway["mode"].strip():
        errors.append(issue("gateway.mode", "must be a non-empty string"))
    if not isinstance(gateway.get("bind"), str) or not gateway["bind"].strip():
        errors.append(issue("gateway.bind", "must be a non-empty string"))
    port = gateway.get("port")
    if not isinstance(port, int) or not (1 <= port <= 65535):
        errors.append(issue("gateway.port", "must be an integer 1..65535"))
    for key in ("auth", "http", "nodes", "tailscale"):
        value = gateway.get(key)
        if value is not None and not isinstance(value, dict):
            errors.append(issue(f"gateway.{key}", "must be an object"))


def validate_agents(cfg: dict[str, Any], errors: list[dict[str, str]], warnings: list[dict[str, str]]) -> None:
    agents = cfg.get("agents")
    if agents is None:
        errors.append(issue("agents", "is required"))
        return
    if not expect_type(agents, dict, "agents", errors):
        return

    defaults = agents.get("defaults")
    if not expect_type(defaults, dict, "agents.defaults", errors):
        return
    warn_unknown_keys("agents.defaults", defaults, KNOWN_AGENT_DEFAULT_KEYS, warnings)
    if not isinstance(defaults.get("workspace"), str) or not defaults["workspace"].strip():
        errors.append(issue("agents.defaults.workspace", "must be a non-empty string"))
    if "model" not in defaults:
        errors.append(issue("agents.defaults.model", "is required"))
    else:
        validate_model_spec("agents.defaults.model", defaults.get("model"), errors)
    validate_thinking("agents.defaults.thinkingDefault", defaults.get("thinkingDefault"), errors)
    if "maxConcurrent" in defaults:
        if not isinstance(defaults["maxConcurrent"], int) or defaults["maxConcurrent"] < 1:
            errors.append(issue("agents.defaults.maxConcurrent", "must be an integer >= 1"))
    memory_search = defaults.get("memorySearch")
    if memory_search is not None and not isinstance(memory_search, dict):
        errors.append(issue("agents.defaults.memorySearch", "must be an object"))
    heartbeat = defaults.get("heartbeat")
    if heartbeat is not None and not isinstance(heartbeat, dict):
        errors.append(issue("agents.defaults.heartbeat", "must be an object"))

    entries = agents.get("list")
    if not isinstance(entries, list) or not entries:
        errors.append(issue("agents.list", "must be a non-empty list"))
        return
    seen_ids: set[str] = set()
    for idx, entry in enumerate(entries):
        path = f"agents.list[{idx}]"
        if not expect_type(entry, dict, path, errors):
            continue
        warn_unknown_keys(path, entry, KNOWN_AGENT_ENTRY_KEYS, warnings)
        agent_id = entry.get("id")
        if not isinstance(agent_id, str) or not agent_id.strip():
            errors.append(issue(f"{path}.id", "must be a non-empty string"))
        elif agent_id in seen_ids:
            errors.append(issue(f"{path}.id", "must be unique"))
        else:
            seen_ids.add(agent_id)
        if not isinstance(entry.get("workspace"), str) or not entry["workspace"].strip():
            errors.append(issue(f"{path}.workspace", "must be a non-empty string"))
        if "model" in entry:
            validate_model_spec(f"{path}.model", entry.get("model"), errors)
        if "thinkingDefault" in entry:
            validate_thinking(f"{path}.thinkingDefault", entry.get("thinkingDefault"), errors)
        if "heartbeat" in entry and not isinstance(entry["heartbeat"], dict):
            errors.append(issue(f"{path}.heartbeat", "must be an object"))


def validate_models(cfg: dict[str, Any], errors: list[dict[str, str]]) -> None:
    models = cfg.get("models")
    if models is None:
        errors.append(issue("models", "is required"))
        return
    if not expect_type(models, dict, "models", errors):
        return
    providers = models.get("providers")
    if not isinstance(providers, dict) or not providers:
        errors.append(issue("models.providers", "must be a non-empty object"))
        return
    for name, provider in providers.items():
        if not isinstance(provider, dict):
            errors.append(issue(f"models.providers.{name}", "must be an object"))


def validate_bindings(cfg: dict[str, Any], errors: list[dict[str, str]]) -> None:
    bindings = cfg.get("bindings")
    if bindings is None:
        return
    if not isinstance(bindings, list):
        errors.append(issue("bindings", "must be a list"))
        return
    for idx, entry in enumerate(bindings):
        path = f"bindings[{idx}]"
        if not expect_type(entry, dict, path, errors):
            continue
        if "agentId" in entry and not isinstance(entry["agentId"], str):
            errors.append(issue(f"{path}.agentId", "must be a string"))
        if "match" in entry and not isinstance(entry["match"], dict):
            errors.append(issue(f"{path}.match", "must be an object"))


def validate_channels(cfg: dict[str, Any], errors: list[dict[str, str]], warnings: list[dict[str, str]]) -> None:
    channels = cfg.get("channels")
    if channels is None:
        return
    if not expect_type(channels, dict, "channels", errors):
        return
    warn_unknown_keys("channels", channels, KNOWN_CHANNEL_KEYS, warnings)
    for channel_name in ("telegram", "whatsapp"):
        channel = channels.get(channel_name)
        if channel is None:
            continue
        path = f"channels.{channel_name}"
        if not expect_type(channel, dict, path, errors):
            continue
        heartbeat = channel.get("heartbeat")
        if heartbeat is not None and not isinstance(heartbeat, dict):
            errors.append(issue(f"{path}.heartbeat", "must be an object"))
        enabled = channel.get("enabled")
        if enabled is not None and not isinstance(enabled, bool):
            errors.append(issue(f"{path}.enabled", "must be a boolean"))
        accounts = channel.get("accounts")
        if accounts is not None and not isinstance(accounts, dict):
            errors.append(issue(f"{path}.accounts", "must be an object"))
        allow_from = channel.get("allowFrom")
        if allow_from is not None and not isinstance(allow_from, list):
            errors.append(issue(f"{path}.allowFrom", "must be a list"))


def validate_hooks(cfg: dict[str, Any], errors: list[dict[str, str]], warnings: list[dict[str, str]]) -> None:
    hooks = cfg.get("hooks")
    if hooks is None:
        return
    if not expect_type(hooks, dict, "hooks", errors):
        return
    warn_unknown_keys("hooks", hooks, KNOWN_HOOK_KEYS, warnings)
    enabled = hooks.get("enabled")
    if enabled is not None:
        validate_bool("hooks.enabled", enabled, errors)
    for key in ("path", "token", "defaultSessionKey", "transformsDir"):
        value = hooks.get(key)
        if value is not None and not isinstance(value, str):
            errors.append(issue(f"hooks.{key}", "must be a string"))
    mappings = hooks.get("mappings")
    if mappings is not None and not isinstance(mappings, list):
        errors.append(issue("hooks.mappings", "must be a list"))
    prefixes = hooks.get("allowedSessionKeyPrefixes")
    if prefixes is not None and not isinstance(prefixes, list):
        errors.append(issue("hooks.allowedSessionKeyPrefixes", "must be a list"))
    gmail = hooks.get("gmail")
    if gmail is not None and not isinstance(gmail, dict):
        errors.append(issue("hooks.gmail", "must be an object"))


def validate_tools(cfg: dict[str, Any], errors: list[dict[str, str]]) -> None:
    tools = cfg.get("tools")
    if tools is None:
        return
    if not expect_type(tools, dict, "tools", errors):
        return
    if "profile" in tools and not isinstance(tools["profile"], str):
        errors.append(issue("tools.profile", "must be a string"))
    for key in ("web", "media", "sessions", "message", "agentToAgent"):
        value = tools.get(key)
        if value is not None and not isinstance(value, dict):
            errors.append(issue(f"tools.{key}", "must be an object"))


def validate_skills(cfg: dict[str, Any], errors: list[dict[str, str]]) -> None:
    skills = cfg.get("skills")
    if skills is None:
        return
    if not expect_type(skills, dict, "skills", errors):
        return
    for key in ("load", "install", "entries"):
        value = skills.get(key)
        if value is not None and not isinstance(value, dict):
            errors.append(issue(f"skills.{key}", "must be an object"))


def validate_wizard(cfg: dict[str, Any], errors: list[dict[str, str]]) -> None:
    wizard = cfg.get("wizard")
    if wizard is None:
        return
    if not expect_type(wizard, dict, "wizard", errors):
        return
    for key in ("lastRunAt", "lastRunVersion", "lastRunCommand", "lastRunMode"):
        value = wizard.get(key)
        if value is not None and not isinstance(value, str):
            errors.append(issue(f"wizard.{key}", "must be a string or null"))


def validate_simple_objects(cfg: dict[str, Any], errors: list[dict[str, str]]) -> None:
    for path in ("messages", "commands", "plugins", "auth"):
        value = cfg.get(path)
        if value is not None and not isinstance(value, dict):
            errors.append(issue(path, "must be an object"))


def validate_config(cfg: dict[str, Any]) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    if not isinstance(cfg, dict):
        return {"ok": False, "errors": [issue("$", "top-level config must be an object")], "warnings": []}

    missing = sorted(REQUIRED_TOP_LEVEL_KEYS - set(cfg))
    for key in missing:
        errors.append(issue(key, "is required"))
    warn_unknown_keys("", cfg, KNOWN_TOP_LEVEL_KEYS, warnings)

    validate_gateway(cfg, errors, warnings)
    validate_agents(cfg, errors, warnings)
    validate_models(cfg, errors)
    validate_bindings(cfg, errors)
    validate_channels(cfg, errors, warnings)
    validate_hooks(cfg, errors, warnings)
    validate_tools(cfg, errors)
    validate_skills(cfg, errors)
    validate_wizard(cfg, errors)
    validate_simple_objects(cfg, errors)

    return {"ok": not errors, "errors": errors, "warnings": warnings}


def validate_config_path(path: Path) -> dict[str, Any]:
    cfg = load_jsonc(path)
    payload = validate_config(cfg)
    payload["config"] = str(path.resolve())
    return payload


def render_human(payload: dict[str, Any]) -> str:
    lines = ["=== HyperClaw-Max Config Validate ===", f"Config: {payload['config']}"]
    if payload["warnings"]:
        lines.append("Warnings:")
        for row in payload["warnings"]:
            lines.append(f"- {row['path']}: {row['message']}")
    if payload["errors"]:
        lines.append("Errors:")
        for row in payload["errors"]:
            lines.append(f"- {row['path']}: {row['message']}")
    lines.append(f"Overall: {'OK' if payload['ok'] else 'FAIL'}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate HyperClaw-Max public config shape")
    ap.add_argument("config", nargs="?", type=Path, default=Path("config/openclaw.public.example.jsonc"))
    ap.add_argument("--format", choices=["json", "human"], default="human")
    args = ap.parse_args()

    try:
        payload = validate_config_path(args.config)
    except ValueError as exc:
        payload = {
            "config": str(args.config.resolve()),
            "ok": False,
            "errors": [issue("config", str(exc))],
            "warnings": [],
        }

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_human(payload))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
