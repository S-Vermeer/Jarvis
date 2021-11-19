import wolframalpha as wa
import wikipedia as wp

# ᕙ(`▿´)ᕗ Connect to wolfram ᕙ(`▿´)ᕗ
APP_ID = 'QW82JW-Q5U44TYEE9'  # get your own at https://products.wolframalpha.com/api/
CLIENT = wa.Client(APP_ID)

def searchInfoOnline(inputQuery):
    try: # ᕙ(`▿´)ᕗ Try to get results for both Wiki and Wolframᕙ(`▿´)ᕗ
        wiki_res = wp.summary(inputQuery,sentences=2)
        res = CLIENT.query(inputQuery)
        wolfram_res = next(res.results).text # ᕙ(`▿´)ᕗ print top wolframalpha results of inputᕙ(`▿´)ᕗ

        return "Wolfram Result: " + wolfram_res, "Wikipedia Result: " + wiki_res

    except (wp.exceptions.DisambiguationError,wp.exceptions.PageError): # ᕙ(`▿´)ᕗ Get only wolfram if wiki throws exceptions ᕙ(`▿´)ᕗ
        try:
            res = CLIENT.query(inputQuery)
            wolfram_res = next(res.results).text # ᕙ(`▿´)ᕗ print top wolframalpha results of inputᕙ(`▿´)ᕗ
            return wolfram_res

        except (StopIteration,AttributeError): # ᕙ(`▿´)ᕗ And if wolfram also doesnt work, say that no results were foundᕙ(`▿´)ᕗ
            return "No results found"

    except (StopIteration,AttributeError):
        try:
            wiki_res = wp.summary(inputQuery,sentences=2)
            return wiki_res

        except:
            return "No results found"

    except: # ᕙ(`▿´)ᕗ All the attributes inside your window. ᕙ(`▿´)ᕗ
        return "No results found"
