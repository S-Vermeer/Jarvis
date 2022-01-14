import random

from discord.ext import commands
import assets.dictionary as dictionary


class WellbeingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ᕙ(`-´)ᕗ How is Phillip doing?
    @commands.command()
    async def mood(self, message):
        response = 'Well I can respond, that\'s something'  # ʕ•́ᴥ•̀ʔっ More responses to how Phillip is doing
        await message.channel.send(response)

    # ᕙ(`-´)ᕗ Prompts someone who is tagged to sleep
    @commands.command()
    async def sleep_helper(self, message):
        response = (random.choice(dictionary.sleep_encouragements) % message.mentions[0].mention)
        await message.channel.send(response)

    # ᕙ(`-´)ᕗ Compliments someone who is tagged
    @commands.command()
    async def complimenter(self, message):
        response = (random.choice(dictionary.compliments) % message.mentions[0].nick)
        await message.channel.send(response)


def setup(bot):
    bot.add_cog(WellbeingCog(bot))
    print("  WellbeingCog added")
