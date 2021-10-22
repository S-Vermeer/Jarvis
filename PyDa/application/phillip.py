import listener

while True:
    try:
        TEXT = listener.get_audio().lower()
        print(TEXT)
        listener.wake(TEXT)
        listener.shutdown(TEXT)
    except Exception as e:
        print("ohnoes")
        print(repr(e))
        exit()
