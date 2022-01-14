"""
Comment legend
ᕙ(`-´)ᕗ - Explanation
ʕ•́ᴥ•̀ʔっ - To do
(ㆆ_ㆆ) - Bug
"""
import logging

import wikipedia as wp
import wolframalpha as wa

from discord.ext import commands

drive = None
http = None
cogs = None
app_id = None
bot = commands.Bot(command_prefix="")


def init(current_globals):
    global drive
    global http
    global cogs
    global app_id
    global bot
    drive = current_globals['drive']
    http = current_globals['http']
    cogs = current_globals['cogs']
    bot = current_globals['bot']
    app_id = current_globals['app_id']


# ᕙ(`-´)ᕗ Connect to the wolfram alpha client
def connect_wa():
    client = wa.Client(app_id)
    return client


# ᕙ(`-´)ᕗ Check which action is asked for after phillip is called
async def search_method(message):
    if message.content.lower().count("how are you") >= 1:
        return cogs['WellbeingCog'].mood(message)

    if message.content.lower().count("search") >= 1:
        return search_answer(message)

    if message.content.lower().count("sleep") >= 1:
        return cogs['WellbeingCog'].sleep_helper(message)

    if message.content.lower().count("hype") >= 1:
        return cogs['WellbeingCog'].complimenter(message)

    if message.content.lower().count("jesse") >= 1:
        return jesse_hype(message)

    if message.content.lower().count("drive") >= 1:
        return await cogs["GoogleDriveCog"].drive_functions(message)

    if message.content.lower().count("morning") >= 1:
        return good_morning(message.guild, cogs['UserCommunicationCog'])

    if message.content.lower().count("tone") and message.content.lower().count("/") >= 1:
        return await cogs['ToneTagCog'].specific_explanation(message)


# ᕙ(`-´)ᕗ Hypes Jesse, a mod from the Avieno discord
async def jesse_hype(message):
    uid = '<@745738275968516176>'
    response = (
            f":regional_indicator_w: :regional_indicator_e:   :regional_indicator_l: :regional_indicator_o: "
            f":regional_indicator_v: :regional_indicator_e:   :regional_indicator_j: :regional_indicator_e: "
            f":regional_indicator_s: :regional_indicator_s: :regional_indicator_e: \n Hey { uid }, we wanna remind "
            f"you that we love you! \n Here have some love from the fan club! \n :partying_face: :heart: "
            f":orange_heart: :yellow_heart: :green_heart: :blue_heart: :purple_heart: :blue_heart: :green_heart: "
            f":yellow_heart: :orange_heart: :heart: :partying_face:")
    await message.channel.send(response)


# ᕙ(`-´)ᕗ Search for the answer of a question on wikipedia and wolframalpha
async def search_answer(message):
    answer = search_internet(message.content)
    msg = await message.channel.send(answer[0])

    # ᕙ(`-´)ᕗ If there is more than one answer, an additional answer can be gotten through reacting with a thumbs up
    if len(answer) > 1:
        await msg.add_reaction('👍')

        @bot.event
        async def on_reaction_add(reaction, user):
            if reaction.emoji == '👍' and user.id != bot.user.id:
                await message.channel.send(answer[1])


# ᕙ(`-´)ᕗ Search the internet for a response on the inputted query
def search_internet(input_query):
    client = connect_wa()
    no_results = "No results"
    try:  # ᕙ(`-´)ᕗ Try to get results for both Wiki and Wolfram
        res = client.query(input_query)
        wolfram_res = next(res.results).text  # ᕙ(`-´)ᕗ print top wolframalpha results of input

        wiki_res = wp.summary(input_query, sentences=2)
        answer_wa = f"Wolfram Result: { wolfram_res }"
        answer_wp = f"Wikipedia Result: { wiki_res }"
        answer = [answer_wa, answer_wp]
        return answer

    except (wp.exceptions.DisambiguationError, wp.exceptions.PageError,
            wp.exceptions.WikipediaException):  # ᕙ(`-´)ᕗ Get only wolfram if wiki throws exceptions
        try:
            res = client.query(input_query)
            wolfram_res = next(res.results).text  # ᕙ(`-´)ᕗ print top wolframalpha results of input
            return [wolfram_res]

        except (StopIteration, AttributeError):
            try:
                wiki_res = wp.summary(input_query, sentences=2)
                return wiki_res
            except BaseException as e:
                logging.exception(f'error while accessing the wiki summary: { repr(e) }')
                return no_results

    except (
            StopIteration,
            AttributeError):  # ᕙ(`-´)ᕗ And if wolfram also doesnt work, say that no results were found
        return [no_results]

    except BaseException as e:  # ᕙ(`-´)ᕗ All the attributes inside your window.
        logging.exception(f'error while accessing the searches that couldn\'t be specified { repr(e) }')
        return no_results


# ᕙ(`-´)ᕗ Sends a good morning message to whoever requests it at a certain time
async def good_morning(guild, com_cog):
    uid = 245989473408647171  # ᕙ(`-´)ᕗ Skyler (Developer) User ID so the message is DMed to them

    skyler = guild.get_member(uid)
    morning_message = "good morning test"
    await com_cog.dm_member(skyler, morning_message)
