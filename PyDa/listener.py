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
            print("Exception " + str(e))
    return spoken.lower()

WAKE_WORD = ["philip", "philly"]

def wake(TEXT):
    for wakeword in WAKE_WORD:
        if TEXT.count(wakeword) >= 1:
            TEXT = action.awoken()
            action_trigger(TEXT)

def action_trigger(TEXT):
    shutdown(TEXT)
    search(TEXT)


SEARCH_TRIGGERS = ["search",""]

def shutdown(TEXT):
    if TEXT.count('stop' >= 1):
        exit()

def search(TEXT):
    for search in SEARCH_TRIGGERS:
        if TEXT.count(search >= 1):
            action.awoken()