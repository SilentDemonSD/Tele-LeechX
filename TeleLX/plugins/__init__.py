#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of Tele-LeechX: https://github.com/SilentDemonSD/Tele-LeechX
# Copyright (c) 2022-2023 SilentDemonSD.
# All rights reserved.

"""
This script is a part of the Tele-LeechX project, a Telegram bot based on Pyrogram Framework and 
extra leeching utilities. Its purpose is to allow users to easily download and save media files 
in Telegram chats and channels.
"""

from asyncio import create_subprocess_exec, subprocess
from shlex import split as ssplit
from shutil import rmtree
from typing import Tuple
from re import match as rmatch
from urllib.parse import unquote, quote
from pyrogram import enums

from TeleLX import DL_DIR, LOGGER, app, AUTO_LEECH, AUTH_CHATS
from TeleLX.core.display.display_utils import format_bytes

async def getUserName():
    return [(await a.get_me()).username for a in app]

async def runcmd(cmd: str, capture_output: bool = True) -> Tuple[str, str, int, int]:
    """
    Run a command in the terminal and return stdout, stderr, return code, and process id.

    Args:
        cmd (str): The command to be executed.
        capture_output (bool): Indicates whether to capture stdout and stderr (default: True).

    Returns:
        Tuple[str, str, int, int]: A tuple containing stdout, stderr, return code, and process ID.
    """
    args = ssplit(cmd)
    stdout_arg = subprocess.PIPE if capture_output else None
    stderr_arg = subprocess.PIPE if capture_output else None

    process = await asyncio.create_subprocess_exec(
        *args, stdout=stdout_arg, stderr=stderr_arg
    )
    stdout, stderr = await process.communicate()

    return (
        stdout.decode("utf-8", "replace").strip() if capture_output else "",
        stderr.decode("utf-8", "replace").strip() if capture_output else "",
        process.returncode,
        process.pid,
    )

def start_cleanup():
    try:
        rmtree(DL_DIR)
    except FileNotFoundError:
        pass
    
async def clean_all():
    aria2 = await aria_start()
    aria2.remove_all(True)
    try:
        rmtree(DOWNLOAD_LOCATION)
    except FileNotFoundError:
        pass

def is_gdtot_link(url: str): 
    url = rmatch(r'https?://.+\.gdtot\.\S+', url) 
    return bool(url)


def is_hubdrive_link(url: str): 
    url = rmatch(r'https?://hubdrive\.\S+', url) 
    return bool(url)


def is_appdrive_link(url: str): 
    url = rmatch(r'https?://appdrive\.\S+', url) 
    return bool(url)

async def AdminCheck(client, chat_id, user_id):
    chat = await client.get_chat(chat_id)
    if chat.type == enums.ChatType.PRIVATE and chat_id in AUTH_CHATS:
        return True
    SELF = await client.get_chat_member(chat_id=chat_id, user_id=user_id)
    if SELF.status not in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
        return False
    return True


def magnet_parse(mag_link):
    link = unquote(mag_link)
    link = link.split("&")
    tracker = ""
    tracCount = 0
    for check in link:
        if check.startswith('dn='):
            name = check.replace("dn=", "")
        elif check.startswith('tr='):
            tracCount += 1
            tracker += f"{tracCount}. <code>{check.replace('tr=', '')}</code>\n"
        elif check.startswith('magnet:?xt=urn:btih:'):
            hashh = check.replace('magnet:?xt=urn:btih:', '')
    return f"🔸️ <b>Hash :</b> <i>{hashh}</i>\n📨 <b>Name :</b> {name}\n🖲 <b>Trackers ({tracCount}) :</b> \n{tracker} \n 🔗 <a href='https://t.me/share/url?url={quote(mag_link)}'>Share To Telegram</a>"

def getDetails(client, message, func_txt: str):
    g_id, u_men = getUserOrChaDetails(message)
    link_send = message.text.split(" ", maxsplit=1)
    reply_to = message.reply_to_message
    txtCancel = False
    text__ = f"<i>⚡️{func_txt} Initiated⚡️</i>\n┃\n┣👤 <b>User</b> : <a href='tg://user?id={g_id}'>{u_men}</a>\n┣🆔 <b>User ID</b> : #ID{g_id}\n"
    if len(link_send) > 1 or (AUTO_LEECH and len(link_send) == 1):
        link = link_send[0] if AUTO_LEECH else link_send[1]
        if link.lower().startswith("magnet:"):
            text__ += f"┗🧲 <b>Magnet Link Details</b> :  \n{magnet_parse(link)}"
        elif link.lower().startswith("http") and "|" not in link:
            text__ += f"┗🔗 <b>Link</b> :  <a href='{link.strip()}'>Click Here</a>"
        elif link.lower().startswith("http") and "|" in link:
            splitData = link.split("|", 1)
            link = splitData[0]
            text__ += f"┗🔗 <b>Link</b> :  <a href='{link.strip()}'>Click Here</a>\n🗳 <b>Custom Name</b> :<code>{splitData[1]}</code>"
        else:
            text__ += f"┗🔗 <b>Link</b> :  <code>{link}</code>"
    elif reply_to is not None:
        if reply_to.media:
            if reply_to.document:
                filename = [reply_to.document][0].file_name
                filesize = format_bytes([reply_to.document][0].file_size)
                if str(filename).lower().endswith(".torrent"):
                    text__ += f"\n📨 <b>File Name:</b> <code>{filename}</code>\n🗃 <b>Total Size:</b> <code>{filesize}</code>\n📂 <b>Media Type</b> : ☢️ <code>Torrent File</code> ☢️"
                else:
                    text__ += f"\n📨 <b>File Name:</b> <code>{filename}</code>\n🗃 <b>Total Size:</b> <code>{filesize}</code>\n📂 <b>Media Type</b> : 🗃 <code>Document</code> 🗃"
            elif reply_to.video:
                filename = [reply_to.video][0].file_name
                filesize = format_bytes([reply_to.video][0].file_size)
                text__ += f"\n📨 <b>File Name:</b> <code>{filename}</code>\n🗃 <b>Total Size:</b> <code>{filesize}</code>\n📂 <b>Media Type</b> :  🎥 <code>Video</code> 🎥"
            elif reply_to.audio:
                filename = [reply_to.audio][0].file_name
                filesize = format_bytes([reply_to.audio][0].file_size)
                text__ += f"\n📨 <b>File Name:</b> <code>{filename}</code>\n🗃 <b>Total Size:</b> <code>{filesize}</code>\n📂 <b>Media Type</b> :  🎶 <code>Audio</code> 🎶"
        elif reply_to.text.lower().startswith("magnet:"):
            text__ += f"🧲 <b>Magnet Link Details</b> :  \n{magnet_parse(reply_to.text)}"
        else:
            link = reply_to.text
            cusfname = ""
            cusfnam = link.split("|", maxsplit=1)
            if len(cusfnam) > 1:
                link, cusfname = cusfnam[0], cusfnam[1]
            LOGGER.info(cusfname)
            if cusfname != "" and link.lower().startswith("http"):
                text__ += f"┗🔗 <b>Link</b> :  <a href='{link.strip()}'>Click Here</a>\n🗳 <b>Custom Name</b> :<code>{cusfname}</code>"
            elif link.lower().startswith("http"):
                text__ += f"┗🔗 <b>Link</b> :  <a href='{link.strip()}'>Click Here</a>"
            else:
                text__ += f"┗🔗 <b>Link</b> :  <code>{link}</code>"
    else:
        txtCancel = True
        link = "N/A"
        text__ += f"🔗 <b>Link</b> : <code>{link}</code>"
    return text__, txtCancel

def getUserOrChaDetails(mess):
    if hasattr(mess.from_user, 'id'):
        uid = mess.from_user.id
        u_tag = mess.from_user.mention
    else:
        uid = str(mess.chat.id)[4:]
        u_tag = (mess.chat.title if mess.author_signature is None else mess.author_signature)
    return uid, u_tag

