import subprocess
import json
from core.infrastructure.services import OrderItem
from core.ai_assistant.prompt_templates import ORDER_EXTRACTION_TEMPLATE


def run_ollama(prompt: str, model: str = "mistral") -> str:
    result = subprocess.run(
        ["ollama", "run", model],
        input = prompt,
        text = True,
        capture_output=True
    )
    return result.stdout.strip()


def parse_order_from_dialog(dialog: list[str], menu: dict) -> list[OrderItem]:
    template = ORDER_EXTRACTION_TEMPLATE
    response = run_ollama(template)

    try:
        data = json.loads(response)
        items = []
        for item in data:
            items.append(OrderItem(
                menu_item_name=item["menu_item_name"],
                quantity=item["quantity"],
                syrup_name=item.get("syrup_name"),
                syrup_quantity=item.get("syrup_quantity")
            ))
        return items

    except Exception as e:
        print("Ошибка парсинга JSON:", e)
        print("Ответ модели:", response)
        return []