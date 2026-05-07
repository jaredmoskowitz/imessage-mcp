# AGENTS.md

Guidance for AI coding agents (Codex, Cursor, Claude Code, etc.) working in this repo.

## What this is

A read-only MCP server that exposes iMessage data to MCP-compatible clients. Runs locally on macOS, reads `~/Library/Messages/chat.db` directly via SQLite, and resolves contact names from the macOS Contacts database.

## Hard constraints

- **macOS only.** The codebase assumes the macOS Messages SQLite layout. Do not add cross-platform abstractions; do not pretend Linux/Windows are supported.
- **Read-only.** Every SQLite connection opens with `mode=ro` (see [src/imessage_mcp/imessage.py](src/imessage_mcp/imessage.py)). Never introduce writes, deletes, schema changes, or commits against `chat.db` or the Contacts database. If you need a write feature, stop and ask first.
- **No data leaves the machine.** Never add network calls, telemetry, analytics, or remote logging. The whole point of this server is local-only access.
- **Privacy-first.** Don't log message bodies, contact identifiers, or phone numbers at info level. Tests use synthetic fixtures, not real data.

## Layout

```
src/imessage_mcp/
  __init__.py     # entry: main()
  __main__.py     # python -m imessage_mcp
  server.py       # FastMCP tool definitions (list_chats, get_messages, search_messages)
  imessage.py     # IMessageReader: SQLite queries against chat.db
  contacts.py     # ContactResolver: maps handle ids -> contact names
tests/            # pytest, one file per module
pyproject.toml    # Python 3.12+, dep: mcp[cli]>=1.9.0
```

## Setup & commands

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e .
pytest                    # run tests
python -m imessage_mcp    # run the MCP server
```

Full Disk Access must be granted to the terminal app (or Claude Desktop) running the server, or SQLite reads will fail with permission errors. This is a runtime-only requirement; tests do not touch real databases.

## MCP tool guidelines

The three tools in [src/imessage_mcp/server.py](src/imessage_mcp/server.py) — `list_chats`, `get_messages`, `search_messages` — have docstrings that are surfaced verbatim to AI clients as the tool description. Treat docstrings as user-facing API docs:

- Document every parameter, including type and default.
- If you change behavior, update the docstring in the same commit.
- Tools return JSON strings, not dicts. Keep `json.dumps(..., indent=2)` formatting consistent.

When adding a new tool: register it with `@mcp.tool()`, write a docstring, add tests in `tests/test_server.py`, and update the `## Tools` section of [README.md](README.md).

## Style

- Type hints on every function parameter and return.
- Use `pathlib.Path` for filesystem paths (see `DEFAULT_CHAT_DB_PATH`).
- Apple-epoch timestamp conversion lives in `_apple_ts_to_iso` / `_iso_to_apple_ts` — reuse them, don't reimplement.
- The `attributedBody` decoding in `parse_attributed_body` is fragile by nature (it's a partial NSKeyedArchiver parse). If you touch it, add fixtures covering the exact byte patterns you change.

## Testing

`pytest` runs everything. Tests build their own temporary SQLite databases with the same schema as `chat.db` — never point tests at the real database.
