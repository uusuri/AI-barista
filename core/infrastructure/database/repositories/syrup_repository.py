import sqlite3


class SyrupRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS syrups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            price_per_portion DECIMAL(5,2) NOT NULL,
            unit TEXT DEFAULT 'мл',
            current_quantity DECIMAL(6,1) NOT NULL,
            min_quantity DECIMAL(6,1)
        )
        """
        with self.conn:
            self.conn.execute(query)