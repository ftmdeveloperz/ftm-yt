import os
import logging
import yt_dlp
import aiohttp
import aiofiles
import asyncio
import time
import math
import random
import string
import psutil
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from threading import Thread
from database.db import db
from PIL import Image
import uuid
from info import DUMP_CHANNEL, LOG_CHANNEL
import ffmpeg
from math import ceil

active_tasks = {}

import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
logger.info("Uploading started")


def format_size(size_in_bytes):
    """✅ File Size को KB, MB, या GB में Convert करता है"""
    if size_in_bytes < 1024:
        return f"{size_in_bytes} B"
    elif size_in_bytes < 1024**2:
        return f"{round(size_in_bytes / 1024, 1)} KB"
    elif size_in_bytes < 1024**3:
        return f"{round(size_in_bytes / 1024**2, 1)} MB"
    else:
        return f"{round(size_in_bytes / 1024**3, 2)} GB"
        
def humanbytes(size):
    if not size:
        return "N/A"
    power = 2**10
    n = 0
    units = ["", "K", "M", "G", "T"]
    while size > power and n < len(units) - 1:
        size /= power
        n += 1
    return f"{round(size, 2)}{units[n]}B"

def TimeFormatter(milliseconds):
    seconds = milliseconds // 1000
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start

    if current == total or round(diff % 5.00) == 0:
        percentage = (current / total) * 100
        speed = current / diff if diff > 0 else 0
        estimated_total_time = TimeFormatter(milliseconds=(total - current) / speed * 1000) if speed > 0 else "∞"

        # CPU & RAM Usage
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent

        # Progress Bar
        progress_bar = "■" + "■" * math.floor(percentage / 5) + "□" * (20 - math.floor(percentage / 5))

        text = (
            f"**╭───────Uᴘʟᴏᴀᴅɪɴɢ───────〄**\n"
            f"**│**\n"
            f"**├📁 Sɪᴢᴇ : {humanbytes(current)} ✗ {humanbytes(total)}**\n"
            f"**│**\n"
            f"**├📦 Pʀᴏɢʀᴇꜱꜱ : {round(percentage, 2)}%**\n"
            f"**│**\n"
            f"**├🚀 Sᴘᴇᴇᴅ : {humanbytes(speed)}/s**\n"
            f"**│**\n"
            f"**├⏱️ Eᴛᴀ : {estimated_total_time}**\n"
            f"**│**\n"
            f"**├🏮 Cᴘᴜ : {cpu_usage}%  |  Rᴀᴍ : {ram_usage}%**\n"
            f"**│**\n"
            f"**╰─[{progress_bar}]**"
        )

        try:
            await message.edit(text=text)
        except:
            pass



async def progress_bar(current, total, status_message, start_time, last_update_time):
    """Display a progress bar for downloads/uploads."""
    try:
        if total == 0:
            return  # Prevent division by zero

        elapsed_time = time.time() - start_time
        percentage = (current / total) * 100
        speed = current / elapsed_time / 1024 / 1024  # Speed in MB/s
        uploaded = current / 1024 / 1024
        total_size = total / 1024 / 1024
        remaining_size = total_size - uploaded
        eta = (remaining_size / speed) if speed > 0 else 0

        eta_min = int(eta // 60)
        eta_sec = int(eta % 60)

        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent

        # Throttle updates
        if time.time() - last_update_time[0] < 2:
            return
        last_update_time[0] = time.time()

        progress_blocks = int(percentage // 5)
        progress_bar_str = "■" * progress_blocks + "□" * (20 - progress_blocks)

        text = (
            "**╭───────Dᴏᴡɴʟᴏᴀᴅɪɴɢ───────〄**\n"
            "**│**\n"
            f"**├📁 Sɪᴢᴇ : {humanbytes(current)} ✗ {humanbytes(total)}**\n"
            "**│**\n"
            f"**├📦 Pʀᴏɢʀᴇꜱꜱ : {percentage:.2f}%**\n"
            "**│**\n"
            f"**├🚀 Sᴘᴇᴇᴅ : {speed:.2f} 𝙼𝙱/s**\n"
            "**│**\n"
            f"**├⏱️ Eᴛᴀ : {eta_min}𝚖𝚒𝚗, {eta_sec}𝚜𝚎𝚌**\n"
            "**│**\n"
            f"**├🏮 Cᴘᴜ : {cpu_usage}%  |  Rᴀᴍ : {ram_usage}%**\n"
            "**│**\n"
            f"**╰─[{progress_bar_str}]**"
        )

        await status_message.edit(text)

        if percentage >= 100:
            await status_message.edit("✅ **Fɪʟᴇ Dᴏᴡɴʟᴏᴀᴅ Cᴏᴍᴘʟᴇᴛᴇ!**\n**🎵 Aᴜᴅɪᴏ Dᴏᴡɴʟᴏᴀᴅɪɴɢ...**")

    except Exception as e:
        print(f"Error updating progress: {e}")


async def update_progress(message, queue):
    """Updates progress bar while downloading."""
    last_update_time = [0]  # Use a list to store the last update time as a mutable object
    start_time = time.time()

    while True:
        data = await queue.get()
        if data is None:
            break

        current, total, status = data
        await progress_bar(current, total, message, start_time, last_update_time)


def yt_progress_hook(d, queue, client):
    """Reports progress of yt-dlp to async queue in a thread-safe way."""
    if d['status'] == 'downloading':
        current = d['downloaded_bytes']
        total = d.get('total_bytes', 1)
        asyncio.run_coroutine_threadsafe(queue.put((current, total, "⬇ **Downloading...**")), client.loop)
    elif d['status'] == 'finished':
        asyncio.run_coroutine_threadsafe(queue.put((1, 1, "✅ **Download Complete! Uploading...**")), client.loop)
        asyncio.run_coroutine_threadsafe(queue.put(None), client.loop)  # Stop progress loop




def generate_thumbnail_path():
    timestamp = int(time.time())
    unique_id = uuid.uuid4().hex
    return os.path.join("downloads", f"thumb_{unique_id}_{timestamp}.jpg")

async def download_and_resize_thumbnail(url):
    save_path = generate_thumbnail_path()

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    async with aiofiles.open(save_path, 'wb') as f:
                        await f.write(await resp.read())
                else:
                    return None

        def resize():
            img = Image.open(save_path).convert("RGB")
            img.save(save_path, "JPEG", quality=85)

        await asyncio.to_thread(resize)
        return save_path

    except Exception as e:
        logging.exception("Thumbnail download failed: %s", e)
        return None
        
    


MAX_TG_FILE_SIZE = 2097152000  # 2GB (Telegram limit)



async def run_ffmpeg_async(cmd):
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        raise Exception(f"FFmpeg failed: {stderr.decode()}")
    return stdout, stderr

async def split_video(output_filename, max_size=MAX_TG_FILE_SIZE):
    file_size = os.path.getsize(output_filename)
    if file_size <= max_size:
        return [output_filename]  # No need to split

    duration = float(ffmpeg.probe(output_filename)["format"]["duration"])
    duration = int(duration)
    parts = ceil(file_size / max_size)
    split_duration = duration // parts
    base_name = os.path.splitext(output_filename)[0]

    split_files = []

    for i in range(parts):
        part_file = f"{base_name}_part{i+1}.mp4"
        start_time = i * split_duration

        cmd = [
            "ffmpeg",
            "-y",
            "-i", output_filename,
            "-ss", str(start_time),
            "-t", str(split_duration),
            "-c", "copy",
            part_file
        ]

        await run_ffmpeg_async(cmd)
        split_files.append(part_file)

    return split_files


async def upload_audio(client, chat_id, output_filename, caption, duration, status_msg):
    if output_filename and os.path.exists(output_filename):
        await status_msg.edit_text("📤 **Uploading audio...**")
        start_time = time.time()

        async def upload_progress(sent, total):
            # Track the upload progress
            await progress_for_pyrogram(sent, total, "📤 **Uploading...**", status_msg, start_time)

        try:
            # Open the audio file and send it to the chat
            with open(output_filename, 'rb') as audio_file:
                await client.send_audio(
                    chat_id,
                    audio_file,
                    progress=upload_progress,
                    caption=f"**🎶 Audio Title:** {caption}\n**🎧 Duration:** {duration} seconds"                    
                )
                
                # Update the status message after successful upload
                await status_msg.edit_text("✅ **Audio Uploaded Successfully!**")
                await db.increment_task(chat_id)
                await db.increment_download_count()
                await status_msg.delete()
            active_tasks.pop(chat_id, None)
        except Exception as e:
            # In case of an error, update the status message
            await status_msg.edit_text(f"❌ **Upload Failed!** Error: {e}")
            active_tasks.pop(chat_id, None)
        
        finally:
            # Clean up the temporary files after upload
            if os.path.exists(output_filename):
                os.remove(output_filename)
            active_tasks.pop(chat_id, None)
    else:
        # If the output filename is not valid
        await status_msg.edit_text("❌ **Audio file not found!**")
        active_tasks.pop(chat_id, None)




async def upload_video(client, chat_id, output_filename, caption, duration, width, height, thumbnail_path, status_msg, youtube_link):
    if output_filename and os.path.exists(output_filename):
        await status_msg.edit_text("📤 **Uploading video...**")
        start_time = time.time()

        async def upload_progress(sent, total):
            await progress_for_pyrogram(sent, total, "📤 **Uploading...**", status_msg, start_time)

        try:
            split_files = await split_video(output_filename)
            total_parts = len(split_files)

            user = await client.get_users(chat_id)
            mention_user = f"[{user.first_name}](tg://user?id={user.id})"

            for idx, part_file in enumerate(split_files, start=1):
                part_caption = f"{caption}\n**Part {idx}/{total_parts}**" if total_parts > 1 else caption
                
                with open(part_file, "rb") as video_file:
                    sent_message = await client.send_video(
                        chat_id=chat_id,
                        video=video_file,
                        progress=upload_progress,
                        caption=part_caption,
                        duration=duration // total_parts if total_parts > 1 else duration,
                        supports_streaming=True,
                        height=height,
                        width=width,
                        disable_notification=True,
                        thumb=thumbnail_path if thumbnail_path else None,
                        file_name=os.path.basename(part_file)
                    )

                formatted_caption = (
                    f"**{part_caption}**\n\n"
                    f"✅ **Dᴏᴡɴʟᴏᴀᴅᴇᴅ Bʏ: {mention_user}**\n"
                    f"📌 **Sᴏᴜʀᴄᴇ URL: [Click Here]({youtube_link})**"
                )
                await client.send_video(
                    chat_id=DUMP_CHANNEL,
                    video=sent_message.video.file_id,
                    caption=formatted_caption,
                    duration=duration // total_parts if total_parts > 1 else duration,
                    supports_streaming=True,
                    height=height,
                    width=width,
                    disable_notification=True,
                    thumb=thumbnail_path if thumbnail_path else None,
                    file_name=os.path.basename(part_file)
                )

                os.remove(part_file)

            await status_msg.edit_text("✅ **Upload Successful!**")
            await db.increment_task(chat_id)
            await db.increment_download_count()
            await status_msg.delete()

        except Exception as e:
            user = await client.get_users(chat_id)
            error_report = (
                f"❌ **Upload Failed!**\n\n"
                f"**User:** [{user.first_name}](tg://user?id={user.id}) (`{user.id}`)\n"
                f"**Filename:** `{output_filename}`\n"
                f"**Source:** [YouTube Link]({youtube_link})\n"
                f"**Error:** `{str(e)}`"
            )
            await client.send_message(LOG_CHANNEL, error_report)
            await status_msg.edit_text("❌ **Oops! Something went wrong during upload.**")

        finally:
            if os.path.exists(output_filename):
                os.remove(output_filename)
            if thumbnail_path and os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
            active_tasks.pop(chat_id, None)

    else:
        try:
            user = await client.get_users(chat_id)
            error_report = (
                f"❌ **Upload Failed - File Not Found!**\n\n"
                f"**User:** [{user.first_name}](tg://user?id={user.id}) (`{user.id}`)\n"
                f"**Expected File:** `{output_filename}`\n"
                f"**Source:** [YouTube Link]({youtube_link})"
            )
            await client.send_message(LOG_CHANNEL, error_report)
        except Exception as e:
            await client.send_message(LOG_CHANNEL, f"❌ Error while logging failed upload:\n`{str(e)}`")

        await status_msg.edit_text("❌ **Oops! Upload failed. Please try again later.**")
        active_tasks.pop(chat_id, None)
        




async def download_video(client, callback_query, chat_id, youtube_link, format_id):
    active_tasks[chat_id] = True  # Mark task as active
    status_msg = await client.send_message(chat_id, "⏳ **Starting Download...**")
    await callback_query.message.delete()
    
    queue = asyncio.Queue()
    output_filename = None
    caption = ""
    duration = 0
    width, height = 360, 360
    thumbnail_path = None
    youtube_thumbnail_url, thumbnails = None, []
    
    timestamp = time.strftime("%y%m%d")
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))

    def run_yt_dlp():
        nonlocal output_filename, caption, duration, width, height, youtube_thumbnail_url, thumbnails
        yt_dlp_options = {
            'format': f"{format_id}+bestaudio/best",
            'merge_output_format': 'mp4',
            'outtmpl': f"downloads/%(title)s_{timestamp}-{random_str}.%(ext)s",
            'progress_hooks': [lambda d: yt_progress_hook(d, queue, client)],
            'cookiefile': 'cookies.txt'
        }

        with yt_dlp.YoutubeDL(yt_dlp_options) as ydl:
            info = ydl.extract_info(youtube_link, download=True)
            caption = info.get('title', '')
            duration = info.get('duration', 0)
            width, height = info.get('width', 360), info.get('height', 360)
            youtube_thumbnail_url = info.get('thumbnail', '')
            thumbnails = info.get('thumbnails', [])
            
            if 'requested_downloads' in info and info['requested_downloads']:
                output_filename = info['requested_downloads'][-1]['filepath']
            else:
                output_filename = info.get('filepath', None)

            # Notify download finished
            asyncio.run_coroutine_threadsafe(queue.put({"status": "finished"}), client.loop)

    # Run yt-dlp and progress in parallel
    download_task = asyncio.create_task(asyncio.to_thread(run_yt_dlp))
    progress_task = asyncio.create_task(update_progress(status_msg, queue))

    await download_task
    await progress_task

    if output_filename and os.path.exists(output_filename):
        await status_msg.edit_text("📤 **Preparing for upload...**")
        thumbnail_file_id = await db.get_user_thumbnail(chat_id)
        if thumbnail_file_id:
            try:
                thumb_message = await client.download_media(thumbnail_file_id)
                thumbnail_path = thumb_message
            except Exception as e:
                print(f"Thumbnail download error: {e}")

        if not thumbnail_path and thumbnails:
            high_quality_thumb = max(thumbnails, key=lambda x: x.get('height', 0))['url']
            if high_quality_thumb:
                thumbnail_path = await download_and_resize_thumbnail(high_quality_thumb)

        await upload_video(
            client, chat_id, output_filename, caption,
            duration, width, height, thumbnail_path,
            status_msg, youtube_link
        )
    else:
        await status_msg.edit_text("❌ **Download Failed!**")
    
    active_tasks.pop(chat_id, None)
    


async def download_audio(client, callback_query, chat_id, youtube_link):
    #if active_tasks.get(chat_id):
      #  await client.send_message(chat_id, "⏳ **Your previous task is still running. Please wait!**")
        #return

    active_tasks[chat_id] = True  # Mark task as active
    status_msg = await client.send_message(chat_id, "⏳ **Starting Audio Download...**")
    await callback_query.message.delete()
    
    queue = asyncio.Queue()
    output_filename = None
    caption = ""
    duration = 0

    timestamp = time.strftime("%y%m%d")
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))

    def run_yt_dlp():
        nonlocal output_filename, caption, duration
        yt_dlp_options = {
            'format': 'bestaudio/best',  # Best audio format
            'merge_output_format': 'mp3',  # Convert to mp3
            'outtmpl': f"downloads/%(title)s_{timestamp}-{random_str}.%(ext)s",
            'progress_hooks': [lambda d: yt_progress_hook(d, queue, client)],
            'cookiefile': 'cookies.txt'
        }

        with yt_dlp.YoutubeDL(yt_dlp_options) as ydl:
            info = ydl.extract_info(youtube_link, download=True)
            caption = info.get('title', '')
            duration = info.get('duration', 0)
            
            if 'requested_downloads' in info and info['requested_downloads']:
                output_filename = info['requested_downloads'][-1]['filepath']
            else:
                output_filename = info.get('filepath', None)

    thread = Thread(target=run_yt_dlp)
    thread.start()
    
    await update_progress(status_msg, queue)
    thread.join()

    if output_filename and os.path.exists(output_filename):
        await status_msg.edit_text("📤 **Preparing for upload...**")
        
        # Upload audio without thumbnail (None for thumbnail)
        await upload_audio(client, chat_id, output_filename, caption, duration, status_msg)
    else:
        await status_msg.edit_text("❌ **Download Failed!**")
        active_tasks.pop(chat_id, None)





@Client.on_message(filters.regex(r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+'))
async def process_youtube_link(client, message):
    chat_id = message.chat.id

    fetching_message = await message.reply_text("🔍 **Fetching available formats... Please wait a moment!**")
    
    if not await db.check_task_limit(chat_id):
        await message.reply_text(
            "❌ **You have reached your daily task limit! Try again tomorrow.**\n\n"
            "**To check your remaining tasks and reset time, use the /mytasks command.**"
        )
        await fetching_message.delete()
        return
        
    if active_tasks.get(chat_id):
        await message.reply_text("⏳ **Your previous task is still running. Please wait!**")
        await fetching_message.delete()
        return

    youtube_link = message.text
    keyboard_buttons = []

    try:
        loop = asyncio.get_event_loop()
        info_dict = await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL({'quiet': True, 'cookiefile': 'cookies.txt'}).extract_info(youtube_link, download=False))
        formats = info_dict.get('formats', [])
        title = info_dict.get('title', 'No title available')
        thumbnail_url = info_dict.get('thumbnail', '')

        quality_options = {}
        for f in formats:
            height = f.get('height')
            format_id = f.get('format_id')
            filesize = f.get('filesize') or f.get('filesize_approx')
            if height and format_id and height >= 144:
                if filesize:
                    quality_options[str(height)] = (format_id, format_size(filesize))

       
        sorted_qualities = sorted(quality_options.keys(), key=lambda x: int(x), reverse=True)
        for quality in sorted_qualities:
            format_id, size_text = quality_options[quality]
            keyboard_buttons.append([InlineKeyboardButton(f"🎬 {quality}p - {size_text}", callback_data=f"download|{format_id}")])

        keyboard_buttons.append([InlineKeyboardButton(f"🎶 Best Audio", callback_data=f"download_audio")])
        
    except Exception as e:
        logging.exception("Error fetching available formats: %s", e)
        await message.reply_text(
            "⚠️ Oᴏᴘs! Sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ ᴡʜɪʟᴇ ғᴇᴛᴄʜɪɴɢ ᴛʜᴇ ғᴏʀᴍᴀᴛs. Pʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.\ɴ\ɴ"
            "Iғ ᴛʜᴇ ɪssᴜᴇ ᴘᴇʀsɪsᴛs, ᴘʟᴇᴀsᴇ ᴀsᴋ ғᴏʀ ʜᴇʟᴘ ɪɴ ᴏᴜʀ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ.\ɴ\ɴ"
            "💬 Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ: [SUPPORT](https://t.me/ftmbotzx_support)"
        )
        await fetching_message.delete()
        return
    
    if keyboard_buttons:
        if thumbnail_url:
            sent_msg = await message.reply_photo(
                thumbnail_url,
                caption=f"**🎥 Title:** {title}\n\n**✨ Choose Video Quality to Download:**",
                reply_markup=InlineKeyboardMarkup(keyboard_buttons),
                reply_to_message_id=message.id
            )
            await fetching_message.delete()
    else:
        await message.reply_text("❌ **Sᴏʀʀʏ! Nᴏ ᴀᴠᴀɪʟᴀʙʟᴇ ᴠɪᴅᴇᴏ ғᴏʀᴍᴀᴛs ғᴏᴜɴᴅ ғᴏʀ ᴛʜɪs ʟɪɴᴋ. ʀᴇᴘᴏʀᴛ ᴛʜɪs ɪssᴜᴇ ᴛᴏ ᴏᴜʀ Dᴇᴠᴇʟᴏᴘᴇʀᴢ**\n**💬 Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ: [SUPPORT](https://t.me/ftmbotzx_support)**")
        

@Client.on_callback_query(filters.regex(r'^download\|'))
async def handle_download_button(client, callback_query):
    format_id = callback_query.data.split('|')[1]
    youtube_link = callback_query.message.reply_to_message.text
    chat_id = callback_query.message.chat.id
    await download_video(client, callback_query, chat_id, youtube_link, format_id)


@Client.on_callback_query(filters.regex(r'^download_audio$'))
async def handle_audio_download_button(client, callback_query):
    youtube_link = callback_query.message.reply_to_message.text
    chat_id = callback_query.message.chat.id
    await download_audio(client, callback_query, chat_id, youtube_link)
