#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52 | MaxxRider | 5MysterySD | Other Contributors 
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved

from os import path as opath, makedirs, rename as orename
from time import time
from pathlib import Path
from requests import get as rget
from asyncio import sleep as asleep
from urllib.parse import unquote, quote

from pyrogram import enums, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

from tobrot import DOWNLOAD_LOCATION, CLONE_COMMAND_G, GLEECH_COMMAND, GLEECH_UNZIP_COMMAND, GLEECH_ZIP_COMMAND, \
                   LOGGER, GPYTDL_COMMAND, STATUS_COMMAND, UPDATES_CHANNEL, LEECH_LOG, BOT_PM, EXCEP_CHATS, app, \
                   FSUB_CHANNEL, USER_DTS, AUTO_LEECH, RCLONE_CONF_URL, EDIT_SLEEP_TIME_OUT, AUTO_USERS
from tobrot.helper_funcs.display_progress import humanbytes, TimeFormatter
from tobrot.helper_funcs.bot_commands import BotCommands
from tobrot.helper_funcs.admin_check import AdminCheck
from tobrot.helper_funcs.cloneHelper import CloneHelper
from tobrot.helper_funcs.download import download_tg
from tobrot.helper_funcs.download_aria_p_n import aria_start, call_apropriate_function, __sendSpecificLogMsg
from tobrot.helper_funcs.extract_link_from_message import extract_link
from tobrot.helper_funcs.upload_to_tg import upload_to_tg
from tobrot.helper_funcs.youtube_dl_extractor import extract_youtube_dl_formats
from tobrot.helper_funcs.ytplaylist import yt_playlist_downg
from tobrot.plugins import getDetails, getUserOrChaDetails, getUserName
from tobrot.plugins.force_sub_handler import handle_force_sub
from tobrot.bot_theme.themes import BotTheme

async def incoming_purge_message_f(client: Client, message: Message):
    msg = await message.reply_text("Purging...", quote=True)
    if await AdminCheck(client, message.chat.id, message.from_user.id):
        aria_i_p = await aria_start()
        downloads = aria_i_p.get_downloads()
        for download in downloads:
            LOGGER.info(download.remove(force=True))
        await msg.edit_text('Purged Successfully !!')
    await asleep(EDIT_SLEEP_TIME_OUT)
    await msg.delete()

async def check_bot_pm(client: Client, message: Message):
    if message.chat.type != enums.ChatType.PRIVATE and message.chat.id not in EXCEP_CHATS:
        LOGGER.info("[BOT PM] Initiated")
        try:
            send = await client.send_message(message.from_user.id, text='Leech Started !!')
            await send.delete()
            return True
        except Exception as e:
            LOGGER.warning(e)
            uname = message.from_user.mention
            button_markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton("⚡️ Click Here to Start Me ⚡️", url=f"http://t.me/{(await client.get_me()).username}")]
                ])
            startwarn = f'''┏ Dear {uname},
┃
┣ <b> Bot is Not Started in PM (Private Chat) yet.</b>
┃
┗ <i> From Now on, Links and Leeched Files in PM and Log Channel Only !!</i>'''
            message = await message.reply_text(text=startwarn, parse_mode=enums.ParseMode.HTML, quote=True, reply_markup=button_markup)
            return False
    else: return True

async def auto_callback(c: Client, cb: CallbackQuery):
    user_id = (cb.data).split()[1]
    if cb.from_user.id != int(user_id):
        await cb.answer('⚠️ Not Your Leech ⚠️', show_alert=True)
        return
    if cb.data.startswith("alxLeech"):
        await cb.message.delete()
        await incoming_message_f(c, cb.message.reply_to_message, BotCommands.LeechCommand.lower())
    elif cb.data.startswith("alxExtract"):
        await cb.message.delete()
        await incoming_message_f(c, cb.message.reply_to_message, BotCommands.ExtractCommand.lower())
    elif cb.data.startswith("alxArchive"):
        await cb.message.delete()
        await incoming_message_f(c, cb.message.reply_to_message, BotCommands.ArchiveCommand.lower())
    elif cb.data.startswith("alxGLeech"):
        await cb.message.delete()
        await incoming_message_f(c, cb.message.reply_to_message, GLEECH_COMMAND.lower())
    elif cb.data.startswith("alxGExtract"):
        await cb.message.delete()
        await incoming_message_f(c, cb.message.reply_to_message, GLEECH_UNZIP_COMMAND.lower())
    elif cb.data.startswith("alxGArchive"):
        await cb.message.delete()
        await incoming_message_f(c, cb.message.reply_to_message, GLEECH_ZIP_COMMAND.lower())
    elif cb.data.startswith("alxClose"):
        await cb.message.edit('<b>🛃 Process Cancelled</b>')

async def incoming_message_f(client: Client, message: Message, auto_cmd=None):
    """/leech command or /gleech command"""
    if not AUTO_LEECH:
        user_command = message.command[0]
    g_id, tag_me = getUserOrChaDetails(message)
    txtCancel = False
    ubot = (await client.get_me()).username

    if FSUB_CHANNEL and not auto_cmd:
        LOGGER.info("[ForceSubscribe] Initiated")
        backCode = await handle_force_sub(client, message)
        if backCode == 400:
            LOGGER.info(f"[ForceSubscribe] User Not In {FSUB_CHANNEL}")
            return

    if BOT_PM and LEECH_LOG and not auto_cmd:
        if not (await check_bot_pm(client, message)):
            return
    elif BOT_PM and not auto_cmd:
        LOGGER.warning("[BOT PM] Must Provide LEECH_LOG to Use it")

    rpy_mssg_id = None
    if USER_DTS and not auto_cmd:
        func_name = 'Auto Leech' if AUTO_LEECH else 'Leech'
        text__, txtCancel = getDetails(client, message, func_name)
        link_text = await message.reply_text(text=text__, parse_mode=enums.ParseMode.HTML, quote=True, disable_web_page_preview=True)
        
        endText = f"\n📬 <b>Source :</b> <a href='{message.link}'>Click Here</a>\n\n#LeechStart #FXLogs"
        if not txtCancel:
            if LEECH_LOG and message.chat.id not in EXCEP_CHATS:
                text__ += endText
                logs_msg = await client.send_message(chat_id=int(LEECH_LOG), text=text__, parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
                rpy_mssg_id = logs_msg.id
            LOGGER.info(f"Leech Started : {tag_me}")

    i_m_sefg = await message.reply_text("<code>Processing ... 🔄</code>", quote=True)
    is_file = False
    dl_url = ''
    cf_name = ''
    if AUTO_LEECH and not auto_cmd:
        _auto = AUTO_USERS.get(g_id, [True, None])
        if _auto[0]:
            buttons = [
            [InlineKeyboardButton('Leech', callback_data=f'alxLeech {g_id}'),
            InlineKeyboardButton('Extract', callback_data=f'alxExtract {g_id}')],
            [InlineKeyboardButton('Archive', callback_data=f'alxArchive {g_id}')]
            ]
            if RCLONE_CONF_URL:
                buttons[1].insert(1, InlineKeyboardButton('GLeech', callback_data=f'alxGLeech {g_id}'))
                buttons.append(
                    [InlineKeyboardButton('GArchive', callback_data=f'alxGArchive {g_id}'),
                    InlineKeyboardButton('GExtract', callback_data=f'alxGExtract {g_id}')]
                )
            buttons.append([InlineKeyboardButton('❌️ Cancel ❌️', callback_data=f'alxClose {g_id}')])
            await i_m_sefg.edit(text="🎛 <b><i>Here you can Configure your Leech Preferences !!</i></b>", reply_markup=InlineKeyboardMarkup(buttons), parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
            return
        else:
            await i_m_sefg.delete()
            await incoming_message_f(client, message, _auto[1])
    elif AUTO_LEECH and auto_cmd:
        dl_url, cf_name, _, _ = await extract_link(message, "LEECH")
        user_command = auto_cmd
    elif rep_mess := message.reply_to_message:
        file_name = ''
        if rep_mess.media:
            file = [rep_mess.document, rep_mess.video, rep_mess.audio]
            file_name = [fi for fi in file if fi is not None][0].file_name
        if not rep_mess.media or str(file_name).lower().endswith(".torrent"):
            dl_url, cf_name, _, _ = await extract_link(message.reply_to_message, "LEECH")
            LOGGER.info(dl_url)
            LOGGER.info(cf_name)
        else:
            if user_command == BotCommands.LeechCommand.lower():
                await i_m_sefg.edit(((BotTheme(g_id)).WRONG_COMMAND).format(
                    u_men = tag_me
                ))
                return
            is_file = True
            dl_url = rep_mess
    elif len(message.command) == 2:
        dl_url = message.command[1]
        LOGGER.info(dl_url)

    elif len(message.command) > 2 and message.command[2] == "|":
        dl_url = message.command[1]
        cf_name = message.text.split('|', 1)[1].strip()

    else:
        await i_m_sefg.edit((BotTheme(g_id)).WRONG_DEF_COMMAND)
        return
    if dl_url is not None:
        new_download_location = opath.join(
            DOWNLOAD_LOCATION, str(g_id), str(time())
        )
        if not opath.isdir(new_download_location):
            makedirs(new_download_location)
        aria_i_p = ''
        if not is_file:
            await i_m_sefg.edit_text("<code>Extracting Links . . . 🔀</code>")
            aria_i_p = await aria_start()

        await i_m_sefg.edit_text(((BotTheme(g_id)).DOWNLOAD_ADDED_MSG).format(
            u_men = tag_me,
            u_id = g_id,
            status_cmd = BotCommands.StatusCommand,
            UPDATES_CHANNEL = UPDATES_CHANNEL
        ))
        is_zip = False
        is_cloud = False
        is_unzip = False
        bot_unzip = f"{BotCommands.ExtractCommand}@{ubot}".lower()
        bot_zip = f"{BotCommands.ArchiveCommand}@{ubot}".lower()
        cloud = f"{GLEECH_COMMAND}@{ubot}".lower()
        cloud_zip = f"{GLEECH_ZIP_COMMAND}@{ubot}".lower()
        cloud_unzip = f"{GLEECH_UNZIP_COMMAND}@{ubot}".lower()

        if user_command == BotCommands.ExtractCommand.lower() or user_command == bot_unzip:
            is_unzip = True
        elif user_command == BotCommands.ArchiveCommand.lower() or user_command == bot_zip:
            is_zip = True

        if user_command == GLEECH_COMMAND.lower() or user_command == cloud:
            is_cloud = True
        if user_command == GLEECH_UNZIP_COMMAND.lower() or user_command == cloud_unzip:
            is_cloud = True
            is_unzip = True
        elif user_command == GLEECH_ZIP_COMMAND.lower() or user_command == cloud_zip:
            is_cloud = True
            is_zip = True

        sagtus, err_message = await call_apropriate_function(
            aria_i_p,
            dl_url,
            new_download_location,
            i_m_sefg,
            is_zip,
            cf_name,
            is_cloud,
            is_unzip,
            is_file,
            message,
            client,
            rpy_mssg_id
        )
        if not sagtus:
            await i_m_sefg.edit_text(err_message)
    else:
        await i_m_sefg.edit_text(((BotTheme(g_id)).EXCEP_DEF_MSG).format(
            cf_name = cf_name
        ))

async def incoming_youtube_dl_f(client, message):
    current_user_id, u_men = getUserOrChaDetails(message)
    text__, txtCancel = getDetails(client, message, 'yt-dlp')
    link_text = await message.reply_text(text=text__, parse_mode=enums.ParseMode.HTML, quote=True, disable_web_page_preview=True)
    i_m_sefg = await message.reply_text("<code>Prrocessing...🔃</code>", quote=True)
    if message.reply_to_message:
        dl_url, cf_name, yt_dl_user_name, yt_dl_pass_word = await extract_link(
            message.reply_to_message, "YTDL"
        )
        LOGGER.info(dl_url)
        LOGGER.info(cf_name)
    elif len(message.command) == 2:
        dl_url = message.command[1]
        LOGGER.info(dl_url)
        cf_name = None
        yt_dl_user_name = None
        yt_dl_pass_word = None
        cf_name = None
    else:
        await i_m_sefg.edit("<b>⚠️ Opps ⚠️</b>\n\n <b><i>⊠ Reply To YTDL Supported Link.</i></b>")
        return
    if dl_url is not None:
        await i_m_sefg.edit_text("<code>Extracting Links . . . 🔀</code>")
        user_working_dir = opath.join(DOWNLOAD_LOCATION, str(current_user_id))
        if not opath.isdir(user_working_dir):
            makedirs(user_working_dir)
        thumb_image, text_message, reply_markup = await extract_youtube_dl_formats(
            dl_url, cf_name, yt_dl_user_name, yt_dl_pass_word, user_working_dir
        )
        if thumb_image is not None:
            req = rget(f"{thumb_image}")
            thumb_img = f"{current_user_id}.jpg"
            with open(thumb_img, "wb") as thumb:
                thumb.write(req.content)
            await message.reply_photo(
                photo=thumb_img,
                quote=True,
                caption=text_message,
                reply_markup=reply_markup,
            )
            await i_m_sefg.delete()
        else:
            await i_m_sefg.edit_text(text=text_message, reply_markup=reply_markup)
    else:
        await i_m_sefg.edit_text(
            "<b> 🏖Maybe You Didn't Know I am Being Used !!</b> \n\n<b>🌐 API Error</b>: {cf_name}"
        )

async def g_yt_playlist(client, message):
    user_command = message.command[0]
    usr_id, u_men = getUserOrChaDetails(message)
    is_cloud = False
    url = None
    if message.reply_to_message:
        url = message.reply_to_message.text
        if user_command == GPYTDL_COMMAND.lower():
            is_cloud = True
    elif len(message.command) == 2:
        url = message.command[1]
        if user_command == GPYTDL_COMMAND.lower():
            is_cloud = True
    else:
        await message.reply_text("<b> Reply with Youtube Playlist link</b>", quote=True)
        return
    if "youtube.com/playlist" in url:
        i_m_sefg = await message.reply_text(
            f"<b>Ok Fine {u_men} Bro!!:\n Your Request has been ADDED</b>\n\n <code> Please wait until Upload</code>",
            parse_mode=enums.ParseMode.HTML
        )
        await yt_playlist_downg(message, i_m_sefg, client, is_cloud)

    else:
        await message.reply_text("<b>YouTube playlist link only 🙄</b>", quote=True)

async def g_clonee(client: Client, message: Message):
    g_id, _ = getUserOrChaDetails(message)

    if BOT_PM and LEECH_LOG: 
        if not (await check_bot_pm(client, message)):
            return
    elif BOT_PM and (not LEECH_LOG):
        LOGGER.warning("[Bot PM] Must Provide LEECH_LOG to Use it")

    if (not RCLONE_CONF_URL):
        LOGGER.info("[RCLONE] RCLONE_CONF_URL not Provided !!")
        return
    _link = message.text.split(" ", maxsplit=1)
    reply_to = message.reply_to_message
    if len(_link) > 1:
        linky = _link[1]
    elif reply_to is not None:
        linky = reply_to.text 
    else:
        linky = None

    if linky is not None:
        try:
            gclone = CloneHelper(message)
            gclone.config()
            a, h = await gclone.get_id()
            LOGGER.info(a)
            LOGGER.info(h)
            await gclone.gcl()
            await gclone.link_gen_size()
        except Exception as e:
            LOGGER.info(f'GClone Error : {e}')
            await message.reply_text(e)
    else:
        await message.reply_text(
            f'''**Send GDrive Link Along with Command :**
/{CLONE_COMMAND_G}(BotName) `Link`

**Reply to a GDrive Link :**
/{CLONE_COMMAND_G}(BotName) to Link

**SUPPORTED SITES :**
__Google Drive, GDToT, AppDrive, Kolop, HubDrive, DriveLinks__'''
        )


async def rename_tg_file(client: Client, message: Message):
    usr_id, tag_me = getUserOrChaDetails(message)
    if BOT_PM and LEECH_LOG:
        if not (await check_bot_pm(client, message)):
            return
    elif BOT_PM and (not LEECH_LOG):
        LOGGER.warning("[Bot PM] Must Provide LEECH_LOG to Use it")
    rpy_mssg_id = None
    if USER_DTS:
        text__, txtCancel = getDetails(client, message, 'Rename')
        await message.reply_text(text=text__, parse_mode=enums.ParseMode.HTML, quote=True, disable_web_page_preview=True)
        endText = f"\n📬 <b>Source :</b> <a href='{message.link}'>Click Here</a>\n\n#LeechStart #FXLogs"
        if not txtCancel:
            if LEECH_LOG and message.chat.id not in EXCEP_CHATS:
                text__ += endText
                logs_msg = await client.send_message(chat_id=int(LEECH_LOG), text=text__, parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
                rpy_mssg_id = logs_msg.id
            LOGGER.info(f"Leech Started : {tag_me}")

    if not message.reply_to_message:
        await message.reply("<b>⚠️ Opps ⚠️</b>\n\n <b><i>⊠ Reply with Telegram Media (File / Video)⁉️</b>", quote=True)
        return

    if len(message.command) > 1:
        new_name = (
            str(Path().resolve()) + "/" +
            message.text.split(" ", maxsplit=1)[1].strip()
        )
        file, mess_age = await download_tg(client, message)
        try:
            if file:
                orename(file, new_name)
            else:
                return
        except Exception as g_g:
            LOGGER.error(f'Rename Error :{g_g}')
        response = {}
        start_upload = time()
        final_response = await upload_to_tg(
            mess_age, new_name, usr_id, response, client
        )
        end_upload = time()
        if not final_response:
            return
        try:
            timeuti = TimeFormatter((end_upload - start_upload) * 1000)
            mention_req_user = ((BotTheme(usr_id)).TOP_LIST_FILES_MSG).format(
                user_id = usr_id,
                u_men = tag_me,
                timeuti = timeuti
            )
            message_credits = ((BotTheme(usr_id)).BOTTOM_LIST_FILES_MSG).format(
                UPDATES_CHANNEL = UPDATES_CHANNEL
            )
            message_to_send = ""
            for key_f_res_se in final_response:
                local_file_name = key_f_res_se
                message_id = final_response[key_f_res_se]
                channel_id = str(LEECH_LOG)[4:] if LEECH_LOG and user_message.chat.id not in EXCEP_CHATS else str(message.chat.id)[4:]
                private_link = f"https://t.me/c/{channel_id}/{message_id}"
                message_to_send += ((BotTheme(usr_id)).SINGLE_LIST_FILES_MSG).format(
                    private_link = private_link,
                    local_file_name = local_file_name
                )
            if message_to_send == "":
                message_to_send = "<i>FAILED</i> \n\nCheck Logs and Try Again Later !!. "
            await __sendSpecificLogMsg(client, message, mention_req_user, message_to_send, message_credits, rpy_mssg_id)
        except Exception as pe:
            LOGGER.info(pe)

    else:
        await message.reply_text(text=(BotTheme(usr_id)).WRONG_RENAME_MSG,
           quote=True
        )
