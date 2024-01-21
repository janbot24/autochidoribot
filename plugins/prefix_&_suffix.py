from pyrogram import Client, filters
from helper.database import db

PREFIX_CMD = 'set_prefix'
DEL_PREFIX_CMD = 'del_prefix'
SEE_PREFIX_CMD = 'see_prefix'
SUFFIX_CMD = 'set_suffix'
DEL_SUFFIX_CMD = 'del_suffix'
SEE_SUFFIX_CMD = 'see_suffix'


async def set_value(client, message, db_function, success_message, no_value_message):
    if len(message.command) == 1:
        return await message.reply_text(f"**__Give The Value__\n\nExample:- `/{message.command[0]} @Roofiverse`**")
    
    value = message.text.split(" ", 1)[1]
    SnowDev = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    await db_function(message.from_user.id, value)
    await SnowDev.edit(f"__**✅ {success_message}**__")


async def delete_value(client, message, db_function, success_message, no_value_message):
    SnowDev = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    value = await db_function(message.from_user.id)
    if not value:
        return await SnowDev.edit(f"__**😔 {no_value_message}**__")
    await db_function(message.from_user.id, None)
    await SnowDev.edit(f"__**❌️ {success_message}**__")


async def see_value(client, message, db_function, no_value_message):
    SnowDev = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    value = await db_function(message.from_user.id)
    if value:
        await SnowDev.edit(f"**Your value: -**\n\n`{value}`")
    else:
        await SnowDev.edit(f"__**😔 You don't have any {no_value_message}**__")


@Client.on_message(filters.private & filters.command(PREFIX_CMD))
async def add_caption(client, message):
    await set_value(client, message, db.set_prefix, "Prefix saved", "You don't have any prefix")


@Client.on_message(filters.private & filters.command(DEL_PREFIX_CMD))
async def delete_prefix(client, message):
    await delete_value(client, message, db.set_prefix, "Prefix deleted", "You don't have any prefix")


@Client.on_message(filters.private & filters.command(SEE_PREFIX_CMD))
async def see_caption(client, message):
    await see_value(client, message, db.get_prefix, "prefix")


# SUFFIX
@Client.on_message(filters.private & filters.command(SUFFIX_CMD))
async def add_csuffix(client, message):
    await set_value(client, message, db.set_suffix, "Suffix saved", "You don't have any suffix")


@Client.on_message(filters.private & filters.command(DEL_SUFFIX_CMD))
async def delete_suffix(client, message):
    await delete_value(client, message, db.set_suffix, "Suffix deleted", "You don't have any suffix")


@Client.on_message(filters.private & filters.command(SEE_SUFFIX_CMD))
async def see_csuffix(client, message):
    await see_value(client, message, db.get_suffix, "suffix")
