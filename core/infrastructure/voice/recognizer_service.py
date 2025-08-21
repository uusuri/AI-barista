import os
from faster_whisper import WhisperModel
from .recognizer_repository import RecognizerRepository

class RecognizerService:
    def __init__(self, model_size = "turbo", repository = RecognizerRepository("output.wav", 5)):
        self.model = WhisperModel(model_size, device='cpu', compute_type='int8')
        self.repository = repository

    @staticmethod
    def delete_temp_file(filename) -> None:
        os.remove(filename)

    def transcribe_dialogue(self) -> list[str]:
        dialogue = []
        segments, info = self.model.transcribe(self.repository.OUTPUT_FILENAME, beam_size=1, language="ru", task="transcribe")

        for segment in segments:
            dialogue.append(segment.text)

        self.delete_temp_file(self.repository.OUTPUT_FILENAME)

        return dialogue