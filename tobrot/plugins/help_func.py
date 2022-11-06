#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) 5MysterySD | Anasty17 [MLTB]
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved

from asyncio import sleep as asleep
from os import path as opath, remove as oremove
from time import time
from telegraph import upload_file
from subprocess import check_output
from psutil import disk_usage, cpu_percent, swap_memory, cpu_count, virtual_memory, net_io_counters, boot_time
from pyrogram import enums, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto, Message

from tobrot import *
from tobrot.helper_funcs.display_progress import humanbytes, TimeFormatter
from tobrot.bot_theme.themes import BotTheme
from tobrot.helper_funcs.bot_commands import BotCommands
from tobrot.plugins import getUserOrChaDetails, progressBar

TGH_LIMIT = 5242880*2

async def stats(client: Client, message: Message):
    user_id, _ = getUserOrChaDetails(message)
    stats = (BotTheme(user_id)).STATS_MSG_1
    if opath.exists('.git'):
        last_commit = check_output(["git log -1 --date=format:'%I:%M:%S %p %d %B, %Y' --pretty=format:'%cr ( %cd )'"], shell=True).decode()
    else:
        LOGGER.info("Stats : No UPSTREAM_REPO")
        last_commit = ''
    if last_commit:
        stats += ((BotTheme(user_id)).STATS_MSG_2).format(
        lc = last_commit
    )
    currentTime = TimeFormatter((time() - BOT_START_TIME)*1000)
    osUptime = TimeFormatter((time() - boot_time())*1000)
    total, used, free, disk= disk_usage('/')
    disk_prog = progressBar(disk)
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    sent = humanbytes(net_io_counters().bytes_sent)
    recv = humanbytes(net_io_counters().bytes_recv)
    cpuUsage = cpu_percent(interval=0.5)
    cpu_prog = progressBar(cpuUsage)
    p_core = cpu_count(logical=False)
    t_core = cpu_count(logical=True)
    core_per = int(p_core)/int(t_core) * 100
    core_prog = progressBar(core_per)
    swap = swap_memory()
    swap_p = swap.percent
    swap_prog = progressBar(swap_p)
    swap_t = humanbytes(swap.total)
    swap_u = humanbytes(swap.used)
    swap_f = humanbytes(swap.free)
    memory = virtual_memory()
    mem_p = memory.percent
    mem_prog = progressBar(mem_p)
    mem_t = humanbytes(memory.total)
    mem_a = humanbytes(memory.available)
    mem_u = humanbytes(memory.used)
    UP_CHANNEL = UPDATES_CHANNEL
    stats += ((BotTheme(user_id)).STATS_MSG_3).format(**locals())
    await message.reply_text(text = stats,
        parse_mode = enums.ParseMode.HTML,
        disable_web_page_preview=True
    )

async def help_message_f(client: Client, message: Message):
    user_id, _ = getUserOrChaDetails(message)
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🆘️ Open Help 🆘️", callback_data = "openHelp_pg1")]]
    )
    await message.reply_text(
        text = ((BotTheme(user_id)).HELP_MSG).format(
        UPDATES_CHANNEL = UPDATES_CHANNEL
    ),
        reply_markup = reply_markup,
        parse_mode = enums.ParseMode.HTML,
        disable_web_page_preview=True
    )


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
        thumb_path = f'{DOWNLOAD_LOCATION}/thumbnails/{getData[1]}.jpg'
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
        __toggle = user_specific_config.get(usid, False)
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

async def picture_add(client: Client, message: Message):
    '''/addpic command'''
    editable = await message.reply_text("Checking Input ...", quote=True)
    resm = message.reply_to_message
    if resm.text:
        msg_text = resm.text
        if msg_text.startswith("http"):
            pic_add = msg_text.strip()
            await editable.edit("Adding your Link ...")
    elif resm.photo:
        if not ((resm.photo and resm.photo.file_size <= TGH_LIMIT)):
            await editable.edit("This Media is Not Supported! Only Send Photos !!")
            return
        await editable.edit("Uploading to te.legra.ph Server ...")
        df = await client.download_media(
            message=resm,
            file_name=f'{DOWNLOAD_LOCATION}/thumbnails/'
        )
        await editable.edit("`Uploading to te.legra.ph Server, Please Wait...`")
        try:
            tgh_post = upload_file(df)
            pic_add = f'https://te.legra.ph{tgh_post[0]}'
        except Exception as err:
            await editable.edit(err)
        finally:
            oremove(df)
    else:
        await editable.edit("Reply to Any Valid Photo!! Or Provide Direct DL Links of Images.")
        return
    PICS_LIST.append(pic_add)
    asleep(1.5)
    await editable.edit("<b><i>Added to Existing Random Pictures Status List!</i></b>")

async def pictures(client: Client, message: Message):
    '''/pics command'''
    if not PICS_LIST:
        await message.reply_text("Add Some Photos OR use API to Let me Show you !!")
    else:
        to_edit = await message.reply_text("Generating Grid of your Images...")
        btn = [
            [InlineKeyboardButton("<<", callback_data=f"pic -1"),
            InlineKeyboardButton(">>", callback_data="pic 1")],
            [InlineKeyboardButton("Remove Photo", callback_data="picsremove 0")]
        ]
        await to_edit.delete()
        await message.reply_photo(photo=PICS_LIST[0], caption=f'• Picture No. : 1 / {len(PICS_LIST)}', reply_markup=InlineKeyboardMarkup(btn))

async def pics_callback(client: Client, query: CallbackQuery):
    if query.data.startswith("pic"):
        if query.data.startswith("picsremove"):
            getData = (query.data).split()
            index = int(getData[1])
            PICS_LIST.pop(index)
            await query.edit_message_media(media=InputMediaPhoto(media="https://te.legra.ph/file/06dbd8fb0628b8ba4ab45.png", caption="Removed from Existing Random Pictures Status List !!"))
            return
        getData = (query.data).split()
        ind = int(getData[1])
        no = len(PICS_LIST) - abs(ind+1) if ind < 0 else ind + 1
        pic_info = f'🌄 <b>Picture No. : {no} / {len(PICS_LIST)}</b>'
        btns = [
            [InlineKeyboardButton("<<", callback_data=f"pic {ind-1}"),
            InlineKeyboardButton(">>", callback_data=f"pic {ind+1}")],
            [InlineKeyboardButton("Remove Photo", callback_data=f"picsremove {ind}")]
        ]
        await query.edit_message_media(media=InputMediaPhoto(media=PICS_LIST[ind], caption=pic_info), reply_markup=InlineKeyboardMarkup(btns))
    await query.answer()
