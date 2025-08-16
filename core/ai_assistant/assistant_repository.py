import subprocess

class AssistantRepository:
    def __init__(self, model: str = "gemma3:12b"):
        self.model = model

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
