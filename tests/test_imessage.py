import sqlite3
import pytest
from imessage_mcp.imessage import IMessageReader, parse_attributed_body


def _create_test_db(tmp_path):
    """Create a test chat.db with realistic schema and data."""
    db_path = tmp_path / "chat.db"
    conn = sqlite3.connect(str(db_path))
    conn.executescript("""
        CREATE TABLE handle (
            ROWID INTEGER PRIMARY KEY,
            id TEXT,
            service TEXT
        );
        CREATE TABLE chat (
            ROWID INTEGER PRIMARY KEY,
            guid TEXT,
            chat_identifier TEXT,
            display_name TEXT
        );
        CREATE TABLE message (
            ROWID INTEGER PRIMARY KEY,
            guid TEXT,
            text TEXT,
            handle_id INTEGER,
            date INTEGER,
            is_from_me INTEGER DEFAULT 0,
            attributedBody BLOB
        );
        CREATE TABLE chat_message_join (
            chat_id INTEGER,
            message_id INTEGER
        );
        CREATE TABLE chat_handle_join (
            chat_id INTEGER,
            handle_id INTEGER
        );

        -- Handles (contacts)
        INSERT INTO handle (ROWID, id, service) VALUES (1, '+15551234567', 'iMessage');
        INSERT INTO handle (ROWID, id, service) VALUES (2, '+15559876543', 'iMessage');
        INSERT INTO handle (ROWID, id, service) VALUES (3, 'bob@example.com', 'iMessage');

        -- Chats
        INSERT INTO chat (ROWID, guid, chat_identifier, display_name)
            VALUES (1, 'chat1', 'chat1', 'Business Ideas');
        INSERT INTO chat (ROWID, guid, chat_identifier, display_name)
            VALUES (2, 'chat2', '+15551234567', '');
        INSERT INTO chat (ROWID, guid, chat_identifier, display_name)
            VALUES (3, 'chat3', 'chat3', NULL);

        -- Messages (dates in Apple epoch nanoseconds — 700000000 * 1e9 = ~2023-03-11)
        INSERT INTO message (ROWID, guid, text, handle_id, date, is_from_me)
            VALUES (1, 'msg1', 'We should build an app', 1, 700000000000000000, 0);
        INSERT INTO message (ROWID, guid, text, handle_id, date, is_from_me)
            VALUES (2, 'msg2', 'Great idea!', 0, 700001000000000000, 1);
        INSERT INTO message (ROWID, guid, text, handle_id, date, is_from_me)
            VALUES (3, 'msg3', 'What about a marketplace?', 2, 700002000000000000, 0);
        INSERT INTO message (ROWID, guid, text, handle_id, date, is_from_me)
            VALUES (4, 'msg4', 'Hello there', 1, 700003000000000000, 0);
        INSERT INTO message (ROWID, guid, text, handle_id, date, is_from_me)
            VALUES (5, 'msg5', NULL, 3, 700004000000000000, 0);

        -- Chat-message joins
        INSERT INTO chat_message_join (chat_id, message_id) VALUES (1, 1);
        INSERT INTO chat_message_join (chat_id, message_id) VALUES (1, 2);
        INSERT INTO chat_message_join (chat_id, message_id) VALUES (1, 3);
        INSERT INTO chat_message_join (chat_id, message_id) VALUES (2, 4);
        INSERT INTO chat_message_join (chat_id, message_id) VALUES (3, 5);

        -- Chat-handle joins (participants)
        INSERT INTO chat_handle_join (chat_id, handle_id) VALUES (1, 1);
        INSERT INTO chat_handle_join (chat_id, handle_id) VALUES (1, 2);
        INSERT INTO chat_handle_join (chat_id, handle_id) VALUES (2, 1);
        INSERT INTO chat_handle_join (chat_id, handle_id) VALUES (3, 3);
    """)
    conn.commit()
    conn.close()
    return str(db_path)


class TestParseAttributedBody:
    def test_returns_none_for_none(self):
        assert parse_attributed_body(None) is None

    def test_returns_none_for_empty_bytes(self):
        assert parse_attributed_body(b"") is None

    def test_returns_none_for_garbage(self):
        assert parse_attributed_body(b"random garbage data") is None


class TestIMessageReader:
    @pytest.fixture
    def reader(self, tmp_path):
        db_path = _create_test_db(tmp_path)
        return IMessageReader(db_path)

    def test_list_chats(self, reader):
        chats = reader.list_chats()
        assert len(chats) == 3
        # Sorted by most recent message
        assert chats[0]["chat_id"] == "chat3"
        assert chats[1]["chat_id"] == "chat2"

    def test_list_chats_with_limit(self, reader):
        chats = reader.list_chats(limit=1)
        assert len(chats) == 1

    def test_list_chats_display_name(self, reader):
        chats = reader.list_chats()
        biz_chat = next(c for c in chats if c["chat_id"] == "chat1")
        assert biz_chat["chat_name"] == "Business Ideas"

    def test_list_chats_empty_display_name_uses_participants(self, reader):
        chats = reader.list_chats()
        dm_chat = next(c for c in chats if c["chat_id"] == "chat2")
        # Empty display name, should fall back to participant identifiers
        assert dm_chat["chat_name"] == "+15551234567"

    def test_list_chats_null_display_name_uses_participants(self, reader):
        chats = reader.list_chats()
        unnamed_chat = next(c for c in chats if c["chat_id"] == "chat3")
        assert unnamed_chat["chat_name"] == "bob@example.com"

    def test_list_chats_participants(self, reader):
        chats = reader.list_chats()
        biz_chat = next(c for c in chats if c["chat_id"] == "chat1")
        assert set(biz_chat["participants"]) == {"+15551234567", "+15559876543"}

    def test_get_messages(self, reader):
        messages = reader.get_messages("chat1")
        assert len(messages) == 3

    def test_get_messages_with_limit(self, reader):
        messages = reader.get_messages("chat1", limit=2)
        assert len(messages) == 2

    def test_get_messages_sender_resolved(self, reader):
        messages = reader.get_messages("chat1")
        senders = [m["sender"] for m in messages]
        assert "+15551234567" in senders

    def test_get_messages_is_from_me(self, reader):
        messages = reader.get_messages("chat1")
        from_me = [m for m in messages if m["sender"] == "Me"]
        assert len(from_me) == 1
        assert from_me[0]["text"] == "Great idea!"

    def test_get_messages_ordered_by_date(self, reader):
        messages = reader.get_messages("chat1")
        texts = [m["text"] for m in messages]
        assert texts == ["We should build an app", "Great idea!", "What about a marketplace?"]

    def test_get_messages_since_filter(self, reader):
        # Use a timestamp between msg2 (700001000s) and msg3 (700002000s)
        # midpoint apple_ns: 700001500000000000 = unix 1678308700 = 2023-03-08T20:51:40Z
        messages = reader.get_messages("chat1", since="2023-03-08T20:51:40Z")
        assert len(messages) == 1
        assert messages[0]["text"] == "What about a marketplace?"

    def test_get_messages_chat_name_included(self, reader):
        messages = reader.get_messages("chat1")
        assert all(m["chat_name"] == "Business Ideas" for m in messages)

    def test_get_messages_nonexistent_chat(self, reader):
        messages = reader.get_messages("nonexistent")
        assert messages == []

    def test_search_messages(self, reader):
        results = reader.search_messages("marketplace")
        assert len(results) == 1
        assert results[0]["text"] == "What about a marketplace?"

    def test_search_messages_case_insensitive(self, reader):
        results = reader.search_messages("GREAT")
        assert len(results) == 1

    def test_search_messages_with_limit(self, reader):
        results = reader.search_messages("a", limit=2)
        assert len(results) <= 2

    def test_search_messages_includes_chat_name(self, reader):
        results = reader.search_messages("Hello")
        assert len(results) == 1
        # chat2 has empty display_name, should show participant
        assert results[0]["chat_name"] == "+15551234567"

    def test_search_messages_no_results(self, reader):
        results = reader.search_messages("xyznonexistent")
        assert results == []
