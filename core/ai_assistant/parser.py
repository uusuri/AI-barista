import re

REMOVE_WORDS = [
    "здравствуйте", "добрый день", "привет",
    "как ваши дела", "как дела", "все хорошо", "всё хорошо",
    "спасибо", "пожалуйста"
]


def remove_words(text: str) -> str:
    text = text.lower().strip()

    for phrase in REMOVE_WORDS:
        text = text.replace(phrase, "")

    text = re.sub(r"\s+", " ", text).strip()
    return text


def clean_dialog(dialog_lines: list[str]) -> str:
    cleaned_lines = []
    for line in dialog_lines:
        cleaned = re.sub(r'[?,!.]', '', remove_words(line))
        if cleaned:
            cleaned_lines.append(cleaned)
    return "\n".join(cleaned_lines)


dialog_lines = [
    "Здравствуйте, как ваши дела?",
    "Всё хорошо, спасибо",
    "Можно мне пожалуйста раф на кокосовом молоке?",
    "А вам с каким сиропом?",
    "Ваниль, и раф лучше на обычном, пожалуйста"
]

print(clean_dialog(dialog_lines))