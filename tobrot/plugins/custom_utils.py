#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) 5MysterySD
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved

from re import split as rsplit
from pyrogram import enums, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from tobrot import LOGGER, DB_URI, PRE_DICT, CAP_DICT, IMDB_TEMPLATE, ANILIST_TEMPLATE, USER_LOGS
from tobrot.database.db_func import DatabaseManager
from tobrot.bot_theme.themes import BotTheme
from tobrot.plugins import getUserOrChaDetails

async def prefix_set(client, message):
    '''/setpre command '''
    lm = await message.reply_text("`Setting Up ...`")
    user_id_, u_men = getUserOrChaDetails(message)
    pre_send = message.text.split(" ", maxsplit=1)
    reply_to = message.reply_to_message
    if len(pre_send) > 1:
        txt = pre_send[1]
    elif reply_to is not None:
        txt = reply_to.text
    else:
        txt = ""
    prefix_ = txt
    if prefix_ != '':
        prefix_ = rsplit(r'c:|s:|no:|\|', prefix_)[0].strip()

    preCus = txt.split('c: ')
    if len(preCus) > 1:
        preCus = preCus[1]
        fname = preCus.split('s:')[0].strip()
    else:
        fname = ""
    preSuf = txt.split('s: ')
    if len(preSuf) > 1:
        preSuf = preSuf[1]
        suffix = preSuf.split('no:')[0]
    else:
        suffix = ""
    preNo = txt.split('no: ')
    if len(preNo) > 1:
        preNo = preNo[1]
        no = preNo.split('|', 1)[0].strip()
    else:
        no = '0'
    preRep = txt.split('|', 1)
    args = preRep[1] if len(preRep) > 1 else ""
    tData = [prefix_, fname, suffix, no, args]
    PRE_DICT[user_id_] = tData
    if DB_URI:
        DatabaseManager().user_pre(user_id_, tData)
        LOGGER.info(f"[DB] User : {user_id_} Prefix Saved to Database")

    pre_text = await lm.edit_text(((BotTheme(user_id_)).PREFIX_MSG).format(
            u_men = u_men,
            uid = user_id_,
            t = txt
        ), 
        parse_mode=enums.ParseMode.HTML
    )
    

async def caption_set(client, message):
    '''  /setcap command '''

    lk = await message.reply_text("`Setting Up ...`")
    user_id_, u_men = getUserOrChaDetails(message)
    cap_send = message.text.split(" ", maxsplit=1)
    reply_to = message.reply_to_message
    if len(cap_send) > 1:
        txt = cap_send[1]
    elif reply_to is not None:
        txt = reply_to.text
    else:
        txt = ""
    caption_ = txt
    CAP_DICT[user_id_] = caption_
    if DB_URI:
        DatabaseManager().user_cap(user_id_, caption_)
        LOGGER.info(f"[DB] User : {user_id_} Caption Saved to Database")
    try:
        txx = txt.split("#", maxsplit=1)
        txt = txx[0]
    except:
        pass 
    cap_text = await lk.edit_text(((BotTheme(user_id_)).CAPTION_MSG).format(
            u_men = u_men,
            uid = user_id_,
            t = txt
        ),
        parse_mode=enums.ParseMode.HTML
    )


async def template_set(client, message):
    '''  /set_template command '''
    lm = await message.reply_text(
        text="`Checking Input ...`",
    )
    user_id_, u_men = getUserOrChaDetails(message)
    tem_send = message.text.split(" ", maxsplit=1)
    reply_to = message.reply_to_message
    if len(tem_send) > 1:
        txt = tem_send[1]
    elif reply_to is not None:
        txt = reply_to.text
    else:
        txt = ""
    template_ = txt
    IMDB_TEMPLATE[user_id_] = template_
    if DB_URI:
        DatabaseManager().user_imdb(user_id_, template_)
        LOGGER.info(f"[DB] User : {user_id_} IMDB Template Saved to Database")
    await lm.edit_text(((BotTheme(user_id_)).IMDB_MSG).format(
            u_men = u_men,
            uid = user_id_,
            t = txt
        ),
        parse_mode=enums.ParseMode.HTML
    )

async def anilist_set(client, message):
    '''  /anime_template command '''
    lm = await message.reply_text("`Checking HTML Input ...`")
    user_id_, u_men = getUserOrChaDetails(message)
    tem_send = message.text.split(" ", 1)
    reply_to = message.reply_to_message
    if len(tem_send) > 1:
        txt = tem_send[1]
    elif reply_to is not None:
        txt = reply_to.text
    else:
        txt = ""
    ani_template_ = txt
    ANILIST_TEMPLATE[user_id_] = ani_template_
    #if DB_URI:
    #    DatabaseManager().user_anilist(user_id_, ani_template_)
    #    LOGGER.info(f"[DB] User : {user_id_} AniList Anime Template Saved to Database")
    await lm.edit_text(((BotTheme(user_id_)).IMDB_MSG).format(
            u_men = u_men,
            uid = user_id_,
            t = txt
        ),
        parse_mode=enums.ParseMode.HTML
    )

async def theme_set(client, message):
    '''  /choosetheme command '''
    lk = await message.reply_text(
        text="`Fetching Current Themes ...`",
    )
    user_id_, u_men = getUserOrChaDetails(message)

    theme_btn = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "fx-optimised-theme",
                    callback_data=f"theme {user_id_} fx-optimised-theme",
                )
            ],
            [
                InlineKeyboardButton(
                    "fx-minimal-theme",
                    callback_data=f"theme {user_id_} fx-minimal-theme",
                )
            ],
            [
                InlineKeyboardButton(
                    "fx-random-theme",
                    callback_data=f"theme {user_id_} fx-random-theme",
                )
            ],
            [InlineKeyboardButton("⛔️ Close ⛔️", callback_data="close")],
        ]
    )
    await lk.edit_text(((BotTheme(user_id_)).THEME_MSG).format(
            u_men = u_men,
            uid = user_id_
        ),
        parse_mode=enums.ParseMode.HTML, 
        reply_markup=theme_btn
    )

async def user_log_set(client: Client, message: Message):
    '''  /userlog command '''
    lm = await message.reply_text("`Checking Log Channel ID...`")
    user_id_, u_men = getUserOrChaDetails(message)
    tem_send = message.text.split(" ", 1)
    reply_to = message.reply_to_message
    if len(tem_send) > 1:
        id = tem_send[1]
    elif reply_to is not None:
        id = reply_to.text
    else:
        await lm.edit_text("<i>Give Channel ID Along /userlog -100xxxxxxxx</i>")
        return
    if not id.startswith('-100'):
        await lm.edit_text("<i><b>Your Channel ID Should Start with</b> -100xxxxxxxx, <u>Retry Again</u> !!</i>")
        return
    user_log_ = int(id.strip())
    try:
        await lm.edit_text("<i>Checking Your Channel Interaction ...</i>")
        await client.send_message(user_log_, text=f'''<b>ᑌՏᗴᖇ ᒪOᘜ ᑕᕼᗩᑎᑎᗴᒪ :</b>
┃
┣ 🆔 <b>Log Chat ID :</b> <code>{user_log_}</code>
┃
┗ 📂 <i>From Now On, The Bot will Send you Files in this Channel !!</i>''')
    except Exception as err:
        await lm.edit_text(f"<i>Make Sure You have Added the Bot as Admin with Post Permission, Retry Again.</i>\n\nError : {err}")
        return
    USER_LOGS[user_id_] = user_log_
    #if DB_URI:
    #    DatabaseManager().user_log(user_id_, user_log_)
    #    LOGGER.info(f"[DB] User : {user_id_} Log Channel Saved to Database")
    await lm.edit_text(f'''⚡️Custom Log Channel Set Successfully⚡️ 

👤 <b>User :</b> {u_men} ( #ID{user_id_} )
🏷 <b>User Log Channel ID :</b> <code>{user_log_}</code>''',
        parse_mode=enums.ParseMode.HTML
    )

async def log_chat_id(c: Client, m: Message):
    '''  /id command  '''
    await m.reply_text(f"<b>Log Channel ID :</b> <code>{m.chat.id}</code>", quote=True)
