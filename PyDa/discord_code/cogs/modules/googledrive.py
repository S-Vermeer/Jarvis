import logging

from discord.ext import commands


class GoogleDriveCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    # async def test(self, ctx):
    async def test(self):
        logging.warning("tested")


def setup(bot):
    bot.add_cog(GoogleDriveCog(bot))
