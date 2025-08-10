import sqlite3
from dataclasses import dataclass
from typing import Dict

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

    def get_recipe(self, menu_item_name: str) -> Dict[str, Dict[str, float]]:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT ingredient_name, quantity, ingredient_type
            FROM recipe
            WHERE menu_item_name = ?
            """,
            (menu_item_name,)
        )
        rows = cursor.fetchall()
        if not rows:
            return {}

        recipe = {'ingredient': {}, 'syrup': {}}
        for name, amount, ingredient_type in rows:
            if ingredient_type not in recipe:
                continue
            recipe[ingredient_type][name] = recipe[ingredient_type].get(name, 0) + amount

        return recipe


    def get_price(self, menu_item_name: str) -> float:
        cursor = self.conn.cursor()
        cursor.execute("SELECT price FROM menu WHERE name = ?", (menu_item_name,))
        row = cursor.fetchone()
        if not row:
            cursor.execute("SELECT price_per_portion FROM syrups WHERE name = ?", (menu_item_name,))
            row = cursor.fetchone()
        return row[0]


    def delete_item(self, item_id: int) -> None:
        query = "DELETE FROM menu WHERE id = ?"
        with self.conn:
            self.conn.execute(query, (item_id,))