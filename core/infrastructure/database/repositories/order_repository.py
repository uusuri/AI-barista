import sqlite3


class OrderRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn


    def create_order(self, customer_name: str, total_sum: float, type_of_payment: str) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO orders (customer_name, order_time, total_sum, type_of_payment)
            VALUES (?, datetime('now'), ?, ?)
            """,
            (customer_name, total_sum, type_of_payment)
        )
        return cursor.lastrowid


    def add_order_item(
        self,
        order_id: int,
        menu_item_name: str,
        quantity: int,
        item_price: float,
        syrup_name: str = None,
        syrup_quantity: int = None
    ) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO order_items 
            (order_id, menu_item_name, quantity, item_price) 
            VALUES (?, ?, ?, ?)
            """,
            (order_id, menu_item_name, quantity, item_price)
        )
        item_id = cursor.lastrowid

        if syrup_name and syrup_quantity:
            self.add_syrup_to_item(item_id, syrup_name, syrup_quantity)

        return item_id


    def add_syrup_to_item(
        self,
        item_id: int,
        syrup_name: str,
        syrup_quantity: int
    ):
        self.conn.cursor().execute(
            """
            INSERT INTO order_item_syrups 
            (order_item_id, syrup_name, syrup_quantity) 
            VALUES (?, ?, ?)
            """,
            (item_id, syrup_name, syrup_quantity)
        )