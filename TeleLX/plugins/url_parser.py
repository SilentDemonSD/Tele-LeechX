#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) SilentDemonSD [Full Code Written By Me !! No Kang Please]
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/SilentDemonSD/Tele-LeechX >
# All Right Reserved

import datetime 
from urllib.parse import quote as q
from TeleLX import LOGGER
from TeleLX.core.display.display_utils import format_time, format_bytes
from TeleLX.plugins import is_appdrive_link, is_gdtot_link, is_hubdrive_link, getUserOrChaDetails
from TeleLX.helper_funcs.direct_link_generator import url_link_generate, gdtot, appdrive_dl, hubdrive 
from TeleLX.helper_funcs.exceptions import DirectDownloadLinkException

drive_list = ['driveapp.in', 'gdflix.pro', 'drivelinks.in', 'drivesharer.in', 'driveflix.in', 'drivebit.in', 'drivehub.in', 'driveace.in']
bypass_vip_list = ['exe.io', 'exey.io', 'sub2unlock.net', 'sub2unlock.com', 'rekonise.com', 'letsboost.net', 'ph.apps2app.com', 'mboost.me', 'shortconnect.com', 'sub4unlock.com', 'ytsubme.com', 'bit.ly', 'social-unlock.com', 'boost.ink', 'goo.gl', 'shrto.ml', 't.co', 'tinyurl.com']

async def url_parser(client, message):
    op = await message.reply_text("`Fetching Data . . .`")
    user_id, u_men = getUserOrChaDetails(message)
    url_parse = message.text.split(" ", maxsplit=1)
    reply_to = message.reply_to_message
    if len(url_parse) > 1:
        url = url_parse[1]
    elif reply_to is not None:
        url = reply_to.text
    else:
        url = None
    if url is not None:
        oo = await op.edit_text(text=f"⚡️__URL Parsing Initiated__⚡️\n\n👤 **User** : {u_men} \n🆔 **User ID** : `{user_id}` \n🔗 **Link** : `{url}`\n\n`Fetching Data . . .`", disable_web_page_preview=True)
        try:
            trigger, bypassed_url = await bypass_link(url)
        except Exception as e:
            not_ok = await op.edit_text(text=f"⚡️__URL Parsing Initiated__⚡️\n\n👤 **User** : {u_men} \n🆔 **User ID** : `{user_id}` \n🔗 **Link** : `{url}`\n\n⛔ **Error** ⛔ : \n `{e}` \n\n#UnParsable ", disable_web_page_preview=True)
            return 
        if trigger is True:
            ok = await oo.edit_text(text="⛔ __Url Parsing Stopped__ ⛔ \n\n `Check your Link First, if I can Parse it or Not !!` \n\n#UnParseable", disable_web_page_preview=True)
            return 
        tell = await oo.edit_text(text=f"⚡️__URL Parsing Initiated__⚡️\n\n👤 **User** : {u_men} \n🆔 **User ID** : `{user_id}` \n🔗 **Link** : `{url}`\n\n📇 **Bypass Info** 📇 : \n\n {bypassed_url}\n\n#Parsed", disable_web_page_preview=True)
    else:
        oo = await op.edit_text(text="**Send Link Along with Command :**\n/parser(BotName) `{link}`\n\n **Reply to a Link :**\n/parser(BotName) to Link \n\n**SUPPORTED SITES**\n__Coming Soon__",)
        return


async def bypass_link(text_url: str):

    url_list = ["zippyshare.com", "osdn.net", "mediafire.com", "https://uptobox.com", "cloud.mail.ru", "github.com", "yadi.sk", "hxfile.co", "https://anonfiles.com", "letsupload.io", "fembed.net", "fembed.com", "femax20.com", "fcdn.stream", "feurl.com", "naniplay.nanime.in", 
                "naniplay.nanime.biz", "naniplay.com", "layarkacaxxi.icu", "sbembed.com", "streamsb.net", "sbplay.org", "1drv.ms", "pixeldrain.com", "antfiles.com", "streamtape.com", "https://bayfiles.com", "1fichier.com", "solidfiles.com", "krakenfiles.com", "gplinks.co",
                "katdrive.net", "drivefire.co", "drivebuzz.icu", "gadrive.vip", "linkvertise.com", "droplink.co", "gofile.io", "ouo.io", "ouo.press", "upindia.mobi", "uploadfile.cc", "adf.ly", "https://sourceforge.net", "https://master.dl.sourceforge.net", "androiddatahost.com",
                "androidfilehost.com", "sfile.mobi", "wetransfer.com", "we.tl", "corneey.com", "sh.st", "racaty.net", "psa.pm", "upload.ee", "dropbox.com", "megaup.net", "mediafire.com", "filecrypt.ws", "shareus.io", "shortlingly.in", "gyanilinks.com", "pixl", "safeurl.sirigan.my.id", 
                "sharer.pw", "rocklinks.net", "olamovies.ink"]

    if any(url in text_url for url in url_list) or any(x in text_url for x in bypass_vip_list):
        try:
            url_string = url_link_generate(text_url)
            return False, q(url_string, safe=':/')
        except DirectDownloadLinkException as e:
            LOGGER.info(f'{text_url}: {e}')
    elif is_hubdrive_link(text_url):
        try:
            info_parsed = hubdrive(text_url)
            url_string = f"📨 **Name** : `{info_parsed['title']}`\n📁 **File Size** : `{info_parsed['File Size']}`\n📬 **File Owner** : `{info_parsed['File Owner']}`\n📮 **Error Type** : `{info_parsed['error']}`\n☁️ **GDrive URL** : `{info_parsed['gdrive_url']}`"
            return False, url_string
        except DirectDownloadLinkException as e:
            LOGGER.info(f'{text_url}: {e}')
    elif is_gdtot_link(text_url):
        try:
            info_parsed = gdtot(text_url)
            url_string = (
                f"📨 **Name** : `{info_parsed['title']}` \n📁 **File Size** : `{info_parsed['size']}` \n📆 **Date** : `{info_parsed['date']}` \n☁️ **GDrive URL** : `{info_parsed['gdrive_link']}`"
                if info_parsed['gdrive_link']
                else f"⛔ **Parsing Error** ⛔ : \n `{info_parsed['message']}`"
            )

            return False, url_string
        except DirectDownloadLinkException as e:
            LOGGER.info(f'{text_url}: {e}')
            return False, e
    elif is_appdrive_link(text_url) or any(x in text_url for x in drive_list):
        try:
            is_direct = False
            info_parsed = appdrive_dl(text_url, is_direct)
            if info_parsed['error'] == True:
                url_string = f"⛔ **Parsing Error** ⛔ : \n `{info_parsed['error_message']}`"
            else:
                url_string = f"📨 **Name** : `{info_parsed['name']}`\n💾 **Format** : `{info_parsed['format']}`\n📁 **File Size** : `{info_parsed['size']}`\n📎 **Link Type** : `{info_parsed['link_type']}`\n☁️ **GDrive URL** : `{info_parsed['gdrive_link']}`"
            return False, url_string
        except DirectDownloadLinkException as er:
            LOGGER.info(f'{text_url}: {er}')
            return False, er
        except Exception as e:
            url_string = f"⛔ **Internal Error** ⛔ : \n `{e}`"
            return False, url_string 
    elif "kolop.icu" in text_url:
        try:
            info_parsed = url_link_generate(text_url)
            if info_parsed['error'] == True:
                url_string = f"⛔ **Parsing Error** ⛔ : \n `{info_parsed['error_message']}`"
            else:
                url_string = f"📨 **Name** : `{info_parsed['title']}`\n📁 **File Size** : `{info_parsed['File Size']}`\n🧾 **Mime Type** : `{info_parsed['File Type']}`\n💳 **File Owner** : `{info_parsed['File Owner']}`\n☁️ **GDrive URL** : `{info_parsed['gdrive_url']}`"
            return False, url_string
        except DirectDownloadLinkException as er:
            LOGGER.info(f'{text_url}: {er}')
            return False, er
        except Exception as e:
            url_string = f"⛔ **Internal Error** ⛔ : \n `{e}`"
            return False, url_string 
    elif "mdisk.me" in text_url:
        try:
            info_parsed = url_link_generate(text_url)
            men_user = 'tg://user?id={info_parsed["from"]}'
            url_string = f"📨 **Name** : `{info_parsed['filename']}` \n📁 **File Size** : `{format_bytes(info_parsed['size'])}` \n🎞 **Duration** : `{format_time(info_parsed['duration']*1000)}` \n💾 **Resolution** : `{info_parsed['width']} × {info_parsed['height']}` \n📆 **Upload On** : `{datetime.datetime.utcfromtimestamp(info_parsed['ts']/1000).strftime('%I:%M:%S %p %d %B, %Y')}` \n💳 **File Uploader** : <a href='{men_user}'>{info_parsed['display_name']}</a> ( `{info_parsed['from']}` ) \n📎 **Download URL** : `{info_parsed['download']}`"
            return False, url_string
        except DirectDownloadLinkException as er:
            LOGGER.info(f'{text_url}: {er}')
            return False, er
    else:
        return True, None

