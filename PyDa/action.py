import talker
import listener
import wikipedia as wp

import os
from dotenv import load_dotenv
#import connector
import wolframalpha as wa

load_dotenv()
app_id = os.getenv('APP_ID')

def connect_wa():
    client = wa.Client(app_id)
    return client

def awoken():
    talker.speak("poggers")
    TEXT = listener.get_audio()
    return TEXT

def search_internet(inputQuery):
    client = connect_wa()
    try: # ᕙ(`▿´)ᕗ Try to get results for both Wiki and Wolframᕙ(`▿´)ᕗ
        wiki_res = wp.summary(inputQuery,sentences=2)
        res = client.query(inputQuery)
        wolfram_res = next(res.results).text # ᕙ(`▿´)ᕗ print top wolframalpha results of inputᕙ(`▿´)ᕗ
        talker.speak(wolfram_res)

        answer = "Wolfram Result: " + wolfram_res + " \n Wikipedia Result: " + wiki_res
        return answer

    except (wp.exceptions.DisambiguationError,wp.exceptions.PageError,wp.exceptions.WikipediaException): # ᕙ(`▿´)ᕗ Get only wolfram if wiki throws exceptions ᕙ(`▿´)ᕗ
        try:
            res = client.query(inputQuery)
            wolfram_res = next(res.results).text # ᕙ(`▿´)ᕗ print top wolframalpha results of inputᕙ(`▿´)ᕗ
            talker.speak(wolfram_res)
            return wolfram_res

        except (StopIteration,AttributeError):
            try:
                wiki_res = wp.summary(inputQuery,sentences=2)
                return wiki_res
            except:
                talker.no_results()

        except (StopIteration,AttributeError): # ᕙ(`▿´)ᕗ And if wolfram also doesnt work, say that no results were foundᕙ(`▿´)ᕗ
            talker.no_results()

        except: # ᕙ(`▿´)ᕗ All the attributes inside your window. ᕙ(`▿´)ᕗ
            talker.no_results()
            return "No results"