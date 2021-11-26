import io
import json
import logging

import requests
import wikipedia as wp
import wolframalpha as wa

import random

import assets.dictionary as dictionary
from discord.ext import tasks
from pydrive2.auth import GoogleAuth


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
        return drive_command(msg, client)

    if msg.content.lower().count("morning") >= 1:
        return good_morning(msg.guild)

    if msg.content.lower().count("tone") and msg.content.lower().count("/") >= 1:
        response = await tone_check(msg)
        await msg.channel.send(response)
        return tone_check(msg)


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


async def get_question_response(question, message, client):
    await message.channel.send(question)
    return await wait_for_response_message_drive(message, client)


async def select_file(message, client):
    file_id = await get_question_response('Please specify the id of the document to change', message, client)
    return drive.CreateFile({'id': file_id.content})


async def drive_command(message, client):

    if message.content.lower().count("inventory") >= 1:
        await drive_inventory(message)

    title_question = 'Please specify the title for the document'

    if message.content.lower().count("create") >= 1:
        title_msg = await get_question_response(title_question, message, client)
        content_msg = await get_question_response('Please specify the content for the document', title_msg, client)
        create_file(title_msg.content, content_msg.content)
        return await message.channel.send("Title: " + title_msg.content + "\n Content: " + content_msg.content)

    if message.content.lower().count("change name") >= 1:
        await drive_inventory(message)
        file = await select_file(message, client)
        title_msg = await get_question_response(title_question, message, client)
        change_title(file, title_msg.content)
        return await message.channel.send("Title was changed to: " + file["title"])

    if message.content.lower().count("append") >= 1:
        file = await select_file(message, client)
        addition_question = 'Please specify the text you want to add to the document'
        content_to_add = await get_question_response(addition_question, message, client)
        add_to_content(file, content_to_add.content)
        return await message.channel.send("add content method triggered")

    if message.content.lower().count("add image") >= 1:
        title_msg = await get_question_response(title_question, message, client)
        content_msg = await get_question_response('Please upload the image(s)', title_msg, client)
        path = content_msg.attachments[0].url
        create_image_file(title_msg.content, path)
        return await message.channel.send("The image was added to the drive")


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
                logging.exception('error while accessing the wiki summary: ' + str(e))
                return no_results

    except (
            StopIteration,
            AttributeError):  # ᕙ(`▿´)ᕗ And if wolfram also doesnt work, say that no results were foundᕙ(`▿´)ᕗ
        return [no_results]

    except BaseException as e:  # ᕙ(`▿´)ᕗ All the attributes inside your window. ᕙ(`▿´)ᕗ
        logging.exception('error while accessing the searches that couldn\'t be specified ' + e)
        return no_results


def check(author):  # check whether the message was sent by the requester
    def inner_check(message):
        if message.author != author or message.channel != author.dm_channel:
            return False
        else:
            return True

    return inner_check


async def drive_inventory(message):
    # View all folders and file in your Google Drive
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    flag = False
    list_msg = ""
    for file in file_list:
        list_msg += 'Title: %s, ID: %s, mimeType: %s \n' % (file['title'], file['id'], file['mimeType'])
        flag = True
    if flag:
        await message.channel.send(list_msg)
    if not flag:
        message.channel.send('Sorry! no file found...')


def create_file(title, content):
    file = drive.CreateFile({'title': title})
    file.SetContentString(content)
    file.Upload()  # Files.insert()


def create_image_file(title, content):
    url = content  # Please set the direct link of the image file.
    filename = title  # Please set the filename on Google Drive.
    folder_id = 'root'  # Please set the folder ID. The file is put to this folder.

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    metadata = {
        "name": filename,
        "parents": [folder_id]
    }
    files = {
        'data': ('metadata', json.dumps(metadata), 'application/json'),
        'file': io.BytesIO(requests.get(url).content)
    }
    requests.post(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        headers={"Authorization": "Bearer " + gauth.credentials.access_token},
        files=files
    )


def change_title(file, newname):
    file.FetchMetadata(fields="title")
    file['title'] = newname  # Change title of the file
    file.Upload()  # Files.patch()


def add_to_content(file, content_to_add):
    content = file.GetContentString()  # 'Hello'
    file.SetContentString(content + " " + content_to_add + "\n")  # 'Hello World!'
    file.Upload()  # Files.update()


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


@tasks.loop(seconds=10)
async def called_every_five_min():
    logging.warning("called")


@called_every_five_min.before_loop
async def before_printer(self):
    logging.warning('waiting...')
    await self.bot.wait_until_ready()


async def wait_for_response_message_drive(message, client):
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

        msg = await client.wait_for('message', check=check_author(message.author), timeout=15)
        return msg

    except Exception as e:
        await message.remove_reaction('👍', client.user)
        logging.warning(str(e))
