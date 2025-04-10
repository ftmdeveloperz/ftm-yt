import os

SESSION = "my_bot"
API_ID = int(os.getenv("API_ID", "8239"))
API_HASH = os.getenv("API_HASH", "171e6f1bf6d8dcc5140fbe827b6b08")
BOT_TOKEN = os.getenv("BOT_TOKEN", "807590ZxZZnChpX5srczTxgxz5YmHQ8")
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1004232975"))
DUMP_CHANNEL = int(os.getenv("DUMP_CHANNEL", "-1002232975"))
PORT = int(os.getenv("PORT", "8080"))
FORCE_CHANNEL = int(os.getenv("FORCE_CHANNEL", "-1002379643238"))
HTTP_PROXY = ''
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv:089@cluster0.y8tpouc.mongodb.net/?retryWrites=true&w=majority")
MONGO_NAME = os.getenv("MONGO_NAME", "YouTubeDL")
ADMINS = [5660839376, 6167872503]
DAILY_LIMITS = 20
