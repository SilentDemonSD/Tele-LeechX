#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @MysterySD (https://github.com/code-rgb/USERGE-X/issues/9)
# Copyright (C) 2020 BY - GitHub.com/code-rgb [TG - @deleteduser420]
# Taken From Slam-mirrorbot !! Added Direct Link Code by 5MysterySD
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved

import os
import datetime

from urllib.parse import unquote
from html_telegraph_poster import TelegraphPoster
from telegraph import Telegraph
from pyrogram import enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tobrot import UPDATES_CHANNEL, TGH_AUTHOR, TGH_AUTHOR_URL, LOGGER
from tobrot.plugins import runcmd, getUserOrChaDetails
from tobrot.helper_funcs.display_progress import humanbytes
from tobrot.bot_theme.themes import BotTheme

def post_to_telegraph_html(a_title: str, content: str) -> str:
    """ Create a Telegram Post using HTML Content """
    post_client = TelegraphPoster(use_api=True)
    post_client.create_api_token(TGH_AUTHOR)
    post_page = post_client.post(
        title=a_title,
        author=TGH_AUTHOR,
        author_url=TGH_AUTHOR_URL,
        text=content,
    )
    return post_page["url"]

def post_to_telegraph(title_input: str, body_text: str) -> str:
    """ Create a Telegram Post using Telegraph HTML Content """
    telegraph = Telegraph()
    telegraph.create_account(short_name=TGH_AUTHOR)
    response = telegraph.create_page(
        title=title_input,
        html_content=body_text,
        author_name=TGH_AUTHOR,
        author_url=TGH_AUTHOR_URL
    )
    return response['url']

def safe_filename(path_):
    if path_ is None:
        return
    safename = path_.replace("'", "").replace('"', "")
    if safename != path_:
        os.rename(path_, safename)
    return safename


async def mediainfo(client, message):
    # Generate MediaInfo of Direct Links or Media Type 
    # ToDo : Add File to Direct Link, Getting MediaInfo without download File

    u_id_, _ = getUserOrChaDetails(message)
    reply_to = message.reply_to_message
    link_send = message.text.split(" ")
    x_media = None
    TG_MEDIA = False
    DIRECT_LINK = False
    link = ""
    available_media = (
        "audio",
        "document",
        "photo",
        "sticker",
        "animation",
        "video",
        "voice",
        "video_note",
        "new_chat_photo",
    )

    if len(link_send) > 1:
        link = link_send[1]
        DIRECT_LINK = True
    elif reply_to is not None:
        if reply_to.media:
            for kind in available_media:
                x_media = getattr(reply_to, kind, None)
                if x_media is not None:
                    TG_MEDIA = True
                    break
            if x_media is None:
                await process.edit_text("<b>⚠️Opps⚠️ \n\n<i>⊠ Reply To a Valid Media Format to process.</i></b>")
                return
        else:
            link = reply_to.text
            DIRECT_LINK = True
    else:
        await message.reply_text("`Reply to Telegram Media or Direct Link to Generate MediaInfo !!`", parse_mode=enums.ParseMode.MARKDOWN)
        return
    if link.endswith("/"):
        await message.reply_text("`Send Direct Download Links only to Generate MediaInfo !!`", parse_mode=enums.ParseMode.MARKDOWN)

    process = await message.reply_text("`Gᴇɴᴇʀᴀᴛɪɴɢ ...`")

    if TG_MEDIA:
        media_type = str(type(x_media)).split("'")[1]
        file_path = safe_filename(await reply_to.download())
        output_ = await runcmd(f'mediainfo "{file_path}"')
    elif DIRECT_LINK:
        output_ = await runcmd(f'mediainfo "{link}" --Ssl_IgnoreSecurity')
    out = output_[0] if len(output_) != 0 else None
    if DIRECT_LINK:
        out = out.replace("\n", "<br>")
    if out:
        body_text = f"""
<h2>DETAILS</h2>
<pre>{out}</pre>
"""
    else:
        await process.edit_text("The requested URL was not found on this server. That’s all we know.")
        return
    title = unquote(link.split('/')[-1]) if DIRECT_LINK else "FX Mediainfo"
    tgh_link = post_to_telegraph_html(title, body_text)

    if TG_MEDIA:
        text_ = str(media_type.split(".")[-1])
        textup = ((BotTheme(u_id_)).MEDIAINFO_MEDIA_MSG).format(
            filename = x_media.file_name,
            mimetype = x_media.mime_type,
            filesize = humanbytes(x_media.file_size),
            date = x_media.date,
            fileid = x_media.file_id,
            txt = text_,
            UPDATES_CHANNEL = UPDATES_CHANNEL
        )
    elif DIRECT_LINK:
        textup = ((BotTheme(u_id_)).MEDIAINFO_DIRECT_MSG).format(
            tit = title,
            link = link,
            UPDATES_CHANNEL = UPDATES_CHANNEL
        )
    markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="Mᴇᴅɪᴀ Iɴғᴏ", url=tgh_link)]])
    await process.delete()
    await message.reply_text(text=textup, reply_markup=markup)
