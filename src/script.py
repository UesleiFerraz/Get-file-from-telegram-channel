from telethon.sync import TelegramClient, events
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import InputPeerEmpty
from tqdm import tqdm
from dotenv import load_dotenv
import os

load_dotenv()
# You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
path_to_save = os.getenv('PATH_TO_SAVE')

def download_media(group, cl, name):
    limit = 50 # limit of files by request. I recommend to set a small number.

    for x in range(3100): # Range is how many files you want to download divided by limit.
      messages = cl.get_messages(group, limit=limit, add_offset=x*limit)
      for message in tqdm(messages):
        try:
          if message.file:
            if (message.file.mime_type == 'image/jpeg' or 
                message.file.mime_type == 'image/png' or 
                message.file.mime_type == 'image/gif'):
              message.download_media(path_to_save + '/' + name + '/images/')
            elif (message.file.mime_type == 'video/mp4' or 
                  message.file.mime_type == 'video/quicktime' or 
                  message.file.mime_type == 'video/x-matroska' or 
                  message.file.mime_type == 'video/x-msvideo' or 
                  message.file.mime_type == 'video/x-flv' or 
                  message.file.mime_type == 'video/x-ms-wmv' or 
                  message.file.mime_type == 'video/x-ms-asf' or 
                  message.file.mime_type == 'video/mp3'):
              message.download_media(path_to_save + name + '/videos/')
            else:
              message.download_media(path_to_save + name + '/others/')
        except Exception as e:
          print(e)
        finally:
          pass


with TelegramClient('name', api_id, api_hash) as client:
    result = client(GetDialogsRequest(
        offset_date=None,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=500,
        hash=0,
    ))

    title = 'example title'         # Title for channel
    channel = client(GetFullChannelRequest(title))
    print(channel.full_chat)

    download_media(channel.full_chat, client, title)
