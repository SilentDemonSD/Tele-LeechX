#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) SilentDemonSD | Anasty17 [MLTB]
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/SilentDemonSD/Tele-LeechX >
# All Right Reserved

from asyncio import sleep as asleep
from os import path as opath, remove as oremove
from time import time
from telegraph import upload_file
from subprocess import check_output
from psutil import disk_usage, cpu_percent, swap_memory, cpu_count, virtual_memory, net_io_counters, boot_time
from pyrogram import enums, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto, Message

from TeleLX import *
from TeleLX.helper_funcs.display_progress import format_bytes, format_time
from TeleLX.core.bot_themes.themes import BotTheme
from TeleLX.helper_funcs.bot_commands import BotCommands
from TeleLX.plugins import getUserOrChaDetails, progressBar

TGH_LIMIT = 5242880*2

async def stats(client: Client, message: Message):
    user_id, _ = getUserOrChaDetails(message)
    stats = (BotTheme(user_id)).STATS_MSG_1
    if opath.exists('.git'):
        last_commit = check_output(["git log -1 --date=format:'%I:%M:%S %p %d %B, %Y' --pretty=format:'%cr ( %cd )'"], shell=True).decode()
    else:
        LOGGER.info("Stats : No UPSTREAM_REPO")
        last_commit = ''
    if last_commit:
        stats += ((BotTheme(user_id)).STATS_MSG_2).format(
        lc = last_commit
    )
    currentTime = format_time((time() - BOT_START_TIME)*1000)
    osUptime = format_time((time() - boot_time())*1000)
    total, used, free, disk= disk_usage('/')
    disk_prog = progressBar(disk)
    total = format_bytes(total)
    used = format_bytes(used)
    free = format_bytes(free)
    sent = format_bytes(net_io_counters().bytes_sent)
    recv = format_bytes(net_io_counters().bytes_recv)
    cpuUsage = cpu_percent(interval=0.5)
    cpu_prog = progressBar(cpuUsage)
    p_core = cpu_count(logical=False)
    t_core = cpu_count(logical=True)
    core_per = int(p_core)/int(t_core) * 100
    core_prog = progressBar(core_per)
    swap = swap_memory()
    swap_p = swap.percent
    swap_prog = progressBar(swap_p)
    swap_t = format_bytes(swap.total)
    swap_u = format_bytes(swap.used)
    swap_f = format_bytes(swap.free)
    memory = virtual_memory()
    mem_p = memory.percent
    mem_prog = progressBar(mem_p)
    mem_t = format_bytes(memory.total)
    mem_a = format_bytes(memory.available)
    mem_u = format_bytes(memory.used)
    UP_CHANNEL = UPDATES_CHANNEL
    stats += ((BotTheme(user_id)).STATS_MSG_3).format(**locals())
    await message.reply_text(text = stats,
        parse_mode = enums.ParseMode.HTML,
        disable_web_page_preview=True
    )

async def help_message_f(client: Client, message: Message):
    user_id, _ = getUserOrChaDetails(message)
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🆘️ Open Help 🆘️", callback_data = "openHelp_pg1")]]
    )
    await message.reply_text(
        text = ((BotTheme(user_id)).HELP_MSG).format(
        UPDATES_CHANNEL = UPDATES_CHANNEL
    ),
        reply_markup = reply_markup,
        parse_mode = enums.ParseMode.HTML,
        disable_web_page_preview=True
    )

async def picture_add(client: Client, message: Message):
    '''/addpic command'''
    editable = await message.reply_text("Checking Input ...", quote=True)
    resm = message.reply_to_message
    if resm.text:
        msg_text = resm.text
        if msg_text.startswith("http"):
            pic_add = msg_text.strip()
            await editable.edit("Adding your Link ...")
    elif resm.photo:
        if not resm.photo and resm.photo.file_size <= TGH_LIMIT:
            await editable.edit("This Media is Not Supported! Only Send Photos !!")
            return
        await editable.edit("Uploading to te.legra.ph Server ...")
        df = await client.download_media(
            message=resm,
            file_name=f'{DL_DIR}/thumbnails/'
        )
        await editable.edit("`Uploading to te.legra.ph Server, Please Wait...`")
        try:
            tgh_post = upload_file(df)
            pic_add = f'https://te.legra.ph{tgh_post[0]}'
        except Exception as err:
            await editable.edit(err)
        finally:
            oremove(df)
    else:
        await editable.edit("Reply to Any Valid Photo!! Or Provide Direct DL Links of Images.")
        return
    PICS_LIST.append(pic_add)
    asleep(1.5)
    await editable.edit("<b><i>Added to Existing Random Pictures Status List!</i></b>")

async def pictures(client: Client, message: Message):
    '''/pics command'''
    if not PICS_LIST:
        await message.reply_text("Add Some Photos OR use API to Let me Show you !!")
    else:
        to_edit = await message.reply_text("Generating Grid of your Images...")
        btn = [
            [InlineKeyboardButton("<<", callback_data=f"pic -1"),
            InlineKeyboardButton(">>", callback_data="pic 1")],
            [InlineKeyboardButton("Remove Photo", callback_data="picsremove 0")]
        ]
        await to_edit.delete()
        await message.reply_photo(photo=PICS_LIST[0], caption=f'• Picture No. : 1 / {len(PICS_LIST)}', reply_markup=InlineKeyboardMarkup(btn))

async def pics_callback(client: Client, query: CallbackQuery):
    if query.data.startswith("pic"):
        if query.data.startswith("picsremove"):
            getData = (query.data).split()
            index = int(getData[1])
            PICS_LIST.pop(index)
            await query.edit_message_media(media=InputMediaPhoto(media="https://te.legra.ph/file/06dbd8fb0628b8ba4ab45.png", caption="Removed from Existing Random Pictures Status List !!"))
            return
        getData = (query.data).split()
        ind = int(getData[1])
        no = len(PICS_LIST) - abs(ind+1) if ind < 0 else ind + 1
        pic_info = f'🌄 <b>Picture No. : {no} / {len(PICS_LIST)}</b>'
        btns = [
            [InlineKeyboardButton("<<", callback_data=f"pic {ind-1}"),
            InlineKeyboardButton(">>", callback_data=f"pic {ind+1}")],
            [InlineKeyboardButton("Remove Photo", callback_data=f"picsremove {ind}")]
        ]
        await query.edit_message_media(media=InputMediaPhoto(media=PICS_LIST[ind], caption=pic_info), reply_markup=InlineKeyboardMarkup(btns))
    await query.answer()
