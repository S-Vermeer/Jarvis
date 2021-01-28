import os
import random

import logging

import discord
from dotenv import load_dotenv

import wikipedia as wp
import wolframalpha as wa

import discordcommands
import dictionary

import json

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def connectToGoogleDrive():
    #Change file path for settings file (hidden in github)
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = "credentials/client_secrets.json"
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth(host_name="phillip.skylervermeer.nl",port_numbers=[8181])
    auth_url = gauth.GetAuthUrl()
    logging.warning(auth_url)
    logging.warning("Authorisation complete")
    drive = GoogleDrive(gauth)

    # Create httplib.Http() object.
    http = drive.auth.Get_Http_Object()
    return drive,http

drive,http = connectToGoogleDrive()

intents = discord.Intents.default()
intents.members = True
intents.reactions = True

client = discord.Client(intents=intents)

TOKEN = ""
GUILD = ""
app_id = ""

def get_env_var():
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD = os.getenv('DISCORD_GUILD')
    app_id = os.getenv('APP_ID')

    return TOKEN,GUILD,app_id

TOKEN,GUILD,app_id = get_env_var()
print(TOKEN)

def connect_wa():
    client = wa.Client(app_id)
    return client

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    logging.warning(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )
    with open('credentials/client_secrets.json') as json_file:
        logging.warning(json.load(json_file))

    members = '\n - '.join([member.name for member in guild.members])
    print(len(guild.members))
#    print(f'Guild Members:\n - {members}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await discordcommands.callingCommand(message,client,app_id)

    if message.content.lower() == 'stop':
        await message.channel.send('Shutting down')
        await client.logout()

    if message.content.lower() == 'names':
        response = "Phillip responds to:\n"
        for name in dictionary.phillip_names:
            response = response + name + "\n"
        await message.channel.send(response)

    if message.content == '99!':
        response = random.choice(dictionary.brooklyn_99_quotes)
        await message.channel.send(response)

    if message.content.lower() == 'help':
        response = "Hello, my name is P.H.I.L.L.I.P. I'll explain what I can do below.\nYou don't have to call my name for me to listen to the following functions: \n"

        for function in dictionary.always_functions:
            response = response + function[0] + "```" + function[1] + "```" + "\n"

        response = response + "\n If you call on me (using one of the names listed in 'names') I will start listening for more commands.\nI will be listening for the first message you sent after you call me for 15 seconds, if you do not respond before that time I'll remove the reaction under your calling message.\nThe commands I will be listening for are the following: \n"

        for function in dictionary.on_call_functions:
            response = response + function[0] + "```" + function[1] + "```" + "\n"
        await message.channel.send(response)

def check(author):
    def inner_check(message):
        if message.author != author:
            return False
        else:
            return True

    return inner_check

def search_internet(inputQuery, message):
    client = connect_wa()
    try: # ᕙ(`▿´)ᕗ Try to get results for both Wiki and Wolframᕙ(`▿´)ᕗ
        res = client.query(inputQuery)
        wolfram_res = next(res.results).text # ᕙ(`▿´)ᕗ print top wolframalpha results of inputᕙ(`▿´)ᕗ

        wiki_res = wp.summary(inputQuery,sentences=2)
        answerWA = "Wolfram Result: " + wolfram_res
        answerWP = "Wikipedia Result: " + wiki_res
        answer = [answerWA,answerWP]
        return answer

    except (wp.exceptions.DisambiguationError,wp.exceptions.PageError,wp.exceptions.WikipediaException): # ᕙ(`▿´)ᕗ Get only wolfram if wiki throws exceptions ᕙ(`▿´)ᕗ
        try:
            res = client.query(inputQuery)
            wolfram_res = next(res.results).text # ᕙ(`▿´)ᕗ print top wolframalpha results of inputᕙ(`▿´)ᕗ
            return [wolfram_res]

        except (StopIteration,AttributeError):
            try:
                wiki_res = wp.summary(inputQuery,sentences=2)
                return wiki_res
            except:
                return ["No results"]

    except (StopIteration,AttributeError): # ᕙ(`▿´)ᕗ And if wolfram also doesnt work, say that no results were foundᕙ(`▿´)ᕗ
        return ["No results"]

    except: # ᕙ(`▿´)ᕗ All the attributes inside your window. ᕙ(`▿´)ᕗ
        return ["No results"]


client.run(TOKEN)