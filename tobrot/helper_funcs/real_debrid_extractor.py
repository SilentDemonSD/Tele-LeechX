#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Shrimadhav U K
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/SilentDemonSD/Tele-LeechX >
# All Right Reserved


import aiohttp
from tobrot import REAL_DEBRID_KEY, LOGGER


BASE_URL = "https://api.real-debrid.com/rest/1.0"


async def fetch(session, url, data):
    async with session.post(url, data=data) as response:
        return await response.json()


async def extract_it(restricted_link, custom_file_name):
    async with aiohttp.ClientSession() as session:
        url_to_send = f"{BASE_URL}/unrestrict/link?auth_token={REAL_DEBRID_KEY}"
        to_send_data = {"link": restricted_link}
        html = await fetch(session, url_to_send, to_send_data)
        LOGGER.info(html)
        downloadable_url = html.get("download")
        original_file_name = custom_file_name
        if original_file_name is None:
            original_file_name = html.get("filename")
        return downloadable_url, original_file_name
