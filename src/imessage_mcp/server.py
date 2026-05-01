import json
from mcp.server.fastmcp import FastMCP
from imessage_mcp.imessage import IMessageReader
from imessage_mcp.contacts import ContactResolver

mcp = FastMCP("imessage")

_reader = IMessageReader()
_resolver = ContactResolver()


def _resolve_sender(sender: str) -> str:
    if sender == "Me":
        return sender
    return _resolver.resolve(sender)


@mcp.tool()
def list_chats(limit: int = 50) -> str:
    """List iMessage chats sorted by most recent activity.

    Args:
        limit: Maximum number of chats to return (default 50)
    """
    chats = _reader.list_chats(limit=limit)
    for chat in chats:
        chat["participants"] = [_resolver.resolve(p) for p in chat["participants"]]
    return json.dumps(chats, indent=2)


@mcp.tool()
def get_messages(chat_id: str, limit: int = 50, since: str | None = None) -> str:
    """Get messages from a specific iMessage chat.

    Args:
        chat_id: The chat identifier (from list_chats)
        limit: Maximum number of messages to return (default 50)
        since: Only return messages after this ISO date (e.g. '2024-01-15' or '2024-01-15T10:30:00')
    """
    messages = _reader.get_messages(chat_id, limit=limit, since=since)
    for msg in messages:
        msg["sender"] = _resolve_sender(msg["sender"])
    return json.dumps(messages, indent=2)


@mcp.tool()
def search_messages(query: str, limit: int = 50) -> str:
    """Search all iMessage chats for messages containing the query text.

    Args:
        query: The text to search for
        limit: Maximum number of results to return (default 50)
    """
    messages = _reader.search_messages(query, limit=limit)
    for msg in messages:
        msg["sender"] = _resolve_sender(msg["sender"])
    return json.dumps(messages, indent=2)
