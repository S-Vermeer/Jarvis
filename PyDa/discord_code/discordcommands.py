"""
Comment legend
ᕙ(`-´)ᕗ - Explanation
ʕ•́ᴥ•̀ʔっ - To do
(ㆆ_ㆆ) - Bug
"""
import asyncio
import logging

import wikipedia as wp
import wolframalpha as wa

import random

import assets.dictionary as dictionary
from discord.ext import tasks


# ᕙ(`-´)ᕗ Send a direct message to a member and wait 60 seconds for a response
async def dm_member_wait_for_response(member, message, bot):
    await dm_member(member, message)
    msg = await bot.wait_for('message', check=check(member), timeout=60)

    return msg


# ᕙ(`-´)ᕗ Send a direct message to a member
async def dm_member(member, message):
    await member.create_dm()
    await member.dm_channel.send(message)


# ᕙ(`-´)ᕗ Connect to the wolfram alpha client
def connect_wa(app_id):
    client = wa.Client(app_id)
    return client


# ᕙ(`-´)ᕗ Check which action is asked for after phillip is called
async def search_method(msg, message, app_id, bot):
    if msg.content.lower().count("how are you") >= 1:
        return wellbeing(message)

    if msg.content.lower().count("search") >= 1:
        return search_answer(message, msg, app_id, bot)

    if msg.content.lower().count("sleep") >= 1:
        return sleep_helper(msg)

    if msg.content.lower().count("hype") >= 1:
        return complimenter(msg)

    if msg.content.lower().count("jesse") >= 1:
        return jesse_hype(msg)

    if msg.content.lower().count("drive") >= 1:
        return drive_command(msg, bot)

    if msg.content.lower().count("morning") >= 1:
        return good_morning(msg.guild)

    if msg.content.lower().count("tone") and msg.content.lower().count("/") >= 1:
        response = await tone_check(msg)
        await msg.channel.send(response)
        return tone_check(msg)

drive = None
http = None


# ᕙ(`-´)ᕗ This is what happens after one of Phillip's names is said
async def calling_command(message, bot, app_id, currentdrive, currenthttp):
    global drive
    global http
    drive = currentdrive
    http = currenthttp
    for name in dictionary.phillip_names:
        if message.content.lower() == name:
            response = 'At your service'
            await message.channel.send(response)
            try:
                # ᕙ(`-´)ᕗ this is added to see whether Phillip is still listening
                await message.add_reaction('👍')

                def check_author(author):
                    # ᕙ(`-´)ᕗ Check whether the person who sent sent the request for phillip, is also the one the
                    # message is from
                    def inner_check(message_to_check):
                        if message_to_check.author != author:
                            return False
                        else:
                            return True

                    return inner_check

                msg = await bot.wait_for('message', check=check_author(message.author), timeout=15)
                method = await search_method(msg, message, app_id, bot)
                await method

            except asyncio.exceptions.TimeoutError as e:
                await message.remove_reaction('👍', bot.user)
                logging.warning("warning: " + repr(e))


# ᕙ(`-´)ᕗ How is Phillip doing?
async def wellbeing(message):
    response = 'Well I can respond, that\'s something'  # ʕ•́ᴥ•̀ʔっ More responses to how Phillip is doing
    await message.channel.send(response)


# ᕙ(`-´)ᕗ Prompts someone who is tagged to sleep
async def sleep_helper(message):
    response = (random.choice(dictionary.sleep_encouragements) % message.mentions[0].mention)
    await message.channel.send(response)


# ᕙ(`-´)ᕗ Compliments someone who is tagged
async def complimenter(message):
    response = (random.choice(dictionary.compliments) % message.mentions[0].nick)
    await message.channel.send(response)


# ᕙ(`-´)ᕗ Hypes Jesse, a mod from the Avieno discord
async def jesse_hype(message):
    uid = '<@745738275968516176>'
    response = (
            ":regional_indicator_w: :regional_indicator_e:   :regional_indicator_l: :regional_indicator_o: "
            ":regional_indicator_v: :regional_indicator_e:   :regional_indicator_j: :regional_indicator_e: "
            ":regional_indicator_s: :regional_indicator_s: :regional_indicator_e: \n Hey " + uid + ", we wanna remind "
                                                                                                   "you that we love "
                                                                                                   "you! \n Here have "
                                                                                                   "some love from "
                                                                                                   "the fan club! \n "
                                                                                                   ":partying_face: "
                                                                                                   ":heart: "
                                                                                                   ":orange_heart: "
                                                                                                   ":yellow_heart: "
                                                                                                   ":green_heart: "
                                                                                                   ":blue_heart: "
                                                                                                   ":purple_heart: "
                                                                                                   ":blue_heart: "
                                                                                                   ":green_heart: "
                                                                                                   ":yellow_heart: "
                                                                                                   ":orange_heart: "
                                                                                                   ":heart: "
                                                                                                   ":partying_face:")
    await message.channel.send(response)


# ᕙ(`-´)ᕗ Search for the answer of a question on wikipedia and wolframalpha
async def search_answer(message, msg, app_id, bot):
    answer = search_internet(msg.content, app_id)

    msg = await message.channel.send(answer[0])

    # ᕙ(`-´)ᕗ If there is more than one answer, an additional answer can be gotten through reacting with a thumbs up
    if len(answer) > 1:
        await msg.add_reaction('👍')

        @bot.event
        async def on_reaction_add(reaction, user):
            if reaction.emoji == '👍' and user.id != bot.user.id:
                await message.channel.send(answer[1])


# ᕙ(`-´)ᕗ Send a question and return the result
async def get_question_response(question, message, bot):
    await message.channel.send(question)
    return await wait_for_response_message_drive(message, bot)


# ᕙ(`-´)ᕗ Select a file based on the specified id. 'Creating' only replicates it, if it isn't uploaded, nothing happens/
async def select_file(message, bot):
    file_id = await get_question_response('Please specify the id of the document to change', message, bot)
    return drive.CreateFile({'id': file_id.content})


# ᕙ(`-´)ᕗ Select one of the drive commands
async def drive_command(message, bot):
    drive_cog = bot.get_cog("GoogleDriveCog")
    if message.content.lower().count("inventory") >= 1:
        await drive_cog.drive_inventory(message)

    title_question = 'Please specify the title for the document'

    if message.content.lower().count("create") >= 1:
        title_msg = await get_question_response(title_question, message, bot)
        content_msg = await get_question_response('Please specify the content for the document', title_msg, bot)
        await drive_cog.create_file(title_msg.content, content_msg.content)
        return await message.channel.send("Title: " + title_msg.content + "\n Content: " + content_msg.content)

    if message.content.lower().count("change name") >= 1:
        await drive_cog.drive_inventory(message)
        file = await select_file(message, bot)
        title_msg = await get_question_response(title_question, message, bot)
        await drive_cog.change_title(file, title_msg.content)
        return await message.channel.send("Title was changed to: " + file["title"])

    if message.content.lower().count("append") >= 1:
        await drive_cog.drive_inventory(message)
        file = await select_file(message, bot)
        addition_question = 'Please specify the text you want to add to the document'
        content_to_add = await get_question_response(addition_question, message, bot)
        await drive_cog.add_to_content(file, content_to_add.content)
        return await message.channel.send("add content method triggered")

    # (ㆆ_ㆆ) Doesnt work in server due to not opening in browser
    # if message.content.lower().count("add image") >= 1:
    #     title_msg = await get_question_response(title_question, message, bot)
    #     content_msg = await get_question_response('Please upload the image(s)', title_msg, bot)
    #     path = content_msg.attachments[0].url
    #     await drive_cog.create_image_file(title_msg.content, path)
    #     return await message.channel.send("The image was added to the drive")


# ᕙ(`-´)ᕗ Search the internet for a response on the inputted query
def search_internet(input_query, app_id):
    client = connect_wa(app_id)
    no_results = "No results"
    try:  # ᕙ(`-´)ᕗ Try to get results for both Wiki and Wolfram
        res = client.query(input_query)
        wolfram_res = next(res.results).text  # ᕙ(`-´)ᕗ print top wolframalpha results of input

        wiki_res = wp.summary(input_query, sentences=2)
        answer_wa = "Wolfram Result: " + wolfram_res
        answer_wp = "Wikipedia Result: " + wiki_res
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
                logging.exception('error while accessing the wiki summary: ' + repr(e))
                return no_results

    except (
            StopIteration,
            AttributeError):  # ᕙ(`-´)ᕗ And if wolfram also doesnt work, say that no results were found
        return [no_results]

    except BaseException as e:  # ᕙ(`-´)ᕗ All the attributes inside your window.
        logging.exception('error while accessing the searches that couldn\'t be specified ' + repr(e))
        return no_results


def check(author):  # ᕙ(`-´)ᕗ check whether the message was sent by the requester
    def inner_check(message):
        if message.author != author or message.channel != author.dm_channel:
            return False
        else:
            return True

    return inner_check


# ᕙ(`-´)ᕗ Send something but need a response to continue
async def require_response(message, bot, app_id):
    try:
        await message.add_reaction('👍')

        def author_check(author):

            def inner_check(message_to_check):
                if message_to_check.author != author:
                    return False
                else:
                    return True

            return inner_check

        msg = await bot.wait_for('message', check=author_check(message.author), timeout=15)
        method = await search_method(msg, message, app_id, bot)
        await method

    except Exception as e:
        await message.remove_reaction('👍', bot.user)
        logging.warning(repr(e))


# ᕙ(`-´)ᕗ Sends a good morning message to whoever requests it at a certain time
async def good_morning(guild):
    uid = 245989473408647171  # ᕙ(`-´)ᕗ Skyler (Developer) User ID so the message is DMed to them

    skyler = guild.get_member(uid)
    morning_message = "good morning test"
    await called_every_five_min()
    await dm_member(skyler, morning_message)


# ᕙ(`-´)ᕗ Check the tone tags based on your own message
async def tone_check(message):
    split_message = message.content.split()
    index_tag = -1
    messages = []

    for msg in split_message:
        index_tag += 1
        if msg.find("/") != -1:
            messages.append(index_tag)

    response = "The following tone tags are possible: \n"
    for msg in messages:
        for tone_tag in dictionary.tone_tags:
            if tone_tag[0].lower().count(split_message[msg]) >= 1:
                response += tone_tag[0] + "  =  " + tone_tag[1] + "\n"
    return response


# ᕙ(`-´)ᕗ Attempt to start a task every x amount of time
@tasks.loop(seconds=10)
async def called_every_five_min():
    logging.warning("called")


# ᕙ(`-´)ᕗ Something that happens before the loop starts
@called_every_five_min.before_loop
async def before_printer(self):
    logging.warning('waiting...')
    await self.bot.wait_until_ready()


# ᕙ(`-´)ᕗ Wai for a response, specifically for the drive
async def wait_for_response_message_drive(message, bot):
    try:
        await message.add_reaction('👍')

        def check_author(author):

            def inner_check(message_to_check):
                if message_to_check.author != author:
                    logging.warning("author doesn't match")
                    return False
                else:
                    return True

            return inner_check

        msg = await bot.wait_for('message', check=check_author(message.author), timeout=15)
        return msg

    except Exception as e:
        await message.remove_reaction('👍', bot.user)
        logging.warning(repr(e))
