import speech_recognition as sr


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        spoken = ""

        try:
            spoken = r.recognize_google(audio)
        except Exception as e:
            print(repr(e))
    print(spoken.lower())
    return spoken.lower()


WAKE_WORD = ["philip", "philly"]


def wake(mic_input):
    for wakeword in WAKE_WORD:
        if mic_input.count(wakeword) >= 1:
            # mic_input = action.awoken()
            print(mic_input)
            action_trigger(mic_input)


def action_trigger(mic_input):
    shutdown(mic_input)
    print(mic_input)
    # search(TEXT)


SEARCH_TRIGGERS = ["search", ""]


def shutdown(mic_input):
    if mic_input.count('stop') >= 1:
        exit()
#
#
# def search(TEXT):
#     for search in SEARCH_TRIGGERS:
#         if TEXT.count(search) >= 1:
#             print(action.search_internet(TEXT))
