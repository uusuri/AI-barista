from .assistant_repository import AssistantRepository

class AssistantService:
    def __init__(self, repository: AssistantRepository):
        self.repository = repository

    def extract_order(self, response: str) -> str:
        return response