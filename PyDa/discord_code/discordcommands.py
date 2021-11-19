import logging

# import discord
import wikipedia as wp
import wolframalpha as wa

import random

import assets.dictionary as dictionary
from discord.ext import tasks


async def dm_member_wait_for_response(member, message, client):
    await member.create_dm()
    await member.dm_channel.send(message)
    msg = await client.wait_for('message', check=check(member), timeout=60)

    return msg


async def dm_member(member, message):
    await member.create_dm()
    await member.dm_channel.send(message)


def connect_wa(app_id):
    client = wa.Client(app_id)
    return client


async def search_method(msg, message, app_id, client):
    if msg.content.lower().count("how are you") >= 1:
        return wellbeing(message)

    if msg.content.lower().count("search") >= 1:
        return search_answer(message, msg, app_id, client)

    if msg.content.lower().count("sleep") >= 1:
        return sleep_helper(msg)

    if msg.content.lower().count("hype") >= 1:
        return complimenter(msg)

    if msg.content.lower().count("jesse") >= 1:
        return jesse_hype(msg)

    if msg.content.lower().count("drive") >= 1:
        return drive_command(msg, client, app_id)

    if msg.content.lower().count("morning") >= 1:
        return good_morning(msg.guild)


async def calling_command(message, client, app_id, currentdrive, currenthttp):
    global drive
    global http
    drive = currentdrive
    http = currenthttp
    for name in dictionary.phillip_names:
        if message.content.lower() == name:
            response = 'At your service'
            await message.channel.send(response)
            try:
                await message.add_reaction('👍')

                def check_author(author):

                    def inner_check(message_to_check):
                        if message_to_check.author != author:
                            return False
                        else:
                            return True

                    return inner_check

                msg = await client.wait_for('message', check=check_author(message.author), timeout=15)
                method = await search_method(msg, message, app_id, client)
                await method

            except Exception as e:
                await message.remove_reaction('👍', client.user)
                logging.warning(str(e))


async def wellbeing(message):
    response = 'Well I can respond, that\'s something'
    await message.channel.send(response)


async def sleep_helper(message):
    response = (random.choice(dictionary.sleep_encouragements) % message.mentions[0].mention)
    await message.channel.send(response)


async def complimenter(message):
    response = (random.choice(dictionary.compliments) % message.mentions[0].nick)
    await message.channel.send(response)


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


async def search_answer(message, msg, app_id, client):
    answer = search_internet(msg.content, app_id)

    msg = await message.channel.send(answer[0])

    if len(answer) > 1:
        await msg.add_reaction('👍')

        @client.event
        async def on_reaction_add(reaction, user):
            if reaction.emoji == '👍' and user.id != client.user.id:
                await message.channel.send(answer[1])


async def drive_command(message, client, app_id):
    flag = True
    if message.content.lower().count("inventory") >= 1:

        # View all folders and file in your Google Drive
        file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        flag = False
        for file in file_list:
            await message.channel.send(
                'Title: %s, ID: %s, mimeType: %s \n\n' % (file['title'], file['id'], file['mimeType']))
            flag = True
    if not flag:
        message.channel.send('Sorry! no file found...')

    if message.content.lower().count("create") >= 1:
        # createFile(title, content,drive)
        return await message.channel.send("create method triggered")

    if message.content.lower().count("change name") >= 1:
        file = require_response(message, client, app_id)
        # changeTitle(file,newname)
        return await message.channel.send("change title method triggered")

    if message.content.lower().count("append") >= 1:
        # addToContent(file,content_to_add)
        return await message.channel.send("add content method triggered")

    if message.content.lower().count("add image") >= 1:
        # createFileWithImageContent(drive,content)
        return await message.channel.send("image add function triggered")


def search_internet(input_query, app_id):
    client = connect_wa(app_id)
    no_results = "No results"
    try:  # ᕙ(`▿´)ᕗ Try to get results for both Wiki and Wolframᕙ(`▿´)ᕗ
        res = client.query(input_query)
        wolfram_res = next(res.results).text  # ᕙ(`▿´)ᕗ print top wolframalpha results of inputᕙ(`▿´)ᕗ

        wiki_res = wp.summary(input_query, sentences=2)
        answer_wa = "Wolfram Result: " + wolfram_res
        answer_wp = "Wikipedia Result: " + wiki_res
        answer = [answer_wa, answer_wp]
        return answer

    except (wp.exceptions.DisambiguationError, wp.exceptions.PageError,
            wp.exceptions.WikipediaException):  # ᕙ(`▿´)ᕗ Get only wolfram if wiki throws exceptions ᕙ(`▿´)ᕗ
        try:
            res = client.query(input_query)
            wolfram_res = next(res.results).text  # ᕙ(`▿´)ᕗ print top wolframalpha results of inputᕙ(`▿´)ᕗ
            return [wolfram_res]

        except (StopIteration, AttributeError):
            try:
                wiki_res = wp.summary(input_query, sentences=2)
                return wiki_res
            except BaseException as e:
                logging.exception('error while accessing the wiki summary' + e)
                return no_results

    except (
            StopIteration,
            AttributeError):  # ᕙ(`▿´)ᕗ And if wolfram also doesnt work, say that no results were foundᕙ(`▿´)ᕗ
        return [no_results]

    except BaseException as e:  # ᕙ(`▿´)ᕗ All the attributes inside your window. ᕙ(`▿´)ᕗ
        logging.exception('error while accessing the searches that couldn\'t be specified + e')
        return no_results


def check(author):  # check whether the message was sent by the requester
    def inner_check(message):
        if message.author != author or message.channel != author.dm_channel:
            return False
        else:
            return True

    return inner_check


def create_file(title, content):
    file = drive.CreateFile({'title': title})
    file.SetContentString(content)
    file.Upload()  # Files.insert()


def change_title(file, newname):
    file['title'] = newname  # Change title of the file
    file.Upload()  # Files.patch()


def add_to_content(file, content_to_add):
    content = file.GetContentString()  # 'Hello'
    file.SetContentString(content + " " + content_to_add)  # 'Hello World!'
    file.Upload()  # Files.update()


def create_file_with_image_content(content):
    file = drive.CreateFile()
    file.SetContentFile(content)
    file.Upload()
    print('Created file %s with mimeType %s' % (file['title'], file['mimeType']))


async def require_response(message, client, app_id):
    try:
        await message.add_reaction('👍')

        def author_check(author):

            def inner_check(message_to_check):
                if message_to_check.author != author:
                    return False
                else:
                    return True

            return inner_check

        msg = await client.wait_for('message', check=author_check(message.author), timeout=15)
        method = await search_method(msg, message, app_id, client)
        await method

    except Exception as e:
        await message.remove_reaction('👍', client.user)
        logging.warning(str(e))


async def good_morning(guild):
    uid = 245989473408647171  # Skyler (Developer) User ID so the message is DMed to them

    skyler = guild.get_member(uid)
    morning_message = "good morning test"
    await called_every_five_min()
    await dm_member(skyler, morning_message)


@tasks.loop(seconds=10)
async def called_every_five_min():
    logging.warning("called")


@called_every_five_min.before_loop
async def before_printer(self):
    logging.warning('waiting...')
    await self.bot.wait_until_ready()
