from discord.ext.commands import Cog

class Wellbeing(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def wellbeing(self,ctx):
        response = 'Well I can respond, thats something'
        await ctx.send(response)