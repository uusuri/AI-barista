from .assistant_repository import AssistantRepository
import re

class AssistantService:
    def __init__(self, repository: AssistantRepository):
        self.repository = repository

    def extract_order(self, response: str) -> str:
        order = re.sub(r'(json`)', "", response)
        return order