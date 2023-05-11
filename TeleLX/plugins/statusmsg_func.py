#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52 | SilentDemonSD | Other Contributors 
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/SilentDemonSD/Tele-LeechX >
# All Right Reserved

import sys

from datetime import datetime
from math import floor
from random import choice
from asyncio import sleep as asleep, subprocess, create_subprocess_shell
from io import BytesIO, StringIO
from os import path as opath, remove as oremove
from psutil import disk_usage
from time import time, sleep as tsleep
from traceback import format_exc
from psutil import virtual_memory, cpu_percent, net_io_counters

from pyrogram.errors import FloodWait, MessageIdInvalid, MessageNotModified
from pyrogram import enums, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, Message

from TeleLX.plugins import getUserOrChaDetails, getUserName, progressBar
from TeleLX.helper_funcs.admin_check import AdminCheck
from TeleLX import AUTH_CHATS, BOT_START_TIME, LOGGER, MAX_MESSAGE_LENGTH, user_doc, \
                   gid_dict, _lock, EDIT_SLEEP_TIME_OUT, FINISHED_PROGRESS_STR, UN_FINISHED_PROGRESS_STR, \
                   UPDATES_CHANNEL, LOG_FILE_NAME, DB_URI, user_settings, HALF_FINISHED, PICS_LIST
from TeleLX.helper_funcs.display_progress import format_bytes, format_time
from TeleLX.helper_funcs.download_aria_p_n import aria_start
from TeleLX.helper_funcs.upload_to_tg import upload_to_tg
from TeleLX.database.db_func import DatabaseManager
from TeleLX.core.bot_themes.themes import BotTheme

def bot_button_stats():
    hr, mi, se = up_time(time() - BOT_START_TIME)
    total, used, free, disk = disk_usage("/")
    ram = virtual_memory().percent
    cpu = cpu_percent()
    total = format_bytes(total)
    used = format_bytes(used)
    free = format_bytes(free)
    sent = format_bytes(net_io_counters().bytes_sent)
    recv = format_bytes(net_io_counters().bytes_recv)
    return f'''
┏━━━━ 𝗕𝗼𝘁 𝗦𝘁𝗮𝘁𝘀 ━━━━━╻
┃ ᑕᑭᑌ: {progressBar(cpu)} {cpu}% 
┃ ᖇᗩᗰ: {progressBar(ram)} {ram}%  
┃ T-ᗪᒪ: {sent} ┃ T-ᑌᒪ: {recv}
┃ ᑌᑭ : {hr}h {mi}m {se}s
┃ T: {total} ┃ ᖴ: {free}
┃ ᗪIՏK: {progressBar(disk)} {disk}%
┗━━━━━━━━━━━━━━━━╹'''

async def status_message_f(client: Client, message: Message):
    u_id_, u_tag = getUserOrChaDetails(message)
    aria_i_p = await aria_start()
    to_edit = await message.reply_photo(photo=choice(PICS_LIST) ,caption="🧭 𝐆𝐞𝐭𝐭𝐢𝐧𝐠 𝐂𝐮𝐫𝐫𝐞𝐧𝐭 𝐒𝐭𝐚𝐭𝐮𝐬 . .") if PICS_LIST else await message.reply("🧭 𝐆𝐞𝐭𝐭𝐢𝐧𝐠 𝐂𝐮𝐫𝐫𝐞𝐧𝐭 𝐒𝐭𝐚𝐭𝐮𝐬 . .")
    chat_id = int(message.chat.id)
    mess_id = int(to_edit.id)
    async with _lock:
        if len(gid_dict[chat_id]) == 0:
            gid_dict[chat_id].append(mess_id)
        elif mess_id not in gid_dict[chat_id]:
            await client.delete_messages(chat_id, gid_dict[chat_id])
            gid_dict[chat_id].pop()
            gid_dict[chat_id].append(mess_id)

    prev_mess = "FXTorrentz"
    try:
        await message.delete()
    except: pass
    while True:
        downloads = aria_i_p.get_downloads()
        msg = ""
        for file in downloads:
            downloading_dir_name = "N/A"
            try:
                downloading_dir_name = str(file.name)
            except:
                pass
            if file.status == "active":
                umess = user_settings[file.gid]
                percentage = int(file.progress_string(0).split('%')[0])
                digits = [int(x) for x in f'{"%.2d" % percentage}']
                prog = "[{0}{1}{2}]".format(
                    "".join([FINISHED_PROGRESS_STR for _ in range(floor(percentage / 5))]),
                    HALF_FINISHED if floor(digits[1]) > 5 else UN_FINISHED_PROGRESS_STR,
                    "".join([UN_FINISHED_PROGRESS_STR for _ in range(19 - floor(percentage / 5))])
                )
                is_file = file.seeder
                curTime = time()
                msg += ((BotTheme(u_id_)).STATUS_MSG_1).format(
                    mess_link = umess.link or '',
                    file_name = downloading_dir_name,
                    progress = prog,
                    prog_string = file.progress_string(),
                    total_string = file.total_length_string(),
                    speed_string = file.download_speed_string(),
                    eta_string = file.eta_string()
                )
                try:
                    inTime = datetime.timestamp(datetime.strptime(str(umess.date),"%Y-%m-%d %H:%M:%S"))
                    msg += ((BotTheme(u_id_)).STATUS_MSG_2).format(
                        etime = format_time((curTime - inTime) * 1000)
                    )
                except: pass
                usr_id, tag_me = getUserOrChaDetails(umess)
                msg += ((BotTheme(u_id_)).STATUS_MSG_3).format(
                    u_men = tag_me,
                    uid = usr_id
                )
                if is_file is None:
                    msg += ((BotTheme(u_id_)).STATUS_MSG_4).format(
                        connections = file.connections
                    )
                else:
                    msg += ((BotTheme(u_id_)).STATUS_MSG_5).format(
                        num_seeders = file.num_seeders,
                        connections = file.connections
                    )
                msg += ((BotTheme(u_id_)).STATUS_MSG_6).format(
                    gid = file.gid
                )

        ms_g = (BotTheme(u_id_)).BOTTOM_STATUS_MSG
        if UPDATES_CHANNEL:
            ms_g += f"\n♦️ ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 {UPDATES_CHANNEL}♦️"
        umen = f'<a href="tg://user?id={u_id_}">{u_tag}</a>'
        mssg = ((BotTheme(u_id_)).TOP_STATUS_MSG).format(
            umen = umen,
            uid = u_id_
        )
        button_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('Sᴛᴀᴛᴜs\nCʜᴇᴄᴋ', callback_data="stats"),
             InlineKeyboardButton('Cʟᴏsᴇ', callback_data="admin_close")]
        ])

        if msg == "":
            msg = (BotTheme(u_id_)).DEF_STATUS_MSG
            msg = mssg + "\n" + msg + "\n" + ms_g
            if PICS_LIST: await to_edit.edit_caption(caption=msg, reply_markup=button_markup)
            else: await to_edit.edit(msg, reply_markup=button_markup)
            await asleep(EDIT_SLEEP_TIME_OUT)
            await to_edit.delete()
            break
        msg = mssg + "\n" + msg + "\n" + ms_g
        if len(msg) > MAX_MESSAGE_LENGTH:
            with BytesIO(str.encode(msg)) as out_file:
                out_file.name = "fxstatus.txt"
                await client.send_document(
                    chat_id=message.chat.id,
                    document=out_file,
                )
            break
        else:
            if msg != prev_mess:
                try:
                    if PICS_LIST: await client.edit_message_media(chat_id=to_edit.chat.id, message_id=to_edit.id, media=InputMediaPhoto(media=choice(PICS_LIST), caption=msg), reply_markup=button_markup)
                    else: await to_edit.edit(msg, parse_mode=enums.ParseMode.HTML, reply_markup=button_markup)
                except MessageIdInvalid:
                    break
                except MessageNotModified as ep:
                    LOGGER.info(ep)
                    await asleep(EDIT_SLEEP_TIME_OUT)
                except FloodWait as e:
                    LOGGER.info(f"FloodWait : Sleeping {e.value}s")
                    tsleep(e.value)
                await asleep(EDIT_SLEEP_TIME_OUT)
                prev_mess = msg

async def cancel_message_f(client, message):
    if '_' in message.text:
        i_m_s_e_g = await message.reply_text("<code>Checking..⁉️</code>", quote=True)
        aria_i_p = await aria_start()
        gidData = (message.text).split("_")
        g_id = gidData[1].strip()
        UserNames = await getUserName()
        for i in range(0, len(UserNames)):
            if g_id.endswith(f'@{UserNames[i]}'):
                g_id = g_id.replace(f'@{UserNames[i]}', '')
        LOGGER.info(f"Cancel GID: {g_id}")
        try:
            downloads = aria_i_p.get_download(g_id)
            name = downloads.name
            size = downloads.total_length_string()
            gid_list = downloads.followed_by_ids
            downloads = [downloads]
            if len(gid_list) != 0:
                downloads = aria_i_p.get_downloads(gid_list)
            aria_i_p.remove(downloads=downloads, force=True, files=True, clean=True)
            await i_m_s_e_g.edit_text(f"⛔<b> Download Cancelled </b>⛔ :\n<code>{name} ({size})</code> By <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>")
        except Exception as e:
            await i_m_s_e_g.edit_text("<i>⚠️ FAILED ⚠️</i>\n\n" + str(e) + "\n#Error")
    else:
        await message.delete()


def up_time(time_taken):
    hours, _hour = divmod(time_taken, 3600)
    minutes, seconds = divmod(_hour, 60)
    return round(hours), round(minutes), round(seconds)


async def upload_log_file(client, message):
    logFile = await AdminCheck(client, message.chat.id, message.from_user.id)
    if logFile and opath.exists(LOG_FILE_NAME):
        try:
            LOGGER.info("Generating LOG Display...")
            with open(LOG_FILE_NAME, "r") as logFileRead:
                logFileLines = logFileRead.read().splitlines()
                toDisplay = min(len(logFileLines), 25)
                startLine = f'Last {toDisplay} Lines : [On Display Telegram LOG]\n\n---------------- START LOG -----------------\n\n'
                endLine = '\n---------------- END LOG -----------------'
                Loglines = ''.join(logFileLines[-l]+'\n\n' for l in range(toDisplay, 0, -1))
                Loglines = Loglines.replace('"', '')
                textLog = startLine + Loglines + endLine
                await message.reply_text(
                    textLog,
                    disable_web_page_preview=True,
                    parse_mode=enums.ParseMode.DISABLED
                )
        except Exception as err:
            LOGGER.error(f"Error Log Display: {err}")
            LOGGER.info(textLog)
        
        h, m, s = up_time(time() - BOT_START_TIME)
        await message.reply_document(LOG_FILE_NAME, caption=f"**Full Log**\n\n**Bot Uptime:** `{h}h, {m}m, {s}s`")