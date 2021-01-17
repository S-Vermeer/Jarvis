import talker
import listener
import wikipedia as wp
#import connector
import wolframalpha as wa



app_id = 'QW82JW-Q5U44TYEE9'  # get your own at https://products.wolframalpha.com/api/

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

        answer = "Wolfram Result: " + wolfram_res + "Wikipedia Result: " + wiki_res
        return answer

    except (wp.exceptions.DisambiguationError,wp.exceptions.PageError): # ᕙ(`▿´)ᕗ Get only wolfram if wiki throws exceptions ᕙ(`▿´)ᕗ
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