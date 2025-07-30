from gigachat import GigaChat
import speech_recognition as sr

giga = GigaChat(credentials='NTY0Yjc3MTktMmExYy00YWIzLWJkOTMtOTU0YzE2MzJjNzlmOmY5MTdmN2I4LTFlNzAtNDlmNC1hN2RlLTc1OTM1ZDJhZWQ2OQ==', verify_ssl_certs=False)

def recognize_speech():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, phrase_time_limit = 10)
        text = r.recognize_google(audio, language = "ru-RU")

        return text

def chat_with_gigachat():
    print("💬 GigaChat Console (Cкажите 'выход' чтобы закрыть)")
    giga.chat(open("/Users/uusuri/Documents/PycharmProjects/Education/.venv/rules/rules.txt", "r").read())

    while True:
        user_input = recognize_speech()
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
    pass
    # chat_with_gigachat()