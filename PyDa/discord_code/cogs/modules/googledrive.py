import json
import logging
import io

from discord.ext import commands
import requests
from googleapiclient.errors import HttpError
from pydrive2.files import ApiRequestError
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

import discordcommands


class GoogleDriveCog(commands.Cog):
    title_question = 'Please specify the title for the document'

    def __init__(self, bot):
        self.bot = bot
        self.drive = None
        self.folder_id = ''
        self.com_cog = None

    @commands.command()
    async def drive_connect(self, guild, user_communication):
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
        self.com_cog = user_communication
        await self.get_folder_id(guild)
        return gdrive, http_obj

    @commands.command()
    async def drive_functions(self, message):
        if message.content.lower().count("inventory") >= 1:
            await self.drive_inventory(message)

        if message.content.lower().count("create") >= 1:
            return await self.create_file(message)

        if message.content.lower().count("change name") >= 1:
            return await self.change_title(message)

        if message.content.lower().count("append") >= 1:
            return await self.add_to_content(message)

        if message.content.lower().count("show") >= 1:
            try:
                return await self.show_file_content(message)
            except (HttpError, ApiRequestError):
                await message.channel.send("I did not recognize that id, are you sure you sent an id from the drive "
                                           "inventory?")

            # (ㆆ_ㆆ) Doesnt work in server due to not opening in browser
            # if message.content.lower().count("add image") >= 1:
            #     return await self.create_image_file(message)

    @commands.command()
    async def drive_inventory(self, message):
        file_list = self.drive.ListFile({'q': "\'" + self.folder_id + "\' in parents and trashed=false"}).GetList()
        flag = False
        list_msg = ""
        for file in file_list:
            list_msg += f"```Title: {file['title']}, ID: {file['id']}, mimeType: {file['mimeType']}```"
            flag = True
        if flag:
            await message.channel.send(list_msg)
        if not flag:
            message.channel.send('Sorry! no file found...')

    # ᕙ(`-´)ᕗ Make a new file and upload it to the drive
    @commands.command()
    async def create_file(self, message):
        title_msg = await self.com_cog.get_question_response(self.title_question, message)
        content_msg = await self.com_cog.get_question_response('Please specify the content for the document', title_msg)
        file = self.drive.CreateFile({'title': title_msg.content, 'parents': [{'id': f'{self.folder_id}'}]})
        file.SetContentString(content_msg.content)
        file.Upload()
        return await message.channel.send(f"Title: {title_msg.content} \n Content: {content_msg.content}")

    # ᕙ(`-´)ᕗ Change the title of an existing file
    @commands.command()
    async def change_title(self, message):
        await self.drive_inventory(message)
        file = await self.select_file(message)
        try:
            file.FetchMetadata(fields="title")
            title_msg = await self.com_cog.get_question_response(self.title_question, message)
            file['title'] = title_msg.content  # Change title of the file
            file.Upload()  # Files.patch()
            return await message.channel.send(f"Title was changed to: {file['title']}")

        except (HttpError, ApiRequestError):
            await message.channel.send("I did not recognize that id, are you sure you sent an id from the drive "
                                       "inventory?")

    # ᕙ(`-´)ᕗ Add some content to an existing file
    @commands.command()
    async def add_to_content(self, message):
        await self.drive_inventory(message)
        file = await self.select_file(message)
        try:
            content = file.GetContentString()
            addition_question = 'Please specify the text you want to add to the document'
            content_to_add = await self.com_cog.get_question_response(addition_question, message)
            file.SetContentString(f"{content} {content_to_add.content} \n")
            file.Upload()
            return await message.channel.send(f"{content_to_add.content} was added to {file['title']}")
        except (HttpError, ApiRequestError):
            await message.channel.send("I did not recognize that id, are you sure you sent an id from the drive "
                                       "inventory?")

    # ᕙ(`-´)ᕗ Upload a new image
    @commands.command()
    async def create_image_file(self, message):
        title_msg = await self.com_cog.get_question_response(self.title_question, message)
        content_msg = await self.com_cog.get_question_response('Please upload the image(s)', title_msg)
        url = content_msg.attachments[0].url
        filename = title_msg.content  # Please set the filename on Google Drive.
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
        return await message.channel.send("The image was added to the drive")

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

    async def show_file_content(self, message):
        await self.drive_inventory(message)
        file = await self.select_file(message)
        content = file.GetContentString()  # 'Hello'
        return await message.channel.send(f"{file['title']}: \n {content}")

    # ᕙ(`-´)ᕗ Select a file based on the specified id. 'Creating' only replicates it, if it isn't uploaded,
    # nothing happens/
    async def select_file(self, message):
        file_id = await self.com_cog.get_question_response('Please specify the id of the document you want to use',
                                                           message)
        return self.drive.CreateFile({'id': file_id.content})


def setup(bot):
    bot.add_cog(GoogleDriveCog(bot))
    print("  GoogleDriveCog Cog added")
