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

    # ᕙ(`-´)ᕗ Send a direct message to a member and wait 60 seconds for a response
    @commands.command()
    async def dm_member_wait_for_response(self, member, message):
        await self.dm_member(member, message)
        msg = await self.bot.wait_for('message', check=check(member), timeout=60)
        return msg

    # ᕙ(`-´)ᕗ Send a direct message to a member
    @commands.command()
    async def dm_member(self, member, message):
        await member.create_dm()
        await member.dm_channel.send(message)

    @commands.command()
    # ᕙ(`-´)ᕗ Send something but need a response to continue
    async def require_response(self, message):
        try:
            await message.add_reaction('👍')

            def author_check(author):

                def inner_check(message_to_check):
                    if message_to_check.author != author:
                        return False
                    else:
                        return True

                return inner_check

            msg = await self.bot.wait_for('message', check=author_check(message.author), timeout=15)
            return msg

        except Exception as e:
            await message.remove_reaction('👍', self.bot.user)
            logging.warning(repr(e))


def setup(bot):
    bot.add_cog(UserCommunicationCog(bot))
    print("  UserCommunicationCog added")


def check(author):  # ᕙ(`-´)ᕗ check whether the message was sent by the requester
    def inner_check(message):
        if message.author != author or message.channel != author.dm_channel:
            return False
        else:
            return True

    return inner_check
