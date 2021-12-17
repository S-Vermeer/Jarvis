import logging

from discord.ext import commands
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

import discordcommands


class GoogleDriveCog(commands.Cog):
    title_question = 'Please specify the title for the document'

    def __init__(self, bot):
        self.bot = bot
        self.drive = None

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
        self.drive = gdrive
        return gdrive, http_obj

    # ᕙ(`-´)ᕗ Displays the files from the drive
    @commands.command()
    async def drive_inventory(self, message):
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        flag = False
        list_msg = ""
        for file in file_list:
            list_msg += '```Title: %s, ID: %s, mimeType: %s ```' % (file['title'], file['id'], file['mimeType'])
            flag = True
        if flag:
            await message.channel.send(list_msg)
        if not flag:
            message.channel.send('Sorry! no file found...')

    # ᕙ(`-´)ᕗ Make a new file and upload it to the drive
    @commands.command()
    async def create_file(self, title, content):
        file = self.drive.CreateFile({'title': title})
        file.SetContentString(content)
        file.Upload()

    @commands.command()
    async def change_title(self, file, newname):
        file.FetchMetadata(fields="title")
        file['title'] = newname  # Change title of the file
        file.Upload()  # Files.patch()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        print(" GoogleDriveCog ready")


# if message.content.lower().count("change name") >= 1:
#     await drive_inventory(message)
#     file = await select_file(message, bot)
#     title_msg = await get_question_response(title_question, message, bot)
#     change_title(file, title_msg.content)
#     return await message.channel.send("Title was changed to: " + file["title"])
#
# if message.content.lower().count("append") >= 1:
#     file = await select_file(message, bot)
#     addition_question = 'Please specify the text you want to add to the document'
#     content_to_add = await get_question_response(addition_question, message, bot)
#     add_to_content(file, content_to_add.content)
#     return await message.channel.send("add content method triggered")
#
# if message.content.lower().count("add image") >= 1:
#     title_msg = await get_question_response(title_question, message, bot)
#     content_msg = await get_question_response('Please upload the image(s)', title_msg, bot)
#     path = content_msg.attachments[0].url
#     create_image_file(title_msg.content, path)
#     return await message.channel.send("The image was added to the drive")

def setup(bot):
    bot.add_cog(GoogleDriveCog(bot))
    print("  GoogleDriveCog Cog added")
