import os
import logging 
import subprocess
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import LOG_CHANNEL, ADMINS, DAILY_LIMITS
from database.db import db
from pyrogram.enums import ParseMode 
from plugins.youtube import active_tasks

logger = logging.getLogger(__name__)

 

@Client.on_message(filters.command("start"))
async def start(client, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("❓ Hᴇʟᴘ", callback_data="help"), InlineKeyboardButton("ℹ️ Aʙᴏᴜᴛ", callback_data="about")],
        [InlineKeyboardButton("📢 Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ", url="https://t.me/ftmbotzx")]
    ])
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(
            LOG_CHANNEL, 
            f"**#NewUser 🔻**\n**ID -> `{message.from_user.id}`**\n**Name -> {message.from_user.mention}**"
        )
    await message.reply_text(
    "ʜᴇʏ ʙʀᴏ! ɪ'ᴍ ғᴛᴍ ᴛᴜʙᴇғᴇᴛᴄʜ ʙᴏᴛ 🎬\n\n"
    "ɪ ᴄᴀɴ ᴅᴏᴡɴʟᴏᴀᴅ ʏᴏᴜᴛᴜʙᴇ ᴠɪᴅᴇᴏs ᴡɪᴛʜ ᴛʜᴜᴍʙɴᴀɪʟs.\n"
    "ʙᴏᴛ ᴡɪʟʟ ʀᴇᴍᴀɪɴ ᴀᴄᴛɪᴠᴇ ᴇᴠᴇɴ ɪғ ᴀʙᴜsᴇᴅ. ✅\n\n"
    "ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ, ʏᴏᴜ ᴍᴜsᴛ ʙᴇ ᴀ sᴜʙsᴄʀɪʙᴇʀ ᴏғ @ғᴛᴍʙᴏᴛᴢx.\n"
    "ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ʀᴇᴍᴏᴠᴇ ʟɪᴍɪᴛs, ʙᴜʏ ᴀ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ɴᴏᴡ ❤️\n\n"
    "────────────────────────\n"
    "✨ **ᴄʀᴇᴀᴛᴇᴅ ᴡɪᴛʜ ʟᴏᴠᴇ ʙʏ**: **[ғᴛᴍ ᴅᴇᴠᴇʟᴏᴘᴇʀᴢ](t.me/ftmdeveloperz)**",
        reply_markup=buttons                
    )

@Client.on_callback_query(filters.regex("start"))
async def start_hendler(client, callback_query):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("❓ Hᴇʟᴘ", callback_data="help"), InlineKeyboardButton("ℹ️ Aʙᴏᴜᴛ", callback_data="about")],
        [InlineKeyboardButton("📢 Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ", url="https://t.me/ftmbotzx")]
    ])
    
    await callback_query.message.edit_text(
    "ʜᴇʏ ʙʀᴏ! ɪ'ᴍ ғᴛᴍ ᴛᴜʙᴇғᴇᴛᴄʜ ʙᴏᴛ 🎬\n\n"
    "ɪ ᴄᴀɴ ᴅᴏᴡɴʟᴏᴀᴅ ʏᴏᴜᴛᴜʙᴇ ᴠɪᴅᴇᴏs ᴡɪᴛʜ ᴛʜᴜᴍʙɴᴀɪʟs.\n"
    "ʙᴏᴛ ᴡɪʟʟ ʀᴇᴍᴀɪɴ ᴀᴄᴛɪᴠᴇ ᴇᴠᴇɴ ɪғ ᴀʙᴜsᴇᴅ. ✅\n\n"
    "ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ, ʏᴏᴜ ᴍᴜsᴛ ʙᴇ ᴀ sᴜʙsᴄʀɪʙᴇʀ ᴏғ @ғᴛᴍʙᴏᴛᴢx.\n"
    "ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ʀᴇᴍᴏᴠᴇ ʟɪᴍɪᴛs, ʙᴜʏ ᴀ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ɴᴏᴡ ❤️\n\n"
    "────────────────────────\n"
    "✨ **ᴄʀᴇᴀᴛᴇᴅ ᴡɪᴛʜ ʟᴏᴠᴇ ʙʏ**: **[ғᴛᴍ ᴅᴇᴠᴇʟᴏᴘᴇʀᴢ](t.me/ftmdeveloperz)**",
        reply_markup=buttons                
    )



@Client.on_callback_query(filters.regex("help"))
async def help(client, callback_query):
    buttons = InlineKeyboardMarkup([
         [InlineKeyboardButton("⬅️ Bᴀᴄᴋ", callback_data="start"), InlineKeyboardButton("ℹ️ Aʙᴏᴜᴛ", callback_data="about")]
     
    ])
    
    await callback_query.message.edit_text(
    "🆘 **ʜᴏᴡ ᴛᴏ ᴜsᴇ ғᴛᴍ ᴛᴜʙᴇғᴇᴛᴄʜ**\n\n"
    "🎥 ᴊᴜsᴛ sᴇɴᴅ ᴀɴʏ ʏᴏᴜᴛᴜʙᴇ ʟɪɴᴋ (ᴠɪᴅᴇᴏ/ᴀᴜᴅɪᴏ)\n"
    "🧾 ᴛʜᴇ ʙᴏᴛ ᴡɪʟʟ ғᴇᴛᴄʜ ᴀʟʟ ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀᴍᴀᴛs\n"
    "⬇️ ᴄʜᴏᴏsᴇ ᴛʜᴇ ғᴏʀᴍᴀᴛ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ\n"
    "📦 ᴛʜᴇ ʙᴏᴛ ᴡɪʟʟ ᴘʀᴏᴄᴇss ᴀɴᴅ sᴇɴᴅ ᴛʜᴇ ғɪʟᴇ\n\n"
    "⚙️ **ᴄᴏᴍᴍᴀɴᴅs:**\n"
    "/start - ʀᴇsᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ\n"
    "/help - sʜᴏᴡ ᴛʜɪs ʜᴇʟᴘ ᴍᴇssᴀɢᴇ\n"
    "/myplan - ᴄʜᴇᴄᴋ ʏᴏᴜʀ sᴜʙsᴄʀɪᴘᴛɪᴏɴ ᴅᴇᴛᴀɪʟs\n"
     "🌟 **ᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ sᴜᴘᴘᴏʀᴛ**\n\n"
         "**🖼️ ᴛʜᴜᴍʙɴᴀɪʟ ꜰᴇᴀᴛᴜʀᴇs:**\n"
           "➤ ᴀᴅᴅ ᴀ ᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ ᴜsɪɴɢ `/add_thumbnail`\n"
           "➤ ʀᴇᴍᴏᴠᴇ ᴛʜᴜᴍʙɴᴀɪʟ ᴜsɪɴɢ `/remove_thumbnail`\n"
           "➤ ᴠɪᴇᴡ ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ ᴛʜᴜᴍʙɴᴀɪʟ ᴜsɪɴɢ `/show_thumbnail`\n"
           "➤ ɪꜰ ɴᴏ ᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ ɪs ᴀᴅᴅᴇᴅ, ᴛʜᴇ ʙᴏᴛ ᴡɪʟʟ **ᴀᴜᴛᴏ-ꜰᴇᴛᴄʜ ᴛʜᴇ ʏᴏᴜᴛᴜʙᴇ ᴛʜᴜᴍʙɴᴀɪʟ**.\n"
     "❗ᴅᴏ ɴᴏᴛ sᴇɴᴅ ᴍᴜʟᴛɪᴘʟᴇ ʟɪɴᴋs ᴀᴛ ᴏɴᴄᴇ.\n"
    "👑 ᴜᴘɢʀᴀᴅᴇ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ ғᴏʀ ᴜɴʟɪᴍɪᴛᴇᴅ ᴅᴏᴡɴʟᴏᴀᴅs\n"
    "🧾 sᴇɴᴅ ᴘᴀʏᴍᴇɴᴛ ᴘʀᴏᴏғ ᴛᴏ: @ғᴛᴍᴅᴇᴠᴇʟᴏᴘᴇʀᴢ\n\n"
    "────────────────────────\n"
    "✨ **ᴄʀᴇᴀᴛᴇᴅ ᴡɪᴛʜ ʟᴏᴠᴇ ʙʏ**: **[ғᴛᴍ ᴅᴇᴠᴇʟᴏᴘᴇʀᴢ](https://t.me/ftmdeveloperz)**",
        reply_markup=buttons
    )
    


@Client.on_callback_query(filters.regex("about"))
async def about(client, callback_query):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Bᴀᴄᴋ", callback_data="start"), InlineKeyboardButton("❓ Hᴇʟᴘ", callback_data="help")]
    ])
    
    await callback_query.message.edit_text(
    "ℹ️ **ᴀʙᴏᴜᴛ ғᴛᴍ ᴛᴜʙᴇғᴇᴛᴄʜ**\n\n"
    "🎬 ᴛʜɪs ɪs ᴀ ᴘᴏᴡᴇʀғᴜʟ ʏᴏᴜᴛᴜʙᴇ ᴅᴏᴡɴʟᴏᴀᴅ ʙᴏᴛ ᴍᴀᴅᴇ ғᴏʀ ᴛᴇʟᴇɢʀᴀᴍ.\n"
    "⚡ ᴊᴜsᴛ sᴇɴᴅ ᴀ ʏᴏᴜᴛᴜʙᴇ ʟɪɴᴋ ᴀɴᴅ ɢᴇᴛ ʜɪɢʜ-Qᴜᴀʟɪᴛʏ ᴠɪᴅᴇᴏ/ᴀᴜᴅɪᴏ.\n"
    "✅ sᴜᴘᴘᴏʀᴛs ᴍᴜʟᴛɪᴘʟᴇ ғᴏʀᴍᴀᴛs (ᴀᴜᴅɪᴏ/ᴠɪᴅᴇᴏ/ᴅᴏᴄ).\n"
    "🔒 ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs ɢᴇᴛ ᴜɴʟɪᴍɪᴛᴇᴅ ᴅᴀɪʟʏ ᴅᴏᴡɴʟᴏᴀᴅs, ᴇxᴛʀᴀ sᴘᴇᴇᴅ & ᴇxᴄʟᴜsɪᴠᴇ ғᴇᴀᴛᴜʀᴇs.\n"
    "🧠 ʙᴏᴛ ᴅᴇᴠᴇʟᴏᴘᴇᴅ ᴡɪᴛʜ sᴍᴀʀᴛ ǫᴜᴇᴜᴇ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ, sᴛʀᴇss ʜᴀɴᴅʟɪɴɢ, ᴀɴᴅ ᴀᴅᴠᴀɴᴄᴇᴅ ᴜsᴇʀ ᴄᴏɴᴛʀᴏʟ.\n\n"
    "👤 ᴏᴡɴᴇʀ:**[ғᴛᴍ ᴅᴇᴠᴇʟᴏᴘᴇʀᴢ](https://t.me/ftmdeveloperz)**\n"
    "👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ: **[ғᴛᴍ ᴅᴇᴠᴇʟᴏᴘᴇʀᴢ](https://t.me/ftmdeveloperz)**\n"
    "📡 ᴏғғɪᴄɪᴀʟ ᴄʜᴀɴɴᴇʟ:**[ғᴛᴍʙᴏᴛᴢx](https://t.me/ftmbotzx)**\n\n"
    "🔧 **ʜᴏᴡ ᴛᴏ ᴜsᴇ:**\n"
    "➤ sᴇɴᴅ ᴀɴʏ ʏᴏᴜᴛᴜʙᴇ ʟɪɴᴋ (ᴠɪᴅᴇᴏ/ᴍᴜsɪᴄ)\n"
    "➤ ᴄʜᴏᴏsᴇ ᴏᴜᴛᴘᴜᴛ ғᴏʀᴍᴀᴛ (ᴀᴜᴅɪᴏ/ᴠɪᴅᴇᴏ/ᴅᴏᴄ)\n"
    "➤ ᴡᴀɪᴛ ғᴏʀ ᴀ ᴍᴏᴍᴇɴᴛ ᴀɴᴅ ᴛᴀᴘ ᴏɴ ᴛʜᴇ ғɪʟᴇ sᴇɴᴛ ʙʏ ʙᴏᴛ\n\n"
    "────────────────────────\n"
    "✨ **ᴄʀᴇᴀᴛᴇᴅ ᴡɪᴛʜ ʟᴏᴠᴇ ʙʏ**: **[ғᴛᴍ ᴅᴇᴠᴇʟᴏᴘᴇʀᴢ](https://t.me/ftmdeveloperz)**",
        reply_markup=buttons,
        disable_web_page_preview=True
    )


@Client.on_message(filters.command('users') & filters.private)
async def total_users(client, message):
    if message.from_user.id not in ADMINS:
        return await message.reply_text("🚫 **You are not authorized to use this command!**")

    response = await message.reply("🔍 Fetching total users...")

    total_users = await db.total_users_count()

    await response.edit_text(
        f"👑 **Admin Panel**\n\n"
        f"🌍 **Total Users in Database:** `{total_users}`\n\n"
        "**🚀 Thanks for managing this bot!**"
    )
    


@Client.on_message(filters.command("stats") & filters.private)
async def stats(client, message):
    if message.from_user.id not in ADMINS:
        return await message.reply_text("🚫 **You are not authorized to use this command!**")
  
    response = await message.reply("**🔍 Fetching Bot Statistics**")

    total_users = await db.total_users_count()
    total_downloads = await db.get_total_downloads()
    
    await response.edit_text(
        f"📊 **Bot Statistics**\n\n"
        f"👥 **Total Users:** {total_users}\n"
        f"⬇️ **Total Downloads:** {total_downloads}\n\n"
        "These stats show the total number of users and downloads recorded in the system."
    )


@Client.on_message(filters.command("mytasks"))
async def my_tasks(client, message):
    user_id = message.from_user.id
    allowed, tasks_used, user_type, total_tasks = await db.get_task_limit(user_id)

    if user_type == "Premium":
        remaining_tasks = "Unlimited 🚀"
        task_limit_text = "∞ (No Limit) 🔥"
    else:
        remaining_tasks = max(0, DAILY_LIMITS - tasks_used)
        task_limit_text = f"{DAILY_LIMITS}"

    text = (
        f"👤 **User Type:** `{user_type}`\n"
        f"📅 **Today's Tasks Used:** `{tasks_used}/{task_limit_text}`\n"
        f"🔹 **Remaining Today:** `{remaining_tasks}`\n"
        f"📊 **Total Tasks Completed:** `{total_tasks}`\n"
    )

    await message.reply_text(text)
    



@Client.on_message(filters.command("checkdc") & filters.private)
async def check_dc(client, message):
    try:
        me = await client.get_me()
        dc_id = me.dc_id
        await message.reply_text(f"🌍 **Your Data Center ID:** `{dc_id}`")
    except Exception as e:
        await message.reply_text(f"❌ Error while checking DC ID:\n`{e}`")


@Client.on_message(filters.command("taskinfo"))
async def show_active_tasks(client, message):
    if message.from_user.id not in ADMINS:
        await message.reply("❌ You are not authorized to use this command.")
        return

    total_tasks = len(active_tasks)
    await message.reply(f"**🧾 Active Tasks (Total: {total_tasks})**")
 





import os
import sys

@Client.on_message(filters.command("restart") & filters.user(ADMINS))
async def restart_cmd(_, message):
    await message.reply("♻️ Restarting bot...")


    os.execv(sys.executable, ["python"] + sys.argv)  # restarts the current process
