import logging
import random
import threading
import time

import schedule
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

    # def morning_message(self):
    #     self.bot.send("test morning message every minute")

    # def non_async_morning_message(self):
    #     # logging.warning(message.content)
    #     self.bot.loop.call_soon_threadsafe(self.morning_message)

    # @commands.command()
    # async def schedule_morning_message(self):
    #     # schedule.every().day.at("14:48").do(self.morning_message(message))
    #     schedule.every().minute.do(self.non_async_morning_message)
    #     run_continuously(1)

    # ᕙ(`-´)ᕗ Hypes Jesse, a mod from the Avieno discord
    @commands.command()
    async def jesse_hype(self, message):
        uid = '<@745738275968516176>'
        response = (
            f":regional_indicator_w: :regional_indicator_e:   :regional_indicator_l: :regional_indicator_o: "
            f":regional_indicator_v: :regional_indicator_e:   :regional_indicator_j: :regional_indicator_e: "
            f":regional_indicator_s: :regional_indicator_s: :regional_indicator_e: \n Hey { uid }, we wanna remind "
            f"you that we love you! \n Here have some love from the fan club! \n :partying_face: :heart: "
            f":orange_heart: :yellow_heart: :green_heart: :blue_heart: :purple_heart: :blue_heart: :green_heart: "
            f":yellow_heart: :orange_heart: :heart: :partying_face:")
        await message.channel.send(response)

    @commands.command()
    async def search_wellbeing_method(self, message):
        if message.content.lower().count("how are you") >= 1:
            await self.mood(message)

        if message.content.lower().count("sleep") >= 1:
            await self.sleep_helper(message)

        if message.content.lower().count("hype") >= 1:
            await self.complimenter(message)

        if message.content.lower().count("jesse") >= 1:
            await self.jesse_hype(message)

        if message.content.lower().count("morning") >= 1:
            await self.schedule_morning_message()
            logging.warning("running")


def setup(bot):
    bot.add_cog(WellbeingCog(bot))
    print("  WellbeingCog added")


morning_active = False


def run_continuously(check, interval=1):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not check:
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


# Start the background thread
stop_run_continuously = run_continuously(morning_active)


# def stop_run_morning():
#     global morning_active
#     morning_active = True
