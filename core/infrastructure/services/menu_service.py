from core.infrastructure.database.repositories.menu_repository import MenuRepository
from core.infrastructure.database.repositories.stock_repository import StockRepository


class MenuService:
    def __init__(self, menu_repo: MenuRepository, stock_repo: StockRepository):
        self.menu_repo = menu_repo
        self.stock_repo = stock_repo


    def add_menu_item(self, name: str, price: float) -> int:
        if price <= 0:
            raise ValueError("Цена должна быть положительной")
        return self.menu_repo.add_item(name, price, is_available=True)


    def update_menu_item(self, name: str, price: float, is_available:bool) -> None:
        return self.menu_repo.update_item(name, price, is_available=is_available)


    def get_low_stock_alert(self) -> str:
        low_stock = self.stock_repo.get_low_stock_items()
        if not low_stock:
            return "Все ингредиенты в норме"
        return "\n".join(f"{name}: {qty}" for name, qty in low_stock)


    def get_price(self, name:str) -> float:
        price = self.menu_repo.get_price(name)
        return price


    def get_recipe(self, name:str) -> dict[str, dict[str, float]]:
        recipe = self.menu_repo.get_recipe(name)
        if not recipe:
            raise ValueError(f"Рецепт для '{name}' не найден")
        return recipe