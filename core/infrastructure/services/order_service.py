from typing import List, Dict
from dataclasses import dataclass

from core.infrastructure.database.repositories import (
    MenuRepository,
    OrderRepository,
    StockRepository
)

@dataclass
class OrderItem:
    menu_item_name: str
    quantity: int
    syrup_name: str = None
    syrup_quantity: int = None


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

    def create_order(
            self,
            customer_name: str,
            order_items: List[OrderItem],
            payment_type: str
    ) -> Dict:
        try:
            self._check_ingredients_availability(order_items)

            order_id = self.create_order_record(
                customer_name,
                order_items,
                payment_type
            )

            self.consume_order_ingredients(order_items)

            return {
                'order_id': order_id,
                'status': 'success',
                'total': self.calculate_total(order_items),
                'message': 'Заказ успешно создан'
            }

        except Exception as e:
            raise ValueError(f"Ошибка создания заказа: {str(e)}")


    def _check_ingredients_availability(self, order_items: List[OrderItem]) -> None:
        ingredients_needed = {}
        syrups_needed = {}

        for item in order_items:
            recipe = self.menu_repo.get_recipe(item.menu_item_name)
            if not recipe:
                raise ValueError(f"Рецепт для '{item.menu_item_name}' не найден")

            for name, amount in recipe.get('ingredient', {}).items():
                ingredients_needed[name] = ingredients_needed.get(name, 0) + amount * item.quantity

            for name, amount in recipe.get('syrup', {}).items():
                syrups_needed[name] = syrups_needed.get(name, 0) + amount * item.quantity

            if item.syrup_name and item.syrup_quantity:
                syrups_needed[item.syrup_name] = syrups_needed.get(item.syrup_name, 0) + item.syrup_quantity

        if not self.stock_repo.has_items(ingredients_needed, 'ingredient'):
            raise ValueError("Недостаточно ингредиентов на складе")

        if syrups_needed and not self.stock_repo.has_items(syrups_needed, 'syrup'):
            raise ValueError("Недостаточно сиропов на складе")


    def create_order_record(
            self,
            customer_name: str,
            order_items: List[OrderItem],
            payment_type: str
    ) -> int:
        order_id = self.order_repo.create_order(
            customer_name=customer_name,
            total_sum=self.calculate_total(order_items),
            type_of_payment=payment_type
        )

        for item in order_items:
            self.order_repo.add_order_item(
                order_id=order_id,
                menu_item_name=item.menu_item_name,
                quantity=item.quantity,
                item_price=self.calculate_item_price(item),
                syrup_name=item.syrup_name,
                syrup_quantity=item.syrup_quantity
            )

        return order_id

    def consume_order_ingredients(self, order_items: List[OrderItem]) -> None:
        ingredients_needed = {}
        syrups_needed = {}

        for item in order_items:
            recipe = self.menu_repo.get_recipe(item.menu_item_name)

            if item.syrup_name and item.syrup_quantity:
                syrups_needed[item.syrup_name] = item.syrup_quantity

            for ing_name, qty in recipe.get('ingredient', {}).items():
                ingredients_needed[ing_name] = ingredients_needed.get(ing_name, 0) + qty * item.quantity

            for syrup_name, qty in recipe.get('syrup', {}).items():
                if item.syrup_name == syrup_name:
                    syrups_needed[syrup_name] = syrups_needed.get(syrup_name, 0) + qty * item.syrup_quantity

        self.stock_repo.consume_items(ingredients_needed, 'ingredient')

        if syrups_needed:
            self.stock_repo.consume_items(syrups_needed, 'syrup')

    def calculate_item_price(self, item: OrderItem) -> float:
        base_price = self.menu_repo.get_price(item.menu_item_name)
        total_price = base_price * item.quantity

        if item.syrup_name and item.syrup_quantity:
            syrup_price_per_10ml = self.menu_repo.get_price(item.syrup_name)
            syrup_price = (item.syrup_quantity / 10) * syrup_price_per_10ml
            total_price += syrup_price * item.quantity

        return round(total_price, 2)

    def calculate_total(self, order_items: List[OrderItem]) -> float:
        return sum(self.calculate_item_price(item) for item in order_items)