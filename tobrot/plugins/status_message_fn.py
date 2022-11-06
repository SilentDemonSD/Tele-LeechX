#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52 | 5MysterySD | Other Contributors 
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
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
from tobrot.plugins import getUserOrChaDetails, getUserName, progressBar
from tobrot.helper_funcs.admin_check import AdminCheck
from tobrot import AUTH_CHANNEL, BOT_START_TIME, LOGGER, MAX_MESSAGE_LENGTH, user_specific_config, \
                   gid_dict, _lock, EDIT_SLEEP_TIME_OUT, FINISHED_PROGRESS_STR, UN_FINISHED_PROGRESS_STR, \
                   UPDATES_CHANNEL, LOG_FILE_NAME, DB_URI, user_settings, HALF_FINISHED, PICS_LIST
from tobrot.helper_funcs.display_progress import humanbytes, TimeFormatter
from tobrot.helper_funcs.download_aria_p_n import aria_start
from tobrot.helper_funcs.upload_to_tg import upload_to_tg
from tobrot.database.db_func import DatabaseManager
from tobrot.bot_theme.themes import BotTheme

async def upload_as_doc(client, message):
    uid, u_tag = getUserOrChaDetails(message)
    user_specific_config[uid] = True
    if DB_URI:
        DatabaseManager().user_doc(uid)
        LOGGER.info("[DB] User Toggle DOC Settings Saved to Database")
    await message.reply_text(((BotTheme(uid)).TOGGLEDOC_MSG).format(
        u_men = u_tag,
        u_id = uid,
        UPDATES_CHANNEL = UPDATES_CHANNEL
    ))

async def upload_as_video(client, message):
    uid, u_tag = getUserOrChaDetails(message)
    user_specific_config[uid] = False
    if DB_URI:
        DatabaseManager().user_vid(uid)
        LOGGER.info("[DB] User Toggle VID Settings Saved to Database")
    await message.reply_text(((BotTheme(uid)).TOGGLEVID_MSG).format(
        u_men = u_tag,
        u_id = uid,
        UPDATES_CHANNEL = UPDATES_CHANNEL
    ))

def bot_button_stats():
    hr, mi, se = up_time(time() - BOT_START_TIME)
    total, used, free, disk = disk_usage("/")
    ram = virtual_memory().percent
    cpu = cpu_percent()
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    sent = humanbytes(net_io_counters().bytes_sent)
    recv = humanbytes(net_io_counters().bytes_recv)
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
                        etime = TimeFormatter((curTime - inTime) * 1000)
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

async def exec_message_f(client, message):
    if message.chat.type == enums.ChatType.CHANNEL:
        if message.chat.id not in AUTH_CHANNEL:
            return
    elif message.chat.type == enums.ChatType.SUPERGROUP:
        if hasattr(message.from_user, 'id') and message.from_user.id not in AUTH_CHANNEL:
            return
        elif message.chat.id not in AUTH_CHANNEL:
            return
    DELAY_BETWEEN_EDITS = 0.3
    PROCESS_RUN_TIME = 100
    cmd = message.text.split(" ", maxsplit=1)[1]
    link = message.text.split(' ', maxsplit=1)[1]
    work_in = await message.reply_text("`Generating ...`")

    reply_to_id = message.id
    if message.reply_to_message:
        reply_to_id = message.reply_to_message.id

    start_time = time() + PROCESS_RUN_TIME
    process = await create_subprocess_shell(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e = stderr.decode()
    if not e:
        e = "No Error"
    o = stdout.decode()
    if not o:
        o = "No Output"
    else:
        _o = o.split("\n")
        o = "`\n".join(_o)
    OUTPUT = f"<b>QUERY:</b>\n\nCommand: {link} \n\nPID: <code>{process.pid}</code>\n\n<b>Stderr:</b> \n<code>{e}</code>\n<b>Output</b>:\n\n <code>{o}</code>"
    await work_in.delete()

    if len(OUTPUT) > MAX_MESSAGE_LENGTH:
        with BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "shell.txt"
            await client.send_document(
                chat_id=message.chat.id,
                document=out_file,
                caption=cmd,
                disable_notification=True,
                reply_to_message_id=reply_to_id,
            )
        await message.delete()
    else:
        await message.reply_text(OUTPUT, disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML, quote=True)

async def upload_document_f(client, message):
    imsegd = await message.reply_text("⚙️ Processing ...")
    if hasattr(message.from_user, 'id'):
        u_id_ = message.from_user.id
    else:
        u_id_ = message.chat.id
    if u_id_ in AUTH_CHANNEL and " " in message.text:
        recvd_command, local_file_name = message.text.split(" ", 1)
        recvd_response = await upload_to_tg(
            imsegd, local_file_name, u_id_, {}, client
        )
        LOGGER.info(recvd_response)
    await imsegd.delete()

async def eval_message_f(client, message):
    if message.chat.type == enums.ChatType.CHANNEL:
        if message.chat.id not in AUTH_CHANNEL:
            return
    elif message.chat.type == enums.ChatType.SUPERGROUP:
        if hasattr(message.from_user, 'id') and message.from_user.id not in AUTH_CHANNEL:
            return
        elif message.chat.id not in AUTH_CHANNEL:
            return
    status_message = await message.reply_text("Processing ...")
    cmd = message.text.split(" ", maxsplit=1)[1]

    reply_to_id = message.id
    if message.reply_to_message:
        reply_to_id = message.reply_to_message.id

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    final_output = f"<b>EVAL</b>: <code>{cmd}</code>\n\n<b>OUTPUT</b>:\n<code>{evaluation.strip()}</code> \n"


    if len(final_output) > MAX_MESSAGE_LENGTH:
        with open("eval.text", "w+", encoding="utf8") as out_file:
            out_file.write(final_output)
        await message.reply_document(
            document="eval.text",
            caption=cmd,
            disable_notification=True,
            reply_to_message_id=reply_to_id,
        )
        oremove("eval.text")
        await status_message.delete()
    else:
        await status_message.edit(final_output)


async def aexec(code, client, message):
    exec((
            "async def __aexec(client, message): "
            + "".join(f"\n {l}" for l in code.split("\n"))
    ))

    return await locals()["__aexec"](client, message)


def up_time(time_taken):
    hours, _hour = divmod(time_taken, 3600)
    minutes, seconds = divmod(_hour, 60)
    return round(hours), round(minutes), round(seconds)


async def upload_log_file(client, message):
    ## No Kanged From Anywhere, Programmed By 5MysterySD >>>>>>>>
    logFile = await AdminCheck(client, message.chat.id, message.from_user.id)
    if logFile and opath.exists(LOG_FILE_NAME):
        logFileRead = open(LOG_FILE_NAME, "r")
        LOGGER.info("Generating LOG Display...")
        logFileLines = logFileRead.read().splitlines()
        toDisplay = 0
        toDisplay = min(len(logFileLines), 25)
        startLine = f'Last {toDisplay} Lines : [On Display Telegram LOG]\n\n---------------- START LOG -----------------\n\n'
        endLine = '\n---------------- END LOG -----------------'
        try:
            Loglines = ''.join(logFileLines[-l]+'\n\n' for l in range (toDisplay, 0, -1))
            Loglines = Loglines.replace('"', '')
            textLog = startLine+Loglines+endLine
            await message.reply_text(textLog,
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.DISABLED #tg Sucks
            )
        except Exception as err:
            LOGGER.info(f"Error Log Display : {err}")
            LOGGER.info(textLog)
        h, m, s = up_time(time() - BOT_START_TIME)
        await message.reply_document(LOG_FILE_NAME, caption=f"**Full Log**\n\n**Bot Uptime:** `{h}h, {m}m, {s}s`")
