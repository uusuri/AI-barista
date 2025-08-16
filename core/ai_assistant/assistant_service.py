from .assistant_repository import AssistantRepository
from .prompt_templates import ORDER_EXTRACTION_PROMPT
import json

class AssistantService:
    def __init__(self, repository: AssistantRepository, menu: dict):
        self.repository = repository
        self.menu = menu

    def extract_order(self, dialogue: str) -> dict:
        prompt = ORDER_EXTRACTION_PROMPT.format(
            dialogue=dialogue,
            drinks=self.menu.get("drinks", ""),
            syrups=self.menu.get("syrups", "")
        )
        raw_response = self.repository.run_ollama(prompt)

        try:
            return json.loads(raw_response)
        except Exception:
            return {"raw_text": raw_response}
