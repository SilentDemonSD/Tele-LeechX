#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Shrimadhav U K | 5MysterySD | Other Contributors 
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved


import aiohttp
from pyrogram import enums
from pyrogram.types import MessageEntity
from tobrot import TG_OFFENSIVE_API, LOGGER

def extract_url_from_entity(entities: MessageEntity, text: str):
    url = None
    for entity in entities:
        if entity.type == enums.MessageEntityType.TEXT_LINK:
            url = entity.url
        elif entity.type == enums.MessageEntityType.URL:
            o = entity.offset
            l = entity.length
            url = text[o : o+l]
        elif entity.type == enums.MessageEntityType.BOT_COMMAND:
            url = text
    return url


async def extract_link(message, type_o_request):
    custom_file_name = None
    url = None
    youtube_dl_username = None
    youtube_dl_password = None

    if message.text is not None:
        LOGGER.info("Extracting Link from Message !!")
        if message.text.lower().startswith("magnet:"):
            url = message.text.strip()

        elif "|" in message.text:
            url_parts = message.text.split("|")
            if len(url_parts) == 2:
                url = url_parts[0]
                custom_file_name = url_parts[1]
            elif len(url_parts) == 4:
                url = url_parts[0]
                custom_file_name = url_parts[1]
                youtube_dl_username = url_parts[2]
                youtube_dl_password = url_parts[3]
        elif message.entities is not None:
            url = extract_url_from_entity(message.entities, message.text)

        else:
            url = message.text.strip()

    elif message.document is not None:
        if message.document.file_name.lower().endswith(".torrent"):
            url = await message.download()
            custom_file_name = message.caption

    elif message.caption is not None:
        if "|" in message.caption:
            url_parts = message.caption.split("|")
            if len(url_parts) == 2:
                url = url_parts[0]
                custom_file_name = url_parts[1]
            elif len(url_parts) == 4:
                url = url_parts[0]
                custom_file_name = url_parts[1]
                youtube_dl_username = url_parts[2]
                youtube_dl_password = url_parts[3]

        elif message.caption_entities is not None:
            url = extract_url_from_entity(message.caption_entities, message.caption)
        else:
            url = message.caption.strip()
    elif message.entities is not None:
        url = message.text
    else:
        url = None
        custom_file_name = None
        LOGGER.warning("Can't Extract Link from Message ! Exiting !")

    if url is not None:
        url = url.strip()
    if custom_file_name is not None:
        custom_file_name = custom_file_name.strip()
    if youtube_dl_username is not None:
        youtube_dl_username = youtube_dl_username.strip()
    if youtube_dl_password is not None:
        youtube_dl_password = youtube_dl_password.strip()

    LOGGER.info(f"TG_OFFENSIVE_API : {TG_OFFENSIVE_API}")
    if TG_OFFENSIVE_API is not None:
        try:
            async with aiohttp.ClientSession() as session:
                api_url = TG_OFFENSIVE_API.format(
                    i=url, m=custom_file_name, t=type_o_request
                )
                LOGGER.info(api_url)
                async with session.get(api_url) as resp:
                    suats = int(resp.status)
                    err = await resp.text()
                    if suats != 200:
                        url = None
                        custom_file_name = err
        except:
            pass

    return url, custom_file_name, youtube_dl_username, youtube_dl_password
