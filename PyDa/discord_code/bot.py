"""
Comment legend
ᕙ(`-´)ᕗ - Explanation
ʕ•́ᴥ•̀ʔっ - To do
(ㆆ_ㆆ) - Bug
"""

import os
import random

import logging

import discord

from dotenv import load_dotenv

import discordcommands
import assets.dictionary as dictionary

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


async def connect_to_google_drive(guild):
    # ᕙ(`-´)ᕗ Change file path for settings file (hidden in github)
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = "credentials/client_secrets.json"
    gauth = GoogleAuth()

    gauth.LoadCredentialsFile("credentials/mycreds.txt")  # ᕙ(`-´)ᕗ Load credentials, if any (hidden in github)
    if gauth.credentials is None:
        # ᕙ(`-´)ᕗ Get the url that the user must use to give access to google drive
        auth_url = gauth.GetAuthUrl()

        uid = 245989473408647171  # ᕙ(`-´)ᕗ Skyler (Developer) User ID so the message is DMed to them

        skyler = guild.get_member(uid)
        msg = await discordcommands.dm_member_wait_for_response(skyler, auth_url, client)

        logging.warning(msg.content)
        gauth.Auth(msg.content)

        logging.warning("Authorisation complete")
    elif gauth.access_token_expired:
        # ᕙ(`-´)ᕗ Refresh them if expired
        # (ㆆ_ㆆ) Does not Refresh yet?
        open('credentials/mycreds.txt', 'w').close()
        logging.warning("refresh")
    else:
        # ᕙ(`-´)ᕗ Initialize the saved creds
        gauth.Authorize()
        logging.warning("used saved creds")
    # ᕙ(`-´)ᕗ Save the current credentials to a file
    gauth.SaveCredentialsFile("credentials/mycreds.txt")

    gdrive = GoogleDrive(gauth)

    # ᕙ(`-´)ᕗ Create httplib.Http() object.
    http_obj = gdrive.auth.Get_Http_Object()
    return gdrive, http_obj

# ᕙ(`-´)ᕗ Discord.py requires intents to open the relevant gateways to make sure only the events you need get triggered.
intents = discord.Intents.default()
intents.members = True  # ᕙ(`-´)ᕗ We want to see information about the members
intents.reactions = True  # ᕙ(`-´)ᕗ And when reactions are added etc

client = discord.Client(intents=intents)


# ᕙ(`-´)ᕗ Get information from the .env file (hidden in the github)
def get_env_var():
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')
    guild = os.getenv('DISCORD_GUILD')
    id_app = os.getenv('APP_ID')

    return token, guild, id_app


TOKEN, GUILD, app_id = get_env_var()

# ᕙ(`-´)ᕗ Global variables that are assigned when the google drive is connected
drive = None
http = None


# ᕙ(`-´)ᕗ When the bot is done with setting up the basics and logging this is triggered
@client.event
async def on_ready():
    # ᕙ(`-´)ᕗ from all the guilds that the bot is connected to, assign to guild the one that has the name from the .env
    guild = discord.utils.get(client.guilds, name=GUILD)
    logging.warning(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )
    logging.warning("There are " + str(len(guild.members)) + " guild members")
    global drive, http
    drive, http = await connect_to_google_drive(guild)
    logging.warning("ready")


# ᕙ(`-´)ᕗ When the bot is notified of a message, this is triggered
@client.event
async def on_message(message):
    if message.guild is None:
        return
    # ᕙ(`-´)ᕗ If the guild the message is from, is the guild that this version of Phillip is listening for,
    # this is enacted
    if GUILD == message.guild.name:
        # ᕙ(`-´)ᕗ if the message was from the bot, don't do anything
        if message.author == client.user:
            return
        # ᕙ(`-´)ᕗ See whether one of the bots names was called
        await discordcommands.calling_command(message, client, app_id, drive, http)

        # ᕙ(`-´)ᕗ These are various options that work without having to say the name first
        await stop(message)
        await name_list(message)
        await b99(message)
        await help_msg(message)
        await tone_tags(message)


# ᕙ(`-´)ᕗ If a reaction is added to a message since the bot started listening, this is triggered.
@client.event
async def on_reaction_add(reaction, user):
    if reaction.message.guild is None:
        return
    # ᕙ(`-´)ᕗ If the guild is correct, it is not sent by the bot, the reaction is an emoji with a monocle and there
    # is at least one / in the message, this is triggered
    if GUILD == reaction.message.guild.name and user != client.user and \
            reaction.emoji == "🧐" and reaction.message.content.count("/") >= 1:
        # ᕙ(`-´)ᕗ You receive a DM with information about the tone tags in the message reacted to.
        response = "You requested tone tag information about: " + reaction.message.content + "\n"
        response += await discordcommands.tone_check(reaction.message)
        await discordcommands.dm_member(user, response)


# ᕙ(`-´)ᕗ Phillip is shut down, when they are misbehaving
async def stop(message):
    # ᕙ(`-´)ᕗ The message has to be solely stop, so it when it is said in a sentence it isn't triggered
    if message.content.lower() == 'stop':
        await message.channel.send('Shutting down')
        await client.close()  # (ㆆ_ㆆ) Gives RuntimeError: Event loop is closed, so it works but probably not exactly


# ᕙ(`-´)ᕗ The bot responds with a list of names that they listen to for more advanced requests
async def name_list(message):
    if message.content.lower() == 'names':
        response = "Phillip responds to:\n"
        for name in dictionary.phillip_names:
            response = response + name + "\n"
        await message.channel.send(response)


# ᕙ(`-´)ᕗ Easter egg from original development, sends a random brooklyn 99 quote
async def b99(message):
    if message.content == '99!':
        response = random.choice(dictionary.brooklyn_99_quotes)
        await message.channel.send(response)


# ᕙ(`-´)ᕗ Phillip sends a list of all the different things they can do.
async def help_msg(message):
    if message.content.lower() == 'help':
        response = "Hello, my name is P.H.I.L.L.I.P. I'll explain what I can do below.\nYou don't have to call my " \
                   "name for me to listen to the following functions: \n "

        for function in dictionary.always_functions:
            response = response + function[0] + "```" + function[1] + "```" + "\n"

        response = response + "\n If you call me (using one of the names listed in 'names') I will start listening " \
                              "for more commands.\nI will be listening for the first message you sent after you call " \
                              "me for 15 seconds, if you do not respond before that time I'll remove the reaction " \
                              "under your calling message.\nThe commands I will be listening for are the following: \n "

        for function in dictionary.on_call_functions:
            response = response + function[0] + "```" + function[1] + "```" + "\n"
        await message.channel.send(response)


# ᕙ(`-´)ᕗ Shows information about tone tags and the different optionsS
async def tone_tags(message):
    response = "tone tags / tone indicators are things you can include with text to indicate what the tone of it is. \n"
    response += "some people have difficulty picking up on tone. communicating through text only makes this harder " \
                "due to lack of audio and physical clues (voice inflection, body language, facial expressions, etc.) "
    response += "Tagging what tone you are using can be very helpful for others understanding of what you're saying, " \
                "clarification, avoiding miscommunications, etc. \n"
    if message.content.lower() == 'tonetags':
        for tone_tag in dictionary.tone_tags:
            response = response + tone_tag[0] + "  =  " + tone_tag[1] + "\n"
        await message.channel.send(response)


# ᕙ(`-´)ᕗ Check whether the message was sent by the requester
def check(author):
    def inner_check(message):
        if message.author != author:
            return False
        else:
            return True

    return inner_check


client.run(TOKEN)
