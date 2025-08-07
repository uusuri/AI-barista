from core.infrastructure.database.database_manager import DatabaseManager
from core.infrastructure.database.repositories import (
    MenuRepository,
    SyrupRepository,
    StockRepository
)
from core.infrastructure.services import MenuService


def main():
    db = DatabaseManager()
    conn = db.get_connection()

    syrup_repo = SyrupRepository(conn)
    menu_repo = MenuRepository(conn)
    stock_repo = StockRepository(conn)
    menu_service = MenuService(menu_repo, stock_repo)

    syrup_repo.create_table()

    try:
        action = input("Действие (add/update/delete/stock): ").lower()

        if action == "add":
            name = input("Название: ")
            price = float(input("Цена: "))
            menu_service.add_menu_item(name, price)

        if action == "update":
            name = input("Введите название обновляемой позиции: ")
            price = float(input("Введите стоимость обновляемой позиции: "))
            is_available = input("Доступна ли данная позиция по умолчанию (true/false): ").lower() == "true"
            menu_service.update_menu_item(name, price, is_available)

        elif action == "stock":
            print(menu_service.get_low_stock_alert())

        elif action == "recipe":
            name = input("Введите название позиции: ")
            menu_service.get_recipe(name)

    finally:
        conn.close()


if __name__ == "__main__":
    main()