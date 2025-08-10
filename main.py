from core.infrastructure.database.database_manager import DatabaseManager
from core.infrastructure.database.repositories import (
    MenuRepository,
    StockRepository,
    OrderRepository
)
from core.infrastructure.services import MenuService, OrderService
from core.infrastructure.services import OrderItem


def main():
    conn = DatabaseManager().get_connection()

    menu_repo = MenuRepository(conn)
    stock_repo = StockRepository(conn)
    order_repo = OrderRepository(conn)

    menu_service = MenuService(menu_repo, stock_repo)
    order_service = OrderService(stock_repo, menu_repo, order_repo)

    try:
        action = input("Действие (add/update/delete/stock/recipe/order): ").lower()

        if action == "add":
            name = input("Название: ").strip()
            price = float(input("Цена: "))
            menu_service.add_menu_item(name, price)

        elif action == "update":
            name = input("Введите название обновляемой позиции: ").strip()
            price = float(input("Введите стоимость обновляемой позиции: "))
            is_available = input("Доступна ли данная позиция по умолчанию (true/false): ").lower() == "true"
            menu_service.update_menu_item(name, price, is_available)

        elif action == "stock":
            print(menu_service.get_low_stock_alert())

        elif action == "price":
            name = input("Введите название позиции: ").strip()
            print(menu_service.get_price(name))

        elif action == "recipe":
            name = input("Введите название позиции: ").strip()
            print(menu_service.get_recipe(name))

        elif action == "order":
            customer_name = input("Имя клиента: ").strip()
            menu_item_name = input("Название напитка: ").strip()
            quantity = int(input("Количество: "))
            use_syrup = input("Добавить сироп? (y/n): ").lower() == "y"
            syrup_name = input("Название сиропа: ").strip() if use_syrup else None
            syrup_quantity = int(input("Количество сиропа (в мл): ")) if use_syrup else None
            payment_type = input("Тип оплаты (cash/card): ").lower()

            order_item = OrderItem(
                menu_item_name=menu_item_name,
                quantity=quantity,
                syrup_name=syrup_name,
                syrup_quantity=syrup_quantity
            )

            try:
                result = order_service.create_order(
                    customer_name=customer_name,
                    order_items=[order_item],
                    payment_type=payment_type
                )
                print(f"\nЗаказ создан ✅\nID: {result['order_id']}\nСумма: {result['total']}\n")
            except ValueError as e:
                print(f"\nОшибка при создании заказа ❌: {e}")

    finally:
        conn.close()


if __name__ == "__main__":
    main()