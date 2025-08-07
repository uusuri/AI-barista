import sqlite3
from pathlib import Path

class DatabaseManager:
    _instance = None

    def __new__(cls, db_path: str = "/Users/uusuri/PycharmProjects/AI-barista/data/coffee_shop.db"):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.db_path = Path(__file__).parent.parent.parent / db_path
        return cls._instance

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn