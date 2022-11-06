#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52 | MaxxRider | 5MysterySD
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved

import sys, aria2p
from datetime import datetime, timedelta
from urllib.request import urlretrieve 
from asyncio import create_subprocess_exec, subprocess, sleep as asleep
from os import path as opath, rename as orename, walk as owalk
from time import sleep as tsleep, time
from aria2p import API as ariaAPI, Client as ariClient
from subprocess import check_output
from natsort import natsorted
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from pyrogram.errors import FloodWait, MessageNotModified

from tobrot import ARIA_TWO_STARTED_PORT, CUSTOM_PREFIX, CUSTOM_SUFFIX, EDIT_SLEEP_TIME_OUT, LOGGER, UPDATES_CHANNEL, \
                   MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START, CLONE_COMMAND_G, user_settings_lock, user_settings, LEECH_LOG, \
                   BOT_PM, LEECH_INVITE, EXCEP_CHATS
from tobrot.helper_funcs.create_compressed_archive import create_archive, get_base_name, unzip_me
from tobrot.helper_funcs.upload_to_tg import upload_to_gdrive, upload_to_tg
from tobrot.helper_funcs.download import download_tg
from tobrot.bot_theme.themes import BotTheme
from tobrot.helper_funcs.direct_link_generator import url_link_generate
from tobrot.helper_funcs.exceptions import DirectDownloadLinkException
from tobrot.plugins import getUserOrChaDetails
from tobrot.plugins.custom_utils import *
from tobrot.plugins import is_appdrive_link, is_gdtot_link, is_hubdrive_link 
from tobrot.helper_funcs.display_progress import TimeFormatter

sys.setrecursionlimit(10 ** 4)

async def aria_start():
    TRACKERS = check_output("curl -Ns https://raw.githubusercontent.com/XIU2/TrackersListCollection/master/all.txt https://ngosang.github.io/trackerslist/trackers_all_http.txt https://newtrackon.com/api/all https://raw.githubusercontent.com/hezhijie0327/Trackerslist/main/trackerslist_tracker.txt | awk '$0' | tr '\n\n' ','", shell=True).decode('utf-8').rstrip(',')
    aria2_daemon_start_cmd = ["chrome", "--conf-path=/app/tobrot/aria2/aria2.conf", f"--rpc-listen-port={ARIA_TWO_STARTED_PORT}", f"--bt-stop-timeout={MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START}", f"--bt-tracker=[{TRACKERS}]"]
    #f"--dir={DOWNLOAD_LOCATION}", "--disk-cache=0", "--seed-ratio=0.01"
    LOGGER.info("[ARIA2C] Daemon Initiated ")

    process = await create_subprocess_exec(
        *aria2_daemon_start_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()

    return ariaAPI(
        ariClient(
            host="http://localhost", port=ARIA_TWO_STARTED_PORT, secret=""
        )
    )

def __changeFileName(to_upload_file, u_id):
    global CUSTOM_PREFIX, CUSTOM_SUFFIX
    preDicData = PRE_DICT.get(u_id, ["", "", "", 0, ""])
    prefix, filename_, suffix, no, filter = preDicData[0], preDicData[1], preDicData[2], preDicData[3], preDicData[4]
    if CUSTOM_PREFIX: prefix = CUSTOM_PREFIX
    if CUSTOM_SUFFIX: suffix = CUSTOM_SUFFIX
    if filter:
        if not filter.startswith("|"):
            filter = f"|{filter}"
        slit = filter.split("|")
        if opath.isfile(to_upload_file):
            __newFileName = to_upload_file
            for rep in range(1, len(slit)):
                args = slit[rep].split(":")
                if len(args) == 3:
                    __newFileName = __newFileName.replace(args[0], args[1], int(args[2]))
                else:
                    __newFileName = __newFileName.replace(args[0], args[1])
            orename(to_upload_file, __newFileName)
            to_upload_file = __newFileName
        else:
            for root, _, files in owalk(to_upload_file):
                for org in files:
                    p_name = f"{root}/{org}"
                    __newFileName = org
                    for rep in range(1, len(slit)):
                        args = slit[rep].split(":")
                        if len(args) == 3:
                            __newFileName = __newFileName.replace(args[0], args[1], int(args[2]))
                        else:
                            __newFileName = __newFileName.replace(args[0], args[1])
                    n_name = f"{root}/{__newFileName}"
                    orename(p_name, n_name)

    if filename_:
        if not opath.isfile(to_upload_file):
            for root, _, files in owalk(to_upload_file):
                n = int(no)
                for org in natsorted(files):
                    p_name = f"{root}/{org}"
                    n += 1
                    n_name = f"{root}/{filename_.format(no = '%.2d' % n)}"
                    orename(p_name, n_name)
    elif prefix:
        if opath.isfile(to_upload_file):
            if not to_upload_file.startswith(prefix):
                orename(to_upload_file, f"{prefix}{to_upload_file}")
                to_upload_file = f"{prefix}{to_upload_file}"
        else:
            for root, _, files in owalk(to_upload_file):
                for org in files:
                    p_name = f"{root}/{org}"
                    if not org.startswith(prefix):
                        n_name = f"{root}/{prefix}{org}"
                        orename(p_name, n_name)
    elif suffix:
     # <!--- Total Code Made by 5MysterySD, Give Credits at least !! --->
        sufLen = len(suffix)
        if opath.isfile(to_upload_file):
            fileDict = to_upload_file.split('.')
            _extIn = 1 + len(fileDict[-1])
            _extOutName = '.'.join(fileDict[:-1]).replace('.', '_').replace('-', '_')
            if not _extOutName.endswith(suffix):
                _extOutName += suffix
                _newExtFileName = f"{_extOutName}{suffix}.{fileDict[-1]}"
                if len(_extOutName) > (64 - (sufLen + _extIn)):
                    _newExtFileName = (
                        _extOutName[: 64 - (sufLen + _extIn)]
                        + f"{suffix}.{fileDict[-1]}"
                    )

                orename(to_upload_file, _newExtFileName)
                to_upload_file = _newExtFileName
        else:
            for root, _, files in owalk(to_upload_file):
                for org in files:
                    p_name = f"{root}/{org}"
                    fileDict = org.split('.')
                    _extIn = 1 + len(fileDict[-1])
                    _extOutName = '.'.join(fileDict[:-1]).replace('.', '_').replace('-', '_')
                    if not _extOutName.endswith(suffix):
                        _extOutName += suffix
                        _newExtFileName = f"{root}/{_extOutName}{suffix}.{fileDict[-1]}"
                        if len(_extOutName) > (64 - (sufLen + _extIn)):
                            _newExtFileName = f"{root}/{_extOutName[:64 - (sufLen + _extIn)]}{suffix}.{fileDict[-1]}"

                        orename(p_name, _newExtFileName)
    return to_upload_file

def add_magnet(aria_instance, magnetic_link, c_file_name, user_msg):
    options = None
    try:
        download = aria_instance.add_magnet(magnetic_link, options=options)
        with user_settings_lock:
            user_settings[download.gid] = user_msg
    except Exception as e:
        return False, f"⛔ **FAILED** ⛔ \n\n<b>⌧ Your link is Dead Maybe ⚰ .\n{e}</b>"
    else:
        return True, download.gid

def add_torrent(aria_instance, torrent_file_path, user_msg):
    if torrent_file_path is None:
        return False, "⛔ **FAILED** ⛔\n\n⌧ <i>Something went Wrong when trying to add <u>TORRENT</u> file to Status.</i>"
    if opath.exists(torrent_file_path):
        try:
            download = aria_instance.add_torrent(torrent_file_path, uris=None, options=None, position=None)
            with user_settings_lock:
                user_settings[download.gid] = user_msg
        except Exception as e:
            return False, f"⛔ **FAILED** ⛔ \n\n<b>⌧ Your Link is Slow to Process .</b>\n⌧ {e}"
        else:
            return True, download.gid
    elif (torrent_file_path.lower()).startswith("https") and (not opath.exists(torrent_file_path)):
        torrent_file_name = (torrent_file_path.split('/'))[-1]
        urlretrieve(torrent_file_path, f"/app/{torrent_file_name}")
        try:
            sagtus, err_message = add_torrent(aria_instance, torrent_file_name, user_msg)
        except Exception as e:
            return False, f"⛔ **FAILED** ⛔ \n\n<b>⌧ Your Link is Slow to Process .</b>\n⌧ {e}"
        else:
            return True, err_message
    else:
        return False, "⛔ **FAILED** ⛔ \n⌧ Please try other sources to get workable link to Process . . ."

def add_url(aria_instance, text_url, c_file_name, user_msg):
    options = None
    uris = None
    if "zippyshare.com" in text_url \
        or "osdn.net" in text_url \
        or "mediafire.com" in text_url \
        or "https://uptobox.com" in text_url \
        or "cloud.mail.ru" in text_url \
        or "github.com" in text_url \
        or "yadi.sk" in text_url  \
        or "hxfile.co" in text_url  \
        or "https://anonfiles.com" in text_url  \
        or "letsupload.io" in text_url  \
        or "fembed.net" in text_url  \
        or "fembed.com" in text_url  \
        or "femax20.com" in text_url  \
        or "fcdn.stream" in text_url  \
        or "feurl.com" in text_url  \
        or "naniplay.nanime.in" in text_url  \
        or "naniplay.nanime.biz" in text_url  \
        or "naniplay.com" in text_url  \
        or "layarkacaxxi.icu" in text_url  \
        or "sbembed.com" in text_url  \
        or "streamsb.net" in text_url  \
        or "sbplay.org" in text_url  \
        or "1drv.ms" in text_url  \
        or "pixeldrain.com" in text_url  \
        or "antfiles.com" in text_url  \
        or "streamtape.com" in text_url  \
        or "https://bayfiles.com" in text_url  \
        or "1fichier.com" in text_url  \
        or "solidfiles.com" in text_url  \
        or "krakenfiles.com" in text_url  \
        or "gplinks.co" in text_url  \
        or "racaty.net" in text_url:
            try:
                urisitring = url_link_generate(text_url)
                uris = [urisitring]
            except DirectDownloadLinkException as e:
                LOGGER.info(f'{text_url}: {e}')
    elif "drive.google.com" in text_url:
        return False, f"⛔ **FAILED** ⛔ \n\n⌧ <i>Please do not send Drive links to Process with this Command. Use /{CLONE_COMMAND_G} for Cloning the Link, then Use the Index Link !!</i>"
    elif "mega.nz" in text_url or "mega.co.nz" in text_url:
        return False, "⛔ **FAILED** ⛔ \n\n⌧ <i>Please do not send Mega links . I am yet not able to Process Those !!</i>"
    elif is_gdtot_link(text_url) or is_hubdrive_link(text_url) or is_appdrive_link(text_url):
        return False, "⛔ **FAILED** ⛔ \n\n⌧ <i>Please Use /parser to Process the Links.</i>"
    else:
        uris = [text_url]

    try:
        download = aria_instance.add_uris(uris, options=options)
        with user_settings_lock:
            user_settings[download.gid] = user_msg
    except Exception as e:
        return False, f"⛔ **FAILED** ⛔ \n\n⌧ <i>Please do not send Slow links to Process.</i>\n{e}"
    else:
        return True, download.gid

async def call_apropriate_function(
    aria_instance,
    incoming_link,
    c_file_name,
    sent_message_to_update_tg_p,
    is_zip,
    cstom_file_name,
    is_cloud,
    is_unzip,
    is_file,
    user_message,
    client,
    rpy_mssg_id=None
):
    if not is_file:

        if incoming_link.lower().startswith("magnet:"):
            sagtus, err_message = add_magnet(aria_instance, incoming_link, c_file_name, user_message)
        elif incoming_link.lower().endswith(".torrent"):
            sagtus, err_message = add_torrent(aria_instance, incoming_link, user_message)
        else:
            sagtus, err_message = add_url(aria_instance, incoming_link, c_file_name, user_message)

        if not sagtus:
            return sagtus, err_message
        LOGGER.info(err_message)

        await check_progress_for_dl(
            aria_instance, err_message, sent_message_to_update_tg_p, None, user_message
        )
        if incoming_link.startswith("magnet:"):
            err_message = await check_metadata(aria_instance, err_message)
            await asleep(1)
            if err_message is not None:
                await check_progress_for_dl(
                    aria_instance, err_message, sent_message_to_update_tg_p, None, user_message
                )
            else:
                return False, "can't get metadata \n\n#MetaDataError"
        await asleep(1)
        try:
            file = aria_instance.get_download(err_message)
        except aria2p.client.ClientException as ee:
            LOGGER.error(ee)
            return True, None
        to_upload_file = file.name
        com_g = file.is_complete
    else:
        await sent_message_to_update_tg_p.delete()
        to_upload_file, sent_message_to_update_tg_p = await download_tg(client=client, message=user_message)
        if not to_upload_file:
            return True, None
        com_g = True

    LOGGER.info(f" Zip : {is_zip}")
    LOGGER.info(f" UnZip : {is_unzip}")

    if is_zip:
        check_if_file = await create_archive(to_upload_file)
        if check_if_file is not None:
            to_upload_file = check_if_file

    if is_unzip:
        try:
            check_ifi_file = get_base_name(to_upload_file)
            await unzip_me(to_upload_file)
            if opath.exists(check_ifi_file):
                to_upload_file = check_ifi_file
        except Exception as ge:
            LOGGER.info(ge)
            LOGGER.info(
                f"Can't extract {opath.basename(to_upload_file)}, Uploading the same file"
            )
    u_id, u_men = getUserOrChaDetails(user_message)
    if to_upload_file:
        to_upload_file = __changeFileName(to_upload_file, u_id)
    if cstom_file_name:
        orename(to_upload_file, cstom_file_name)
        to_upload_file = cstom_file_name

    response = {}
    if com_g:
        if is_cloud:
            await upload_to_gdrive(
                to_upload_file, sent_message_to_update_tg_p, user_message, u_id
            )
        else:
            start_upload = time()
            final_response = await upload_to_tg(
                sent_message_to_update_tg_p, to_upload_file, u_id, response, client
            )
            end_upload = time()
            if not final_response:
                return True, None
            try:
                timeuti = TimeFormatter((end_upload - start_upload) * 1000)
                message_to_send = ""
                mention_req_user = ((BotTheme(u_id)).TOP_LIST_FILES_MSG).format(
                    user_id = u_id,
                    u_men = u_men,
                    timeuti = timeuti
                )                
                message_credits = ((BotTheme(u_id)).BOTTOM_LIST_FILES_MSG).format(
                    UPDATES_CHANNEL = UPDATES_CHANNEL
                )
                for key_f_res_se in final_response:
                    local_file_name = key_f_res_se
                    message_id = final_response[key_f_res_se]
                    channel_id = str(LEECH_LOG)[4:] if LEECH_LOG and user_message.chat.id not in EXCEP_CHATS else str(sent_message_to_update_tg_p.chat.id)[4:]
                    private_link = f"https://t.me/c/{channel_id}/{message_id}"
                    message_to_send += ((BotTheme(u_id)).SINGLE_LIST_FILES_MSG).format(
                        private_link = private_link,
                        local_file_name = local_file_name
                    )
                    if len(mention_req_user.encode('utf-8') + message_to_send.encode('utf-8') + message_credits.encode('utf-8')) > 4000:
                        tsleep(1.5)
                        await __sendSpecificLogMsg(client, user_message, mention_req_user, message_to_send, message_credits, u_id, rpy_mssg_id)
                        message_to_send = ""
                if message_to_send != "":
                    tsleep(1.5)
                    await __sendSpecificLogMsg(client, user_message, mention_req_user, message_to_send, message_credits, u_id, rpy_mssg_id)
            except Exception as go:
                LOGGER.error(go)
    return True, None

async def __sendSpecificLogMsg(client, user_message, req, send, cred, u_id, rpy_mssg_id=None):
    if LEECH_LOG and str(user_message.chat.id) not in str(EXCEP_CHATS):
        log_txt = "┃ <b>♻️ File(s) are Uploaded on Leech Log Channel, Check Down to View.</b>\n"
        if BOT_PM: 
            log_txt += "┃ <b>🖨 Requested Leeched File are Sent to User PM.</b>\n"
            await client.send_message(chat_id=u_id, text=req + "┃ <b>🛰 Your Leeched Files are Send above </b>\n" + cred, disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)
        leech_msg = await client.send_message(chat_id=int(LEECH_LOG), text=req + send + cred, disable_web_page_preview=True, reply_to_message_id=rpy_mssg_id, parse_mode=enums.ParseMode.HTML)
        inbtns = [
            [InlineKeyboardButton("Gᴇᴛ Lᴇᴇᴄʜᴇᴅ Fɪʟᴇs", url=leech_msg.link)]
        ]
        if LEECH_INVITE.lower() == "true":
            leech_link = await client.create_chat_invite_link(chat_id=int(LEECH_LOG), name=f"{UPDATES_CHANNEL} Tele-LeechX Invite Link", member_limit=10, expire_date=datetime.now() + timedelta(days=1))
            inbtns[0].insert(1, InlineKeyboardButton("Jᴏɪɴ Lᴇᴇᴄʜ Lᴏɢ", url=leech_link.invite_link))
        await user_message.reply_text(text=req + log_txt + cred, disable_web_page_preview=True, quote=True, parse_mode=enums.ParseMode.HTML, reply_markup=InlineKeyboardMarkup(inbtns))
    else:
        await user_message.reply_text(text=req + send + cred, disable_web_page_preview=True, quote=True, parse_mode=enums.ParseMode.HTML)

async def check_progress_for_dl(aria2, gid, event, previous_message, user_message):
    while True:
        try:
            file = aria2.get_download(gid)
            complete = file.is_complete
            is_file = file.seeder
            if not complete:
                if not file.error_message:
                    if file.has_failed:
                        LOGGER.info(f"⛔ Cancel Downloading . .⛔ \n\n ⌧ <i>FileName: `{file.name}` \n⌧ May Be Due to Slow Torrent (Less Seeds to Process).</i>")
                        await event.reply(
                            f"⛔ Download Cancelled ⛔ :\n\n⌧ <i>FileName: </i><code>{file.name}</code>\n\n #MetaDataError", quote=True
                        )
                        file.remove(force=True, files=True)
                        return
                else:
                    msg = file.error_message
                    LOGGER.info(msg)
                    await asleep(EDIT_SLEEP_TIME_OUT)
                    await event.reply(f"`{msg}`")
                    return
                await asleep(EDIT_SLEEP_TIME_OUT)
                # await check_progress_for_dl(aria2, gid, event, previous_message)
            else:
                LOGGER.info(
                    f"Downloaded Successfully : `{file.name} ({file.total_length_string()})` "
                )
                u_id, _ = getUserOrChaDetails(user_message)
                if not file.is_metadata:
                    await event.edit(((BotTheme(u_id)).DOWN_COM_MSG).format(
                        filename = file.name,
                        size = file.total_length_string()
                    ))
                return
        except aria2p.client.ClientException:
            await event.reply(f"<i>⛔ Download Cancelled ⛔</i> :\n<code>{file.name} ({file.total_length_string()})</code>", quote=True)
            return
        except MessageNotModified as ep:
            LOGGER.info(ep)
            await asleep(EDIT_SLEEP_TIME_OUT)
            # await check_progress_for_dl(aria2, gid, event, previous_message)
            return
        except FloodWait as e:
            LOGGER.info(f"FloodWait : Sleeping {e.value}s")
            tsleep(e.value)
        except Exception as e:
            LOGGER.info(str(e))
            if "not found" in str(e) or "'file'" in str(e):
                await event.edit(
                    f"<i>⛔ Download Cancelled ⛔</i> :\n<code>{file.name} ({file.total_length_string()})</code>"
                )
            else:
                LOGGER.info(str(e))
                await event.edit(f"⛔ <u>ERROR</u> ⛔ :\n<code>{e}</code> \n\n#Error")

            return

async def check_metadata(aria2, gid):
    file = aria2.get_download(gid)

    if not file.followed_by_ids:
        return None
    new_gid = file.followed_by_ids[0]
    with user_settings_lock:
        user_settings[new_gid] = user_settings.pop(gid)
    LOGGER.info(f"Changing GID : {gid} to {new_gid}")
    return new_gid
