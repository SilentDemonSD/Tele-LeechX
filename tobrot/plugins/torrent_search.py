#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) 5MysterySD | Other Contributors 
# Total Code Kanged from MLTB by Anasty17 
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved

import time
import html
import asyncio
import aiohttp
import feedparser
import itertools
from urllib.parse import quote as urlencode, urlsplit

from pyrogram import filters, emoji, enums
from pyrogram.parser import html as pyrogram_html
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.handlers import MessageHandler, CallbackQueryHandler

from tobrot import app, LOGGER, UPDATES_CHANNEL
from tobrot.helper_funcs.bot_commands import BotCommands

search_lock = asyncio.Lock()
search_info = {False: dict(), True: dict()}

def callback_data(data):
    def func(flt, client, callback_query):
        return callback_query.data in flt.data

    data = data if isinstance(data, list) else [data]
    return filters.create(
        func,
        'CustomCallbackDataFilter',
        data=data
    )

async def return_search(query, page=1, sukebei=False):
    page -= 1
    query = query.lower().strip()
    used_search_info = search_info[sukebei]
    async with search_lock:
        results, get_time = used_search_info.get(query, (None, 0))
        if (time.time() - get_time) > 3600:
            results = []
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://{"sukebei." if sukebei else ""}nyaa.si/?page=rss&q={urlencode(query)}') as resp:
                    d = feedparser.parse(await resp.text())
            text = ''
            a = 0
            parser = pyrogram_html.HTML(None)
            for i in sorted(d['entries'], key=lambda i: int(i['nyaa_seeders']), reverse=True):
                if i['nyaa_size'].startswith('0'):
                    continue
                if not int(i['nyaa_seeders']):
                    break
                link = i['link']
                splitted = urlsplit(link)
                if splitted.scheme == 'magnet' and splitted.query:
                    link = f'<code>{link}</code>'
                newtext = f'''<b>{a + 1}.</b> <code>{html.escape(i["title"])}</code>
<b>Link:</b> <code>{link}</code>
<b>Size:</b> <code>{i["nyaa_size"]}</code>
<b>Seeders:</b> <code>{i["nyaa_seeders"]}</code>
<b>Leechers:</b> <code>{i["nyaa_leechers"]}</code>
<b>Category:</b> <code>{i["nyaa_category"]}</code>\n\n'''
                futtext = text + newtext
                if (a and not a % 10) or len((await parser.parse(futtext))['message']) > 4096:
                    results.append(text)
                    futtext = newtext
                text = futtext
                a += 1
            results.append(text)
        ttl = time.time()
        used_search_info[query] = results, ttl
        try:
            return results[page], len(results), ttl
        except IndexError:
            return '', len(results), ttl

message_info = dict()
ignore = set()

async def nyaa_search(client, message):
    text = message.text.split(' ')
    text.pop(0)
    query = ' '.join(text)
    await init_search(client, message, query, False)

async def nyaa_search_sukebei(client, message):
    text = message.text.split(' ')
    text.pop(0)
    query = ' '.join(text)
    await init_search(client, message, query, True)

async def init_search(client, message, query, sukebei):
    result, pages, ttl = await return_search(query, sukebei=sukebei)
    if not result:
        await message.reply_text('No results found')
    else:
        buttons = [InlineKeyboardButton(f'1/{pages}', 'nyaa_nop'), InlineKeyboardButton(f'Next', 'nyaa_next')]
        if pages == 1:
            buttons.pop()
        reply = await message.reply_text(result, reply_markup=InlineKeyboardMarkup([
            buttons 
        ]))
        message_info[(reply.chat.id, reply.id)] = message.from_user.id, ttl, query, 1, pages, sukebei

async def nyaa_nop(client, callback_query):
    await callback_query.answer(cache_time=3600)

callback_lock = asyncio.Lock()
async def nyaa_callback(client, callback_query):
    message = callback_query.message
    message_identifier = (message.chat.id, message.id)
    data = callback_query.data
    async with callback_lock:
        if message_identifier in ignore:
            await callback_query.answer()
            return
        user_id, ttl, query, current_page, pages, sukebei = message_info.get(message_identifier, (None, 0, None, 0, 0, None))
        og_current_page = current_page
        if data == 'nyaa_back':
            current_page -= 1
        elif data == 'nyaa_next':
            current_page += 1
        if current_page < 1:
            current_page = 1
        elif current_page > pages:
            current_page = pages
        ttl_ended = (time.time() - ttl) > 3600
        if ttl_ended:
            text = getattr(message.text, 'html', 'Search expired')
        else:
            if callback_query.from_user.id != user_id:
                await callback_query.answer('...no', cache_time=3600)
                return
            text, pages, ttl = await return_search(query, current_page, sukebei)
        buttons = [InlineKeyboardButton(f'Prev', 'nyaa_back'), InlineKeyboardButton(f'{current_page}/{pages}', 'nyaa_nop'), InlineKeyboardButton(f'Next', 'nyaa_next')]
        if ttl_ended:
            buttons = [InlineKeyboardButton('Search Expired', 'nyaa_nop')]
        else:
            if current_page == 1:
                buttons.pop(0)
            if current_page == pages:
                buttons.pop()
        if ttl_ended or current_page != og_current_page:
            await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([
                buttons
            ]))
        message_info[message_identifier] = user_id, ttl, query, current_page, pages, sukebei
        if ttl_ended:
            ignore.add(message_identifier)
    await callback_query.answer()

# Using upstream API based on: https://github.com/Ryuk-me/Torrents-Api
# Implemented by https://github.com/jusidama18

class TorrentSearch:
    index = 0
    query = None
    message = None
    response = None
    response_range = None

    RESULT_LIMIT = 4
    RESULT_STR = None

    def __init__(self, command: str, source: str, result_str: str):
        self.command = command
        self.source = source.rstrip('/')
        self.RESULT_STR = result_str
        
    @staticmethod
    def format_magnet(string: str):
        if not string:
            return ""
        return string.split('&tr', 1)[0]

    def get_formatted_string(self, values):
        string = self.RESULT_STR.format(**values)
        extra = ""
        if "Files" in values:
            tmp_str = "❂[{Quality} - {Type} ({Size})]({Torrent}): `{magnet}`"
            extra += "\n".join(
                tmp_str.format(**f, magnet=self.format_magnet(f['Magnet']))
                for f in values['Files']
            )
        else:
            magnet = values.get('magnet', values.get('Magnet'))  # Avoid updating source dict
            if magnet:
                extra += f"⚡Magnet: `{self.format_magnet(magnet)}`"
        if (extra):
            string += "\n" + extra
        return string

    async def update_message(self):
        prevBtn = InlineKeyboardButton(f"Prev", callback_data=f"{self.command}_previous")
        delBtn = InlineKeyboardButton(f"{emoji.CROSS_MARK}", callback_data=f"{self.command}_delete")
        nextBtn = InlineKeyboardButton(f"Next", callback_data=f"{self.command}_next")

        inline = []
        if (self.index != 0):
            inline.append(prevBtn)
        inline.append(delBtn)
        if (self.index != len(self.response_range) - 1):
            inline.append(nextBtn)

        res_lim = min(self.RESULT_LIMIT, len(self.response) - self.RESULT_LIMIT*self.index)
        result = f"**Page - {self.index+1}**\n\n"
        result += "\n\n━━━━━━━✦✗✦━━━━━━━━\n\n".join(
            self.get_formatted_string(self.response[self.response_range[self.index]+i])
            for i in range(res_lim)
        )

        await self.message.edit(
            result,
            reply_markup=InlineKeyboardMarkup([inline]),
            parse_mode=enums.ParseMode.MARKDOWN,
        )

    async def find(self, client, message):
        if len(message.command) < 2:
            await message.reply_text(f"Usage: /{self.command} query")
            return

        query = urlencode(message.text.split(None, 1)[1])
        self.message = await message.reply_text("Searching")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.source}/{query}", timeout=15) as resp:
                    if (resp.status != 200):
                        raise Exception('unsuccessful request')
                    result = await resp.json()
                    if (result and isinstance(result[0], list)):
                        result = list(itertools.chain(*result))
                    self.response = result
                    self.response_range = range(0, len(self.response), self.RESULT_LIMIT)
        except:
            await self.message.edit("No Results Found.")
            return
        await self.update_message()

    async def delete(self, client, message):
        index = 0
        query = None
        message = None
        response = None
        response_range = None
        await self.message.delete()

    async def previous(self, client, message):
        self.index -= 1
        await self.update_message()

    async def next(self, client, message):
        self.index += 1
        await self.update_message()

RESULT_STR_1337 = (
    "✘ Name: `{Name}`\n"
    "✘ Size: {Size}\n"
    "✘ Seeders: {Seeders} ✘ Leechers: {Leechers}"
)
RESULT_STR_PIRATEBAY = (
    "➲ Name: `{Name}`\n"
    "➲ Size: {Size}\n"
    "➲ Seeders: {Seeders} ➲ Leechers: {Leechers}"
)
RESULT_STR_TGX = (
    "⇒ Name: `{Name}`\n" 
    "⇒ Size: {Size}\n"
    "⇒ Seeders: {Seeders} ⇒ Leechers: {Leechers}"
)
RESULT_STR_YTS = (
    "❂ Name: `{Name}`\n"
    "❂ Released on: {ReleasedDate}\n"
    "❂ Genre: {Genre}\n"
    "❂ Rating: {Rating}\n"
    "❂ Likes: {Likes}\n"
    "❂ Duration: {Runtime}\n"
    "❂ Language: {Language}"
)
RESULT_STR_EZTV = (
    "★ Name: `{Name}`\n"
    "★ Size: {Size}\n"
    "★ Seeders: {Seeders}"
)
RESULT_STR_TORLOCK = (
    "✿ Name: `{Name}`\n"
    "✿ Size: {Size}\n"
    "✿ Seeders: {Seeders} ✿ Leechers: {Leechers}"
)
RESULT_STR_RARBG = (
    "⊗ Name: `{Name}`\n"
    "⊗ Size: {Size}\n"
    "⊗ Seeders: {Seeders} ⊗ Leechers: {Leechers}"
)
RESULT_STR_ALL = (
    "❖ Name: `{Name}`\n"
    "❖ Size: {Size}\n"
    "❖ Seeders: {Seeders} ❖ Leechers: {Leechers}"
)

async def searchhelp(self, message):
    help_string = f'''
┏━ 𝗧𝗼𝗿𝗿𝗲𝗻𝘁 𝗦𝗲𝗮𝗿𝗰𝗵 𝗠𝗼𝗱𝘂𝗹𝗲 ━━╻
┃
┃• /nyaasi <i>[search in nyaasi]</i>
┃• /sukebei <i>[search in sukebei]</i>
┃• /1337x <i>[search 1337x]</i>
┃• /piratebay <i>[search piratebay]</i>
┃• /tgx <i>[search torrentgalaxy]</i>
┃• /yts <i>[search yts]</i>
┃• /eztv <i>[search eztv]</i>
┃• /torlock <i>[search torlock]</i>
┃• /rarbg <i>[search rarbg]</i>
┃• /ts <i>[search on all torrents]</i>
┃
┗━♦️ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 {UPDATES_CHANNEL}♦️━╹
'''
    await message.reply(text=help_string, parse_mode=enums.ParseMode.HTML)
