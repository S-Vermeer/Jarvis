import pyttsx3
import random


def init_engine():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    return engine


def speak(output):
    engine = init_engine()
    engine.say(output)
    engine.runAndWait()
    return output


NO_RESULT_ANSWERS = ["No results were found", "I was unable to find relevant information", "I do not know, try google", "What do I look like, your slave?"]


def no_results():
    speak(random.choice(NO_RESULT_ANSWERS))
