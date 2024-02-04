from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.utils import progress_for_pyrogram, convert, humanbytes
from helper.database import db
from PIL import Image
import os
import time

# Define a function to handle the 'rename' callback
@Client.on_callback_query(filters.regex('rename'))
async def rename(bot, update):
    await update.message.delete()
    await update.message.reply_text("```Pʟᴇᴀsᴇ Eɴᴛᴇʀ Nᴇᴡ Fɪʟᴇ Nᴀᴍᴇ...```",
                                    reply_to_message_id=update.message.reply_to_message.id,
                                    reply_markup=ForceReply(True))

# Define the main message handler for private messages with replies
@Client.on_message(filters.private & filters.reply)
async def refunc(client, message):
    reply_message = message.reply_to_message
    if isinstance(reply_message.reply_markup, ForceReply):
        new_name = message.text
        await message.delete()
        msg = await client.get_messages(message.chat.id, reply_message.id)
        file = msg.reply_to_message
        media = getattr(file, file.media.value)
        if not "." in new_name:
            if "." in media.file_name:
                extn = media.file_name.rsplit('.', 1)[-1]
            else:
                extn = "mkv"
            new_name = new_name + "." + extn
        await reply_message.delete()

        # Use a list to store the inline keyboard buttons
        button = [
            [InlineKeyboardButton(
                "📁 Dᴏᴄᴜᴍᴇɴᴛ", callback_data="upload_document"),
            InlineKeyboardButton(
                "🎥 Vɪᴅᴇᴏ", callback_data="upload_video")]
        ]
        if file.media == MessageMediaType.AUDIO:
            button.append([InlineKeyboardButton(
                "🎵 Aᴜᴅɪᴏ", callback_data="upload_audio")])

        # Use a single call to reply with both text and inline keyboard
        await message.reply(
            text=f"**Sᴇʟᴇᴄᴛ Tʜᴇ Oᴜᴛᴩᴜᴛ Fɪʟᴇ Tyᴩᴇ**\n\n**• Fɪʟᴇ Nᴀᴍᴇ :-** `{new_name}`",
            reply_to_message_id=file.id,
            reply_markup=InlineKeyboardMarkup(button)
        )

# Define the callback for the 'upload' buttons
@Client.on_callback_query(filters.regex("upload"))
async def doc(bot, update):
    # Extracting necessary information
    prefix = await db.get_prefix(update.message.chat.id)
    suffix = await db.get_suffix(update.message.chat.id)
    new_name = update.message.text
    new_filename_ = new_name.split(":-")[1]

    try:
        # Construct the new filename based on prefix and suffix
        if prefix and suffix:
            shorted = new_filename_[:-4:]
            extension = new_filename_[-4::]
            new_filename = f"{prefix} {shorted} {suffix}{extension}"
        elif prefix:
            shorted = new_filename_[:-4:]
            extension = new_filename_[-4::]
            new_filename = f"{prefix} {shorted}{extension}"
        elif suffix:
            shorted = new_filename_[:-4:]
            extension = new_filename_[-4::]
            new_filename = f"{shorted} {suffix}{extension}"
        else:
            new_filename = new_filename_
    except Exception as e:
        return await update.message.edit(f"⚠️ Something went wrong can't able to set Prefix or Suffix ☹️ \n\n❄️ Contact My Creator -> @Shidoteshika1\nError: {e}")

    file_path = f"downloads/{new_filename}"
    file = update.message.reply_to_message

    ms = await update.message.edit("**➪ Tʀyɪɴɢ Tᴏ Dᴏᴡɴʟᴏᴀᴅɪɴɢ...**")
    try:
        path = await bot.download_media(message=file, file_name=file_path, progress=progress_for_pyrogram, progress_args=(f"🌀 **Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....**\n```NEW FILE NAME:\n{new_filename}```", ms, time.time()))
    except Exception as e:
        return await ms.edit(e)

    duration = 0
    try:
        metadata = extractMetadata(createParser(file_path))
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
    except:
        pass
    ph_path = None
    media = getattr(file, file.media.value)
    c_caption = await db.get_caption(update.message.chat.id)
    c_thumb = await db.get_thumbnail(update.message.chat.id)

    if c_caption:
        try:
            caption = c_caption.format(filename=new_filename, filesize=humanbytes(
                media.file_size), duration=convert(duration))
        except Exception as e:
            return await ms.edit(text=f"Yᴏᴜʀ Cᴀᴩᴛɪᴏɴ Eʀʀᴏʀ Exᴄᴇᴩᴛ Kᴇyᴡᴏʀᴅ Aʀɢᴜᴍᴇɴᴛ ●> ({e})")
    else:
        caption = f"**{new_filename}**"

    if (media.thumbs or c_thumb):
        if c_thumb:
            ph_path = await bot.download_media(c_thumb)
        else:
            ph_path = await bot.download_media(media.thumbs[0].file_id)
        Image.open(ph_path).convert("RGB").save(ph_path)
        img = Image.open(ph_path)
        img.resize((320, 320))
        img.save(ph_path, "JPEG")

    await ms.edit("**➪ Tʀyɪɴɢ Tᴏ Uᴩʟᴏᴀᴅɪɴɢ...**")
    type = update.data.split("_")[1]
    try:
        if type == "document":
            await bot.send_document(
                update.message.chat.id,
                document=file_path,
                thumb=ph_path,
                caption=caption,
                progress=progress_for_pyrogram,
                progress_args=(f"🌀 **Uᴩʟᴏᴅ Sᴛᴀʀᴛᴇᴅ....**\n```RENAMED FILE:\n{new_filename}```", ms, time.time()))
        elif type == "video":
            await bot.send_video(
                update.message.chat.id,
                video=file_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=(f"🌀 **Uᴩʟᴏᴅ Sᴛᴀʀᴛᴇᴅ....**\n```RENAMED FILE:\n{new_filename}```", ms, time.time()))
        elif type == "audio":
            await bot.send_audio(
                update.message.chat.id,
                audio=file_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=(f"🌀 **Uᴩʟᴏᴅ Sᴛᴀʀᴛᴇᴅ....**\n```RENAMED FILE:\n{new_filename}```", ms, time.time()))
    except Exception as e:
        os.remove(file_path)
        if ph_path:
            os.remove(ph_path)
        return await ms.edit(f" Eʀʀᴏʀ {e}")

    await ms.delete()
    os.remove(file_path)
    if ph_path:
        os.remove(ph_path)
