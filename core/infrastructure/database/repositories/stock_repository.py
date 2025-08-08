import sqlite3
from typing import Dict, List, Tuple

class StockRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def consume_items(self, items: Dict[str, float], item_type: str) -> bool:
        cursor = self.conn.cursor()
        table = 'ingredients' if item_type == 'ingredient' else 'syrup'

        for name, qty in items.items():
            cursor.execute(f"SELECT stock FROM {table} WHERE name = ?", (name,))
            row = cursor.fetchone()
            if not row or row[0] < qty:
                return False

        for name, qty in items.items():
            cursor.execute(
                f"UPDATE {table} SET stock = stock - ? WHERE name = ?",
                (qty, name)
            )
        return True


    def get_low_stock_items(self) -> List[Tuple[str, float]]:
        query = """
        SELECT name, current_quantity 
        FROM ingredients 
        WHERE current_quantity < min_quantity
        UNION ALL
        SELECT name, current_quantity 
        FROM syrups 
        WHERE current_quantity < min_quantity
        ORDER BY current_quantity ASC
        """
        with self.conn:
            return [
                (row["name"], row["current_quantity"])
                for row in self.conn.execute(query).fetchall()
            ]

    def get_current_quantity(self, item_name: str, item_type: str) -> float:
        table = 'ingredients' if item_type == 'ingredient' else 'syrups'
        query = f"SELECT current_quantity FROM {table} WHERE name = ?"
        with self.conn:
            result = self.conn.execute(query, (item_name,)).fetchone()
            return result[0] if result else 0.0