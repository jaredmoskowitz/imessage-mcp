import sqlite3
from datetime import datetime, timezone
from pathlib import Path

# Apple epoch: 2001-01-01 00:00:00 UTC
# Offset from Unix epoch (1970-01-01) to Apple epoch in seconds
APPLE_EPOCH_OFFSET = 978307200
NANOSECONDS = 1_000_000_000

DEFAULT_CHAT_DB_PATH = str(Path.home() / "Library" / "Messages" / "chat.db")


def parse_attributed_body(blob: bytes | None) -> str | None:
    """Extract text from an NSAttributedString binary blob.

    On macOS Ventura+, some messages store text in attributedBody
    instead of the text column.
    """
    if not blob:
        return None
    try:
        # The text is stored after an NSString marker
        parts = blob.split(b"NSString")
        if len(parts) < 2:
            return None
        text_data = parts[1]
        # Skip 5 bytes of preamble after NSString
        text_data = text_data[5:]
        if not text_data:
            return None
        # Read length: if first byte is 0x81, length is next 2 bytes (little-endian)
        if text_data[0] == 0x81:
            length = int.from_bytes(text_data[1:3], "little")
            text_bytes = text_data[3 : 3 + length]
        else:
            length = text_data[0]
            text_bytes = text_data[1 : 1 + length]
        return text_bytes.decode("utf-8", errors="replace")
    except (IndexError, UnicodeDecodeError):
        return None


def _apple_ts_to_iso(apple_ns: int) -> str:
    """Convert Apple nanosecond timestamp to ISO 8601 string."""
    unix_seconds = (apple_ns / NANOSECONDS) + APPLE_EPOCH_OFFSET
    dt = datetime.fromtimestamp(unix_seconds, tz=timezone.utc)
    return dt.isoformat()


def _iso_to_apple_ts(iso_str: str) -> int:
    """Convert ISO 8601 string to Apple nanosecond timestamp."""
    dt = datetime.fromisoformat(iso_str)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    unix_seconds = dt.timestamp()
    apple_seconds = unix_seconds - APPLE_EPOCH_OFFSET
    return int(apple_seconds * NANOSECONDS)


class IMessageReader:
    def __init__(self, db_path: str = DEFAULT_CHAT_DB_PATH):
        self._db_path = db_path

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(f"file:{self._db_path}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        return conn

    def _get_chat_name(self, conn: sqlite3.Connection, chat_row: sqlite3.Row) -> str:
        """Get display name for a chat, falling back to participant list."""
        display_name = chat_row["display_name"]
        if display_name:
            return display_name
        # Fall back to participant identifiers
        participants = self._get_participants(conn, chat_row["guid"])
        if participants:
            return ", ".join(participants)
        return chat_row["chat_identifier"]

    def _get_participants(self, conn: sqlite3.Connection, chat_guid: str) -> list[str]:
        """Get participant identifiers for a chat."""
        rows = conn.execute("""
            SELECT h.id
            FROM handle h
            JOIN chat_handle_join chj ON h.ROWID = chj.handle_id
            JOIN chat c ON c.ROWID = chj.chat_id
            WHERE c.guid = ?
        """, (chat_guid,)).fetchall()
        return [row["id"] for row in rows]

    def list_chats(self, limit: int = 50) -> list[dict]:
        conn = self._connect()
        rows = conn.execute("""
            SELECT c.guid, c.chat_identifier, c.display_name,
                   MAX(m.date) as last_date
            FROM chat c
            LEFT JOIN chat_message_join cmj ON c.ROWID = cmj.chat_id
            LEFT JOIN message m ON cmj.message_id = m.ROWID
            GROUP BY c.ROWID
            ORDER BY last_date DESC
            LIMIT ?
        """, (limit,)).fetchall()

        chats = []
        for row in rows:
            participants = self._get_participants(conn, row["guid"])
            chat_name = row["display_name"]
            if not chat_name:
                chat_name = ", ".join(participants) if participants else row["chat_identifier"]

            chats.append({
                "chat_id": row["guid"],
                "chat_name": chat_name,
                "participants": participants,
                "last_message_date": _apple_ts_to_iso(row["last_date"]) if row["last_date"] else None,
            })
        conn.close()
        return chats

    def get_messages(
        self, chat_id: str, limit: int = 50, since: str | None = None
    ) -> list[dict]:
        conn = self._connect()

        # Get chat display name
        chat_row = conn.execute(
            "SELECT * FROM chat WHERE guid = ?", (chat_id,)
        ).fetchone()
        if not chat_row:
            conn.close()
            return []
        chat_name = self._get_chat_name(conn, chat_row)

        query = """
            SELECT m.text, m.handle_id, m.date, m.is_from_me, m.attributedBody,
                   h.id as handle_identifier
            FROM message m
            JOIN chat_message_join cmj ON m.ROWID = cmj.message_id
            JOIN chat c ON c.ROWID = cmj.chat_id
            LEFT JOIN handle h ON m.handle_id = h.ROWID
            WHERE c.guid = ?
        """
        params: list = [chat_id]

        if since:
            apple_ts = _iso_to_apple_ts(since)
            query += " AND m.date > ?"
            params.append(apple_ts)

        query += " ORDER BY m.date ASC LIMIT ?"
        params.append(limit)

        rows = conn.execute(query, params).fetchall()
        conn.close()

        messages = []
        for row in rows:
            text = row["text"]
            if text is None:
                text = parse_attributed_body(row["attributedBody"])

            if row["is_from_me"]:
                sender = "Me"
            else:
                sender = row["handle_identifier"] or "Unknown"

            messages.append({
                "sender": sender,
                "text": text,
                "timestamp": _apple_ts_to_iso(row["date"]),
                "chat_name": chat_name,
            })
        return messages

    def search_messages(self, query: str, limit: int = 50) -> list[dict]:
        conn = self._connect()
        rows = conn.execute("""
            SELECT m.text, m.handle_id, m.date, m.is_from_me, m.attributedBody,
                   h.id as handle_identifier,
                   c.guid as chat_guid, c.chat_identifier, c.display_name
            FROM message m
            JOIN chat_message_join cmj ON m.ROWID = cmj.message_id
            JOIN chat c ON c.ROWID = cmj.chat_id
            LEFT JOIN handle h ON m.handle_id = h.ROWID
            WHERE m.text LIKE ?
            ORDER BY m.date DESC
            LIMIT ?
        """, (f"%{query}%", limit)).fetchall()

        messages = []
        for row in rows:
            text = row["text"]
            chat_name = row["display_name"]
            if not chat_name:
                participants = self._get_participants(conn, row["chat_guid"])
                chat_name = ", ".join(participants) if participants else row["chat_identifier"]

            if row["is_from_me"]:
                sender = "Me"
            else:
                sender = row["handle_identifier"] or "Unknown"

            messages.append({
                "sender": sender,
                "text": text,
                "timestamp": _apple_ts_to_iso(row["date"]),
                "chat_name": chat_name,
            })
        conn.close()
        return messages
