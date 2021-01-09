import speech_recognition as sr

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        spoken = ""

        try:
            spoken = r.recognize_google(audio)
            print(spoken)
        except Exception as e:
            print("Exception " + str(e))
    return spoken.lower()