# imessage-mcp

A read-only MCP server that exposes your iMessage data to Claude Code and Claude Desktop, with automatic contact name resolution.

## Setup

### 1. Install

```bash
cd ~/workspace/imessage-mcp
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 2. Grant Full Disk Access

The server needs to read `~/Library/Messages/chat.db` and the Contacts database. Grant **Full Disk Access** to the app that runs the server:

1. Open **System Settings → Privacy & Security → Full Disk Access**
2. For **Claude Code**: add your terminal app (e.g., Terminal, iTerm2, Ghostty)
3. For **Claude Desktop**: add the Claude app

### 3. Configure Claude Code

Add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "imessage": {
      "command": "/Users/jaredmoskowitz/workspace/imessage-mcp/.venv/bin/python",
      "args": ["-m", "imessage_mcp"]
    }
  }
}
```

### 4. Configure Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "imessage": {
      "command": "/Users/jaredmoskowitz/workspace/imessage-mcp/.venv/bin/python",
      "args": ["-m", "imessage_mcp"]
    }
  }
}
```

## Tools

### `list_chats`
List your iMessage chats sorted by recent activity.
- `limit` (optional, default 50): max chats to return

### `get_messages`
Get messages from a specific chat.
- `chat_id` (required): chat identifier from `list_chats`
- `limit` (optional, default 50): max messages
- `since` (optional): ISO date string — only messages after this date

### `search_messages`
Search all chats for messages containing a keyword.
- `query` (required): search text
- `limit` (optional, default 50): max results

## Example Usage

> "List my group chats"
> "Get the last 20 messages from my Business Ideas chat"
> "Search my messages for 'startup idea'"
