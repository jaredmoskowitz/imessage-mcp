import sqlite3
import tempfile
import os
import pytest
from imessage_mcp.contacts import ContactResolver, normalize_phone


class TestNormalizePhone:
    def test_strips_formatting(self):
        assert normalize_phone("(555) 123-4567") == "5551234567"

    def test_strips_country_code(self):
        assert normalize_phone("+15551234567") == "5551234567"

    def test_strips_spaces_and_dashes(self):
        assert normalize_phone("555 - 123 - 4567") == "5551234567"

    def test_short_number_unchanged(self):
        assert normalize_phone("12345") == "12345"

    def test_international_number_takes_last_10(self):
        assert normalize_phone("+445551234567") == "5551234567"


class TestContactResolver:
    @pytest.fixture
    def contacts_db(self, tmp_path):
        db_path = tmp_path / "AddressBook-v22.abcddb"
        conn = sqlite3.connect(str(db_path))
        conn.execute("""
            CREATE TABLE ZABCDRECORD (
                Z_PK INTEGER PRIMARY KEY,
                ZFIRSTNAME TEXT,
                ZLASTNAME TEXT,
                ZORGANIZATION TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE ZABCDPHONENUMBER (
                Z_PK INTEGER PRIMARY KEY,
                ZOWNER INTEGER,
                ZFULLNUMBER TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE ZABCDEMAILADDRESS (
                Z_PK INTEGER PRIMARY KEY,
                ZOWNER INTEGER,
                ZADDRESS TEXT
            )
        """)
        conn.execute(
            "INSERT INTO ZABCDRECORD (Z_PK, ZFIRSTNAME, ZLASTNAME) VALUES (1, 'Alice', 'Smith')"
        )
        conn.execute(
            "INSERT INTO ZABCDRECORD (Z_PK, ZFIRSTNAME, ZLASTNAME) VALUES (2, 'Bob', NULL)"
        )
        conn.execute(
            "INSERT INTO ZABCDRECORD (Z_PK, ZFIRSTNAME, ZLASTNAME, ZORGANIZATION) VALUES (3, NULL, NULL, 'Acme Corp')"
        )
        conn.execute(
            "INSERT INTO ZABCDPHONENUMBER (Z_PK, ZOWNER, ZFULLNUMBER) VALUES (1, 1, '+1 (555) 123-4567')"
        )
        conn.execute(
            "INSERT INTO ZABCDPHONENUMBER (Z_PK, ZOWNER, ZFULLNUMBER) VALUES (2, 2, '555-987-6543')"
        )
        conn.execute(
            "INSERT INTO ZABCDEMAILADDRESS (Z_PK, ZOWNER, ZADDRESS) VALUES (1, 1, 'alice@example.com')"
        )
        conn.commit()
        conn.close()
        return str(db_path)

    def test_resolve_phone_number(self, contacts_db):
        resolver = ContactResolver(contacts_db)
        assert resolver.resolve("+15551234567") == "Alice Smith"

    def test_resolve_phone_with_different_format(self, contacts_db):
        resolver = ContactResolver(contacts_db)
        assert resolver.resolve("(555) 123-4567") == "Alice Smith"

    def test_resolve_first_name_only(self, contacts_db):
        resolver = ContactResolver(contacts_db)
        assert resolver.resolve("5559876543") == "Bob"

    def test_resolve_organization_fallback(self, contacts_db):
        resolver = ContactResolver(contacts_db)
        # No phone for org, so won't resolve
        assert resolver.resolve("+15550000000") == "+15550000000"

    def test_resolve_email(self, contacts_db):
        resolver = ContactResolver(contacts_db)
        assert resolver.resolve("alice@example.com") == "Alice Smith"

    def test_resolve_unknown_returns_identifier(self, contacts_db):
        resolver = ContactResolver(contacts_db)
        assert resolver.resolve("+15559999999") == "+15559999999"

    def test_missing_db_degrades_gracefully(self, tmp_path):
        resolver = ContactResolver(str(tmp_path / "nonexistent.db"))
        assert resolver.resolve("+15551234567") == "+15551234567"
