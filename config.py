import re, os, time

id_pattern = re.compile(r'^.\d+$') 

class Config(object):
    # pyro client config
    API_ID    = os.environ.get("API_ID", "") #⚠️ Required
    API_HASH  = os.environ.get("API_HASH", "") #⚠️ Required
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "") #⚠️ Required
   
    # database config
    DB_NAME = os.environ.get("DB_NAME","Snow_User_Data")     
    DB_URL  = os.environ.get("DB_URL","") #⚠️ Required
 
    # other configs
    BOT_UPTIME  = time.time()
    START_PIC   = os.environ.get("START_PIC", "")
    ADMIN       = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '').split()] #⚠️ Required
    FORCE_SUB   = os.environ.get("FORCE_SUB", "") #⚠️ Required Username without @
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "")) #⚠️ Required
    FLOOD = int(os.environ.get("FLOOD", '10'))
    BANNED_USERS = set(int(x) for x in os.environ.get("BANNED_USERS", "1234567890").split())

    # wes response configuration     
    WEBHOOK = bool(os.environ.get("WEBHOOK", True))
    PORT = int(os.environ.get("PORT", "8080"))



class Txt(object):
    # part of text configuration
    START_TXT = """<b>Hᴇʟʟᴏ {} 👋,

<b>Tʜɪs ɪs ᴀɴ ᴀᴅᴠᴀɴᴄᴇᴅ... nah man, 😂 i don't think i should
tell you the work of a rename bot , but if you're new to the 
process,... 😂ask your friends 


⚡️Pʀᴇsᴇɴᴛᴇᴅ Bʏ - @notmoviebuff</b>"""

    ABOUT_TXT = """<b>🤖 My Name: {}
    
I ᴀᴍ Dᴇᴠᴇʟᴏᴘᴇᴅ ғᴏʀ Fɪʟᴇ Oᴘᴇʀᴀᴛɪᴏɴ ᴜᴘᴛᴏ 𝟸GB ᴏɴ Tᴇʟᴇɢʀᴀᴍ.</b>

    <b>Mʏ Dᴀᴛᴀʙᴀsᴇ, Lɪʙʀᴀʀʏ, Sᴇʀᴠᴇʀ, Sᴏᴜʀᴄᴇ Cᴏᴅᴇs ᴅᴇᴛᴀɪʟs ᴀʀᴇ Rᴇsᴛʀɪᴄᴛᴇᴅ ʙʏ ᴍʏ Oᴡɴᴇʀ.Iғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴋɴᴏᴡ ᴛʜᴇɴ ᴀsᴋ Mʏ Oᴡɴᴇʀ: @notmoviebuff</b>"""

    HELP_TXT = """
🌌 <b><u>HOW TO SET THUMBNILE</u></b>
  
‣ /start the BOT and send any photo to automatically set thumbnile
‣ /del_thumb - Delete your old thumbnile
‣ /view_thumb - View your current thumbnile

📑 <b><u>HOW TO SET CUSTOM CAPTION</u></b>

‣ /set_caption - Set a custom caption
‣ /see_caption - View your caption
‣ /del_caption - Delete your caption

Example:- /set_caption `📕 Fɪʟᴇ Nᴀᴍᴇ: {filename}
💾 Sɪᴢᴇ: {filesize}
⏰ Dᴜʀᴀᴛɪᴏɴ: {duration}`

✏️ <b><u>HOW TO RENAME A FILE</u></b>

‣ new_file_name.extension
Send any file and type new file name \nAnd select the format [ document, video, audio ].
Example:- `E01 Solo Leveling (480p) ESUB @AnimeChidori.mkv`

<b><u>AUTO RENAME OPTION</u>:</b>
‣ /autorename {formatt}
Example:- `/autorename EP  Solo Leveling () ESUB @AnimeChidori`
"""


    PROGRESS_BAR = """<b>
    
‣ 🗃️ Sɪᴢᴇ: {1} | {2}
‣ ⏳️ Dᴏɴᴇ : {0}%
‣ 🚀 Sᴩᴇᴇᴅ: {3}/s
‣ ⏰️ Eᴛᴀ: {4}

⚡️Pᴏᴡᴇʀᴇᴅ Bʏ - @the_moviebuff_tv</b>"""
