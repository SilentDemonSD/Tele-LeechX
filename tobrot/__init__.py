#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52 | MaxxRider | 5MysterySD | Other Contributors 
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved 

import logging
from itertools import count
from time import time
from requests import get as rget
from os import environ, path as opath
from subprocess import run
from threading import Lock as ThreadLock
from asyncio import Lock
from urllib.request import urlretrieve
from collections import defaultdict
from logging.handlers import RotatingFileHandler
from sys import exit
from dotenv import load_dotenv
from pyrogram import Client

run(["chmod", "+x", "extract"])

def getVar(var: str, val):
    return environ.get(var, val)

CONFIG_FILE_URL = getVar('CONFIG_FILE_URL', '')

try:
    if len(CONFIG_FILE_URL) == 0:
        raise TypeError
    try:
        res = rget(CONFIG_FILE_URL)
        if res.status_code == 200:
            with open('config.env', 'wb+') as f:
                f.write(res.content)
        else:
            LOGGER.error(f"Failed to download config.env : {res.status_code}")
    except Exception as e:
        LOGGER.error(f"CONFIG_FILE_URL: {e}")
except:
    pass

load_dotenv("config.env", override=True)

UPDATES_CHANNEL = getVar("UPDATES_CHANNEL", "")
LOG_FILE_NAME = f"{UPDATES_CHANNEL}Logs.txt"

if opath.exists(LOG_FILE_NAME):
    with open(LOG_FILE_NAME, "r+") as f_d:
        f_d.truncate(0)

# Logging Requirements >>>>>>>>>>>
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%d-%b-%y %I:%M:%S %p",
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME, maxBytes=50000000, backupCount=10
        ),
        logging.StreamHandler(),
    ],
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("PIL").setLevel(logging.WARNING)

LOGGER = logging.getLogger(__name__)

user_specific_config = {}
PRE_DICT = {}
CAP_DICT = {}
IMDB_TEMPLATE = {}
ANILIST_TEMPLATE = {}
USER_THEMES = {}
AVAILABLE_THEMES = {}
USER_LOGS = {}
AUTO_USERS = {}
__version__ = "2.9.1"

TG_BOT_TOKEN, APP_ID, API_HASH = [], [], []

# The Telegram API things >>>>>>>>>>>
for x in count():
    bot_tok = getVar(f"TG_BOT_TOKEN{x + 1}", "")
    tg_id = getVar(f"APP_ID{x + 1}", "")
    tg_hash = getVar(f"API_HASH{x + 1}", "")
    if bot_tok == "" or tg_id == "" or tg_hash == "":
        break
    TG_BOT_TOKEN.append(bot_tok)
    APP_ID.append(int(tg_id))
    API_HASH.append(tg_hash)
OWNER_ID = int(getVar("OWNER_ID", ""))

# Heroku & Restart Utils >>>>>>>>>>>
HEROKU_API_KEY = getVar('HEROKU_API_KEY', None)
HEROKU_APP_NAME = getVar('HEROKU_APP_NAME', None)

# Authorised Chat Functions >>>>>>>>>>>
AUTH_CHANNEL = [int(x) for x in getVar("AUTH_CHANNEL", "").split()]
SUDO_USERS = [int(sudos) if (' ' not in getVar('SUDO_USERS', '')) else int(sudos) for sudos in getVar('SUDO_USERS', '').split()]
AUTH_CHANNEL.extend((OWNER_ID, 1242011540))
AUTH_CHANNEL += SUDO_USERS # Change Permissions Soon
# Download Directory >>>>>>>>>>>
DOWNLOAD_LOCATION = "./Downloads"

# Compulsory Variables >>>>>>>>
for imp in ["TG_BOT_TOKEN1", "APP_ID1", "API_HASH1", "OWNER_ID", "AUTH_CHANNEL"]:
    try:
        value = environ[imp]
        if not value:
            raise KeyError
    except KeyError:
        LOGGER.critical(f"[ERROR] Variable : {imp} Missing from config.env. Fill Up and Retry")
        exit()

# Telegram Max File Upload Size >>>>>>>>>>
TG_MAX_FILE_SIZE = 2097152000
TG_PRM_FILE_SIZE = 4194304000

# Chunk Size that should be used with Requests >>>>>>>>>>
CHUNK_SIZE = int(getVar("CHUNK_SIZE", "128"))
DEF_THUMB_NAIL_VID_S = getVar("DEF_THUMB_NAIL_VID_S", "")
MAX_MESSAGE_LENGTH = 4096

# Timeout for Subprocess >>>>>>>>
PROCESS_MAX_TIMEOUT = 3600

# Internal Requirements >>>>>>>>>>>
SP_LIT_ALGO_RITH_M = getVar("SP_LIT_ALGO_RITH_M", "hjs")
ARIA_TWO_STARTED_PORT = int(getVar("ARIA_TWO_STARTED_PORT", "6800"))
EDIT_SLEEP_TIME_OUT = int(getVar("EDIT_SLEEP_TIME_OUT", "10"))
MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START = int(getVar("MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START", 1200))
SPLIT_SIZE = getVar("SPLIT_SIZE", None)

# Vars for the Display Progress >>>>>>>>
FINISHED_PROGRESS_STR = getVar("FINISHED_PROGRESS_STR", "■")
HALF_FINISHED = getVar("HALF_FINISHED", "◩")
UN_FINISHED_PROGRESS_STR = getVar("UN_FINISHED_PROGRESS_STR", "□")

# Add Offensive API & Filename Parsing >>>>>>>>
TG_OFFENSIVE_API = getVar("TG_OFFENSIVE_API", None)
CUSTOM_PREFIX = getVar("CUSTOM_PREFIX", "")
CUSTOM_SUFFIX = getVar("CUSTOM_SUFFIX", "")

#Bot Command [Leech]  >>>>>>>>>>>
LEECH_COMMAND = getVar("LEECH_COMMAND", "leech")
LEECH_UNZIP_COMMAND = getVar("LEECH_UNZIP_COMMAND", "extract")
LEECH_ZIP_COMMAND = getVar("LEECH_ZIP_COMMAND", "archive")
GLEECH_COMMAND = getVar("GLEECH_COMMAND", "gleech")
GLEECH_UNZIP_COMMAND = getVar("GLEECH_UNZIP_COMMAND", "gleechunzip")
GLEECH_ZIP_COMMAND = getVar("GLEECH_ZIP_COMMAND", "gleechzip")

#Bot Command [yt-dlp] >>>>>>>>>>>
YTDL_COMMAND = getVar("YTDL_COMMAND", "ytdl")
GYTDL_COMMAND = getVar("GYTDL_COMMAND", "gytdl")
PYTDL_COMMAND = getVar("PYTDL_COMMAND", "pytdl")
GPYTDL_COMMAND = getVar("GPYTDL_COMMAND", "gpytdl")

#Bot Command [RClone]  >>>>>>>>>>>
DESTINATION_FOLDER = getVar("DESTINATION_FOLDER", "Tele-LeechX")
INDEX_LINK = getVar("INDEX_LINK", "")
VIEW_LINK = getVar("VIEW_LINK", True)
GET_SIZE_G = getVar("GET_SIZE_G", "getsize")
CLONE_COMMAND_G = getVar("CLONE_COMMAND_G", "gclone")
TELEGRAM_LEECH_COMMAND = getVar("TELEGRAM_LEECH_COMMAND", "tleech")
TELEGRAM_LEECH_UNZIP_COMMAND = getVar("TELEGRAM_LEECH_UNZIP_COMMAND", "tleechunzip")

#Bot Command [Miscs]  >>>>>>>>>>>
STATUS_COMMAND = getVar("STATUS_COMMAND", "status")
SAVE_THUMBNAIL = getVar("SAVE_THUMBNAIL", "savethumb")
CLEAR_THUMBNAIL = getVar("CLEAR_THUMBNAIL", "clearthumb")
UPLOAD_AS_DOC = getVar("UPLOAD_AS_DOC", "False")
LOG_COMMAND = getVar("LOG_COMMAND", "log")
STATS_COMMAND = getVar("STATS_COMMAND", "stats")

#Bot Command [Custom Bot Cmd Name]  >>>>>>>>>>>
SET_BOT_COMMANDS = getVar("SET_BOT_COMMANDS", "True")
UPLOAD_COMMAND = getVar("UPLOAD_COMMAND", "upload")
RENEWME_COMMAND = getVar("RENEWME_COMMAND", "renewme")
RENAME_COMMAND = getVar("RENAME_COMMAND", "rename")
TOGGLE_VID = getVar("TOGGLE_VID", "togglevid")
TOGGLE_DOC = getVar("TOGGLE_DOC", "toggledoc")
RCLONE_COMMAND = getVar("RCLONE_COMMAND", "rclone")
HELP_COMMAND = getVar("HELP_COMMAND", "help")
SPEEDTEST = getVar("SPEEDTEST", "speedtest")
TSEARCH_COMMAND = getVar("TSEARCH_COMMAND", "tshelp")
MEDIAINFO_CMD = getVar("MEDIAINFO_CMD", "mediainfo")
CAP_STYLE = getVar("CAP_STYLE", "code")
BOT_NO = getVar("BOT_NO", "")
USER_DTS = getVar("USER_DTS", True)
INDEX_SCRAPE = getVar("INDEX_SCRAPE", "indexscrape")

#Bot Command [Token Utils]  >>>>>>>>>>>
UPTOBOX_TOKEN = getVar("UPTOBOX_TOKEN", "")
EMAIL = getVar("EMAIL", "")
PWSSD = getVar("PWSSD", "")
LARAVEL_SESSION = getVar("LARAVEL_SESSION", "")
XSRF_TOKEN = getVar("XSRF_TOKEN", "")
GDRIVE_FOLDER_ID = getVar("GDRIVE_FOLDER_ID", "")
CRYPT = getVar("CRYPT", "")
HUB_CRYPT = getVar("HUB_CRYPT", "")
DRIVEFIRE_CRYPT = getVar("DRIVEFIRE_CRYPT", "")
KATDRIVE_CRYPT = getVar("KATDRIVE_CRYPT", "")
KOLOP_CRYPT = getVar("KOLOP_CRYPT", "")
DRIVEBUZZ_CRYPT = getVar("DRIVEBUZZ_CRYPT", "")
GADRIVE_CRYPT = getVar("GADRIVE_CRYPT", "")
STRING_SESSION = getVar("STRING_SESSION", "")

#Bot Command [IMDB]  >>>>>>>>>>>
CUSTOM_CAPTION = getVar("CUSTOM_CAPTION", "")
MAX_LIST_ELM = getVar("MAX_LIST_ELM", 4)
DEF_IMDB_TEMPLATE = getVar("IMDB_TEMPLATE", "")
if DEF_IMDB_TEMPLATE == "":
    DEF_IMDB_TEMPLATE = '''<b>Title: </b> {title} [{year}]
<b>Also Known As:</b> {aka}
<b>Rating ⭐️:</b> <i>{rating}</i>
<b>Release Info: </b> <a href="{url_releaseinfo}">{release_date}</a>
<b>Genre: </b>{genres}
<b>IMDb URL:</b> {url}
<b>Language: </b>{languages}
<b>Country of Origin : </b> {countries}

<b>Story Line: </b><code>{plot}</code>

<a href="{url_cast}">Read More ...</a>'''
DEF_ANILIST_TEMPLATE = getVar("ANILIST_TEMPLATE", """<b>{ro_title}</b>({na_title})
<b>Format</b>: <code>{format}</code>
<b>Status</b>: <code>{status}</code>
<b>Start Date</b>: <code>{startdate}</code>
<b>End Date</b>: <code>{enddate}</code>
<b>Season</b>: <code>{season}</code>
<b>Country</b>: {country}
<b>Episodes</b>: <code>{episodes}</code>
<b>Duration</b>: <code>{duration}</code>
<b>Average Score</b>: <code>{avgscore}</code>
<b>Genres</b>: {genres}
<b>Hashtag</b>: {hashtag}
<b>Studios</b>: {studios}
<b>Description</b>: <i>{description}</i>""")

#Telegraph Creds  >>>>>>>>>>>
TGH_AUTHOR = getVar("TGH_AUTHOR ", "Tele-LeechX")
TGH_AUTHOR_URL = getVar("TGH_AUTHOR_URL", "https://t.me/FXTorrentz")

#Bot Command [Bot PM & Log Channel]  >>>>>>>>>>>
LEECH_LOG = getVar("LEECH_LOG", "")
LEECH_INVITE = getVar("LEECH_INVITE", "False")
EX_LEECH_LOG = [int(chats) if (' ' not in getVar('EX_LEECH_LOG', '')) else int(chats) for chats in getVar('EX_LEECH_LOG', '').split()]
EXCEP_CHATS = [int(chats) if (' ' not in getVar('EXCEP_CHATS', '')) else int(chats) for chats in getVar('EXCEP_CHATS', '').split()]
BOT_PM = getVar("BOT_PM", "False")
BOT_PM = True if BOT_PM.lower() == "true" else False
AUTO_LEECH = getVar("AUTO_LEECH", "False")
AUTO_LEECH = True if AUTO_LEECH.lower() == "true" else False

#Status Photos & Pixabay API >>>>>>>>>>
PICS_LIST = (getVar("PICS", "")).split()
PIXABAY_API_KEY = getVar("PIXABAY_API_KEY", "")
PIXABAY_CATEGORY = getVar("PIXABAY_CATEGORY", "")
PIXABAY_SEARCH = getVar("PIXABAY_SEARCH", "")

# 4 GB Upload Utils >>>>>>>>>>>
PRM_USERS = getVar("PRM_USERS", "") #Optional 
PRM_LOG = getVar("PRM_LOG", "") #Optional 

# Bot Theme [ UI & Customization ] >>>>>>>>
BOT_THEME = getVar("BOT_THEME", "fx-optimised-theme")

# ForceSubscribe [ Channel ] >>>>>>>>
FSUB_CHANNEL = getVar("FSUB_CHANNEL", "")

# Quotes in Restart Message & Utils >>>>>>>>
TIMEZONE = getVar("TIMEZONE", "Asia/Kolkata")
RDM_QUOTE = getVar("RDM_QUOTE", "False")
RDM_QUOTE = True if RDM_QUOTE.lower() == "true" else False

# Buttons in Start Message >>>>>>>>
START_BTN1 = getVar("START_BTN1", "🛃 FXTorrentz 🛃")
START_URL1 = getVar("START_URL1", "https://t.me/FXTorrentz")
START_BTN2 = getVar("START_BTN2", "🔍 Source Code")
START_URL2 = getVar("START_URL2", "https://github.com/5MysterySD/Tele-LeechX")

# Database Handler >>>>>>>>
DB_URI = getVar("DATABASE_URL", "")

BOT_START_TIME = time()

gDict = defaultdict(lambda: [])
user_settings = defaultdict(lambda: {})
gid_dict = defaultdict(lambda: [])
_lock = Lock()
user_settings_lock = ThreadLock()

# Rclone Config Via Raw Gist URL & BackUp >>>>>>>>
try:                                                                      
    RCLONE_CONF_URL = getVar('RCLONE_CONF_URL', "")              
    if len(RCLONE_CONF_URL) == 0:                                        
        RCLONE_CONF_URL = None                                           
    else:                                                                
        urlretrieve(RCLONE_CONF_URL, '/app/rclone.conf')
        LOGGER.info("[SUCCESS] RClone Setup Complete via URL")
except KeyError:                                                       
    RCLONE_CONF_URL = None                                              

# Rclone Config via Root Directory & BackUp >>>>>>>>
if not opath.exists("rclone.conf"):
    LOGGER.warning("[NOT FOUND] rclone.conf not found in Root Directory .")
if opath.exists("rclone.conf") and not opath.exists("rclone_bak.conf"):
    with open("rclone_bak.conf", "w+", newline="\n", encoding="utf-8") as fole:
        with open("rclone.conf", "r") as f:
            fole.write(f.read())
    LOGGER.info("[SUCCESS] rclone.conf BackUped to rclone_bak.conf!")

# Pyrogram Client Intialization >>>>>>>>>>>
app = [ 
    Client("LeechBot", bot_token=TG_BOT_TOKEN[0], api_id=APP_ID[0], api_hash=API_HASH[0], workers=343), 
]
for i in range(1, len(TG_BOT_TOKEN)):
    app.append(Client(f"LeechBot-{i}", bot_token=TG_BOT_TOKEN[i], api_id=APP_ID[i], api_hash=API_HASH[i], workers=343))
if len(app) > 1:
    LOGGER.info(f"[Multi Client Initiated] Total Bots : {len(app)}")

# Start The Bot >>>>>>>
for a in app:
    a.start()

isUserPremium = False
if STRING_SESSION:
    if userBot := Client(
        "Tele-UserBot",
        api_id=APP_ID[0],
        api_hash=API_HASH[0],
        session_string=STRING_SESSION,
    ):
        userBot.start()
        if (userBot.get_me()).is_premium:
            isUserPremium = True
            LOGGER.info("[SUCCESS] Initiated UserBot : Premium Mode") #Logging is Needed Very Much
        else:
            isUserPremium = False
            LOGGER.info("[SUCCESS] Initiated UserBot : Non-Premium Mode. Add Premium Account StringSession to Use 4GB Upload. ")
    else:
        LOGGER.warning("[FAILED] Userbot Not Started. ReCheck Your STRING_SESSION, and Other Vars")
