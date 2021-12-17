import logging
from datetime import datetime

from discord.ext import commands
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

from PyDa.discord_code import discordcommands


class GoogleDriveCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def drive_connect(self, guild):
        GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = "credentials/client_secrets.json"
        gauth = GoogleAuth()

        gauth.LoadCredentialsFile("./credentials/mycreds.txt")  # ᕙ(`-´)ᕗ Load credentials, if any (hidden in github)
        if gauth.credentials is None:
            # ᕙ(`-´)ᕗ Get the url that the user must use to give access to google drive
            auth_url = gauth.GetAuthUrl()

            uid = 245989473408647171  # ᕙ(`-´)ᕗ Skyler (Developer) User ID so the message is DMed to them

            skyler = guild.get_member(uid)
            msg = await discordcommands.dm_member_wait_for_response(skyler, auth_url, self.bot)

            logging.warning(msg.content)
            gauth.Auth(msg.content)

            logging.warning("Authorisation complete")
        elif gauth.access_token_expired:
            # ᕙ(`-´)ᕗ Refresh them if expired
            # (ㆆ_ㆆ) Does not Refresh yet?
            open('./credentials/mycreds.txt', 'w').close()
            logging.warning("refresh")
        else:
            # ᕙ(`-´)ᕗ Initialize the saved creds
            gauth.Authorize()
            logging.warning("used saved creds")
        # ᕙ(`-´)ᕗ Save the current credentials to a file
        gauth.SaveCredentialsFile("credentials/mycreds.txt")

        gdrive = GoogleDrive(gauth)

        # ᕙ(`-´)ᕗ Create httplib.Http() object.
        http_obj = gdrive.auth.Get_Http_Object()
        return gdrive, http_obj

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        print(" GoogleDriveCog ready")


def setup(bot):
    bot.add_cog(GoogleDriveCog(bot))
    print("  GoogleDriveCog Cog added")