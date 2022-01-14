import logging
import os

import discord
from discord.ext import commands

import assets.dictionary as dictionary
from dotenv import load_dotenv


class ToneTagCog(commands.Cog):
    def __init__(self, bot, guild):
        self.bot = bot
        self.guild = guild
        self.com_cog = None

    @commands.command()
    async def general_explanation(self, message):
        if message.content.lower() == 'tonetags':
            introduction = "tone tags / tone indicators are things you can include with text to indicate what the " \
                           "tone of it is. Some people have difficulty picking up on tone. communicating through text "\
                           "only makes this harder due to lack of audio and physical clues (voice inflection, " \
                           "body language, facial expressions, etc.) Tagging what tone you are using can be very " \
                           "helpful for others understanding of what you're saying, clarification, avoiding " \
                           "miscommunications, etc. \n "

            embed = discord.Embed(title='Tone tags', description=introduction, color=0xFF0000)

            for tone_tag in dictionary.tone_tags:
                embed.add_field(name=tone_tag[0], value=tone_tag[1], inline=True)

            await message.channel.send(embed=embed)

    @commands.command()
    async def specific_explanation(self, message):
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
                    response += f"{ tone_tag[0] } = { tone_tag[1] } \n"

        if response == "The following tone tags are possible: \n":
            response = "Unfortunately I could not find a tone tag matching this"

        return response

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        print(" ToneTagCog ready")

    # ᕙ(`-´)ᕗ If a reaction is added to a message since the bot started listening, this is triggered.
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message.guild is None:
            return
        # ᕙ(`-´)ᕗ If the guild is correct, it is not sent by the bot, the reaction is an emoji with a monocle and there
        # is at least one / in the message, this is triggered
        if self.guild == reaction.message.guild.name and user != self.bot.user and \
                reaction.emoji == "🧐" and reaction.message.content.count("/") >= 1:
            # ᕙ(`-´)ᕗ You receive a DM with information about the tone tags in the message reacted to.
            response = f"You requested tone tag information about: {reaction.message.content} \n"
            response += await self.specific_explanation(reaction.message)
            await self.com_cog.dm_member(user, response)


def setup(bot):
    load_dotenv()
    guild = os.getenv('DISCORD_GUILD')
    bot.add_cog(ToneTagCog(bot, guild))
    bot.get_cog("UserCommunicationCog")
    print("  ToneTagCog added")
