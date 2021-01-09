import listener
import talker


WAKE_WORD = ["whaddup philip", "yo philip", "my boy philip", "hey philip", "yo philly boy"]
print("Start")
while True:
    try:
        TEXT = listener.get_audio()
        print(TEXT)
        for wakeword in WAKE_WORD:
            if TEXT.count(wakeword) >= 1:
                talker.speak("Poggers")
                TEXT = listener.get_audio()
        if TEXT.count('stop') >= 1:
            exit()
    except Exception as e:
        print("ohnoes")
        if hasattr(e, 'message'):
            print(e.message)
        print(e)
        exit()
