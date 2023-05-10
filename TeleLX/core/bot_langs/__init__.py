#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of Tele-LeechX: https://github.com/SilentDemonSD/Tele-LeechX
# Copyright (c) 2022-2023 SilentDemonSD.
# All rights reserved.

"""
This script is a part of the Tele-LeechX project, a Telegram bot based on Pyrogram Framework and 
extra leeching utilities. Its purpose is to allow users to easily download and save media files 
in Telegram chats and channels.
"""

from TeleLX import LOGGER
from TeleLX.core.bot_langs import en, bn

AVAILABLE_LANG = {'english': en, 'bengali': bn}
BOT_LANG = "English"

def BotLang():

    if BOT_LANG.lower() in AVAILABLE_LANG.keys():
        return (AVAILABLE_LANG.get(BOT_LANG)).TXLanguage()
    
    return en.TXLanguage()
