import logging

import wikipedia as wp
import wolframalpha as wa

import random

import assets.dictionary as dictionary


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


async def searchMethod(msg, message, app_id, client):
    if msg.content.lower() == "how are you":
        return wellbeing(message)

    if msg.content.lower().count("search") >= 1:
        return searchAnswer(message, msg, app_id, client)

    if msg.content.lower().count("sleep") >= 1:
        return sleepHelper(msg)

    if msg.content.lower().count("hype") >= 1:
        return complimenter(msg)

    if msg.content.lower().count("jesse") >= 1:
        return jesseHype(msg)

    if msg.content.lower().count("drive") >= 1:
        return driveCommand(msg, client, app_id)


async def callingCommand(message, client, app_id, currentdrive, currenthttp):
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

                def check(author):

                    def inner_check(message):
                        if message.author != author:
                            return False
                        else:
                            return True

                    return inner_check

                msg = await client.wait_for('message', check=check(message.author), timeout=15)
                method = await searchMethod(msg, message, app_id, client)
                await method


            except Exception as e:
                await message.remove_reaction('👍', client.user)
                logging.warning(str(e))


async def wellbeing(message):
    response = 'Well I can respond, thats something'
    await message.channel.send(response)


async def sleepHelper(message):
    response = (random.choice(dictionary.sleep_encouragements) % message.mentions[0].mention)
    await message.channel.send(response)


async def complimenter(message):
    response = (random.choice(dictionary.compliments) % message.mentions[0].nick)
    await message.channel.send(response)


async def jesseHype(message):
    uid = '<@745738275968516176>'
    response = (
            ":regional_indicator_w: :regional_indicator_e:   :regional_indicator_l: :regional_indicator_o: :regional_indicator_v: :regional_indicator_e:   :regional_indicator_j: :regional_indicator_e: :regional_indicator_s: :regional_indicator_s: :regional_indicator_e: \n Hey " + uid + ", we wanna remind you that we love you! \n Here have some love from the fan club! \n :partying_face: :heart: :orange_heart: :yellow_heart: :green_heart: :blue_heart: :purple_heart: :blue_heart: :green_heart: :yellow_heart: :orange_heart: :heart: :partying_face:")
    await message.channel.send(response)


async def searchAnswer(message, msg, app_id, client):
    answer = search_internet(msg.content, app_id)

    msg = await message.channel.send(answer[0])

    if len(answer) > 1:
        await msg.add_reaction('👍')

        @client.event
        async def on_reaction_add(reaction, user):
            if reaction.emoji == '👍' and user.id != client.user.id:
                await message.channel.send(answer[1])


async def driveCommand(message,client, app_id):
    if message.content.lower().count("inventory") >= 1:

        # View all folders and file in your Google Drive
        fileList = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        flag = False
        for file in fileList:
            await message.channel.send('Title: %s, ID: %s, mimeType: %s \n\n' % (file['title'], file['id'], file['mimeType']))
            flag = True
    if(not flag):
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


def search_internet(inputQuery, app_id):
    client = connect_wa(app_id)
    no_results = "No results"
    try:  # ᕙ(`▿´)ᕗ Try to get results for both Wiki and Wolframᕙ(`▿´)ᕗ
        res = client.query(inputQuery)
        wolfram_res = next(res.results).text  # ᕙ(`▿´)ᕗ print top wolframalpha results of inputᕙ(`▿´)ᕗ

        wiki_res = wp.summary(inputQuery, sentences=2)
        answerWA = "Wolfram Result: " + wolfram_res
        answerWP = "Wikipedia Result: " + wiki_res
        answer = [answerWA, answerWP]
        return answer

    except (wp.exceptions.DisambiguationError, wp.exceptions.PageError,
            wp.exceptions.WikipediaException):  # ᕙ(`▿´)ᕗ Get only wolfram if wiki throws exceptions ᕙ(`▿´)ᕗ
        try:
            res = client.query(inputQuery)
            wolfram_res = next(res.results).text  # ᕙ(`▿´)ᕗ print top wolframalpha results of inputᕙ(`▿´)ᕗ
            return [wolfram_res]

        except (StopIteration, AttributeError):
            try:
                wiki_res = wp.summary(inputQuery, sentences=2)
                return wiki_res
            except BaseException as e:
                raise e
                return [no_results]

    except (
            StopIteration,
            AttributeError):  # ᕙ(`▿´)ᕗ And if wolfram also doesnt work, say that no results were foundᕙ(`▿´)ᕗ
        return [no_results]

    except BaseException as e:  # ᕙ(`▿´)ᕗ All the attributes inside your window. ᕙ(`▿´)ᕗ
        raise e
        return [no_results]


def check(author):  # check whether the message was sent by the requester
    def inner_check(message):
        if message.author != author or message.channel != author.dm_channel:
            return False
        else:
            return True

    return inner_check


def createFile(title, content, drive):
    file = drive.CreateFile({'title': title})
    file.SetContentString(content)
    file.Upload()  # Files.insert()


def changeTitle(file, newname):
    file['title'] = newname  # Change title of the file
    file.Upload()  # Files.patch()


def addToContent(file, content_to_add):
    content = file.GetContentString()  # 'Hello'
    file.SetContentString(content + " " + content_to_add)  # 'Hello World!'
    file.Upload()  # Files.update()


def createFileWithImageContent(drive, content):
    file = drive.CreateFile()
    file.SetContentFile(content)
    file.Upload()
    print('Created file %s with mimeType %s' % (file['title'], file['mimeType']))

async def require_response(message, client, app_id):
    try:
        await message.add_reaction('👍')

        def check(author):

            def inner_check(message):
                if message.author != author:
                    return False
                else:
                    return True

            return inner_check

        msg = await client.wait_for('message', check=check(message.author), timeout=15)
        method = await searchMethod(msg, message, app_id, client)
        await method


    except Exception as e:
        await message.remove_reaction('👍', client.user)
        logging.warning(str(e))