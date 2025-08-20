from faster_whisper import WhisperModel

model_size = "turbo"

model = WhisperModel(model_size, device="cpu", compute_type="int8")
segments, info = model.transcribe("123.wav", beam_size=7)

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))