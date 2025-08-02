import vosk
import pyaudio
from gigachat import GigaChat

giga = GigaChat(credentials='NTY0Yjc3MTktMmExYy00YWIzLWJkOTMtOTU0YzE2MzJjNzlmOmY5MTdmN2I4LTFlNzAtNDlmNC1hN2RlLTc1OTM1ZDJhZWQ2OQ==', verify_ssl_certs=False)


def recognize_speech_vosk():
    model = vosk.Model("/Users/uusuri/PycharmProjects/AI-barista/vosk-model-ru-0.42")
    recognizer = vosk.KaldiRecognizer(model, 16000)

    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)

    print("Говорите... (для остановки нажмите Ctrl+C)")
    while True:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            return vosk_result_to_text(recognizer.Result())


def vosk_result_to_text(result):
    import json
    return json.loads(result)["text"]


def chat_with_gigachat():
    print("💬 GigaChat Console (Cкажите 'выход' чтобы закрыть)")
    giga.chat(open("/Users/uusuri/Documents/PycharmProjects/Education/.venv/rules/rules.txt", "r").read())

    while True:
        user_input = recognize_speech_vosk()
        print(user_input)

        if user_input.lower() in ["выход", "exit", "quit", "q"]:
            print("До свидания!")
            break

        try:
            response = giga.chat(user_input)
            print(f"GigaChat: {response.choices[0].message.content}")

        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    chat_with_gigachat()