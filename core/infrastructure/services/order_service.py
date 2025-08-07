from core.infrastructure.database.repositories.stock_repository import StockRepository
from core.infrastructure.database.repositories.menu_repository import MenuRepository
from core.infrastructure.database.repositories.order_repository import OrderRepository

class OrderService:
    def __init__(
        self,
        stock_repo: StockRepository,
        menu_repo: MenuRepository,
        order_repo: OrderRepository
    ):
        self.stock_repo = stock_repo
        self.menu_repo = menu_repo
        self.order_repo = order_repo

    def process_order(
        self,
        customer_name: str,
        menu_item_name: str,
        order_summ: float,
        type_of_payment: str,
        syrup_name: str = None,
        syrup_quantity: int = None
    ) -> int:
        recipe = self.menu_repo.get_recipe(menu_item_name)
        if not recipe:
            raise ValueError(f"Позиция '{menu_item_name}' не найдена в меню")

        if syrup_name and syrup_quantity:
            recipe[syrup_name] = recipe.get(syrup_name, 0) + syrup_quantity

        if not self.stock_repo.consume_ingredients(recipe):
            raise ValueError("Недостаточно ингредиентов на складе")

        return self.order_repo.create_order(
            customer_name=customer_name,
            menu_item_name=menu_item_name,
            order_summ=order_summ,
            type_of_payment=type_of_payment,
            syrup_name=syrup_name,
            syrup_quantity=syrup_quantity
        )