from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from helper.database import db
from config import Config, Txt
import humanize
from time import sleep


@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    if message.from_user.id in Config.BANNED_USERS:
        await message.reply_text("Sorry, You are banned.")
        return

    user = message.from_user
    await db.add_user(client, message)
    
    button_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('⛅ Uᴩᴅᴀᴛᴇꜱ', url='https://t.me/Kdramaland'),
         InlineKeyboardButton('🌨️ Sᴜᴩᴩᴏʀᴛ', url='https://t.me/SnowDevs')],
        [InlineKeyboardButton('☃️ Aʙᴏᴜᴛ', callback_data='about'),
         InlineKeyboardButton('❗ Hᴇʟᴩ', callback_data='help')]
    ])

    if Config.START_PIC:
        await message.reply_photo(Config.START_PIC, caption=Txt.START_TXT.format(user.mention), reply_markup=button_markup)
    else:
        await message.reply_text(text=Txt.START_TXT.format(user.mention), reply_markup=button_markup, disable_web_page_preview=True)


@Client.on_message(filters.private & (filters.document | filters.audio | filters.video))
async def rename_start(client, message):
    file = getattr(message, message.media.value)
    filename = file.file_name
    filesize = humanize.naturalsize(file.file_size)

    async def send_rename_message():
        text = f"""**__What do you want me to do with this file.?__**\n\n**File Name** :- `{filename}`\n\n**File Size** :- `{filesize}`"""
        buttons = [[InlineKeyboardButton("📝 𝚂𝚃𝙰𝚁𝚃 𝚁𝙴𝙽𝙰𝙼𝙴 📝", callback_data="rename")],
                   [InlineKeyboardButton("✖️ 𝙲𝙰𝙽𝙲𝙴𝙻 ✖️", callback_data="close")]]
        await message.reply_text(text=text, reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(buttons))

    try:
        await send_rename_message()
    except FloodWait as e:
        await sleep(e.value)
        await send_rename_message()
    except:
        pass


@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data
    message = query.message

    async def edit_message(text, markup):
        await message.edit_text(text=text, disable_web_page_preview=True, reply_markup=markup)

    if data == "start":
        await edit_message(Txt.START_TXT.format(query.from_user.mention), button_markup)
    elif data in ["help", "about"]:
        text = Txt.HELP_TXT if data == "help" else Txt.ABOUT_TXT.format(client.mention)
        await edit_message(text, back_markup)
    elif data == "close":
        try:
            await message.delete()
            await message.reply_to_message.delete()
            await message.continue_propagation()
        except:
            await message.delete()
            await message.continue_propagation()
