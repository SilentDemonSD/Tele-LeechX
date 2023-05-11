#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) SilentDemonSD
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/SilentDemonSD/Tele-LeechX >
# All Right Reserved

import os
from re import split as rsplit
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from pyrogram import enums, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from TeleLX import LOGGER, user_doc, DB_URI, PRE_DICT, CAP_DICT, IMDB_TEMPLATE, ANILIST_TEMPLATE, USER_LOGS, DL_DIR
from TeleLX.core.database.mongodb import DatabaseManager
from TeleLX.core.bot_theme.themes import BotTheme
from TeleLX.plugins import getUserOrChaDetails

async def upload_as_doc(client, message):
    uid, u_tag = getUserOrChaDetails(message)
    user_doc[uid] = True
    if DB_URI:
        DatabaseManager().user_doc(uid)
        LOGGER.info("[DB] User Toggle DOC Settings Saved to Database")
    await message.reply_text(((BotTheme(uid)).TOGGLEDOC_MSG).format(
        u_men = u_tag,
        u_id = uid,
        UPDATES_CHANNEL = UPDATES_CHANNEL
    ))

async def upload_as_video(client, message):
    uid, u_tag = getUserOrChaDetails(message)
    user_doc[uid] = False
    if DB_URI:
        DatabaseManager().user_vid(uid)
        LOGGER.info("[DB] User Toggle VID Settings Saved to Database")
    await message.reply_text(((BotTheme(uid)).TOGGLEVID_MSG).format(
        u_men = u_tag,
        u_id = uid,
        UPDATES_CHANNEL = UPDATES_CHANNEL
    ))

async def prefix_set(client, message):
    '''/setpre command '''
    lm = await message.reply_text("`Setting Up ...`")
    user_id_, u_men = getUserOrChaDetails(message)
    pre_send = message.text.split(" ", maxsplit=1)
    reply_to = message.reply_to_message
    if len(pre_send) > 1:
        txt = pre_send[1]
    elif reply_to is not None:
        txt = reply_to.text
    else:
        txt = ""
    prefix_ = txt
    if prefix_ != '':
        prefix_ = rsplit(r'c:|s:|no:|\|', prefix_)[0].strip()

    preCus = txt.split('c: ')
    if len(preCus) > 1:
        preCus = preCus[1]
        fname = preCus.split('s:')[0].strip()
    else:
        fname = ""
    preSuf = txt.split('s: ')
    if len(preSuf) > 1:
        preSuf = preSuf[1]
        suffix = preSuf.split('no:')[0]
    else:
        suffix = ""
    preNo = txt.split('no: ')
    if len(preNo) > 1:
        preNo = preNo[1]
        no = preNo.split('|', 1)[0].strip()
    else:
        no = '0'
    preRep = txt.split('|', 1)
    args = preRep[1] if len(preRep) > 1 else ""
    tData = [prefix_, fname, suffix, no, args]
    PRE_DICT[user_id_] = tData
    if DB_URI:
        DatabaseManager().user_pre(user_id_, tData)
        LOGGER.info(f"[DB] User : {user_id_} Prefix Saved to Database")

    pre_text = await lm.edit_text(((BotTheme(user_id_)).PREFIX_MSG).format(
            u_men = u_men,
            uid = user_id_,
            t = txt
        ), 
        parse_mode=enums.ParseMode.HTML
    )


async def caption_set(client, message):
    '''  /setcap command '''

    lk = await message.reply_text("`Setting Up ...`")
    user_id_, u_men = getUserOrChaDetails(message)
    cap_send = message.text.split(" ", maxsplit=1)
    reply_to = message.reply_to_message
    if len(cap_send) > 1:
        txt = cap_send[1]
    elif reply_to is not None:
        txt = reply_to.text
    else:
        txt = ""
    caption_ = txt
    CAP_DICT[user_id_] = caption_
    if DB_URI:
        DatabaseManager().user_cap(user_id_, caption_)
        LOGGER.info(f"[DB] User : {user_id_} Caption Saved to Database")
    try:
        txx = txt.split("#", maxsplit=1)
        txt = txx[0]
    except:
        pass 
    cap_text = await lk.edit_text(((BotTheme(user_id_)).CAPTION_MSG).format(
            u_men = u_men,
            uid = user_id_,
            t = txt
        ),
        parse_mode=enums.ParseMode.HTML
    )


async def template_set(client, message):
    '''  /set_template command '''
    lm = await message.reply_text(
        text="`Checking Input ...`",
    )
    user_id_, u_men = getUserOrChaDetails(message)
    tem_send = message.text.split(" ", maxsplit=1)
    reply_to = message.reply_to_message
    if len(tem_send) > 1:
        txt = tem_send[1]
    elif reply_to is not None:
        txt = reply_to.text
    else:
        txt = ""
    template_ = txt
    IMDB_TEMPLATE[user_id_] = template_
    if DB_URI:
        DatabaseManager().user_imdb(user_id_, template_)
        LOGGER.info(f"[DB] User : {user_id_} IMDB Template Saved to Database")
    await lm.edit_text(((BotTheme(user_id_)).IMDB_MSG).format(
            u_men = u_men,
            uid = user_id_,
            t = txt
        ),
        parse_mode=enums.ParseMode.HTML
    )

async def anilist_set(client, message):
    '''  /anime_template command '''
    lm = await message.reply_text("`Checking HTML Input ...`")
    user_id_, u_men = getUserOrChaDetails(message)
    tem_send = message.text.split(" ", 1)
    reply_to = message.reply_to_message
    if len(tem_send) > 1:
        txt = tem_send[1]
    elif reply_to is not None:
        txt = reply_to.text
    else:
        txt = ""
    ani_template_ = txt
    ANILIST_TEMPLATE[user_id_] = ani_template_
    #if DB_URI:
    #    DatabaseManager().user_anilist(user_id_, ani_template_)
    #    LOGGER.info(f"[DB] User : {user_id_} AniList Anime Template Saved to Database")
    await lm.edit_text(((BotTheme(user_id_)).IMDB_MSG).format(
            u_men = u_men,
            uid = user_id_,
            t = txt
        ),
        parse_mode=enums.ParseMode.HTML
    )

async def theme_set(client, message):
    '''  /choosetheme command '''
    lk = await message.reply_text(
        text="`Fetching Current Themes ...`",
    )
    user_id_, u_men = getUserOrChaDetails(message)

    theme_btn = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "fx-optimised-theme",
                    callback_data=f"theme {user_id_} fx-optimised-theme",
                )
            ],
            [
                InlineKeyboardButton(
                    "fx-minimal-theme",
                    callback_data=f"theme {user_id_} fx-minimal-theme",
                )
            ],
            [
                InlineKeyboardButton(
                    "fx-random-theme",
                    callback_data=f"theme {user_id_} fx-random-theme",
                )
            ],
            [InlineKeyboardButton("⛔️ Close ⛔️", callback_data="close")],
        ]
    )
    await lk.edit_text(((BotTheme(user_id_)).THEME_MSG).format(
            u_men = u_men,
            uid = user_id_
        ),
        parse_mode=enums.ParseMode.HTML, 
        reply_markup=theme_btn
    )

async def user_log_set(client: Client, message: Message):
    '''  /userlog command '''
    lm = await message.reply_text("`Checking Log Channel ID...`")
    user_id_, u_men = getUserOrChaDetails(message)
    tem_send = message.text.split(" ", 1)
    reply_to = message.reply_to_message
    if len(tem_send) > 1:
        id = tem_send[1]
    elif reply_to is not None:
        id = reply_to.text
    else:
        await lm.edit_text("<i>Give Channel ID Along /userlog -100xxxxxxxx</i>")
        return
    if not id.startswith('-100'):
        await lm.edit_text("<i><b>Your Channel ID Should Start with</b> -100xxxxxxxx, <u>Retry Again</u> !!</i>")
        return
    user_log_ = int(id.strip())
    try:
        await lm.edit_text("<i>Checking Your Channel Interaction ...</i>")
        await client.send_message(user_log_, text=f'''<b>ᑌՏᗴᖇ ᒪOᘜ ᑕᕼᗩᑎᑎᗴᒪ :</b>
┃
┣ 🆔 <b>Log Chat ID :</b> <code>{user_log_}</code>
┃
┗ 📂 <i>From Now On, The Bot will Send you Files in this Channel !!</i>''')
    except Exception as err:
        await lm.edit_text(f"<i>Make Sure You have Added the Bot as Admin with Post Permission, Retry Again.</i>\n\nError : {err}")
        return
    USER_LOGS[user_id_] = user_log_
    #if DB_URI:
    #    DatabaseManager().user_log(user_id_, user_log_)
    #    LOGGER.info(f"[DB] User : {user_id_} Log Channel Saved to Database")
    await lm.edit_text(f'''⚡️Custom Log Channel Set Successfully⚡️ 

👤 <b>User :</b> {u_men} ( #ID{user_id_} )
🏷 <b>User Log Channel ID :</b> <code>{user_log_}</code>''',
        parse_mode=enums.ParseMode.HTML
    )

async def save_thumb_nail(client, message):
    uid, _ = getUserOrChaDetails(message)
    thumbnail_location = os.path.join(DL_DIR, "thumbnails")
    thumb_image_path = os.path.join(thumbnail_location, f"{str(uid)}.jpg")
    ismgs = await message.reply_text((BotTheme(uid)).THUMB_REPLY)
    if message.reply_to_message is not None:
        if not os.path.isdir(thumbnail_location):
            os.makedirs(thumbnail_location)
        DL_DIR = f"{thumbnail_location}/"
        downloaded_file_name = await client.download_media(
            message=message.reply_to_message, file_name=DL_DIR
        )
        Image.open(downloaded_file_name).convert("RGB").save(downloaded_file_name)
        metadata = extractMetadata(createParser(downloaded_file_name))
        height = metadata.get("height") if metadata.has("height") else 0
        img = Image.open(downloaded_file_name)
        img.resize((320, height))
        img.save(thumb_image_path, "JPEG")
        os.remove(downloaded_file_name)
        if DB_URI is not None:
            DatabaseManager().user_save_thumb(uid, thumb_image_path)
            LOGGER.info("[DB] User Thumbnail Saved in Database")
        await ismgs.edit((BotTheme(uid)).SAVE_THUMB_MSG)
    else:
        await ismgs.edit((BotTheme(uid)).SAVE_THUMB_FAIL_MSG)

async def clear_thumb_nail(client, message):
    uid, _ = getUserOrChaDetails(message)
    thumbnail_location = os.path.join(DL_DIR, "thumbnails")
    thumb_image_path = os.path.join(thumbnail_location, f"{str(uid)}.jpg")
    ismgs = await message.reply_text((BotTheme(uid)).THUMB_REPLY)
    if os.path.exists(thumb_image_path):
        os.remove(thumb_image_path)
        if DB_URI is not None:
            DatabaseManager().user_rm_thumb(uid, thumb_image_path)
            LOGGER.info("[DB] User Thumbnail Removed from Database")
        await ismgs.edit((BotTheme(uid)).CLEAR_THUMB_SUCC_MSG)
    else:
        await ismgs.edit((BotTheme(uid)).CLEAR_THUMB_FAIL_MSG)

async def log_chat_id(c: Client, m: Message):
    '''  /id command  '''
    await m.reply_text(f"<b>Log Channel ID :</b> <code>{m.chat.id}</code>", quote=True)

async def user_settings(client: Client, message: Message):
    uid, _ = getUserOrChaDetails(message)
    to_edit = await message.reply_text('Fetching your Details . . .')
    lcode = message.from_user.language_code
    did = message.from_user.dc_id
    __theme = USER_THEMES.get(uid, 'Default Bot Theme')
    __text = f'''┏━ 𝙐𝙨𝙚𝙧 𝙎𝙚𝙩𝙩𝙞𝙣𝙜𝙨 ━━╻
┃
┃• ᑌՏᗴᖇ ᗪᗴTᗩIᒪՏ :
┣ 👤 User : {message.from_user.first_name}
┣ 🖋 Username : @{message.from_user.username}
┣ 🆔 User ID : #ID{uid}
┣ 🌐 DC ID : {did if did else ''}
┣ 🔡 Language Code : {lcode.upper() if lcode else '-'}
┣ 💸 Premium : {str(message.from_user.is_premium).capitalize()}
┃
┗━━━━━━━━━━━━━━╹
'''
    set_btn = InlineKeyboardMarkup([
        [InlineKeyboardButton("✏️ Prefix", callback_data = f"setpre {uid}"),
        InlineKeyboardButton("🗃 Theme", callback_data = f"settheme {uid}"),
        InlineKeyboardButton("🔖 Caption", callback_data = f"setcap {uid}")],
        [InlineKeyboardButton("📒 IMDB", callback_data = f"setimdb {uid}"),
        InlineKeyboardButton("📘 AniList", callback_data = f"setani {uid}"),
        InlineKeyboardButton("🖼 Thumb", callback_data = f"setthumb {uid}")],
        [InlineKeyboardButton("📩 Upload Type", callback_data = f"setupload {uid}"),
        InlineKeyboardButton(f"{'🔋' if AUTO_LEECH else '🪫'} Auto Leech", callback_data = f"setauto {uid}")],
        [InlineKeyboardButton("🚛 User Log Channel", callback_data = f"setlog {uid}")]
    ])
    await to_edit.delete()
    await message.reply_photo(photo = 'https://te.legra.ph/file/a3dea655deb2a6f213813.jpg', caption=__text, parse_mode=enums.ParseMode.HTML, reply_markup=set_btn)

async def settings_callback(client, query: CallbackQuery):
    getData = (query.data).split(" ")
    usid = int(getData[1])
    if query.from_user.id != usid:
        await query.answer(text="Why Messing with Others Settings ??", show_alert=True)
        return
    if query.data.startswith("setthumb"):
        thumb_path = f'{DL_DIR}/thumbnails/{getData[1]}.jpg'
        if not opath.exists(thumb_path):
            _text = '''• ᑌՏᗴᖇ TᕼᑌᗰᗷᑎᗩIᒪ :
┃
┗ <b>User Thumbnail :</b> <code>Not Set Yet !</code>'''
            await query.edit_message_caption(caption=_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⌫ Back", callback_data = f"sethome {usid} thumb")]]))
        else:
            _text = '''• ᑌՏᗴᖇ TᕼᑌᗰᗷᑎᗩIᒪ :
┃
┗ <b>User Thumbnail :</b> <code>Already have A Custom Thumbnail !</code>'''
            await query.edit_message_media(media=InputMediaPhoto(media=thumb_path, caption=_text), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⌫ Back", callback_data = f"sethome {usid} thumb")]]))
    elif query.data.startswith("setimdb"):
        __template = IMDB_TEMPLATE.get(usid, "Default IMDB Template")
        _text = f'''• ᑌՏᗴᖇ Iᗰᗪᗷ TᗴᗰᑭᒪᗩTᗴ :
┃
┗ **User IMDB Template :**
╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾
`{__template}`
╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾'''
        await query.edit_message_caption(caption=_text, parse_mode=enums.ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⌫ Back", callback_data = f"sethome {usid}")]]))
    elif query.data.startswith("setani"):
        __template = ANILIST_TEMPLATE.get(usid, "Default AniList Template")
        _text = f'''• ᑌՏᗴᖇ ᗩᑎIᒪIՏT TᗴᗰᑭᒪᗩTᗴ :
┃
┗ **User AniList Template :**
╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾
`{__template}`
╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾'''
        await query.edit_message_caption(caption=_text, parse_mode=enums.ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⌫ Back", callback_data = f"sethome {usid}")]]))
    elif query.data.startswith("setupload"):
        __toggle = user_doc.get(usid, False)
        toggle_ = 'Document' if __toggle else 'Video'
        _text = f'''• ᑌՏᗴᖇ ᑌᑭᒪOᗩᗪ TYᑭᗴ :
┃
┗ <b>User Toggle Type :</b> {toggle_}'''
        await query.edit_message_caption(caption=_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⌫ Back", callback_data = f"sethome {usid}")]]))
    elif query.data.startswith("setpre"):
        __prefix = PRE_DICT.get(usid, ["", "", "", 0, ""])
        _text = f'''• ᑌՏᗴᖇ ᑭᖇᗴᖴI᙭ ᗪᗴTᗩIᒪՏ :
┃
┣ <b>User Prefix :</b> {__prefix[0]}
┣ <b>User Suffix :</b> {__prefix[2]}
┣ <b>User Custom Batch Name :</b> {__prefix[1]}
┗ <b>User Filters :</b> {__prefix[4]}'''
        await query.edit_message_caption(caption=_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⌫ Back", callback_data = f"sethome {usid}")]]))
    elif query.data.startswith("setcap"):
        __caption = CAP_DICT.get(usid, "-")
        _text = f'''• ᑌՏᗴᖇ ᑕᗩᑭTIOᑎ ᗪᗴTᗩIᒪՏ :
┃
┣ **User Caption :** {__caption}
┗ **User Caption Filters :**'''
        await query.edit_message_caption(caption=_text, parse_mode=enums.ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⌫ Back", callback_data = f"sethome {usid}")]]))
    elif query.data.startswith("settheme"):
        __theme = USER_THEMES.get(usid, 'Default Bot Theme')
        _text = f'''• ᑌՏᗴᖇ Tᕼᗴᗰᗴ ᗪᗴTᗩIᒪՏ :
┃
┗ <b>User Bot Theme :</b> {__theme}'''
        await query.edit_message_caption(caption=_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⌫ Back", callback_data = f"sethome {usid}")]]))
    elif query.data.startswith("setauto"):
        if AUTO_LEECH:
            _auto = AUTO_USERS.get(usid, [True, None])
            _text = f'''• ᑌՏᗴᖇ ᗩᑌTO ᒪᗴᗴᑕᕼ ՏᗴTTIᑎᘜՏ :
┃
┣ <b>Auto Usage :</b> <i>♻️ Enabled ♻️</i>
┃
┣ <b>Use Leech Buttons :</b> <i>{'✅️ Enabled ✅️' if _auto[0] else '❌️ Disabled ❌️'}</i>
┗ <b>User Leech Type:</b> <i>{_auto[1].capitalize() if _auto[1] else 'Not Set !!'}</i>'''
            if _auto[0]: auto_btns = [[InlineKeyboardButton('🚫 Disable Leech Buttons 🚫', callback_data=f'setleech {usid} False')]]
            else: auto_btns = [[InlineKeyboardButton('✅️ Enable Leech Buttons ✅️', callback_data=f'setleech {usid} True')]]
        else:
            _text = '''• ᑌՏᗴᖇ ᗩᑌTO ᒪᗴᗴᑕᕼ ՏᗴTTIᑎᘜՏ :
┃
┗ <b>Auto Usage :</b> <i>⛔️ Disabled ⛔️</i>'''
        auto_btns.append([InlineKeyboardButton("⌫ Back", callback_data = f"sethome {usid}")])
        await query.edit_message_caption(caption=_text, reply_markup=InlineKeyboardMarkup(auto_btns))
    elif query.data.startswith("setleech"):
        if getData[2] == 'False':
            AUTO_USERS[usid] = [False, None]
            _text = f'{query.message.caption}\n\n<b>Choose the Leech Type from Below :</b>'
            auto_btns = [
                [InlineKeyboardButton('Leech', callback_data=f'setmystery {usid} {BotCommands.LeechCommand.lower()}'),
                InlineKeyboardButton('Extract', callback_data=f'setmystery {usid} {BotCommands.ExtractCommand.lower()}')],
                [InlineKeyboardButton('Archive', callback_data=f'setmystery {usid} {BotCommands.ArchiveCommand.lower()}')]
            ]
            if RCLONE_CONF_URL:
                auto_btns[1].insert(1, InlineKeyboardButton('GLeech', callback_data=f'setmystery {usid} {GLEECH_COMMAND.lower()}'))
                auto_btns.append(
                    [InlineKeyboardButton('GArchive', callback_data=f'setmystery {usid} {GLEECH_ZIP_COMMAND.lower()}'),
                    InlineKeyboardButton('GExtract', callback_data=f'setmystery {usid} {GLEECH_UNZIP_COMMAND.lower()}')]
                )
            auto_btns.append([InlineKeyboardButton("⌫ Back", callback_data = f"sethome {usid}")])
            await query.edit_message_caption(caption=_text, reply_markup=InlineKeyboardMarkup(auto_btns))
        elif getData[2] == 'True':
            AUTO_USERS.pop(usid)
            await query.answer(text="✅️ Your Leech Buttons Successfully Enabled ✅️ \n\n⛔️ Bulk Leech Disabled ⛔️", show_alert=True)
            _text = f'''• ᑌՏᗴᖇ ᗩᑌTO ᒪᗴᗴᑕᕼ ՏᗴTTIᑎᘜՏ :
┃
┣ <b>Auto Usage :</b> <i>♻️ Enabled ♻️</i>
┃
┣ <b>Use Leech Buttons :</b> <i>✅️ Enabled ✅️</i>
┗ <b>User Leech Type:</b> <i>Not Set !!</i>'''
            auto_btns = [[InlineKeyboardButton('🚫 Disable Leech Buttons 🚫', callback_data=f'setleech {usid} False')],
                        [InlineKeyboardButton("⌫ Back", callback_data = f"sethome {usid}")]]
            await query.edit_message_caption(caption=_text, reply_markup=InlineKeyboardMarkup(auto_btns))

    elif query.data.startswith("setmystery"):
        AUTO_USERS[usid] = [False, getData[2]]
        await query.answer(text="⛔️ Your Leech Buttons Successfully Disabled ⛔️ \n\n✅️ Bulk Leech Enabled ✅️", show_alert=True)
        _text = f'''• ᑌՏᗴᖇ ᗩᑌTO ᒪᗴᗴᑕᕼ ՏᗴTTIᑎᘜՏ :
┃
┣ <b>Auto Usage :</b> <i>♻️ Enabled ♻️</i>
┃
┣ <b>Use Leech Buttons :</b> <i>❌️ Disabled ❌️</i>
┗ <b>User Leech Type:</b> <i>{getData[2].capitalize()}</i>'''
        auto_btns = [[InlineKeyboardButton('✅️ Enable Leech Buttons ✅️', callback_data=f'setleech {usid} True')],
                    [InlineKeyboardButton("⌫ Back", callback_data = f"sethome {usid}")]]
        await query.edit_message_caption(caption=_text, reply_markup=InlineKeyboardMarkup(auto_btns))
    elif query.data.startswith("setlog"):
        __log_id = USER_LOGS.get(usid, None)
        _text = f'''• ᑌՏᗴᖇ ᒪOᘜ ᑕᕼᗩᑎᑎᗴᒪ ՏᗴTTIᑎᘜՏ :
┃
┣ <b>Log Channel Leech :</b> {'Enabled' if __log_id else 'Disabled'}
┗ <b>Log Channel ID :</b> {__log_id or '-'}'''
        log_buttons = [[InlineKeyboardButton("⌫ Back", callback_data = f"sethome {usid}")]]
        if __log_id: log_buttons[0].insert(1, InlineKeyboardButton('🚫 Disable 🚫', callback_data=f'setdislog {usid}'))
        await query.edit_message_caption(caption=_text, reply_markup=InlineKeyboardMarkup(log_buttons))
    elif query.data.startswith("setdislog"):
        USER_LOGS.pop(usid)
        await query.answer(text="✅️ Your Log Channel Is Successfully Disabled ✅️", show_alert=True)
        __log_id = USER_LOGS.get(usid, None)
        _text = f'''• ᑌՏᗴᖇ ᒪOᘜ ᑕᕼᗩᑎᑎᗴᒪ ՏᗴTTIᑎᘜՏ :
┃
┣ <b>Log Channel :</b> {'Enabled' if __log_id else 'Disabled'}
┗ <b>Log Channel ID :</b> {__log_id or '-'}'''
        log_buttons = [[InlineKeyboardButton("⌫ Back", callback_data = f"sethome {usid}")]]
        await query.edit_message_caption(caption=_text, reply_markup=InlineKeyboardMarkup(log_buttons))
    elif query.data.startswith("sethome"):
        lcode = query.from_user.language_code
        did = query.from_user.dc_id
        uid = usid
        __text = f'''┏━ 𝙐𝙨𝙚𝙧 𝙎𝙚𝙩𝙩𝙞𝙣𝙜𝙨 ━━╻
┃
┃• ᑌՏᗴᖇ ᗪᗴTᗩIᒪՏ :
┣ 👤 User : {query.from_user.first_name}
┣ 🖋 Username : @{query.from_user.username}
┣ 🆔 User ID : #ID{uid}
┣ 🌐 DC ID : {did if did else ''}
┣ 🔡 Language Code : {lcode.upper() if lcode else '-'}
┣ 💸 Premium : {str(query.from_user.is_premium).capitalize()}
┃
┗━━━━━━━━━━━━━━╹'''
        set_btn = InlineKeyboardMarkup([
        [InlineKeyboardButton("✏️ Prefix", callback_data = f"setpre {uid}"),
        InlineKeyboardButton("🗃 Theme", callback_data = f"settheme {uid}"),
        InlineKeyboardButton("🔖 Caption", callback_data = f"setcap {uid}")],
        [InlineKeyboardButton("📒 IMDB", callback_data = f"setimdb {uid}"),
        InlineKeyboardButton("📘 AniList", callback_data = f"setani {uid}"),
        InlineKeyboardButton("🖼 Thumb", callback_data = f"setthumb {uid}")],
        [InlineKeyboardButton("📩 Upload Type", callback_data = f"setupload {uid}"),
        InlineKeyboardButton(f"{'🔋' if AUTO_LEECH else '🪫'} Auto Leech", callback_data = f"setauto {uid}")],
        [InlineKeyboardButton("🚛 User Log Channel", callback_data = f"setlog {uid}")]
        ])
        if len(getData) == 3: await query.edit_message_media(media=InputMediaPhoto(media='https://te.legra.ph/file/a3dea655deb2a6f213813.jpg', caption=__text), reply_markup=set_btn)
        else: await query.edit_message_caption(caption=__text, reply_markup=set_btn)
    await query.answer()
