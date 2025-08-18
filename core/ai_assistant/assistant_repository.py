import subprocess
from .prompt_templates import ORDER_EXTRACTION_PROMPT

class AssistantRepository:
    def __init__(self, menu:dict, model: str = "gemma3:12b"):
        self.model = model
        self.menu = menu

    def run_ollama(self, prompt: str) -> str:
        try:
            result = subprocess.run(
                ["ollama", "run", self.model],
                input=prompt,
                text=True,
                capture_output=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Ollama error: {e.stderr}")

    def get_response(self, dialogue: str) -> str:
        prompt = ORDER_EXTRACTION_PROMPT.format(
            dialogue=dialogue,
            drinks=self.menu.get("drinks", ""),
            syrups=self.menu.get("syrups", "")
        )
        response = self.run_ollama(prompt)

        return response
