#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) YashDK [TorToolKit] | 5MysterySD | Other Contributors 
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved


from speedtest import Speedtest
from pyrogram import enums

from tobrot import LOGGER
from tobrot.bot_theme.themes import BotTheme
from tobrot.plugins import getUserOrChaDetails
from tobrot.helper_funcs.display_progress import humanbytes

async def get_speed(self, message):
    imspd = await message.reply("`Running Speed Test...`")
    user_id, _ = getUserOrChaDetails(message)
    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()
    path = (result['share'])
    string_speed = ((BotTheme(user_id)).SPEEDTEST_MSG).format(
        upload = humanbytes(result['upload'] / 8),
        download = humanbytes(result['download'] / 8),
        ping = result['ping'],
        timestamp = result['timestamp'],
        bytes_sent = humanbytes(result['bytes_sent']),
        bytes_received = humanbytes(result['bytes_received']),
        name = result['server']['name'],
        country = result['server']['country'],
        cc = result['server']['cc'],
        sponsor = result['server']['sponsor'],
        latency = result['server']['latency'],
        serverlat = result['server']['lat'],
        serverlon = result['server']['lon'],
        ip = result['client']['ip'],
        clientlat = result['client']['lat'],
        clientlon = result['client']['lon'],
        clicountry = result['client']['country'],
        isp = result['client']['isp'],
        isprating = result['client']['isprating']
    )
    await imspd.delete()
    try:
        await message.reply_photo(path, caption=string_speed, parse_mode=enums.ParseMode.HTML)
    except:
        await message.reply(string_speed, parse_mode=enums.ParseMode.HTML)
    LOGGER.info(f'Server Speed result:-\nDL: {humanbytes(result["download"] / 8)}/s UL: {humanbytes(result["upload"] / 8)}/s')
