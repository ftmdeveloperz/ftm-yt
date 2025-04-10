import os
import asyncio
import time
import logging
from pytdbot import Client

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,  # Change this to DEBUG for more detailed logs
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("upload.log"), logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

# Configuration
API_ID = int(os.getenv("API_ID", "8012239"))
API_HASH = os.getenv("API_HASH", "171e6f1bf66ed8dcc5140fbe827b6b08")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8075909999:AAFxpyj49WZxZZnChpX5srczTxgxz5YmHQ8")
CHAT_ID = -1002284232975

FILE_PATH = "/home/ubuntu/YouTubeDL/downloads/ansh.mp4"  # Path to your file

# Initialize client
client = Client(
    token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    files_directory="BotDB",
    database_encryption_key="1234echobot$"
)

# Progress bar function
def progress_bar(current, total):
    percent = current * 100 / total
    done = int(percent // 2)
    bar = '█' * done + '-' * (50 - done)
    speed = current / (time.time() - start_time + 1e-6)
    logger.info(f"Uploading: |{bar}| {percent:.2f}% "
                f"({current / (1024*1024):.2f} MB of {total / (1024*1024):.2f} MB) "
                f"Speed: {speed / (1024*1024):.2f} MB/s")

# Main upload logic
async def main():
    global start_time
    if not os.path.exists(FILE_PATH):
        logger.error("❌ File not found.")
        return

    logger.info("Uploading file...")
    start_time = time.time()

    try:
        await client.send_document(
            chat_id=CHAT_ID,
            document=FILE_PATH,
            caption="Here is your file!",
            progress=progress_bar
        )
        logger.info("✅ Upload complete.")
    except Exception as e:
        logger.exception(f"❌ Upload failed: {e}")

# Handle messages
@client.on_message
async def handle_message(message):
    if message.text == '/dl':
        logger.info("Received /dl command, starting file upload.")
        
        # Reply to the user
        await message.reply("File upload is starting... Please wait.")
        
        # Call main function to start uploading
        await main()
    else:
        logger.debug(f"Unknown message received: {message.text}")


# Run the bot
if __name__ == "__main__":
    client.run()
