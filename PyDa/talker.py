import pyttsx3
import random

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

NO_RESULT_ANSWERS = ["No results were found", "I was unable to find relevant information", "I do not know, try google", "What do I look like, your slave?"]
def no_results():
    speak(random.choice(NO_RESULT_ANSWERS))
