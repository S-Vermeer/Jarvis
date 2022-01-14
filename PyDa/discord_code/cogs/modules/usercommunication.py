import logging

from discord.ext import commands


class UserCommunicationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ᕙ(`-´)ᕗ Send a question and return the result
    @commands.command()
    async def get_question_response(self, question, message):
        await message.channel.send(question)
        return await self.wait_for_response_message_drive(message)

# ᕙ(`-´)ᕗ Wait for a response, specifically for the drive
    @commands.command()
    async def wait_for_response_message_drive(self, message):
        try:
            await message.add_reaction('👍')

            def check_author(author):

                def inner_check(message_to_check):
                    if message_to_check.author != author:
                        logging.warning("author doesn't match")
                        return False
                    else:
                        return True

                return inner_check

            msg = await self.bot.wait_for('message', check=check_author(message.author), timeout=15)
            return msg

        except Exception as e:
            await message.remove_reaction('👍', self.bot.user)
            logging.warning(repr(e))


def setup(bot):
    bot.add_cog(UserCommunicationCog(bot))
    print("  UserCommunicationCog added")