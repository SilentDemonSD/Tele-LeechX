#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52 | MaxxRider | 5MysterySD | Other Contributors 
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved

import sys, errno
from asyncio import sleep as asleep, subprocess, create_subprocess_exec
from os import path as opath, listdir, remove as oremove
from re import escape as rescape, findall
from shutil import rmtree
from time import time, sleep as tsleep
from functools import partial
from pathlib import Path
from requests import utils, get as rget

from pyrogram import enums, Client
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from hurry.filesize import size
from PIL import Image
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import InputMediaAudio, InputMediaDocument, InputMediaVideo
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tobrot import DESTINATION_FOLDER, DOWNLOAD_LOCATION, EDIT_SLEEP_TIME_OUT, INDEX_LINK, VIEW_LINK, LOGGER, \
                   TG_MAX_FILE_SIZE, UPLOAD_AS_DOC, CAP_STYLE, CUSTOM_CAPTION, user_specific_config, LEECH_LOG, \
                   EXCEP_CHATS, EX_LEECH_LOG, BOT_PM, TG_PRM_FILE_SIZE, PRM_USERS, PRM_LOG, isUserPremium, AUTH_CHANNEL, \
                   UPDATES_CHANNEL, SPLIT_SIZE, USER_LOGS
if isUserPremium:
    from tobrot import userBot
from tobrot.bot_theme.themes import BotTheme
from tobrot.helper_funcs.help_Nekmo_ffmpeg import copy_file
from tobrot.helper_funcs.display_progress import humanbytes, Progress
from tobrot.helper_funcs.help_Nekmo_ffmpeg import take_screen_shot
from tobrot.helper_funcs.split_large_files import split_large_files
from tobrot.plugins.custom_utils import *

def getFolderSize(p):
    prepend = partial(opath.join, p)
    return sum(
        opath.getsize(f) if opath.isfile(f) else getFolderSize(f)
        for f in map(prepend, listdir(p))
    )

async def upload_to_tg(message, local_file_name, from_user, dict_contatining_uploaded_files, client, edit_media=False, yt_thumb=None):
    global SPLIT_SIZE, CUSTOM_CAPTION
    base_file_name = opath.basename(local_file_name)
    file_size = opath.getsize(local_file_name)
    #duration = #Do Something

    caption_str = ""
    caption = CAP_DICT.get(from_user, "")

    if caption != "":
        slit = caption.split("#")
        CAP_ = slit[0]
        caption_str = CAP_.format(
            filename = base_file_name,
            size = humanbytes(file_size)
        )
        if len(slit) > 1:
            for rep in range(1, len(slit)):
                args = slit[rep].split(":")
                if len(args) == 3:
                    caption_str = caption_str.replace(args[0], args[1], int(args[2]))
                else:
                    caption_str = caption_str.replace(args[0], args[1])
    elif CUSTOM_CAPTION != "":
        caption_str = CUSTOM_CAPTION
    else:
        caption_str = f"<{CAP_STYLE}>{base_file_name}</{CAP_STYLE}>"

    IS_RETRT = bool(PRM_USERS and str(from_user) not in str(PRM_USERS))
    if opath.isdir(local_file_name):
        directory_contents = listdir(local_file_name)
        directory_contents.sort()
        LOGGER.info(directory_contents)
        new_m_esg = message
        if not message.photo:
            new_m_esg = await message.reply_text(((BotTheme(from_user)).EXTRACT_MSG).format(
                    no_of_con = len(directory_contents)
                ),
                quote=True
            )
        for single_file in directory_contents:
            await upload_to_tg(
                new_m_esg,
                opath.join(local_file_name, single_file),
                from_user,
                dict_contatining_uploaded_files,
                client,
                edit_media,
                yt_thumb,
            )
    else:
        sizze = opath.getsize(local_file_name)
        if not SPLIT_SIZE:
            SPLIT_SIZE = 4194304000 if isUserPremium and (not IS_RETRT) else 2097152000
        if sizze > TG_MAX_FILE_SIZE and sizze < TG_PRM_FILE_SIZE and isUserPremium and (not IS_RETRT):
            LOGGER.info(f"User Type : Premium ({from_user})")
            sent_message = await upload_single_file(
                message,
                local_file_name,
                caption_str,
                from_user,
                client,
                edit_media,
                yt_thumb,
                True
            )
            if sent_message is None:
                return
            dict_contatining_uploaded_files[opath.basename(local_file_name)] = sent_message.id
        elif sizze > TG_MAX_FILE_SIZE:
            LOGGER.info(f"User Type : Non Premium ({from_user})")
            i_m_s_g = await message.reply_text(
                "<b><i>📑 Telegram doesn't Support Uploading this File.</i></b>\n"
                f"<b><i>🎯 File Size :</i></b> {humanbytes(opath.getsize(local_file_name))}\n"
                "\n<code>🗃 Trying to Split the files ...</code>"
            )
            splitted_dir = await split_large_files(local_file_name, int(SPLIT_SIZE))
            totlaa_sleif = listdir(splitted_dir)
            totlaa_sleif.sort()
            number_of_files = len(totlaa_sleif)
            LOGGER.info(totlaa_sleif)
            ba_se_file_name = opath.basename(local_file_name)
            await i_m_s_g.edit_text(
                f"📬 <b>FileName : </b> <code>{ba_se_file_name}</code>\n\n"
                f"🎯 <b>File Size :</b> <code>{humanbytes(sizze)}</code>\n"
                f"🗂 <b>Total Splitted Parts :</b> {number_of_files}"
            )
            for le_file in totlaa_sleif:
                await upload_to_tg(
                    message,
                    opath.join(splitted_dir, le_file),
                    from_user,
                    dict_contatining_uploaded_files,
                    client,
                    edit_media,
                    yt_thumb,
                )
        else:
            sizze = opath.getsize(local_file_name)
            LOGGER.info("Files Less Than 2 GB")
            sent_message = await upload_single_file(
                message,
                local_file_name,
                caption_str,
                from_user,
                client,
                edit_media,
                yt_thumb,
                False
            )
            if sent_message is not None:
                dict_contatining_uploaded_files[opath.basename(local_file_name)] = sent_message.id
            else:
                return
    return dict_contatining_uploaded_files


# © gautamajay52 | RClone.org
async def upload_to_gdrive(file_upload, message, messa_ge, g_id):
    await asleep(EDIT_SLEEP_TIME_OUT)
    del_it = await message.edit_text(
        f"┏⚡️ <i>RClone Initiated</i> ⚡️\n┃\n┗📈 𝐒𝐭𝐚𝐭𝐮𝐬: <b><i>Uploading to Cloud...☁️</i></b>"
    )
    if opath.exists("rclone.conf"):
        with open("rclone.conf", "r+") as file:
            con = file.read()
            try:
                gUP = findall(r"\[(.*)\]", con)[0]
            except Exception as e:
                LOGGER.warning(f"[GClone] Make sure you have Set up the Name for the RClone Config Section. Error : {e}")
    destination = str(DESTINATION_FOLDER)
    file_upload = str(Path(file_upload).resolve())
    LOGGER.info(file_upload)
    if opath.isfile(file_upload):
        g_au = ["rclone", "copy", "--config=rclone.conf", f"{file_upload}", f"{gUP}:{destination}", "-v"]
        LOGGER.info(g_au)
        tmp = await create_subprocess_exec(
            *g_au, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        pro, cess = await tmp.communicate()
        LOGGER.info(pro.decode("utf-8"))
        LOGGER.info(cess.decode("utf-8"))
        gk_file = rescape(opath.basename(file_upload))
        LOGGER.info(gk_file)
        with open("filter.txt", "w+", encoding="utf-8") as filter:
            print(f"+ {gk_file}\n- *", file=filter)

        cmd = ["rclone", "lsf", "--config=rclone.conf", "-F", "i", "--filter-from=filter.txt", "--files-only", f"{gUP}:{destination}"]
        checkResults = await create_subprocess_exec(
            *cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        # oremove("filter.txt")
        gau, tam = await checkResults.communicate()
        gautam = gau.decode().strip()
        LOGGER.info(gau.decode())
        LOGGER.info(tam.decode())
        # oremove("filter.txt")
        gURL = f"https://drive.google.com/file/d/{gautam}/view?usp=drivesdk"
        gjay = size(opath.getsize(file_upload))
        button = [
            [
                InlineKeyboardButton(text="☁️ GDrive Link ☁️", url=f"{gURL}")
            ]
        ]
        fileURL = opath.basename(file_upload)
        if INDEX_LINK:
            _idno = 1
            INDEXS = INDEX_LINK.split(" ")
            for index in INDEXS:
                indexurl = f"{index}/{fileURL}"
                tam_link = utils.requote_uri(indexurl)
                LOGGER.info(f'Index Link #{_idno} : {tam_link}')
                if VIEW_LINK and (not indexurl.endswith('/')):
                    view_link_ = f"{tam_link}?a=view"
                    button.append([
                        InlineKeyboardButton(text=f"⚡️ Index Link #{_idno}⚡️", url=f"{tam_link}"),
                        InlineKeyboardButton(text=f"🌐 View Link #{_idno}", url=f"{view_link_}")
                    ])
                else:
                    button.append([
                        InlineKeyboardButton(text=f"⚡️ Index Link #{_idno}⚡️", url=f"{tam_link}")
                    ])
                _idno += 1
        button_markup = InlineKeyboardMarkup(button)
        await asleep(EDIT_SLEEP_TIME_OUT)
        await messa_ge.reply_text(
            f"📨 **Name** : `{fileURL}`\n\n📊 **Total Size** : `{gjay}B`\n\n👤 **Req By:** {messa_ge.from_user.mention} ( #ID{messa_ge.from_user.id} )",
            reply_markup=button_markup,
        )
        oremove(file_upload)
    else:
        tt = opath.join(destination, opath.basename(file_upload))
        LOGGER.info(tt)
        t_am = [
            "rclone",
            "copy",
            "--config=rclone.conf",
            f"{file_upload}",
            f"{gUP}:{tt}",
            "-v",
        ]
        tmp = await create_subprocess_exec(
            *t_am, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        pro, cess = await tmp.communicate()
        LOGGER.info(pro.decode("utf-8"))
        LOGGER.info(cess.decode("utf-8"))
        g_file = rescape(opath.basename(file_upload))
        LOGGER.info(g_file)
        with open("filter1.txt", "w+", encoding="utf-8") as filter1:
            print(f"+ {g_file}/\n- *", file=filter1)

        g_a_u = [
            "rclone",
            "lsf",
            "--config=rclone.conf",
            "-F",
            "i",
            "--filter-from=filter1.txt",
            "--dirs-only",
            f"{gUP}:{destination}",
        ]
        gau_tam = await create_subprocess_exec(
            *g_a_u, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        # oremove("filter1.txt")
        gau, tam = await gau_tam.communicate()
        gautam = gau.decode("utf-8")
        LOGGER.info(gautam)
        LOGGER.info(tam.decode("utf-8"))
        # oremove("filter1.txt")
        gURL = f"https://drive.google.com/folderview?id={gautam}"
        gjay = size(getFolderSize(file_upload))
        LOGGER.info(gjay)
        button = [[
                InlineKeyboardButton(text="☁️ GDrive Link ☁️", url=f"{gURL}")
        ]]
        fileURL = opath.basename(file_upload)
        if INDEX_LINK:
            _idno = 1
            INDEXS = INDEX_LINK.split(" ")
            for index in INDEXS:
                indexurl = f"{index}/{fileURL}"
                tam_link = utils.requote_uri(indexurl)
                LOGGER.info(f'Index Link #{_idno} : {tam_link}')
                button.append([
                    InlineKeyboardButton(text=f"⚡️ Index Link #{_idno}⚡️", url=f"{tam_link}")
                ])
                _idno += 1
        button_markup = InlineKeyboardMarkup(button)
        await asleep(EDIT_SLEEP_TIME_OUT)
        await messa_ge.reply_text(
            f"📨 **Name** : `{fileURL}`\n\n📊 **Total Size** : `{gjay}B`\n\n👤 **Req By:** {messa_ge.from_user.mention} ( #ID{messa_ge.from_user.id} )",
            reply_markup=button_markup,
        )
        rmtree(file_upload)
    await del_it.delete()


VIDEO_SUFFIXES = ("MKV", "MP4", "MOV", "WMV", "3GP", "MPG", "WEBM", "AVI", "FLV", "M4V", "GIF")
AUDIO_SUFFIXES = ("MP3", "M4A", "M4B", "FLAC", "WAV", "AIF", "OGG", "AAC", "DTS", "MID", "AMR", "MKA")
IMAGE_SUFFIXES = ("JPG", "JPX", "PNG", "WEBP", "CR2", "TIF", "BMP", "JXR", "PSD", "ICO", "HEIC", "JPEG")

async def sendPRMDocument(local_file_name, thumb, caption_str, prog, from_user,  start_time):
    LOGGER.info("UserBot Upload : Started")
    _upPRMDocument = await userBot.send_document(
             chat_id=int(PRM_LOG),
             document=local_file_name,
             thumb=thumb,
             caption=caption_str,
             parse_mode=enums.ParseMode.HTML,
             disable_notification=True,
             progress=prog.progress_for_pyrogram,
             progress_args=(
                 ((BotTheme(from_user)).TOP_PROG_MSG).format(base_file_name = opath.basename(local_file_name)),
                 start_time,
            ),
    )
    LOGGER.info("UserBot Upload : Completed")
    return _upPRMDocument

async def sendPRMVideo(local_file_name, thumb, duration, width, height, caption_str, prog, from_user, start_time):
    LOGGER.info("UserBot Upload : Started [VIDEO]")
    _upPRMVideo = await userBot.send_video(
            chat_id=int(PRM_LOG),
            video=local_file_name,
            thumb=thumb,
            duration=duration,
            width=width,
            height=height,
            supports_streaming=True,
            caption=caption_str,
            parse_mode=enums.ParseMode.HTML,
            disable_notification=True,
            progress=prog.progress_for_pyrogram,
            progress_args=(
                ((BotTheme(from_user)).START_UPLOAD_MSG).format(filename = opath.basename(local_file_name)),
                start_time,
            ),
    )
    LOGGER.info("UserBot Upload : Completed")
    return _upPRMVideo
async def replyDocument(message, local_file_name, thumb, caption_str, prog, from_user, start_time):
    doc = await message.reply_document(
                document=local_file_name,
                thumb=thumb,
                caption=caption_str,
                parse_mode=enums.ParseMode.HTML,
                disable_notification=True,
                progress=prog.progress_for_pyrogram,
                progress_args=(
                    ((BotTheme(from_user)).TOP_PROG_MSG).format(base_file_name = opath.basename(local_file_name)),
                    start_time,
                ),
            )
    return doc

async def replyVideo(message, local_file_name, caption_str, duration, width, height, thumb, prog, from_user, start_time):
    video = await message.reply_video(
        video=local_file_name,
        caption=caption_str,
        parse_mode=enums.ParseMode.HTML,
        duration=duration,
        width=width,
        height=height,
        thumb=thumb,
        supports_streaming=True,
        disable_notification=True,
        progress=prog.progress_for_pyrogram,
        progress_args=(
            ((BotTheme(from_user)).TOP_PROG_MSG).format(base_file_name = opath.basename(local_file_name)),
            start_time,
        ),
    )
    return video

async def copyMedia(client: Client, chatt, rply, sent_msg, caption_str):
    await asleep(3)
    copied = await client.copy_message(
        chat_id=int(chatt),
        from_chat_id=int(PRM_LOG),
        message_id=sent_msg.id,
        caption=caption_str,
        parse_mode=enums.ParseMode.HTML,
        reply_to_message_id=rply
    )
    return copied

async def upload_single_file(message, local_file_name, caption_str, from_user, client, edit_media, yt_thumb, prm_atv: bool):
    base_file_name = opath.basename(local_file_name)
    await asleep(EDIT_SLEEP_TIME_OUT)
    local_file_name = str(Path(local_file_name).resolve())
    sent_message = None
    thumbnail_location = f"{DOWNLOAD_LOCATION}/thumbnails/{from_user}.jpg"
    start_time = time()

    __uploadAsDoc = user_specific_config.get(from_user, False)
        
    global PRM_LOG
    if isUserPremium and (not PRM_LOG) and LEECH_LOG:
        PRM_LOG = LEECH_LOG
        LOGGER.info("[IDLE] Switching PRM_LOG to LEECH_LOG")
    elif isUserPremium and (not PRM_LOG) and (not LEECH_LOG):
        LOGGER.warning("[ERROR] Provide PRM_LOG or LEECH_LOG Var to Upload 4GB Contents")
        prm_atv = False

    global EXCEP_CHATS
    if (not EXCEP_CHATS) and (not LEECH_LOG):
        EXCEP_CHATS = AUTH_CHANNEL
        LOGGER.info("[IDLE] Switching AUTH_CHANNEL to EXCEP_CHATS")

    log_chat = USER_LOGS.get(from_user, None)
    if UPLOAD_AS_DOC.lower() == "true" or __uploadAsDoc:
        thumb = None
        thumb_image_path = None
        if opath.exists(thumbnail_location):
            thumb_image_path = await copy_file(
                thumbnail_location, opath.dirname(opath.abspath(local_file_name))
            )
        thumb = thumb_image_path
        
        message_for_progress_display = message
        if not edit_media:
            message_for_progress_display = await message.reply_text(
                ((BotTheme(from_user)).START_UPLOAD_MSG).format(filename = opath.basename(local_file_name))
            )
            prog = Progress(from_user, client, message_for_progress_display)
        LOGGER.info(f"Premium Active : {prm_atv}")
        if message.chat.id in EXCEP_CHATS and not prm_atv:
            sent_message = await replyDocument(message, local_file_name, thumb, caption_str, prog, from_user, start_time)
        elif message.chat.id in EXCEP_CHATS and prm_atv:
            sent_msg = await sendPRMDocument(local_file_name, thumb, caption_str, prog, from_user,  start_time)
            sent_message = await copyMedia(client, message.chat.id, message.id, sent_msg, caption_str)
            LOGGER.info("Bot 4GB Upload : Completed")
        else:
            if prm_atv:
                sent_msg = await sendPRMDocument(local_file_name, thumb, caption_str, prog, from_user,  start_time)
                sent_message = await copyMedia(client, LEECH_LOG, None, sent_msg, caption_str)
                LOGGER.info("Bot 4GB Upload : Completed")
            else:
                sent_message = await client.send_document(
                    chat_id=int(LEECH_LOG),
                    document=local_file_name,
                    thumb=thumb,
                    caption=f"<code>{base_file_name}</code>\n\n♨️ 𝕌𝕡𝕝𝕠𝕒𝕕𝕖𝕕 𝔹𝕪 {UPDATES_CHANNEL} ♨️",
                    parse_mode=enums.ParseMode.HTML,
                    disable_notification=True,
                )
            if BOT_PM:
                try:
                  await client.send_document(
                      chat_id=from_user, 
                      document=sent_message.document.file_id,
                      thumb=thumb,
                      caption=caption_str,
                      parse_mode=enums.ParseMode.HTML
                  )
                except Exception as err:
                   LOGGER.error(f"Failed To Send Document in User PM:\n{err}")
            if EX_LEECH_LOG:
                try:
                    for chat_id in EX_LEECH_LOG:
                        await client.send_document(
                            chat_id=int(chat_id), 
                            document=sent_message.document.file_id,
                            thumb=thumb,
                            caption=f"<code>{base_file_name}</code>\n\n♨️ 𝕌𝕡𝕝𝕠𝕒𝕕𝕖𝕕 𝔹𝕪 {UPDATES_CHANNEL} ♨️",
                            parse_mode=enums.ParseMode.HTML
                        )
                except Exception as err:
                    LOGGER.error(f"Failed To Send Document in Channel:\n{err}")
        if log_chat:
            try:
                if prm_atv: await copyMedia(client, log_chat, None, sent_msg, caption_str)
                else: await client.send_document(
                    chat_id=log_chat,
                    document=sent_message.document.file_id,
                    thumb=thumb,
                    caption=caption_str,
                    parse_mode=enums.ParseMode.HTML
                    )
            except Exception as e:
                LOGGER.error(f'Failed to Send Media to User Log Channel:{e}')
        if message.id != message_for_progress_display.id:
            try:
                await message_for_progress_display.delete()
            except FloodWait as gf:
                tsleep(gf.value)
            except Exception as rr:
                LOGGER.warning(rr)
        oremove(local_file_name)
        if thumb is not None:
            oremove(thumb)
    else:
        try:
            message_for_progress_display = message
            if not edit_media:
                message_for_progress_display = await message.reply_text(
                    ((BotTheme(from_user)).START_UPLOAD_MSG).format(filename = opath.basename(local_file_name))
                )
                prog = Progress(from_user, client, message_for_progress_display)
            if local_file_name.upper().endswith(VIDEO_SUFFIXES):
                duration = 0
                try:
                    metadata = extractMetadata(createParser(local_file_name))
                    if metadata.has("duration"):
                        duration = metadata.get("duration").seconds
                except Exception as g_e:
                    LOGGER.info(g_e)
                width = 0
                height = 0
                thumb_image_path = None
                if opath.exists(thumbnail_location):
                    thumb_image_path = await copy_file(
                        thumbnail_location,
                        opath.dirname(opath.abspath(local_file_name)),
                    )
                else:
                    if not yt_thumb:
                        LOGGER.info("📸 Taking Screenshot..")
                        thumb_image_path = await take_screen_shot(
                            local_file_name,
                            opath.dirname(opath.abspath(local_file_name)),
                            (duration / 2),
                        )
                    else:
                        req = rget(yt_thumb)
                        thumb_image_path = opath.join(
                            opath.dirname(opath.abspath(local_file_name)),
                            str(time()) + ".jpg",
                        )
                        with open(thumb_image_path, "wb") as thum:
                            thum.write(req.content)
                        img = Image.open(thumb_image_path).convert("RGB")
                        img.save(thumb_image_path, format="jpeg")
                    if opath.exists(thumb_image_path):
                        metadata = extractMetadata(createParser(thumb_image_path))
                        if metadata.has("width"):
                            width = metadata.get("width")
                        if metadata.has("height"):
                            height = metadata.get("height")
                        Image.open(thumb_image_path).convert("RGB").save(thumb_image_path)
                        img = Image.open(thumb_image_path)
                        img.resize((320, height))
                        img.save(thumb_image_path, "JPEG")

                thumb = None
                if thumb_image_path is not None and opath.isfile(thumb_image_path):
                    thumb = thumb_image_path

                if edit_media and message.photo:
                    await asleep(EDIT_SLEEP_TIME_OUT)
                    sent_message = await message.edit_media(
                        media=InputMediaVideo(
                            media=local_file_name,
                            thumb=thumb,
                            caption=caption_str,
                            parse_mode=enums.ParseMode.HTML,
                            width=width,
                            height=height,
                            duration=duration,
                            supports_streaming=True,
                        )
                    )
                else:
                    if message.chat.id in EXCEP_CHATS and not prm_atv:
                        sent_message = await replyVideo(message, local_file_name, caption_str, duration, width, height, thumb, prog, from_user, start_time)
                    elif message.chat.id in EXCEP_CHATS and prm_atv:
                        send_msg = await sendPRMVideo(local_file_name, thumb, duration, width, height, caption_str, prog, from_user, start_time)
                        sent_message = await copyMedia(client, message.chat.id, message.id, send_msg, caption_str)
                        LOGGER.info("Bot 4GB Upload : Completed")
                    else:
                        if prm_atv:
                            send_msg = await sendPRMVideo(local_file_name, thumb, duration, width, height, caption_str, prog, from_user, start_time)
                            sent_message = await copyMedia(client, LEECH_LOG, None, send_msg, caption_str)
                            LOGGER.info("Bot 4GB Upload : Completed")
                        else:
                            sent_message = await client.send_video(
                                chat_id=int(LEECH_LOG),
                                video=local_file_name,
                                caption=f"<code>{base_file_name}</code>\n\n♨️ 𝕌𝕡𝕝𝕠𝕒𝕕𝕖𝕕 𝔹𝕪 {UPDATES_CHANNEL} ♨️",
                                parse_mode=enums.ParseMode.HTML,
                                duration=duration,
                                width=width,
                                height=height,
                                thumb=thumb,
                                supports_streaming=True,
                                disable_notification=True,
                                progress=prog.progress_for_pyrogram,
                                progress_args=(
                                    ((BotTheme(from_user)).TOP_PROG_MSG).format(base_file_name = opath.basename(local_file_name)),
                                    start_time,
                                ),
                            )
                        if BOT_PM:
                            try:
                                await client.send_video(
                                    chat_id=from_user, 
                                    video=sent_message.video.file_id,
                                    thumb=thumb,
                                    supports_streaming=True,
                                    caption=caption_str,
                                    parse_mode=enums.ParseMode.HTML
                                )
                            except Exception as err:
                                LOGGER.error(f"Failed To Send Video in User PM:\n{err}")
                        if EX_LEECH_LOG:
                            try:
                                for chat_id in EX_LEECH_LOG:
                                    await client.send_video(
                                        chat_id=int(chat_id), 
                                        video=sent_message.video.file_id,
                                        thumb=thumb,
                                        supports_streaming=True,
                                        caption=f"<code>{base_file_name}</code>\n\n♨️ 𝕌𝕡𝕝𝕠𝕒𝕕𝕖𝕕 𝔹𝕪 {UPDATES_CHANNEL} ♨️",
                                        parse_mode=enums.ParseMode.HTML
                                    )
                            except Exception as err:
                                LOGGER.error(f"Failed To Send Video in Channel:\n{err}")
                if log_chat:
                    try:
                        if prm_atv: await copyMedia(client, log_chat, None, send_msg, caption_str)
                        else: await client.send_video(
                                    chat_id=log_chat, 
                                    video=sent_message.video.file_id,
                                    thumb=thumb,
                                    supports_streaming=True,
                                    caption=caption_str,
                                    parse_mode=enums.ParseMode.HTML
                            )
                    except Exception as err:
                        LOGGER.error(f'Failed to Send Media to User Log Channel : {err}')
                if thumb is not None:
                    oremove(thumb)
            elif local_file_name.upper().endswith(AUDIO_SUFFIXES):

                metadata = extractMetadata(createParser(local_file_name))
                duration = 0
                title = ""
                artist = ""
                if metadata.has("duration"):
                    duration = metadata.get("duration").seconds
                if metadata.has("title"):
                    title = metadata.get("title")
                if metadata.has("artist"):
                    artist = metadata.get("artist")

                thumb_image_path = None
                if opath.isfile(thumbnail_location):
                    thumb_image_path = await copy_file(
                        thumbnail_location,
                        opath.dirname(opath.abspath(local_file_name)),
                    )
                thumb = None
                if thumb_image_path is not None and opath.isfile(thumb_image_path):
                    thumb = thumb_image_path
                if edit_media and message.photo:
                    await asleep(EDIT_SLEEP_TIME_OUT)
                    sent_message = await message.edit_media(
                        media=InputMediaAudio(
                            media=local_file_name,
                            thumb=thumb,
                            caption=caption_str,
                            parse_mode=enums.ParseMode.HTML,
                            duration=duration,
                            performer=artist,
                            title=title,
                        )
                    )
                else:
                    if message.chat.id in EXCEP_CHATS:
                        sent_message = await message.reply_audio(
                            audio=local_file_name,
                            caption=caption_str,
                            parse_mode=enums.ParseMode.HTML,
                            duration=duration,
                            performer=artist,
                            title=title,
                            thumb=thumb,
                            disable_notification=True,
                            progress=prog.progress_for_pyrogram,
                            progress_args=(
                                ((BotTheme(from_user)).START_UPLOAD_MSG).format(filename = opath.basename(local_file_name)),
                                start_time,
                            ),
                        )
                    else:
                        sent_message = await client.send_audio(
                            chat_id=int(LEECH_LOG),
                            audio=local_file_name,
                            caption=caption_str,
                            parse_mode=enums.ParseMode.HTML,
                            duration=duration,
                            performer=artist,
                            title=title,
                            thumb=thumb,
                            disable_notification=True,
                            progress=prog.progress_for_pyrogram,
                            progress_args=(
                                ((BotTheme(from_user)).START_UPLOAD_MSG).format(filename = opath.basename(local_file_name)),
                                start_time,
                            ),
                        )
                        if BOT_PM:
                            try:
                                await client.send_audio(
                                    chat_id=from_user, 
                                    audio=sent_message.audio.file_id,
                                    thumb=thumb,
                                    caption=caption_str,
                                )
                            except Exception as err:
                                LOGGER.error(f"Failed To Send Audio in User PM:\n{err}")
                        if EX_LEECH_LOG:
                            try:
                                for chat_id in EX_LEECH_LOG:
                                    await client.send_audio(
                                        chat_id=int(chat_id), 
                                        document=sent_message.audio.file_id,
                                        thumb=thumb,
                                        caption=f"<code>{base_file_name}</code>",
                                    )
                            except Exception as err:
                                LOGGER.error(f"Failed To Send Audio in User PM:\n{err}")
                if thumb is not None:
                    oremove(thumb)
            else:
                thumb_image_path = None
                if opath.isfile(thumbnail_location):
                    thumb_image_path = await copy_file(
                        thumbnail_location,
                        opath.dirname(opath.abspath(local_file_name)),
                    )
                thumb = None
                if thumb_image_path is not None and opath.isfile(thumb_image_path):
                    thumb = thumb_image_path
                if edit_media and message.photo:
                    sent_message = await message.edit_media(
                        media=InputMediaDocument(
                            media=local_file_name,
                            thumb=thumb,
                            caption=caption_str,
                            parse_mode=enums.ParseMode.HTML
                        )
                    )
                else:
                    if message.chat.id in EXCEP_CHATS and not prm_atv:
                        sent_message = await replyDocument(message, local_file_name, thumb, caption_str, prog, from_user, start_time)
                    elif message.chat.id in EXCEP_CHATS and prm_atv:
                        sent_msg = await sendPRMDocument(local_file_name, thumb, caption_str, prog, from_user,  start_time)
                        sent_message = await copyMedia(client, message.chat.id, message.id, sent_msg, caption_str)
                        LOGGER.info("Bot 4GB Upload : Completed")
                    else:
                        if prm_atv:
                            sent_msg = await sendPRMDocument(local_file_name, thumb, caption_str, prog, from_user,  start_time)
                            sent_message = await copyMedia(client, LEECH_LOG, None, sent_msg, caption_str)
                            LOGGER.info("Bot 4GB Upload : Completed")
                        else:
                            sent_message = await client.send_document(
                                chat_id=int(LEECH_LOG),
                                document=local_file_name,
                                thumb=thumb,
                                caption=f"<code>{base_file_name}</code>\n\n♨️ 𝕌𝕡𝕝𝕠𝕒𝕕𝕖𝕕 𝔹𝕪 {UPDATES_CHANNEL} ♨️",
                                parse_mode=enums.ParseMode.HTML,
                                disable_notification=True,
                                progress=prog.progress_for_pyrogram,
                                progress_args=(
                                    ((BotTheme(from_user)).TOP_PROG_MSG).format(base_file_name = opath.basename(local_file_name)),
                                    start_time,
                                ),
                            )
                        if BOT_PM:
                            try:
                                await client.send_document(
                                    chat_id=from_user, 
                                    document=sent_message.document.file_id,
                                    thumb=thumb,
                                    caption=caption_str,
                                    parse_mode=enums.ParseMode.HTML
                                )
                            except Exception as err:
                                LOGGER.error(f"Failed To Send Document in User PM:\n{err}")
                        if EX_LEECH_LOG:
                            try:
                                for chat_id in EX_LEECH_LOG:
                                    await client.send_document(
                                        chat_id=int(chat_id), 
                                        document=sent_message.document.file_id,
                                        thumb=thumb,
                                        caption=f"<code>{base_file_name}</code>\n\n♨️ 𝕌𝕡𝕝𝕠𝕒𝕕𝕖𝕕 𝔹𝕪 {UPDATES_CHANNEL} ♨️",
                                        parse_mode=enums.ParseMode.HTML
                                    )
                            except Exception as err:
                                LOGGER.error(f"Failed To Send Document in Channel:\n{err}")
                if log_chat:
                    try:
                        if prm_atv: await copyMedia(client, log_chat, None, sent_msg, caption_str)
                        else: await client.send_document(
                                chat_id=log_chat,
                                document=sent_message.document.file_id,
                                thumb=thumb,
                                caption=caption_str,
                                parse_mode=enums.ParseMode.HTML
                            )
                    except Exception as e:
                        LOGGER.error(f'Failed to Send Media to User Log Channel:{e}')
                if thumb is not None:
                    oremove(thumb)
        except MessageNotModified:
            pass
        except FloodWait as g:
            LOGGER.info(f"FloodWait : Sleeping {g.value}s")
            tsleep(g.value)
        except FileNotFoundError:
            pass
        except IOError as e:
            if e.errno == errno.EPIPE:
                pass
        except Exception as e:
            LOGGER.info(f"[ERROR] : {e}")
            try:
                await message_for_progress_display.edit_text("**FAILED**\n" + str(e))
            except FloodWait as g:
                LOGGER.info(f"FloodWait : Sleeping {g.value}s")
                tsleep(g.value)
        else:
            if message.id != message_for_progress_display.id:
                try:
                    if sent_message is not None:
                        await message_for_progress_display.delete()
                except FloodWait as gf:
                    LOGGER.info(f"FloodWait : Sleeping {gf.value}s")
                    tsleep(gf.value)
                except Exception as rr:
                    LOGGER.warning(str(rr))
                    await asleep(5)
        oremove(local_file_name)
    return sent_message
