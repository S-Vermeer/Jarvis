import logging

import discord
from discord.ext import commands

import wikipedia as wp
import wolframalpha as wa


class SearchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = wa.Client("")
        self.cogs = {}

    @commands.command()
    async def assign_cogs_and_connect(self, cogs, app_id):
        self.cogs = cogs
        self.client = wa.Client(app_id)


    @commands.command()
    # ᕙ(`-´)ᕗ Check which action is asked for after phillip is called
    async def called_function_search(self, message):
        await self.cogs["WellbeingCog"].search_wellbeing_method(message)

        if message.content.lower().count("search") >= 1:
            await self.search_answer(message)

        if message.content.lower().count("drive") >= 1:
            await self.cogs["GoogleDriveCog"].drive_functions(message)

        # if message.content.lower().count("morning") >= 1:
        #     return good_morning(message.guild, self.cogs['UserCommunicationCog'])

        if message.content.lower().count("tone") and message.content.lower().count("/") >= 1:
            response = await self.cogs['ToneTagCog'].specific_explanation(message)
            await message.channel.send(response)

    @commands.command()
    # ᕙ(`-´)ᕗ Search for the answer of a question on wikipedia and wolframalpha
    async def search_answer(self, message):
        embed = discord.Embed(title="Search results", color=0xFF0000)
        answer = await self.search_internet(message.content)
        embed.add_field(name=answer[0][0], value=answer[0][1], inline=True)
        if len(answer) > 1:
            embed.add_field(name=answer[1][0], value=answer[1][1], inline=True)
        return await message.channel.send(embed=embed)

    # ᕙ(`-´)ᕗ Search the internet for a response on the inputted query
    @commands.command()
    async def search_internet(self, input_query):
        no_results = ["No results", "Unfortunately no results could be found"]
        try:  # ᕙ(`-´)ᕗ Try to get results for both Wiki and Wolfram
            res = self.client.query(input_query)
            wolfram_res = next(res.results).text  # ᕙ(`-´)ᕗ print top wolframalpha results of input

            wiki_res = wp.summary(input_query, sentences=2)
            answer_wa = ["Wolfram Result:", wolfram_res]
            answer_wp = ["Wikipedia Result:", wiki_res]
            answer = [answer_wa, answer_wp]
            return answer

        except (wp.exceptions.DisambiguationError, wp.exceptions.PageError,
                wp.exceptions.WikipediaException):  # ᕙ(`-´)ᕗ Get only wolfram if wiki throws exceptions
            try:
                res = self.client.query(input_query)
                wolfram_res = next(res.results).text  # ᕙ(`-´)ᕗ print top wolframalpha results of input
                return [["Wolfram Result:", wolfram_res]]

            except (StopIteration, AttributeError):
                try:
                    wiki_res = wp.summary(input_query, sentences=2)
                    result = [["Wikipedia result:", wiki_res]]
                    return result
                except BaseException as e:
                    logging.exception(f'error while accessing the wiki summary: { repr(e) }')
                    return [no_results]

        except (
                StopIteration,
                AttributeError):  # ᕙ(`-´)ᕗ And if wolfram also doesnt work, say that no results were found
            return [no_results]

        except BaseException as e:  # ᕙ(`-´)ᕗ All the attributes inside your window.
            logging.exception(f'error while accessing the searches that couldn\'t be specified { repr(e) }')
            return no_results


def setup(bot):
    bot.add_cog(SearchCog(bot))
    print("  SearchCog added")
