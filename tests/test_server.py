import json
import sqlite3
import pytest
from unittest.mock import patch
from imessage_mcp.imessage import IMessageReader
from imessage_mcp.contacts import ContactResolver


def _create_test_dbs(tmp_path):
    """Create both test databases."""
    # iMessage DB
    chat_db = tmp_path / "chat.db"
    conn = sqlite3.connect(str(chat_db))
    conn.executescript("""
        CREATE TABLE handle (ROWID INTEGER PRIMARY KEY, id TEXT, service TEXT);
        CREATE TABLE chat (ROWID INTEGER PRIMARY KEY, guid TEXT, chat_identifier TEXT, display_name TEXT);
        CREATE TABLE message (ROWID INTEGER PRIMARY KEY, guid TEXT, text TEXT, handle_id INTEGER, date INTEGER, is_from_me INTEGER DEFAULT 0, attributedBody BLOB);
        CREATE TABLE chat_message_join (chat_id INTEGER, message_id INTEGER);
        CREATE TABLE chat_handle_join (chat_id INTEGER, handle_id INTEGER);

        INSERT INTO handle VALUES (1, '+15551234567', 'iMessage');
        INSERT INTO chat VALUES (1, 'chat1', 'chat1', 'Business Ideas');
        INSERT INTO message VALUES (1, 'msg1', 'Build an AI startup', 1, 700000000000000000, 0, NULL);
        INSERT INTO chat_message_join VALUES (1, 1);
        INSERT INTO chat_handle_join VALUES (1, 1);
    """)
    conn.commit()
    conn.close()

    # Contacts DB
    contacts_db = tmp_path / "AddressBook-v22.abcddb"
    conn = sqlite3.connect(str(contacts_db))
    conn.executescript("""
        CREATE TABLE ZABCDRECORD (Z_PK INTEGER PRIMARY KEY, ZFIRSTNAME TEXT, ZLASTNAME TEXT, ZORGANIZATION TEXT);
        CREATE TABLE ZABCDPHONENUMBER (Z_PK INTEGER PRIMARY KEY, ZOWNER INTEGER, ZFULLNUMBER TEXT);
        CREATE TABLE ZABCDEMAILADDRESS (Z_PK INTEGER PRIMARY KEY, ZOWNER INTEGER, ZADDRESS TEXT);

        INSERT INTO ZABCDRECORD VALUES (1, 'Alice', 'Smith', NULL);
        INSERT INTO ZABCDPHONENUMBER VALUES (1, 1, '+15551234567');
    """)
    conn.commit()
    conn.close()

    return str(chat_db), str(contacts_db)


class TestServerIntegration:
    """Test that server tools return contact-resolved messages."""

    @pytest.fixture
    def dbs(self, tmp_path):
        return _create_test_dbs(tmp_path)

    def test_get_messages_resolves_contacts(self, dbs):
        chat_db, contacts_db = dbs
        reader = IMessageReader(chat_db)
        resolver = ContactResolver(contacts_db)
        messages = reader.get_messages("chat1")
        # Resolve contacts
        for msg in messages:
            if msg["sender"] != "Me":
                msg["sender"] = resolver.resolve(msg["sender"])
        assert messages[0]["sender"] == "Alice Smith"

    def test_list_chats_resolves_participants(self, dbs):
        chat_db, contacts_db = dbs
        reader = IMessageReader(chat_db)
        resolver = ContactResolver(contacts_db)
        chats = reader.list_chats()
        for chat in chats:
            chat["participants"] = [resolver.resolve(p) for p in chat["participants"]]
        assert "Alice Smith" in chats[0]["participants"]

    def test_search_resolves_contacts(self, dbs):
        chat_db, contacts_db = dbs
        reader = IMessageReader(chat_db)
        resolver = ContactResolver(contacts_db)
        results = reader.search_messages("AI startup")
        for msg in results:
            if msg["sender"] != "Me":
                msg["sender"] = resolver.resolve(msg["sender"])
        assert results[0]["sender"] == "Alice Smith"
