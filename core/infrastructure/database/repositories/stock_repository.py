import sqlite3
from typing import List, Tuple

class StockRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection

    def consume_ingredients(self, items: dict[str, float]) -> bool:
        try:
            with self.conn:
                for name, amount in items.items():
                    check_query = """SELECT 1 FROM ingredients WHERE name = ? AND current_quantity >= ?"""
                    if not self.conn.execute(check_query, (name, amount,)).fetchone():
                        return False

                for name, amount in items.items():
                    update_query = """
                                UPDATE ingredients 
                                SET current_quantity = current_quantity - ? 
                                WHERE name = ?
                                """
                    self.conn.execute(update_query, (amount, name))
                return True
        except sqlite3.OperationalError:
            return False

    def get_low_stock_items(self) -> List[Tuple[str, float]]:
        query = """
        SELECT name, current_quantity 
        FROM ingredients 
        WHERE current_quantity < min_quantity
        ORDER BY current_quantity ASC
        """
        with self.conn:
            return [
                (row["name"], row["current_quantity"])
                for row in self.conn.execute(query).fetchall()
            ]