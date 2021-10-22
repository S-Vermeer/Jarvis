import os
import random

import logging

import discord
from dotenv import load_dotenv

import discordcommands
import PyDa.discord.assets.dictionary as dictionary

import json

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

async def connectToGoogleDrive(guild):
    #Change file path for settings file (hidden in github)
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = "credentials/client_secrets.json"
    gauth = GoogleAuth()

    gauth.LoadCredentialsFile("credentials/mycreds.txt")
    if gauth.credentials is None:
        #Get the url that the user must use to give access to google drive
        auth_url = gauth.GetAuthUrl()

        uid = 245989473408647171 #Skyler (Developer) User ID so the message is DMed to them

        skyler = guild.get_member(uid)
        msg = await discordcommands.dm_member_wait_for_response(skyler,auth_url,client)
        gauth.Auth(msg.content)

        logging.warning("Authorisation complete")
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
        logging.warning("refresh")
    else:
        # Initialize the saved creds
        gauth.Authorize()
        logging.warning("used saved creds")
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("credentials/mycreds.txt")

    drive = GoogleDrive(gauth)

    # Create httplib.Http() object.
    http = drive.auth.Get_Http_Object()
    return drive,http


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
print(GUILD)

@client.event
async def on_ready():

    guild = discord.utils.get(client.guilds, name=GUILD)
    logging.warning(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )
    logging.warning(os.getcwd())
    with open('credentials/client_secrets.json') as json_file:
        logging.warning(json.load(json_file))

    members = '\n - '.join([member.name for member in guild.members])
    print(len(guild.members))
#    print(f'Guild Members:\n - {members}')
    global drive,http
    drive,http = await connectToGoogleDrive(guild)
    print("done")


@client.event
async def on_message(message):
    if GUILD == message.guild.name:
        logging.warning(GUILD)
        if message.author == client.user:
            return
        await discordcommands.callingCommand(message,client,app_id,drive,http)

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

    else:
        logging.warning(GUILD)


def check(author): #check whether the message was sent by the requester
    def inner_check(message):
        if message.author != author:
            return False
        else:
            return True

    return inner_check


client.run(TOKEN)