# Create a new config.py or rename this to config.py file in same dir and import, then extend this class.

import json
import os


def get_user_list(config, key):
    with open('{}/Optimus_Prime/{}'.format(os.getcwd(), config),
              'r') as json_file:
        return json.load(json_file)[key]


# Create a new config.py or rename this to config.py file in same dir and import, then extend this class.
class Config(object):
    LOGGER = True
    # REQUIRED
    #Login to https://my.telegram.org and fill in these slots with the details given by it

    API_ID = 123456  # integer value, dont use ""
    API_HASH = ""
    TOKEN = ""
    OWNER_ID = 123456789  # If you dont know, run the bot and do /id in your private chat with it, also an integer
    OWNER_USERNAME = "awoo"
    SUPPORT_CHAT = "awoo"  # Your own group for support, do not add the @
    JOIN_LOGGER = 1234567890123 # Prints any new group the bot is added to, prints just the name and ID.
    EVENT_LOGS = 1234567890123 # Prints information like gbans, sudo promotes, AI enabled disable states that may help in debugging and shit
    SPAMWATCH_API = ""

    #RECOMMENDED
    ARQ_API_KEY = ""
    ARQ_API_URL = "https://thearq.tech/"
    SQLALCHEMY_DATABASE_URI = 'something://somewhat:user@hosturl:port/databasename'  # needed for any database modules
    LOAD = []
    NO_LOAD = ['rss', 'cleaner', 'connection', 'math']
    WEBHOOK = False
    INFOPIC = True
    URL = None
    SPAMWATCH_API = ""  # go to support.spamwat.ch to get key
    SPAMWATCH_SUPPORT_CHAT = ""

    #OPTIONAL
    AI_API_KEY = ""
    ##List of id's -  (not usernames) for users which have sudo access to the bot.
    SUDO_USERS = get_user_list('elevated_users.json', 'sudos')
    ##List of id's - (not usernames) for developers who will have the same perms as the owner
    DEV_USERS = get_user_list('elevated_users.json', 'devs')
    ##List of id's (not usernames) for users which are allowed to gban, but can also be banned.
    SUPPORT_USERS = get_user_list('elevated_users.json', 'supports')
    #List of id's (not usernames) for users which WONT be banned/kicked by the bot.
    TIGER_USERS = get_user_list('elevated_users.json', 'tigers')
    WHITELIST_USERS = get_user_list('elevated_users.json', 'whitelists')
    DONATION_LINK = None  # EG, paypal
    CERT_PATH = None
    PORT = 5000
    DEL_CMDS = True  #Delete commands that users dont have access to, like delete /ban if a non admin uses it.
    STRICT_GBAN = True
    STRICT_GMUTE = True
    WORKERS = 8  # Number of subthreads to use. Set as number of threads your processor uses
    BAN_STICKER = ''  # banhammer marie sticker id, the bot will send this sticker before banning or kicking a user in chat.
    ALLOW_EXCL = True  # Allow ! commands as well as / (Leave this to true so that blacklist can work)
    CASH_API_KEY = 'awoo'  # Get your API key from https://www.alphavantage.co/support/#api-key
    TIME_API_KEY = 'awoo'  # Get your API key from https://timezonedb.com/api
    WALL_API = 'awoo'  #For wallpapers, get one from https://wall.alphacoders.com/api.php
    AI_API_KEY = 'awoo'  #For chatbot, get one from https://coffeehouse.intellivoid.net/dashboard
    BL_CHATS = []  # List of groups that you want blacklisted.
    SPAMMERS = None
    WALL_API = ""

    # Mirror Bot
    AUTHORIZED_CHATS = ""
    GDRIVE_FOLDER_ID = ""
    DOWNLOAD_DIR = "/usr/src/app/downloads"
    DOWNLOAD_STATUS_UPDATE_INTERVAL = 5
    AUTO_DELETE_MESSAGE_DURATION = -1
    IS_TEAM_DRIVE = ""
    AUTHORIZED_CHATS = ""
    IGNORE_PENDING_REQUESTS = ""
    USE_SERVICE_ACCOUNTS = ""
    INDEX_URL = ""
    STATUS_LIMIT = ""
    STOP_DUPLICATE = ""
    TG_SPLIT_SIZE = ""
    BASE_URL_OF_BOT = ""
    IS_VPS = ""
    MEGA_API_KEY = ""
    MEGA_EMAIL_ID = ""
    MEGA_PASSWORD = ""
    BLOCK_MEGA_FOLDER = ""
    BLOCK_MEGA_LINKS = ""
    TORRENT_DIRECT_LIMIT = ""
    ZIP_UNZIP_LIMIT = ""
    CLONE_LIMIT = ""
    MEGA_LIMIT = ""
    VIEW_LINK = ""
    BUTTON_FOUR_NAME = ""
    BUTTON_FOUR_URL = ""
    BUTTON_FIVE_NAME = ""
    BUTTON_FIVE_URL = ""
    BUTTON_SIX_NAME = ""
    BUTTON_SIX_URL = ""


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
