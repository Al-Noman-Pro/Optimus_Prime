import logging
import os
import sys
import time
import spamwatch
import threading
import telegram.ext as tg

from aiohttp import ClientSession
from telegram.ext import CallbackContext
from pyrogram import Client, errors
from Python_ARQ import ARQ
from telethon import TelegramClient

StartTime = time.time()

AUTHORIZED_CHATS = set()
SUDO_USERS = set()
AS_DOC_USERS = set()
AS_MEDIA_USERS = set()
DRIVES_IDS = []
DRIVES_NAMES = []
INDEX_URLS = []
Interval = []
download_dict = {}
download_dict_lock = threading.Lock()
status_reply_dict = {}
status_reply_dict_lock = threading.Lock()


StartTime = time.time()

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting.")
    quit(1)

ENV = bool(os.environ.get("ENV", False))

if ENV:
    TOKEN = os.environ.get("TOKEN", None)

    try:
        OWNER_ID = int(os.environ.get("OWNER_ID", None))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")

    JOIN_LOGGER = os.environ.get("JOIN_LOGGER", None)
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)

    try:
        SUDO_USERS = set(int(x) for x in os.environ.get("SUDO_USERS", "").split())
        DEV_USERS = set(int(x) for x in os.environ.get("DEV_USERS", "").split())
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    try:
        SUPPORT_USERS = set(int(x) for x in os.environ.get("SUPPORT_USERS", "").split())
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        WHITELIST_USERS = set(int(x) for x in os.environ.get("WHITELIST_USERS", "").split())
    except ValueError:
        raise Exception("Your whitelisted users list does not contain valid integers.")

    try:
        TIGER_USERS = set(int(x) for x in os.environ.get("TIGER_USERS", "").split())
    except ValueError:
        raise Exception("Your tiger users list does not contain valid integers.")

    try:
        AUTHORIZED_CHATS = set(int(x) for x in os.environ.get("AUTHORIZED_CHATS", "").split())
    except ValueError:
        raise Exception(
            "Your authorized chat list does not contain valid integers.")

    ALLOW_CHATS = "True"
    ALLOW_EXCL = os.environ.get("ALLOW_EXCL", False)
    AI_API_KEY = os.environ.get("AI_API_KEY", None)
    API_HASH = os.environ.get("API_HASH", None)
    API_ID = os.environ.get("API_ID", None)
    ARQ_API_KEY = os.environ.get("ARQ_API_KEY", None)
    ARQ_API_URL = os.environ.get("ARQ_API_URL", None)
    BAN_STICKER = os.environ.get("BAN_STICKER", "CAADAgADOwADPPEcAXkko5EB3YGYAg")
    CASH_API_KEY = os.environ.get("CASH_API_KEY", None)
    CERT_PATH = os.environ.get("CERT_PATH")
    DB_URI = os.environ.get("DATABASE_URL")
    DEL_CMDS = bool(os.environ.get("DEL_CMDS", False))
    EVENT_LOGS = os.environ.get("EVENT_LOGS", None)
    INFOPIC = bool(os.environ.get("INFOPIC", False))
    LOAD = os.environ.get("LOAD", "").split()
    NO_LOAD = os.environ.get("NO_LOAD", "translation").split()
    PORT = int(os.environ.get("PORT", 5000))
    SPAMWATCH_API = os.environ.get("SPAMWATCH_API", None)
    SPAMWATCH_SUPPORT_CHAT = os.environ.get("SPAMWATCH_SUPPORT_CHAT", None)
    STRICT_GBAN = bool(os.environ.get("STRICT_GBAN", False))
    STRICT_GMUTE = bool(os.environ.get("STRICT_GMUTE", False))
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", None)
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")
    TIME_API_KEY = os.environ.get("TIME_API_KEY", None)
    URL = os.environ.get("URL", "")  # Does not contain token
    WEBHOOK = bool(os.environ.get("WEBHOOK", False))
    WORKERS = int(os.environ.get("WORKERS", 8))

    # Optimus Prime Bot By AL-Noman
    AUTO_DELETE_MESSAGE_DURATION = -1
    BUTTON_FOUR_NAME = os.environ.get("BUTTON_FOUR_NAME")
    BUTTON_FOUR_URL = os.environ.get("BUTTON_FOUR_URL")
    BUTTON_FIVE_NAME = os.environ.get("BUTTON_FIVE_NAME")
    BUTTON_FIVE_URL = os.environ.get("BUTTON_FIVE_URL")
    BUTTON_SIX_NAME = os.environ.get("BUTTON_SIX_NAME")
    BUTTON_SIX_URL = os.environ.get("BUTTON_SIX_URL")
    CLONE_LIMIT = os.environ.get("CLONE_LIMIT", None)
    CRYPT = os.environ.get("CRYPT", None)
    DOWNLOAD_DIR = os.environ.get("DOWNLOAD_DIR", "usr/src/app/downloads")
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    DOWNLOAD_STATUS_UPDATE_INTERVAL = os.environ.get("DOWNLOAD_STATUS_UPDATE_INTERVAL")
    EQUAL_SPLITS = bool(os.environ.get("EQUAL_SPLITS", False))
    INDEX_URLS = os.environ.get("INDEX_URL", None)
    INDEX_URL = os.environ.get("INDEX_URL", None)
    IS_TEAM_DRIVE = bool(os.environ.get("IS_TEAM_DRIVE", False))
    parent_id = os.environ.get("GDRIVE_FOLDER_ID")
    PHPSESSID = os.environ.get("PHPSESSID", None)
    RSS_CHAT_ID = os.environ.get("RSS_CHAT_ID")
    rss_session = os.environ.get("USER_STRING_SESSION, api_id=int(TELEGRAM_API), api_hash=TELEGRAM_HASH", None)
    SHORTENER = os.environ.get("SHORTENER")
    SHORTENER_API = os.environ.get("SHORTENER_API")
    STATUS_LIMIT = os.environ.get("STATUS_LIMIT", "3")
    STOP_DUPLICATE = bool(os.environ.get("STOP_DUPLICATE", False))
    TG_SPLIT_SIZE = os.environ.get("TG_SPLIT_SIZE", 2097151000)
    UPTOBOX_TOKEN = os.environ.get("UPTOBOX_TOKEN", None)
    USE_SERVICE_ACCOUNTS = False
    VIEW_LINK = bool(os.environ.get("VIEW_LINK", False))
    AS_DOCUMENT = False
    CUSTOM_FILENAME = None
    PROCESS_MAX_TIMEOUT = 3600
    TG_MAX_FILE_SIZE = 2097152000

    try:
        BL_CHATS = set(int(x) for x in os.environ.get("BL_CHATS", "").split())
    except ValueError:
        raise Exception("Your blacklisted chats list does not contain valid integers.")
else:
    from Optimus_Prime.config import Development as Config

    TOKEN = Config.TOKEN

    try:
        OWNER_ID = int(Config.OWNER_ID)
    except ValueError:
        raise Exception("Your OWNER_ID variable is not a valid integer.")

    JOIN_LOGGER = Config.JOIN_LOGGER
    OWNER_USERNAME = Config.OWNER_USERNAME

    try:
        SUDO_USERS = set(int(x) for x in Config.SUDO_USERS or [])
        DEV_USERS = set(int(x) for x in Config.DEV_USERS or [])
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    try:
        SUPPORT_USERS = set(int(x) for x in Config.SUPPORT_USERS or [])
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        WHITELIST_USERS = set(int(x) for x in Config.WHITELIST_USERS or [])
    except ValueError:
        raise Exception("Your whitelisted users list does not contain valid integers.")

    try:
        TIGER_USERS = set(int(x) for x in Config.TIGER_USERS or [])
    except ValueError:
        raise Exception("Your tiger users list does not contain valid integers.")

    try:
        AUTHORIZED_CHATS = set(int(x) for x in Config.AUTHORIZED_CHATS or [])
    except ValueError:
        raise Exception(
            "Your authorized chat list does not contain valid integers.")

    try:
        AS_DOCUMENT = Config("AS_DOCUMENT")
        AS_DOCUMENT = AS_DOCUMENT.lower() == "true"
    except KeyError:
        AS_DOCUMENT = False

    try:
        CUSTOM_FILENAME = Config("CUSTOM_FILENAME")
        if len(CUSTOM_FILENAME) == 0:
            raise KeyError
    except KeyError:
        CUSTOM_FILENAME = None


    AI_API_KEY = Config.AI_API_KEY
    ALLOW_EXCL = Config.ALLOW_EXCL
    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    ARQ_API_KEY = Config.ARQ_API_KEY
    ARQ_API_URL = Config.ARQ_API_URL
    BACKUP_PASS = Config.BACKUP_PASS
    BAN_STICKER = Config.BAN_STICKER
    CASH_API_KEY = Config.CASH_API_KEY
    CERT_PATH = Config.CERT_PATH
    DB_NAME = Config.DB_NAME
    DEL_CMDS = Config.DEL_CMDS
    EVENT_LOGS = Config.EVENT_LOGS
    LOAD = Config.LOAD
    NO_LOAD = Config.NO_LOAD
    PORT = Config.PORT
    SPAMWATCH_API = Config.SPAMWATCH_API
    SPAMWATCH_SUPPORT_CHAT = Config.SPAMWATCH_SUPPORT_CHAT
    STRICT_GBAN = Config.STRICT_GBAN
    STRICT_GMUTE = Config.STRICT_GMUTE
    SUPPORT_CHAT = Config.SUPPORT_CHAT
    TIME_API_KEY = Config.TIME_API_KEY
    URL = Config.URL
    WALL_API = Config.WALL_API
    WORKERS = Config.WORKERS
    WEBHOOK = Config.WEBHOOK


DRIVES_NAMES.append("Main")
DRIVES_IDS.append(parent_id)
if os.path.exists("drive_folder"):
    with open("drive_folder", "r+") as f:
        lines = f.readlines()
        for line in lines:
            try:
                temp = line.strip().split()
                DRIVES_IDS.append(temp[1])
                DRIVES_NAMES.append(temp[0].replace("_", " "))
            except:
                pass
            try:
                INDEX_URLS.append(temp[2])
            except IndexError as e:
                INDEX_URLS.append(None)


if not SPAMWATCH_API:
    sw = None
    LOGGER.warning("SpamWatch API key missing! recheck your config.")
else:
    try:
        sw = spamwatch.Client(SPAMWATCH_API)
    except:
        sw = None
        LOGGER.warning("Can't connect to SpamWatch!")

# Create download directory, if not exist.
    if not os.path.isdir(DOWNLOAD_LOCATION):
        os.makedirs(DOWNLOAD_LOCATION)



# Install aiohttp session
print("[Optimus Prime]: Initializing AIOHTTP Session")
aiohttpsession = ClientSession()    
    
# Install arq
print("[Optimus Prime]: Initializing ARQ Client")
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)

pbot = Client("PyrogramBot", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)
telethn = TelegramClient("TelethonBot", API_ID, API_HASH)
updater = tg.Updater(TOKEN, workers=8, use_context=True)
bot = updater.bot
dispatcher = updater.dispatcher

SUDO_USERS.add(OWNER_ID)
DEV_USERS.add(OWNER_ID)

AUTHORIZED_CHATS = list(AUTHORIZED_CHATS)
SUDO_USERS = list(SUDO_USERS) + list(DEV_USERS)
DEV_USERS = list(DEV_USERS)
WHITELIST_USERS = list(WHITELIST_USERS)
SUPPORT_USERS = list(SUPPORT_USERS)
TIGER_USERS = list(TIGER_USERS)

# Load at end to ensure all prev variables have been set
from Optimus_Prime.modules.helper_funcs.handlers import (
    CustomCommandHandler,
    CustomMessageHandler)

# make sure the regex handler can take extra kwargs
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler

