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

from random import choice

from TeleLX import BOT_THEME, USER_THEMES, LOGGER
from TeleLX.core.bot_themes import fx_optimised, fx_minimal

AVAILABLE_THEMES = {'fx-optimised-theme': fx_optimised, 'fx-minimal-theme': fx_minimal}

def BotTheme(user_id_):
    theme = USER_THEMES.get(str(user_id_), BOT_THEME)

    if theme in AVAILABLE_THEMES.keys():
        return AVAILABLE_THEMES[theme].TXStyle()

    if theme == "fx-random-theme":
        random_theme = choice(list(AVAILABLE_THEMES.values()))
        LOGGER.info(f"Random Theme Chosen: {random_theme}")
        return random_theme.TXStyle()

    return fx_optimised.TXStyle()

