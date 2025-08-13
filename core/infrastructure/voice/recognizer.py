import vosk
import pyaudio

def recognize_speech_vosk():
    model = vosk.Model("/Users/uusuri/PycharmProjects/AI-barista/data/vosk-model-ru-0.42")
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