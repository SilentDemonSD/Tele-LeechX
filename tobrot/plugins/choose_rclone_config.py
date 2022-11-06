#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) xiaoqi-beta | gautamajay52 | Other Contributors 
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved

from configparser import ConfigParser

from pyrogram import enums
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from tobrot import LOGGER, OWNER_ID
from tobrot.plugins import getUserOrChaDetails

async def rclone_command_f(client, message):
    # This is code to switch which rclone config section to use. This setting affects the entire bot
    #(And at this time, the cloneHelper only support gdrive, so you should only choose to use gdrive config section)
    """/rclone command"""
    usr_id, _ = getUserOrChaDetails(message)
    LOGGER.info(f"[RCLONE] Init Chat ID : {message.chat.id}, User ID : {usr_id}")
    if usr_id == OWNER_ID and message.chat.type == enums.ChatType.PRIVATE:
        config = ConfigParser()
        config.read("rclone_bak.conf")
        sections = list(config.sections())
        inline_keyboard = []
        for section in sections:
            ikeyboard = [InlineKeyboardButton(
                    section, callback_data=(f"rclone_{section}").encode("UTF-8")
                )]
            inline_keyboard.append(ikeyboard)
        config = ConfigParser()
        config.read("rclone.conf")
        section = config.sections()[0]
        msg_text = f"""Default section of rclone config is: **{section}**\n\n
There are {len(sections)} sections in your rclone.conf file, 
please choose which section you want to use:"""
        ikeyboard = [
            InlineKeyboardButton(
                "‼️ Cancel ‼️", callback_data="rcloneCancel".encode("UTF-8")
            )
        ]

        inline_keyboard.append(ikeyboard)
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        await message.reply_text(text=msg_text, reply_markup=reply_markup)
    else:
        try:
            await message.delete()
        except:
            pass
        LOGGER.warning(f"User ID = {usr_id} have no permission to edit rclone config!")


async def rclone_button_callback(bot, update: CallbackQuery):
    """rclone button callback"""
    if update.data == "rcloneCancel":
        config = ConfigParser()
        config.read("rclone.conf")
        section = config.sections()[0]
        await update.message.edit_text(
            f"Opration canceled! \n\nThe default section of rclone config is: **{section}**"
        )
        LOGGER.info(
            f"Opration canceled! The default section of rclone config is: {section}"
        )
    else:
        section = update.data.split("_", maxsplit=1)[1]
        with open("rclone.conf", "w", newline="\n", encoding="utf-8") as f:
            config = ConfigParser()
            config.read("rclone_bak.conf")
            temp = ConfigParser()
            temp[section] = config[section]
            temp.write(f)
        await update.message.edit_text(
            f"Default rclone config changed to **{section}**"
        )
        LOGGER.info(f"Default rclone config changed to {section}")
