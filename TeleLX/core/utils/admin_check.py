#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52 | MaxxRider | SilentDemonSD | Other Contributors 
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/SilentDemonSD/Tele-LeechX >
# All Right Reserved

from pyrogram import enums
from TeleLX import AUTH_CHATS

async def AdminCheck(client, chat_id, user_id):
    chat = await client.get_chat(chat_id)
    if chat.type == enums.ChatType.PRIVATE and chat_id in AUTH_CHATS:
        return True
    SELF = await client.get_chat_member(chat_id=chat_id, user_id=user_id)
    if SELF.status not in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
        return False
    return True
