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
        [InlineKeyboardButton("❓ Help", callback_data="help"), InlineKeyboardButton("ℹ️ About", callback_data="about")],
        [InlineKeyboardButton("📢 Updates Channel", url="https://t.me/ftmbotzx")]
    ])
    if not await db.is_user_exist(message.from_u09ser.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(
            LOG_CHANNEL, 
            f"**#NewUser 🔻**\n**ID -> `{message.from_user.id}`**\n**Name -> {message.from_user.mention}**"
        )
    await message.reply_text(
        "🎬✨ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ **Fᴛᴍ TᴜʙᴇFᴇᴛᴄʜ** ✨🎬\n\n"
        "🚀 ʏᴏᴜʀ ᴜʟᴛɪᴍᴀᴛᴇ ᴅᴇsᴛɪɴᴀᴛɪᴏɴ ꜰᴏʀ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ʏᴏᴜᴛᴜʙᴇ 🎥 ᴠɪᴅᴇᴏs, sʜᴏʀᴛs & ᴀᴜᴅɪᴏs ɪɴ sᴇᴄᴏɴᴅs!\n"
        "💫 ɴᴏ ᴄᴏᴍᴘʟɪᴄᴀᴛɪᴏɴs — ᴊᴜsᴛ sᴇɴᴅ ᴀɴʏ ʏᴏᴜᴛᴜʙᴇ ʟɪɴᴋ ᴀɴᴅ ᴄʜᴏᴏsᴇ ᴍᴘ3/ᴍᴘ4.\n\n"
        "🔸 **ꜰᴇᴀᴛᴜʀᴇs** 🔸\n"
        "✅ **Supports Videos, Shorts, MP3, MP4 in HD Quality**\n"
        "🎵 **Download Audio (MP3) & Video (MP4)**\n"
        "🔹 **No Watermark, Full HD Quality**\n"
        "🌟 **Custom Thumbnails for Each Video**\n\n"
        "✨ **Cʀᴇᴀᴛᴇᴅ ᴡɪᴛʜ ʟᴏᴠᴇ ʙʏ**: **[Fᴛᴍ Dᴇᴠᴇʟᴏᴘᴇʀᴢ](t.me/ftmdeveloperz)**",
        reply_markup=buttons                
    )

@Client.on_callback_query(filters.regex("start"))
async def start_hendler(client, callback_query):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("❓ Help", callback_data="help"), InlineKeyboardButton("ℹ️ About", callback_data="about")],
        [InlineKeyboardButton("📢 Updates Channel", url="https://t.me/ftmbotzx")]
    ])
    
    await callback_query.message.edit_text(
    "🎬✨ **Welcome to the Ultimate YouTube Downloader!** ✨🎬\n\n"
    "🚀 **Download YouTube Videos, Shorts & Music Instantly!** 🎶\n"
    "💫 Just send any YouTube link & get **high-speed downloads in seconds!**\n\n"
    "⚡ **Fast & Secure Downloads**\n"
    "✅ **Supports Videos, Shorts, MP3, MP4 in HD Quality**\n"
    "🎵 **Download Audio (MP3) & Video (MP4)**\n"
    "ꜱᴛᴀʀᴛ ʙʏ ᴅʀᴏᴘᴘɪɴɢ ᴀ ʟɪɴᴋ ʙᴇʟᴏᴡ! \n\n"
    "💖 **Enjoy Hassle-Free Downloads!** 💖"
    " ────────────────────────\n"
    "✨ **Cʀᴇᴀᴛᴇᴅ ᴡɪᴛʜ ʟᴏᴠᴇ ʙʏ**: **[Fᴛᴍ Dᴇᴠᴇʟᴏᴘᴇʀᴢ**](t.me/ftmdeveloperz)",
    reply_markup=buttons                
    )0


@Client.on_callback_query(filters.regex("help"))
async def help(client, callback_query):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Back", callback_data="start"), InlineKeyboardButton("ℹ️ About", callback_data="about")]
    ])
    
    await callback_query.message.edit_text(
        "**❓ Help Guide - YouTube Downloader**\n\n"
        "📌 Just send any **YouTube video link** here.\n"
        "🔹 The bot will instantly fetch & send your download link.\n"
        "🎥 **Supports MP4 (Video) & MP3 (Audio) Downloads**\n"
        "🎵 **High-Quality Audio & Video** (upto 320kbps & 4K)\n"
        "🌟 **Custom Thumbnail Support**\n\n"
        "**🖼️ Thumbnail Features:**\n"
        "➤ Add a custom thumbnail using `/add_thumbnail`\n"
        "➤ Remove thumbnail using `/remove_thumbnail`\n"
        "➤ View your current thumbnail using `/show_thumbnail`\n"
        "➤ If no custom thumbnail is added, the bot will **auto-fetch the YouTube thumbnail**.\n\n"
        "**🎬 How to Download?**\n"
        "1️⃣ Send a YouTube link.\n"
        "2️⃣ Choose between **MP3 (Audio) or MP4 (Video).**\n"
        "3️⃣ Get your download instantly!\n\n"
        "🚀 **Fast, Secure & Unlimited Downloads!** 💖",
        reply_markup=buttons
    )
    


@Client.on_callback_query(filters.regex("about"))
async def about(client, callback_query):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Back", callback_data="start"), InlineKeyboardButton("❓ Help", callback_data="help")]
    ])
    
    await callback_query.message.edit_text(
        "**ℹ️ About This Bot**\n\n"
        "🎬 **YouTube Video & Audio Downloader**\n"
        "🚀 **Fastest YouTube downloader with custom thumbnail support!**\n"
        "🎥 **Supports:** MP4 (Video) & MP3 (Audio)\n"
        "🔹 **High-Quality Downloads** (upto 320kbps & 1080p)\n"
        "🖼️ **Custom Thumbnail Support**\n\n"
        "**⚡ Features:**\n"
        "➤ **Blazing Fast & Secure**\n"
        "➤ **Unlimited Downloads**\n"
        "➤ **Easy-to-use Interface**\n\n"
        "💎 **Developed By: [Fᴛᴍ Dᴇᴠᴇʟᴏᴘᴇʀᴢ](https://t.me/ftmdeveloperz)**\n"
        "💖 **Enjoy & Share!**",
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

@Client.on_message(filters.command("restart1") & filters.user(ADMINS))
async def restart_cmd(_, message):
    await message.reply("♻️ Restarting bot...")


    os.execv(sys.executable, ["python"] + sys.argv)  # restarts the current process
