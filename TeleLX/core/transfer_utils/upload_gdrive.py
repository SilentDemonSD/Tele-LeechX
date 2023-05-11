import sys, errno
from asyncio import sleep as asleep, subprocess, create_subprocess_exec
from os import path as opath, listdir, remove as oremove
from re import escape as rescape, findall
from shutil import rmtree
from time import time, sleep as tsleep
from functools import partial
from pathlib import Path
from requests import utils, get as rget

from pyrogram import enums, Client
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from hurry.filesize import size
from PIL import Image
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import InputMediaAudio, InputMediaDocument, InputMediaVideo
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from TeleLX import DESTINATION_FOLDER, DL_DIR, EDIT_SLEEP_TIME_OUT, INDEX_LINK, VIEW_LINK, LOGGER, \
                   TG_MAX_FILE_SIZE, UPLOAD_AS_DOC, CAP_STYLE, CUSTOM_CAPTION, user_doc, LEECH_LOG, \
                   EXCEP_CHATS, EX_LEECH_LOG, BOT_PM, TG_PRM_FILE_SIZE, PRM_USERS, PRM_LOG, isUserPremium, AUTH_CHATS, \
                   UPDATES_CHANNEL, SPLIT_SIZE, USER_LOGS
if isUserPremium:
    from TeleLX import userBot
from TeleLX.core.bot_themes.themes import BotTheme
from TeleLX.core.ffmpeg.ffmpeg_extract import copy_file, take_screen_shot
from TeleLX.helper_funcs.display_progress import format_bytes, Progress
from TeleLX.helper_funcs.split_large_files import split_large_files
from TeleLX.plugins.custom_utils import *

# © gautamajay52 | RClone.org
async def upload_to_gdrive(file_upload, message, messa_ge, g_id):
    await asleep(EDIT_SLEEP_TIME_OUT)
    del_it = await message.edit_text(
        f"┏⚡️ <i>RClone Initiated</i> ⚡️\n┃\n┗📈 𝐒𝐭𝐚𝐭𝐮𝐬: <b><i>Uploading to Cloud...☁️</i></b>"
    )
    if opath.exists("rclone.conf"):
        with open("rclone.conf", "r+") as file:
            con = file.read()
            try:
                gUP = findall(r"\[(.*)\]", con)[0]
            except Exception as e:
                LOGGER.warning(f"[GClone] Make sure you have Set up the Name for the RClone Config Section. Error : {e}")
    destination = str(DESTINATION_FOLDER)
    file_upload = str(Path(file_upload).resolve())
    LOGGER.info(file_upload)
    if opath.isfile(file_upload):
        g_au = ["rclone", "copy", "--config=rclone.conf", f"{file_upload}", f"{gUP}:{destination}", "-v"]
        LOGGER.info(g_au)
        tmp = await create_subprocess_exec(
            *g_au, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        pro, cess = await tmp.communicate()
        LOGGER.info(pro.decode("utf-8"))
        LOGGER.info(cess.decode("utf-8"))
        gk_file = rescape(opath.basename(file_upload))
        LOGGER.info(gk_file)
        with open("filter.txt", "w+", encoding="utf-8") as filter:
            print(f"+ {gk_file}\n- *", file=filter)

        cmd = ["rclone", "lsf", "--config=rclone.conf", "-F", "i", "--filter-from=filter.txt", "--files-only", f"{gUP}:{destination}"]
        checkResults = await create_subprocess_exec(
            *cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        # oremove("filter.txt")
        gau, tam = await checkResults.communicate()
        gautam = gau.decode().strip()
        LOGGER.info(gau.decode())
        LOGGER.info(tam.decode())
        # oremove("filter.txt")
        gURL = f"https://drive.google.com/file/d/{gautam}/view?usp=drivesdk"
        gjay = size(opath.getsize(file_upload))
        button = [
            [
                InlineKeyboardButton(text="☁️ GDrive Link ☁️", url=f"{gURL}")
            ]
        ]
        fileURL = opath.basename(file_upload)
        if INDEX_LINK:
            _idno = 1
            INDEXS = INDEX_LINK.split(" ")
            for index in INDEXS:
                indexurl = f"{index}/{fileURL}"
                tam_link = utils.requote_uri(indexurl)
                LOGGER.info(f'Index Link #{_idno} : {tam_link}')
                if VIEW_LINK and (not indexurl.endswith('/')):
                    view_link_ = f"{tam_link}?a=view"
                    button.append([
                        InlineKeyboardButton(text=f"⚡️ Index Link #{_idno}⚡️", url=f"{tam_link}"),
                        InlineKeyboardButton(text=f"🌐 View Link #{_idno}", url=f"{view_link_}")
                    ])
                else:
                    button.append([
                        InlineKeyboardButton(text=f"⚡️ Index Link #{_idno}⚡️", url=f"{tam_link}")
                    ])
                _idno += 1
        button_markup = InlineKeyboardMarkup(button)
        await asleep(EDIT_SLEEP_TIME_OUT)
        await messa_ge.reply_text(
            f"📨 **Name** : `{fileURL}`\n\n📊 **Total Size** : `{gjay}B`\n\n👤 **Req By:** {messa_ge.from_user.mention} ( #ID{messa_ge.from_user.id} )",
            reply_markup=button_markup,
        )
        oremove(file_upload)
    else:
        tt = opath.join(destination, opath.basename(file_upload))
        LOGGER.info(tt)
        t_am = [
            "rclone",
            "copy",
            "--config=rclone.conf",
            f"{file_upload}",
            f"{gUP}:{tt}",
            "-v",
        ]
        tmp = await create_subprocess_exec(
            *t_am, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        pro, cess = await tmp.communicate()
        LOGGER.info(pro.decode("utf-8"))
        LOGGER.info(cess.decode("utf-8"))
        g_file = rescape(opath.basename(file_upload))
        LOGGER.info(g_file)
        with open("filter1.txt", "w+", encoding="utf-8") as filter1:
            print(f"+ {g_file}/\n- *", file=filter1)

        g_a_u = [
            "rclone",
            "lsf",
            "--config=rclone.conf",
            "-F",
            "i",
            "--filter-from=filter1.txt",
            "--dirs-only",
            f"{gUP}:{destination}",
        ]
        gau_tam = await create_subprocess_exec(
            *g_a_u, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        # oremove("filter1.txt")
        gau, tam = await gau_tam.communicate()
        gautam = gau.decode("utf-8")
        LOGGER.info(gautam)
        LOGGER.info(tam.decode("utf-8"))
        # oremove("filter1.txt")
        gURL = f"https://drive.google.com/folderview?id={gautam}"
        gjay = size(getFolderSize(file_upload))
        LOGGER.info(gjay)
        button = [[
                InlineKeyboardButton(text="☁️ GDrive Link ☁️", url=f"{gURL}")
        ]]
        fileURL = opath.basename(file_upload)
        if INDEX_LINK:
            _idno = 1
            INDEXS = INDEX_LINK.split(" ")
            for index in INDEXS:
                indexurl = f"{index}/{fileURL}"
                tam_link = utils.requote_uri(indexurl)
                LOGGER.info(f'Index Link #{_idno} : {tam_link}')
                button.append([
                    InlineKeyboardButton(text=f"⚡️ Index Link #{_idno}⚡️", url=f"{tam_link}")
                ])
                _idno += 1
        button_markup = InlineKeyboardMarkup(button)
        await asleep(EDIT_SLEEP_TIME_OUT)
        await messa_ge.reply_text(
            f"📨 **Name** : `{fileURL}`\n\n📊 **Total Size** : `{gjay}B`\n\n👤 **Req By:** {messa_ge.from_user.mention} ( #ID{messa_ge.from_user.id} )",
            reply_markup=button_markup,
        )
        rmtree(file_upload)
    await del_it.delete()
