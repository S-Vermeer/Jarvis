import listener
import talker

WAKE_WORD = ["whaddup phillip", "yo phillip", "my boy phillip", "hey phillip", "yo philly boy"]
print("Start")
while True:
    try:
        TEXT = listener.get_audio()
        print(TEXT)
        for wakeword in WAKE_WORD:
            if TEXT.count(wakeword) >= 1:
                talker.speak("Poggers")
                TEXT = listener.get_audio()
    except Exception as e:
        print("ohnoes")
        print(e)
        exit()
