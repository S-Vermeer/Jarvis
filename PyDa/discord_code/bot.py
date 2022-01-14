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
from discord.ext import commands
from discord.ext.commands import bot

from dotenv import load_dotenv

import assets.dictionary as dictionary

# ᕙ(`-´)ᕗ Discord.py requires intents to open the relevant gateways to make sure only the events you need get triggered.
intents = discord.Intents.default()
intents.members = True  # ᕙ(`-´)ᕗ We want to see information about the members
intents.reactions = True  # ᕙ(`-´)ᕗ And when reactions are added etc

bot = commands.Bot(command_prefix="", intents=intents)
cog_names = [["googledrive", "GoogleDriveCog"],
             ["usercommunication", "UserCommunicationCog"],
             ["tonetag", "ToneTagCog"],
             ["wellbeing", "WellbeingCog"],
             ["search", "SearchCog"]]
cogs = {}


async def cogs_load():
    for cog in cog_names:
        bot.load_extension(f"cogs.modules.{cog[0]}")
        print(f"{cog[0]} cog loaded")
        cogs[cog[1]] = bot.get_cog(cog[1])
    print("cogs setup complete")
    return cogs


async def connect_to_google_drive(guild):
    com_cog = cogs['UserCommunicationCog']
    return await cogs['GoogleDriveCog'].drive_connect(guild, com_cog)


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
@bot.event
async def on_ready():
    # ᕙ(`-´)ᕗ from all the guilds that the bot is connected to, assign to guild the one that has the name from the .env
    guild = discord.utils.get(bot.guilds, name=GUILD)
    logging.warning(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )
    logging.warning(f"There are {str(len(guild.members))} guild members")
    global cogs, drive, http
    cogs = await cogs_load()
    drive, http = await connect_to_google_drive(guild)
    await cogs['SearchCog'].assign_cogs_and_connect(cogs, app_id)
    logging.warning("ready")


# ᕙ(`-´)ᕗ When the bot is notified of a message, this is triggered
@bot.event
async def on_message(message):
    if message.guild is None:
        return
    # ᕙ(`-´)ᕗ If the guild the message is from, is the guild that this version of Phillip is listening for,
    # this is enacted
    if GUILD == message.guild.name:
        # ᕙ(`-´)ᕗ if the message was from the bot, don't do anything
        if message.author == bot.user:
            return
        # ᕙ(`-´)ᕗ See whether one of the bots names was called
        await calling_command(message)

        # ᕙ(`-´)ᕗ These are various options that work without having to say the name first
        await stop(message)
        await name_list(message)
        await b99(message)
        await help_msg(message)
        await tone_tags(message)


# ᕙ(`-´)ᕗ Phillip is shut down, when they are misbehaving
async def stop(message):
    # ᕙ(`-´)ᕗ The message has to be solely stop, so it when it is said in a sentence it isn't triggered
    if message.content.lower() == 'stop':
        await message.channel.send('Shutting down')
        await bot.close()  # (ㆆ_ㆆ) Gives RuntimeError: Event loop is closed, so it works but probably not exactly


# ᕙ(`-´)ᕗ The bot responds with a list of names that they listen to for more advanced requests
async def name_list(message):
    if message.content.lower() == 'names':
        introduction = "Phillip responds to:"
        names = ""
        for name in dictionary.phillip_names:
            names += name + "\n"

        embed = discord.Embed(title=introduction, description=names, color=0xFF0000)
        await message.channel.send(embed=embed)


# ᕙ(`-´)ᕗ Easter egg from original development, sends a random brooklyn 99 quote
async def b99(message):
    if message.content == '99!':
        response = random.choice(dictionary.brooklyn_99_quotes)
        await message.channel.send(response)


# ᕙ(`-´)ᕗ Phillip sends a list of all the different things they can do.
async def help_msg(message):
    if message.content.lower() == 'help':
        introduction = "Hello, my name is P.H.I.L.L.I.P. I'll explain what I can do below."
        embed = discord.Embed(title='Phillip help list', description=introduction, color=0xFF0000)

        no_name_function = "\nYou don't have to call my name for me to listen to the following functions: \n"

        embed.add_field(name="No name", value=no_name_function, inline=False)

        for function in dictionary.always_functions:
            embed.add_field(name=function[0], value=function[1], inline=True)

        called_name_function = "\n If you call me (using one of the names listed in 'names') I will start listening " \
                               "for more commands.I will be listening for the first message you sent after you call " \
                               "me for 15 seconds, if you do not respond before that time I'll remove the reaction " \
                               "under your calling message.The commands I will be listening for are the following: \n"
        embed.add_field(name="Name called", value=called_name_function, inline=False)

        for function in dictionary.on_call_functions:
            embed.add_field(name=function[0], value=function[1], inline=True)

        await message.channel.send(embed=embed)


# ᕙ(`-´)ᕗ Shows information about tone tags and the different optionsS
async def tone_tags(message):
    await cogs['ToneTagCog'].general_explanation(message)


# ᕙ(`-´)ᕗ This is what happens after one of Phillip's names is said
async def calling_command(message):
    for name in dictionary.phillip_names:
        if message.content.lower() == name:
            response = 'At your service'
            await message.channel.send(response)
            msg = await cogs['UserCommunicationCog'].require_response(message)
            await cogs['SearchCog'].called_function_search(msg)
            # method =
            # await method


bot.run(TOKEN)
