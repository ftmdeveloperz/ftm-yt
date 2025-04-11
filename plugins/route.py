from aiohttp import web
import datetime

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = f"""
🎬✨ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ꜰᴛᴍ ᴛᴜʙᴇꜰᴇᴛᴄʜ ✨🎬

🚀 ʏᴏᴜʀ ᴜʟᴛɪᴍᴀᴛᴇ ᴅᴇꜱᴛɪɴᴀᴛɪᴏɴ ꜰᴏʀ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ʏᴏᴜᴛᴜʙᴇ 🎥 ᴠɪᴅᴇᴏꜱ, ꜱʜᴏʀᴛꜱ & ᴀᴜᴅɪᴏꜱ ɪɴ ꜱᴇᴄᴏɴᴅꜱ!
💫 ɴᴏ ᴄᴏᴍᴘʟɪᴄᴀᴛɪᴏɴꜱ — ᴊᴜꜱᴛ ꜱᴇɴᴅ ᴀɴʏ ʏᴏᴜᴛᴜʙᴇ ʟɪɴᴋ ᴀɴᴅ ᴄʜᴏᴏꜱᴇ ᴍᴘ3/ᴍᴘ4 ꜰᴏʀᴍᴀᴛ.

🔸 ꜰᴇᴀᴛᴜʀᴇꜱ 🔸
✅ ꜱᴜᴘᴘᴏʀᴛꜱ ᴠɪᴅᴇᴏꜱ, ꜱʜᴏʀᴛꜱ, ᴍᴘ3, ᴍᴘ4 ɪɴ ʜᴅ ǫᴜᴀʟɪᴛʏ  
🎵 ᴅᴏᴡɴʟᴏᴀᴅ ᴀᴜᴅɪᴏ (ᴍᴘ3) & ᴠɪᴅᴇᴏ (ᴍᴘ4)  
🔹 ɴᴏ ᴡᴀᴛᴇʀᴍᴀʀᴋ, ꜰᴜʟʟ ʜᴅ ᴏᴜᴛᴘᴜᴛ  
🌟 ᴄᴜꜱᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟꜱ ꜰᴏʀ ᴇᴀᴄʜ ᴅᴏᴡɴʟᴏᴀᴅ  
⚡ ꜱᴜᴘᴇʀ ꜰᴀꜱᴛ, ᴀᴅ-ꜰʀᴇᴇ & ꜱɪᴍᴘʟᴇ ᴛᴏ ᴜꜱᴇ

────────────────────────  
✨ ᴄʀᴇᴀᴛᴇᴅ ᴡɪᴛʜ ʟᴏᴠᴇ ʙʏ: <a href="https://t.me/ftmdeveloperz">ꜰᴛᴍ ᴅᴇᴠᴇʟᴏᴘᴇʀᴢ</a>

<br><br>
✅ <b>Server Status:</b> Live  
📡 <b>Status:</b> Success  
🕒 <b>Time:</b> {now}
"""
    return web.Response(text=message, content_type="text/html")
