#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AnyDLBot | Other Contributors 
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/SilentDemonSD/Tele-LeechX >
# All Right Reserved


import os

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from TeleLX import DL_DIR, DB_URI, LOGGER
from TeleLX.database.db_func import DatabaseManager
from TeleLX.core.bot_themes.themes import BotTheme
from TeleLX.plugins import getUserOrChaDetails

async def save_thumb_nail(client, message):
    uid, _ = getUserOrChaDetails(message)
    thumbnail_location = os.path.join(DL_DIR, "thumbnails")
    thumb_image_path = os.path.join(thumbnail_location, f"{str(uid)}.jpg")
    ismgs = await message.reply_text((BotTheme(uid)).THUMB_REPLY)
    if message.reply_to_message is not None:
        if not os.path.isdir(thumbnail_location):
            os.makedirs(thumbnail_location)
        DL_DIR = f"{thumbnail_location}/"
        downloaded_file_name = await client.download_media(
            message=message.reply_to_message, file_name=DL_DIR
        )
        Image.open(downloaded_file_name).convert("RGB").save(downloaded_file_name)
        metadata = extractMetadata(createParser(downloaded_file_name))
        height = metadata.get("height") if metadata.has("height") else 0
        img = Image.open(downloaded_file_name)
        img.resize((320, height))
        img.save(thumb_image_path, "JPEG")
        os.remove(downloaded_file_name)
        if DB_URI is not None:
            DatabaseManager().user_save_thumb(uid, thumb_image_path)
            LOGGER.info("[DB] User Thumbnail Saved in Database")
        await ismgs.edit((BotTheme(uid)).SAVE_THUMB_MSG)
    else:
        await ismgs.edit((BotTheme(uid)).SAVE_THUMB_FAIL_MSG)

async def clear_thumb_nail(client, message):
    uid, _ = getUserOrChaDetails(message)
    thumbnail_location = os.path.join(DL_DIR, "thumbnails")
    thumb_image_path = os.path.join(thumbnail_location, f"{str(uid)}.jpg")
    ismgs = await message.reply_text((BotTheme(uid)).THUMB_REPLY)
    if os.path.exists(thumb_image_path):
        os.remove(thumb_image_path)
        if DB_URI is not None:
            DatabaseManager().user_rm_thumb(uid, thumb_image_path)
            LOGGER.info("[DB] User Thumbnail Removed from Database")
        await ismgs.edit((BotTheme(uid)).CLEAR_THUMB_SUCC_MSG)
    else:
        await ismgs.edit((BotTheme(uid)).CLEAR_THUMB_FAIL_MSG)
