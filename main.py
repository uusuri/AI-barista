from core.infrastructure.database.database_manager import DatabaseManager
from core.infrastructure.database.repositories import (
    MenuRepository,
    StockRepository,
    OrderRepository
)
from core.infrastructure.services import MenuService, OrderService
from core.infrastructure.services import OrderItem

from ai_assistant.assistant_repository import AssistantRepository
from ai_assistant.assistant_service import AssistantService
from ai_assistant.parser import clean_dialogue

from core.infrastructure.voice import RecognizerRepository
from core.infrastructure.voice import RecognizerService

def main():
    conn = DatabaseManager().get_connection()

    menu_repo = MenuRepository(conn)
    stock_repo = StockRepository(conn)
    order_repo = OrderRepository(conn)
    recognizer_repository = RecognizerRepository("output.wav", 8)

    recognizer_service = RecognizerService('turbo', recognizer_repository)
    menu_service = MenuService(menu_repo, stock_repo)
    order_service = OrderService(stock_repo, menu_repo, order_repo)

    dialogue = clean_dialogue(recognizer_service.transcribe_dialogue())

    menu = menu_service.get_full_menu_items()

    repo = AssistantRepository(menu, model= "gemma3:12b")
    service = AssistantService(repo)

    response = repo.get_response(dialogue)
    order = service.extract_order(response)

    print(order)

    try:
        action = input("Действие (add/update/delete/stock/recipe/order): ").lower()

        match action:
            case "add":
                name = input("Название: ").strip()
                price = float(input("Цена: "))
                menu_service.add_menu_item(name, price)

            case "menu":
                print(menu_service.get_full_menu_items())

            case "update":
                name = input("Введите название обновляемой позиции: ").strip()
                price = float(input("Введите стоимость обновляемой позиции: "))
                is_available = input("Доступна ли данная позиция по умолчанию (true/false): ").lower() == "true"
                menu_service.update_menu_item(name, price, is_available)

            case "stock":
                print(menu_service.get_low_stock_alert())

            case "price":
                name = input("Введите название позиции: ").strip()
                print(menu_service.get_price(name))

            case "recipe":
                name = input("Введите название позиции: ").strip()
                print(menu_service.get_recipe(name))

            case "order":
                customer_name = input("Имя клиента: ").strip()
                raw_items = order.split(",")
                order_items = []

                for item_in_order in raw_items:
                    parts = item_in_order.strip().split()

                    quantity = int(parts[-1])

                    menu_item_name = " ".join(parts[:-1])
                    syrup_name = None
                    syrup_quantity = None

                    if "сироп" in parts:
                        syrup_index = parts.index("сироп")

                        menu_item_name = " ".join(parts[:syrup_index])
                        syrup_name = parts[syrup_index + 1]
                        syrup_quantity = int(parts[-2])
                        quantity = int(parts[-1])

                    order_items.append(OrderItem(
                        menu_item_name=menu_item_name,
                        quantity=quantity,
                        syrup_name=syrup_name,
                        syrup_quantity=syrup_quantity
                    ))

                    payment_type = input("Тип оплаты (cash/card): ").lower()
                    confirm = True if input("Подтвердить оплату? ") == "y" else False

                    if confirm:
                        try:
                            result = order_service.create_order(
                                customer_name=customer_name,
                                order_items=order_items,
                                payment_type=payment_type
                            )
                            print(f"\nЗаказ создан ✅\nID: {result['order_id']}\nСумма: {result['total']}\n")
                        except ValueError as e:
                            print(f"\nОшибка при создании заказа ❌: {e}")

    finally:
        conn.close()


if __name__ == "__main__":
    main()