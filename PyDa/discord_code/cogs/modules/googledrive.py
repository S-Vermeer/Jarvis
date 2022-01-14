import json
import logging
import io

from discord.ext import commands
import requests
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

import discordcommands


class GoogleDriveCog(commands.Cog):
    title_question = 'Please specify the title for the document'

    def __init__(self, bot):
        self.bot = bot
        self.drive = None
        self.folder_id = ''

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
            logging.warning(gauth.Refresh())

            # (ㆆ_ㆆ) Does not Refresh yet?

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
        await self.get_folder_id(guild)
        return gdrive, http_obj

    @commands.command()
    async def drive_inventory(self, message):
        file_list = self.drive.ListFile({'q': "\'" + self.folder_id + "\' in parents and trashed=false"}).GetList()
        flag = False
        list_msg = ""
        for file in file_list:
            list_msg += f"```Title: { file['title'] }, ID: { file['id'] }, mimeType: { file['mimeType'] }```"
            flag = True
        if flag:
            await message.channel.send(list_msg)
        if not flag:
            message.channel.send('Sorry! no file found...')

    # ᕙ(`-´)ᕗ Make a new file and upload it to the drive
    @commands.command()
    async def create_file(self, title, content):
        file = self.drive.CreateFile({'title': title, 'parents': [{'id': f'{self.folder_id}'}]})
        file.SetContentString(content)
        file.Upload()

    # ᕙ(`-´)ᕗ Change the title of an existing file
    @commands.command()
    async def change_title(self, file, newname):
        file.FetchMetadata(fields="title")
        file['title'] = newname  # Change title of the file
        file.Upload()  # Files.patch()

    # ᕙ(`-´)ᕗ Add some content to an existing file
    @commands.command()
    async def add_to_content(self, file, content_to_add):
        content = file.GetContentString()  # 'Hello'
        file.SetContentString(f"{ content } { content_to_add } \n")
        file.Upload()

    # ᕙ(`-´)ᕗ Upload a new image
    @commands.command()
    async def create_image_file(self, title, content):
        url = content  # Please set the direct link of the image file.
        filename = title  # Please set the filename on Google Drive.
        folder_id = self.folder_id  # Please set the folder ID. The file is put to this folder.

        # ᕙ(`-´)ᕗ To get these requests, LocalWebserverAuth has to be used
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        metadata = {
            "name": filename,
            "parents": [folder_id]
        }
        files = {
            'data': ('metadata', json.dumps(metadata), 'application/json'),
            'file': io.BytesIO(requests.get(url).content)
        }
        requests.post(
            "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
            headers={"Authorization": "Bearer " + gauth.credentials.access_token},
            files=files
        )

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        print(" GoogleDriveCog ready")

    async def get_folder_id(self, guild):
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file in file_list:
            if file['title'] == guild.name:
                print(file['id'])
                self.folder_id = file['id']
                break

    async def show_file_content(self, file):
        content = file.GetContentString()  # 'Hello'
        return content



def setup(bot):
    bot.add_cog(GoogleDriveCog(bot))
    print("  GoogleDriveCog Cog added")
