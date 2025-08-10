import sqlite3


class SyrupRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection