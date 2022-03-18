import speech_recognition as sr
import action

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        spoken = ""

        try:
            spoken = r.recognize_google(audio)
        except Exception as e:
            print(repr(e))
    return spoken.lower()

WAKE_WORD = ["philip", "philly"]

def wake(TEXT):
    for wakeword in WAKE_WORD:
        if TEXT.count(wakeword) >= 1:
            TEXT = action.awoken()
            print(TEXT)
            action_trigger(TEXT)

def action_trigger(TEXT):
    shutdown(TEXT)
    print(TEXT)
    search(TEXT)


SEARCH_TRIGGERS = ["search",""]

def shutdown(TEXT):
    if TEXT.count('stop') >= 1:
        exit()

def search(TEXT):
    for search in SEARCH_TRIGGERS:
        if TEXT.count(search) >= 1:
            print(action.search_internet(TEXT))