import sqlite3


class OrderRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection

    def create_order(
            self,
            customer_name: str,
            menu_item_name: str,
            order_summ: float,
            type_of_payment: str,
            syrup_name: str = None,
            syrup_quantity: int = None
    ) -> int:
        query = """
        INSERT INTO orders (
            customer_name,
            menu_item_name,
            syrup_name,
            syrup_quantity,
            order_summ,
            type_of_payment
        ) VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (
            customer_name,
            menu_item_name,
            syrup_name,
            syrup_quantity,
            order_summ,
            type_of_payment
        )

        with self.conn:
            cursor = self.conn.execute(query, params)
            return cursor.lastrowid

    def get_order_details(self, order_id: int) -> dict:
        query = """
        SELECT * FROM orders 
        WHERE id = ?
        """
        with self.conn:
            row = self.conn.execute(query, (order_id,)).fetchone()
            return dict(row) if row else None