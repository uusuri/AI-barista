import pyaudio
import wave

class RecognizerRepository:
    def __init__(self, filename, record_seconds):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024
        self.RECORD_SECONDS = record_seconds
        self.OUTPUT_FILENAME = filename

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )

    def record(self):
        print("Запись началась...")
        frames = []
        for _ in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = self.stream.read(self.CHUNK)
            frames.append(data)
        print("Запись завершена.")
        return frames

    def save_file(self, frames, mode="wb"):
        wf = wave.open(self.OUTPUT_FILENAME, mode)
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        print(f"Файл сохранён: {self.OUTPUT_FILENAME}")

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()


rec = RecognizerRepository("output.wav", 8)
frames = rec.record()
rec.save_file(frames)
rec.close()
