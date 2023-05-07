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

import aiohttp
from TeleLX import REAL_DEBRID_KEY, LOGGER

BASE_URL = "https://api.real-debrid.com/rest/1.0"


async def fetch(session, url, data):
    async with session.post(url, data=data) as response:
        return await response.json()


async def extract_it(restricted_link, custom_file_name):
    async with aiohttp.ClientSession() as session:
        url_to_send = f"{BASE_URL}/unrestrict/link?auth_token={REAL_DEBRID_KEY}"
        to_send_data = {"link": restricted_link}
        async with session.post(url_to_send, data=to_send_data) as response:
            json_data = await response.json()
            LOGGER.info(json_data)
            downloadable_url = json_data.get("download")
            original_file_name = custom_file_name or json_data.get("filename")
            return downloadable_url, original_file_name
