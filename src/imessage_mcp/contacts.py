import re
import sqlite3
from pathlib import Path


DEFAULT_ADDRESSBOOK_PATH = str(
    Path.home() / "Library" / "Application Support" / "AddressBook" / "AddressBook-v22.abcddb"
)


def normalize_phone(phone: str) -> str:
    """Strip a phone number to its last 10 digits for comparison."""
    digits = re.sub(r"\D", "", phone)
    if len(digits) > 10:
        digits = digits[-10:]
    return digits


class ContactResolver:
    def __init__(self, db_path: str = DEFAULT_ADDRESSBOOK_PATH):
        self._phone_map: dict[str, str] = {}
        self._email_map: dict[str, str] = {}
        self._load(db_path)

    def _load(self, db_path: str) -> None:
        if not Path(db_path).exists():
            return
        try:
            conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
            # Build phone -> name map
            rows = conn.execute("""
                SELECT r.ZFIRSTNAME, r.ZLASTNAME, r.ZORGANIZATION, p.ZFULLNUMBER
                FROM ZABCDRECORD r
                JOIN ZABCDPHONENUMBER p ON r.Z_PK = p.ZOWNER
                WHERE p.ZFULLNUMBER IS NOT NULL
            """).fetchall()
            for first, last, org, phone in rows:
                name = _build_name(first, last, org)
                if name:
                    self._phone_map[normalize_phone(phone)] = name

            # Build email -> name map
            rows = conn.execute("""
                SELECT r.ZFIRSTNAME, r.ZLASTNAME, r.ZORGANIZATION, e.ZADDRESS
                FROM ZABCDRECORD r
                JOIN ZABCDEMAILADDRESS e ON r.Z_PK = e.ZOWNER
                WHERE e.ZADDRESS IS NOT NULL
            """).fetchall()
            for first, last, org, email in rows:
                name = _build_name(first, last, org)
                if name:
                    self._email_map[email.lower()] = name

            conn.close()
        except (sqlite3.Error, OSError):
            return

    def resolve(self, identifier: str) -> str:
        """Resolve a phone number or email to a contact name. Returns the identifier if not found."""
        # Try email first (contains @)
        if "@" in identifier:
            return self._email_map.get(identifier.lower(), identifier)
        # Try phone
        normalized = normalize_phone(identifier)
        return self._phone_map.get(normalized, identifier)


def _build_name(first: str | None, last: str | None, org: str | None) -> str | None:
    parts = [p for p in (first, last) if p]
    if parts:
        return " ".join(parts)
    return org
