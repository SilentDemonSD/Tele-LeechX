#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52 | MaxxRider | 5MysterySD | Other Contributors 
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved

import logging
from pytz import timezone
from urllib.parse import quote as q
from os import path as opath, makedirs, remove as oremove, execl
from shutil import rmtree
from datetime import datetime
from requests import get as rget
from heroku3 import from_key as from_apikey

from pyrogram import enums, Client, filters, idle
from pyrogram.errors import ChannelInvalid, PeerIdInvalid
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from pyrogram.handlers import CallbackQueryHandler, MessageHandler
from sys import executable
from subprocess import run as srun

from tobrot import HEROKU_API_KEY, HEROKU_APP_NAME, app, __version__
from tobrot import OWNER_ID, SUDO_USERS, AUTH_CHANNEL, DOWNLOAD_LOCATION, GET_SIZE_G, GLEECH_COMMAND, \
                   GLEECH_UNZIP_COMMAND, GLEECH_ZIP_COMMAND, LOGGER, RENEWME_COMMAND, TELEGRAM_LEECH_UNZIP_COMMAND, \
                   TELEGRAM_LEECH_COMMAND, UPLOAD_COMMAND, GYTDL_COMMAND, GPYTDL_COMMAND, RCLONE_COMMAND, \
                   UPDATES_CHANNEL, LEECH_LOG, STRING_SESSION, SET_BOT_COMMANDS, RDM_QUOTE, INDEX_SCRAPE, TIMEZONE, \
                   AUTO_LEECH, PICS_LIST, PIXABAY_API_KEY, PIXABAY_CATEGORY, PIXABAY_SEARCH, START_BTN1, START_URL1, \
                   START_BTN2, START_URL2
if STRING_SESSION:
    from tobrot import userBot
from tobrot.helper_funcs.download import down_load_media_f
from tobrot.helper_funcs.download_aria_p_n import aria_start
from tobrot.plugins import *
from tobrot.plugins.anilist import get_anime_query, anilist_callbackquery
from tobrot.plugins.index_scrape import index_scrape
from tobrot.plugins.call_back_button_handler import button
from tobrot.plugins.imdb import imdb_search, imdb_callback
from tobrot.plugins.torrent_search import searchhelp, nyaa_callback, nyaa_nop, nyaa_search, nyaa_search_sukebei, TorrentSearch, \
                                          RESULT_STR_1337, RESULT_STR_PIRATEBAY, RESULT_STR_TGX, RESULT_STR_YTS, RESULT_STR_EZTV, \
                                          RESULT_STR_TORLOCK, RESULT_STR_RARBG, RESULT_STR_ALL
from tobrot.plugins.custom_utils import prefix_set, caption_set, template_set, theme_set, anilist_set, user_log_set, log_chat_id
from tobrot.plugins.url_parser import url_parser
from tobrot.helper_funcs.bot_commands import BotCommands
from tobrot.database.db_func import DatabaseManager
from tobrot.plugins.choose_rclone_config import rclone_command_f
from tobrot.plugins.custom_thumbnail import clear_thumb_nail, save_thumb_nail
from tobrot.plugins.incoming_message_fn import g_clonee, g_yt_playlist, incoming_message_f, incoming_purge_message_f, \
                                               incoming_youtube_dl_f, rename_tg_file, auto_callback
from tobrot.plugins.help_func import help_message_f, stats, user_settings, settings_callback, picture_add, pictures, pics_callback
from tobrot.plugins.speedtest import get_speed
from tobrot.plugins.mediainfo import mediainfo
from tobrot.plugins.rclone_size import check_size_g, g_clearme
from tobrot.plugins.status_message_fn import cancel_message_f, eval_message_f, exec_message_f, status_message_f, \
                                             upload_document_f, upload_log_file, upload_as_doc, upload_as_video

botcmds = [
        BotCommand(f'{BotCommands.LeechCommand}', '📨 [Reply] Leech any Torrent/ Magnet/ Direct Link '),
        BotCommand(f'{BotCommands.ExtractCommand}', '🔐 Unarchive items . .'),
        BotCommand(f'{BotCommands.ArchiveCommand}', '🗜 Archive as .tar.gz acrhive... '),
        BotCommand(f'{BotCommands.ToggleDocCommand}', '📂 Toggle to Document Upload '),
        BotCommand(f'{BotCommands.ToggleVidCommand}', '🎞 Toggle to Streamable Upload '),
        BotCommand(f'{BotCommands.SaveCommand}', '🖼 Save Thumbnail For Uploads'),
        BotCommand(f'{BotCommands.ClearCommand}', '🕹 Clear Thumbnail '),
        BotCommand(f'{BotCommands.RenameCommand}', '📧 [Reply] Rename Telegram File '),
        BotCommand(f'{BotCommands.StatusCommand}', '🖲 Show Bot stats and concurrent Downloads'),
        BotCommand(f'{BotCommands.SpeedCommand}', '📡 Get Current Server Speed of Your Bot'),
        BotCommand(f'{BotCommands.YtdlCommand}', '🧲 [Reply] YT-DL Links for Uploading...'),
        BotCommand(f'{BotCommands.PytdlCommand}', '🧧 [Reply] YT-DL Playlists Links for Uploading...'),
        BotCommand(f'{BotCommands.GCloneCommand}', '♻️ [G-Drive] Clone Different Supported Sites !!'),
        BotCommand(f'{BotCommands.StatsCommand}', '📊 Show Bot Internal Statistics'),
        BotCommand(f'{BotCommands.MediaInfoCommand}', '🆔️ [Reply] Get Telegram Files Media Info'),
        BotCommand('setpre', '🔠 <Text> Save Custom Prefix for Uploads'),
        BotCommand('setcap', '🔣 <Text> Save Custom Caption for Uploads'),
        BotCommand('parser', '🧮 <URL> Get Bypassed Link After Parsing !!'),
        BotCommand('imdb', '🎬 [Title] Get IMDb Details About It !!'),
        BotCommand('set_template', '📋 [HTML] Set IMDb Custom Template for Usage!!'),
        BotCommand('choosetheme', '🗄 Set Custom Bot Theme for Usage for Own Decorative Purposes !!'),
        BotCommand(f'{BotCommands.HelpCommand}', '🆘 Get Help, How to Use and What to Do. . .'),
        BotCommand(f'{BotCommands.LogCommand}', '🔀 Get the Bot Log [Owner Only]'),
        BotCommand(f'{BotCommands.TsHelpCommand}', '🌐 Get help for Torrent Search Module')
    ]

async def start(client, message):
    """/start command"""
    buttons = [
            [InlineKeyboardButton(START_BTN1, url=START_URL1),
            InlineKeyboardButton(START_BTN2, url=START_URL2)]
            ]
    reply_markup=InlineKeyboardMarkup(buttons)
    u_men = message.from_user.mention
    start_log_string = f'''
┏ <i>Dear {u_men}</i>,
┃
┃ <i>If You Want To Use Me, You Have To Join {UPDATES_CHANNEL}</i>
┃
┣ <b>NOTE:</b> <code>All The Uploaded Leeched Contents By You Will Be Sent Here In Your Private Chat From Now.</code>
┃
┗━♦️ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 {UPDATES_CHANNEL}♦️
'''

    if message.chat.type == enums.ChatType.PRIVATE:
        if LEECH_LOG:
            await message.reply_text(
                start_log_string,
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML,
                quote=True
            )
        else:
            await message.delete()
    else:
        await message.reply_text(
            "**I Am Alive and Working, Send /help to Know How to Use Me !** ✨",
            parse_mode=enums.ParseMode.MARKDOWN,
        )

async def clean_all():
    aria2 = await aria_start()
    aria2.remove_all(True)
    try:
        rmtree(DOWNLOAD_LOCATION)
    except FileNotFoundError:
        pass

async def restart(client: Client, message: Message):
    if message.from_user.id != OWNER_ID and message.from_user.id not in SUDO_USERS:
        return
    cmd = message.text.split(' ', 1)
    dynoRestart = False
    dynoKill = False
    if len(cmd) == 2:
        dynoRestart = (cmd[1].lower()).startswith('d')
        dynoKill = (cmd[1].lower()).startswith('k')
    if (not HEROKU_API_KEY) or (not HEROKU_APP_NAME):
        LOGGER.info("[ATTENTION] Fill HEROKU_API_KEY & HEROKU_APP_NAME for Using this Feature.")
        dynoRestart = False
        dynoKill = False
    if dynoRestart:
        LOGGER.info("[HEROKU] Dyno Restarting...")
        restart_message = await message.reply_text("__Dyno Restarting...__")
        await app.stop()
        if STRING_SESSION: await userBot.stop()
        heroku_conn = from_apikey(HEROKU_API_KEY)
        appx = heroku_conn.app(HEROKU_APP_NAME)
        appx.restart()
    elif dynoKill:
        LOGGER.info("[HEROKU] Killing Dyno...")
        await message.reply_text("__Killed Dyno__")
        heroku_conn = from_apikey(HEROKU_API_KEY)
        appx = heroku_conn.app(HEROKU_APP_NAME)
        proclist = appx.process_formation()
        for po in proclist:
            appx.process_formation()[po.type].scale(0)
    else:
        LOGGER.info("[HEROKU] Normally Restarting...")
        restart_message = await message.reply_text("__Restarting...__")
        try:
            await clean_all()
        except Exception as err:
            LOGGER.info(f"Restart Clean Error : {err}")
        srun(["pkill", "-f", "extra-api|new-api"])
        srun(["python3", "update.py"])
        with open(".restartmsg", "w") as f:
            f.truncate(0)
            f.write(f"{restart_message.chat.id}\n{restart_message.id}\n")
        execl(executable, executable, "-m", "tobrot")

if __name__ == "__main__":
    # Generat Download Directory, if Not Exist !!
    if not opath.isdir(DOWNLOAD_LOCATION):
        makedirs(DOWNLOAD_LOCATION)

    # Pixabay API >>>>>>>>
    if PIXABAY_API_KEY:
        try:
            PIXABAY_ENDPOINT = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&image_type=all&orientation=horizontal&min_width=1280&min_height=720&per_page=200&safesearch=true&editors_choice=true"
            if PIXABAY_CATEGORY: PIXABAY_ENDPOINT += f"&category={PIXABAY_CATEGORY}"
            if PIXABAY_SEARCH: PIXABAY_ENDPOINT += f"&q={q(PIXABAY_SEARCH)}"
            resp = rget(PIXABAY_ENDPOINT)
            jdata = resp.json()
            for x in range(0, 200):
                largeImageURL = jdata['hits'][x]['largeImageURL']
                PICS_LIST.append(largeImageURL)
        except Exception as err:
            LOGGER.info(f"Pixabay API Error: {err}")

    # Bot Restart & Restart Message >>>>>>>>
    curr = datetime.now(timezone(TIMEZONE))
    date = curr.strftime('%d %B, %Y')
    time = curr.strftime('%I:%M:%S %p')
    rst_text = f'''<b>Bᴏᴛ Rᴇsᴛᴀʀᴛᴇᴅ !!</b>

<b>📆 𝘿𝙖𝙩𝙚 :</b> <code>{date}</code> 
<b>⏰ 𝙏𝙞𝙢𝙚 :</b> <code>{time}</code>
<b>🚧 𝙏𝙞𝙢𝙚𝙕𝙤𝙣𝙚 :</b> <code>{TIMEZONE}</code>

<b>ℹ️ 𝙑𝙚𝙧𝙨𝙞𝙤𝙣 :</b> <code>{__version__}</code>'''
    if opath.isfile(".restartmsg"):
        with open(".restartmsg") as f:
            chat_id, msg_id = map(int, f)
        for a in app:
            a.edit_message_text(chat_id, msg_id, rst_text, disable_web_page_preview=True)
        oremove(".restartmsg")
    elif OWNER_ID:
        if RDM_QUOTE:
            try:
                qResponse = rget("https://quote-garden.herokuapp.com/api/v3/quotes/random")
                if qResponse.status_code == 200:
                    qData = qResponse.json() 
                    qText = qData['data'][0]['quoteText']
                    qAuthor = qData['data'][0]['quoteAuthor']
                    #qGenre = qData['data'][0]['quoteGenre']
                    text += f"\n\n📬 𝙌𝙪𝙤𝙩𝙚 :\n\n<b>{qText}</b>\n\n🏷 <i>By {qAuthor}</i>"
            except Exception as q:
                LOGGER.error("Quote API Error : {q}")
        for chatx in AUTH_CHANNEL:
            for a in app:
                try:
                    a.send_message(chat_id=int(chatx), text=rst_text, parse_mode=enums.ParseMode.HTML)
                except ChannelInvalid:
                    LOGGER.warning(f'Make Sure the Bot is Added to Chat ID : {chatx}')
                except PeerIdInvalid:
                    LOGGER.warning(f'Make Sure the Chat ID is Valid ( Multiple Chat ID are Separated by single Space ), Chat ID : {chatx}')
                except Exception as e:
                    LOGGER.error(e)
    if SET_BOT_COMMANDS.lower() == "true":
        for a in app:
            a.set_bot_commands(botcmds)

    TORRENT_API = 'https://api.linkstore.eu.org/api'

    torrents_dict = {
        '1337x': {'source': f"{TORRENT_API}/1337x/", 'result_str': RESULT_STR_1337},
        'piratebay': {'source': f"{TORRENT_API}/piratebay/", 'result_str': RESULT_STR_PIRATEBAY},
        'tgx': {'source': f"{TORRENT_API}/tgx/", 'result_str': RESULT_STR_TGX},
        'yts': {'source': f"{TORRENT_API}/yts/", 'result_str': RESULT_STR_YTS},
        'eztv': {'source': f"{TORRENT_API}/eztv/", 'result_str': RESULT_STR_EZTV},
        'torlock': {'source': f"{TORRENT_API}/torlock/", 'result_str': RESULT_STR_TORLOCK},
        'rarbg': {'source': f"{TORRENT_API}/rarbg/", 'result_str': RESULT_STR_RARBG},
        'ts': {'source': f"{TORRENT_API}/all/", 'result_str': RESULT_STR_ALL}
    }

    # Command Initialize >>>>>>>>
    for a in app:
        username = (a.get_me()).username
        if AUTO_LEECH:
            a.add_handler(MessageHandler(incoming_message_f, filters=filters.regex(r"^(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))") & filters.chat(chats=AUTH_CHANNEL)))
        else:
            a.add_handler(MessageHandler(
                incoming_message_f,
                filters=filters.command([
                    BotCommands.LeechCommand, f"{BotCommands.LeechCommand}@{username}",
                    BotCommands.ArchiveCommand, f"{BotCommands.ArchiveCommand}@{username}",
                    BotCommands.ExtractCommand, f"{BotCommands.ExtractCommand}@{username}",
                    GLEECH_COMMAND, f"{GLEECH_COMMAND}@{username}",
                    GLEECH_UNZIP_COMMAND, f"{GLEECH_UNZIP_COMMAND}@{username}",
                    GLEECH_ZIP_COMMAND, f"{GLEECH_ZIP_COMMAND}@{username}",
                    ])
                & filters.chat(chats=AUTH_CHANNEL),
            ))
        a.add_handler(MessageHandler(down_load_media_f, filters=filters.command([TELEGRAM_LEECH_COMMAND, f"{TELEGRAM_LEECH_COMMAND}@{username}", TELEGRAM_LEECH_UNZIP_COMMAND, f"{TELEGRAM_LEECH_UNZIP_COMMAND}@{username}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(incoming_purge_message_f, filters=filters.command(["purge", f"purge@{username}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(g_clonee, filters=filters.command([f"{BotCommands.GCloneCommand}", f"{BotCommands.GCloneCommand}@{username}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(check_size_g, filters=filters.command([f"{GET_SIZE_G}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(g_clearme, filters=filters.command([f"{RENEWME_COMMAND}", f"{RENEWME_COMMAND}@{username}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(incoming_youtube_dl_f, filters=filters.command([f"{BotCommands.YtdlCommand}", f"{BotCommands.YtdlCommand}@{username}", f"{GYTDL_COMMAND}", f"{GYTDL_COMMAND}@{username}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(g_yt_playlist, filters=filters.command([f"{BotCommands.PytdlCommand}", f"{BotCommands.PytdlCommand}@{username}", GPYTDL_COMMAND]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(status_message_f, filters=filters.command([f"{BotCommands.StatusCommand}", f"{BotCommands.StatusCommand}@{username}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(cancel_message_f, filters=filters.regex(r'^/cancel($|\_([a-z]|[0-9])+($|\@\S+$))') & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(exec_message_f, filters=filters.command(["exec", "exec@{username}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(eval_message_f, filters=filters.command(["eval", "exec@{username}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(rename_tg_file, filters=filters.command([f"{BotCommands.RenameCommand}", f"{BotCommands.RenameCommand}@{username}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(upload_document_f, filters=filters.command([f"{UPLOAD_COMMAND}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(upload_log_file, filters=filters.command([f"{BotCommands.LogCommand}", f"{BotCommands.LogCommand}@{username}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(help_message_f, filters=filters.command([f"{BotCommands.HelpCommand}", f"{BotCommands.HelpCommand}@{username}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(save_thumb_nail, filters=filters.command([f"{BotCommands.SaveCommand}", f"{BotCommands.SaveCommand}@{username}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(clear_thumb_nail, filters=filters.command([f"{BotCommands.ClearCommand}", f"{BotCommands.ClearCommand}@{username}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(rclone_command_f, filters=filters.command([f"{RCLONE_COMMAND}", f"{RCLONE_COMMAND}@{username}"])))
        a.add_handler(MessageHandler(upload_as_doc, filters=filters.command([f"{BotCommands.ToggleDocCommand}", f"{BotCommands.ToggleDocCommand}@{username}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(upload_as_video, filters=filters.command([f"{BotCommands.ToggleVidCommand}", f"{BotCommands.ToggleVidCommand}@{username}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(get_speed, filters=filters.command([f"{BotCommands.SpeedCommand}", f"{BotCommands.SpeedCommand}@{username}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(searchhelp, filters=filters.command([f"{BotCommands.TsHelpCommand}", f"{BotCommands.TsHelpCommand}@{username}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(mediainfo, filters=filters.command([f"{BotCommands.MediaInfoCommand}", f"{BotCommands.MediaInfoCommand}@{username}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(restart, filters=filters.command(["restart", f"restart@{username}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(stats, filters=filters.command([f"{BotCommands.StatsCommand}", f"{BotCommands.StatsCommand}@{username}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(start, filters=filters.command(["start", f"start@{username}"])))
        a.add_handler(MessageHandler(prefix_set, filters=filters.command(["setpre", f"setpre@{username}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(caption_set, filters=filters.command(["setcap", f"setcap@{username}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(url_parser, filters=filters.command(["parser", f"parser@{username}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(imdb_search, filters=filters.command(["imdb", f"imdb@{username}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(template_set, filters=filters.command(["set_template", f"set_template@{username}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(index_scrape, filters=filters.command([f"{INDEX_SCRAPE}", f"{INDEX_SCRAPE}@{username}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(theme_set, filters=filters.command([f"choosetheme", f"choosetheme@{username}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(user_settings, filters=filters.command([f"usersettings", f"usersettings@{username}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(get_anime_query, filters=filters.command(["ani", f"ani@{username}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(anilist_set, filters=filters.command(["anime_template", f"anime_template@{username}"]) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(nyaa_search, filters=filters.command(['nyaasi', f'nyaasi@{username}']) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(nyaa_search_sukebei, filters=filters.command(['sukebei', f'sukebei@{username}']) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(picture_add, filters=filters.command(['addpic', f'addpic@{username}']) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(pictures, filters=filters.command(['pics', f'pics@{username}']) & filters.chat(chats=AUTH_CHANNEL)))
        #a.add_handler(MessageHandler(set_configvar, filters=filters.command(['setvar', f'setvar@{username}']) & filters.chat(chats=AUTH_CHANNEL) & filters.private))
        a.add_handler(MessageHandler(user_log_set, filters=filters.command(['userlog', f'userlog@{username}']) & filters.chat(chats=AUTH_CHANNEL)))
        a.add_handler(MessageHandler(log_chat_id, filters=filters.command(['id', f'id@{username}']) & filters.channel))
        for tcom, value in torrents_dict.items():
            a.add_handler(MessageHandler(TorrentSearch(tcom, value['source'], value['result_str']).find, filters.command([tcom, f'{tcom}@{username}'])))
            a.add_handler(CallbackQueryHandler(TorrentSearch(tcom, value['source'], value['result_str']).previous, filters.regex(f"{tcom}_previous")))
            a.add_handler(CallbackQueryHandler(TorrentSearch(tcom, value['source'], value['result_str']).delete, filters.regex(f"{tcom}_delete")))
            a.add_handler(CallbackQueryHandler(TorrentSearch(tcom, value['source'], value['result_str']).next, filters.regex(f"{tcom}_next")))

        a.add_handler(CallbackQueryHandler(anilist_callbackquery, filters=filters.regex(pattern="^(tags|stream|reviews|relations|characters|home)")))
        a.add_handler(CallbackQueryHandler(imdb_callback, filters=filters.regex(pattern="^imdb")))
        a.add_handler(CallbackQueryHandler(auto_callback, filters=filters.regex(pattern="^alx")))
        a.add_handler(CallbackQueryHandler(settings_callback, filters=filters.regex(pattern="^set")))
        a.add_handler(CallbackQueryHandler(pics_callback, filters=filters.regex(pattern="^pic")))
        a.add_handler(CallbackQueryHandler(nyaa_nop, filters=filters.regex(pattern="nyaa_nop")))
        a.add_handler(CallbackQueryHandler(nyaa_callback, filters=filters.regex(pattern="nyaa_back|nyaa_next")))
        a.add_handler(CallbackQueryHandler(button))

    logging.info(r'''
 ______    __        __               __   _  __
/_  __/__ / /__ ____/ /  ___ ___ ____/ /  | |/_/
 / / / -_) / -_)___/ /__/ -_) -_) __/ _ \_>  <  
/_/  \__/_/\__/   /____/\__/\__/\__/_//_/_/|_|''')
    for a in app:
        logging.info(f"{(a.get_me()).first_name} [@{(a.get_me()).username}] has Started Running...🏃💨💨")
    if STRING_SESSION:
            logging.info(f"User : {(userBot.get_me()).first_name} has Started Revolving...♾️⚡️")

    idle()

    for a in app:
        a.stop()
    if STRING_SESSION: 
        userBot.stop()
        logging.info("UserBot Stopped !!")
