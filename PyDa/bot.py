import os
import random
import asyncio

import discord
from dotenv import load_dotenv

import wikipedia as wp
import wolframalpha as wa

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
app_id = os.getenv('APP_ID')
intents = discord.Intents.default()
intents.members = True
intents.reactions = True

client = discord.Client(intents=intents)


def connect_wa():
    client = wa.Client(app_id)
    return client

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

#    members = '\n - '.join([member.name for member in guild.members])
#    print(f'Guild Members:\n - {members}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    phillip_names = ["whaddup phillip", "yo phillip", "my boy phillip", "hey phillip", "yo philly boy", "phillip", "p.h.i.l.l.i.p.", "p.h.i.l.l.i.p"]
    for name in phillip_names:
        if message.content.lower() == name:
            response = 'At your service'
            await message.channel.send(response)
            try:
                await message.add_reaction('👍')
                msg = await client.wait_for('message', check=check(message.author), timeout=15)

                if msg.content == "How are you":
                    response = 'Well I can respond, thats something'
                await message.channel.send(response)

                if msg.content.lower().count("search") >= 1:
                    answer = search_internet(msg.content,message)

                    msg = await message.channel.send(answer[0])

                    if len(answer) > 1:
                        await msg.add_reaction('👍')
                        @client.event
                        async def on_reaction_add(reaction, user):
                            if reaction.emoji == '👍' and user.id != client.user.id:
                                await message.channel.send(answer[1])
            except:
                await message.remove_reaction('👍',client.user)


    if message.content.lower() == 'stop':
        await message.channel.send('Shutting down')
        await client.logout()

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    if message.content == '99!':
        response = random.choice(brooklyn_99_quotes)
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