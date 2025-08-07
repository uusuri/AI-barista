import sqlite3
from dataclasses import dataclass

@dataclass
class MenuItem:
    id: int
    name: str
    price: float
    is_available: bool

class MenuRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection

    def add_item(self, name: str, price: float, is_available: bool) -> int:
        query = "INSERT INTO menu (name, price, is_available) VALUES (?, ?, ?)"
        with self.conn:
            cursor = self.conn.execute(query, (name, price, is_available))
            return cursor.lastrowid

    def update_item(self, name: str, price: float, is_available: bool) -> None:
        query = "UPDATE menu SET price = ?, is_available = ? WHERE name = ?"
        with self.conn:
            self.conn.execute(query, (price, is_available, name))

    def get_recipe(self, item_name:str) -> dict[str, float]:
        query = "SELECT ingredient_name, quantity FROM recipe WHERE name = ?"
        with self.conn:
            return dict(self.conn.execute(query, (item_name,)).fetchall())

    def delete_item(self, item_id: int) -> None:
        query = "DELETE FROM menu WHERE id = ?"
        with self.conn:
            self.conn.execute(query, (item_id,))