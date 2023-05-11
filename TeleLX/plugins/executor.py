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

async def exec_message_f(client, message):
    if message.chat.type == enums.ChatType.CHANNEL:
        if message.chat.id not in AUTH_CHATS:
            return
    elif message.chat.type == enums.ChatType.SUPERGROUP:
        if hasattr(message.from_user, 'id') and message.from_user.id not in AUTH_CHATS:
            return
        if message.chat.id not in AUTH_CHATS:
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
    if u_id_ in AUTH_CHATS and " " in message.text:
        recvd_command, local_file_name = message.text.split(" ", 1)
        recvd_response = await upload_to_tg(imsegd, local_file_name, u_id_, {}, client)
        LOGGER.info(recvd_response)
    await imsegd.delete()

async def eval_message_f(client, message):
    if message.chat.type == enums.ChatType.CHANNEL and message.chat.id not in AUTH_CHATS:
        return
    elif message.chat.type == enums.ChatType.SUPERGROUP:
        if hasattr(message.from_user, 'id') and message.from_user.id not in AUTH_CHATS:
            return
        if message.chat.id not in AUTH_CHATS:
            return

    status_message = await message.reply_text("Processing ...")
    cmd = message.text.split(" ", maxsplit=1)[1]

    reply_to_id = message.id
    if message.reply_to_message:
        reply_to_id = message.reply_to_message.id

    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()

    stdout, exc = None, None

    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = format_exc()

    stdout = redirected_output.getvalue()
    sys.stdout = old_stdout

    evaluation = exc or stdout or "Success"
    evaluation = evaluation.strip()

    final_output = f"<b>EVAL</b>: <code>{cmd}</code>\n\n<b>OUTPUT</b>:\n<code>{evaluation}</code>\n"

    if len(final_output) > MAX_MESSAGE_LENGTH:
        with open("eval.txt", "w", encoding="utf-8") as file:
            file.write(final_output)
        await message.reply_document(
            document="eval.txt",
            caption=cmd,
            disable_notification=True,
            reply_to_message_id=reply_to_id
        )
        os.remove("eval.txt")
        await status_message.delete()
    else:
        await status_message.edit(final_output)


async def aexec(code, client, message):
    exec(f"async def __aexec(client, message):\n    {code}")
    return await locals()["__aexec"](client, message)