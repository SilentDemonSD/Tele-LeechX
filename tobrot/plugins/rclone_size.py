#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) gautamajay52 | 5MysterySD
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved

from asyncio import sleep as asleep, create_subprocess_exec, subprocess
from os import path as opath
from re import findall

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from tobrot import DESTINATION_FOLDER, LOGGER, UPDATES_CHANNEL 
from tobrot.plugins import getUserOrChaDetails

async def check_size_g(client, message):
    user_id, u_men = getUserOrChaDetails(message)
    del_it = await message.reply_text("`💾 Checking Cloud Size... Please Wait !!!`")
    if opath.exists("rclone.conf"):
        with open("rclone.conf", "r+") as file:
            con = file.read()
            gUP = findall(r"\[(.*)\]", con)[0]
    cmd = ["rclone", "size", "--config=./rclone.conf", f"{gUP}:{DESTINATION_FOLDER}"]
    gau_tam = await create_subprocess_exec(
        *cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    gau, tam = await gau_tam.communicate()
    gautam = (gau.decode("utf-8")).replace("Total objects:", "┣🗄 **Total Files** :").replace("Total size:", "┣🗂 **Total Size** :")
    await asleep(5)
    await message.reply_text(f"┏━━━━ ☁ __GDriveInfo__ ☁ ━━━━━━╻\n┃\n┣👤 **User** : {u_men}\n┣🆔 **User ID** : #ID{user_id}\n┣🧾 **Folder Name** : `{DESTINATION_FOLDER}`\n{gautam}┃\n┗━♦️ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 {UPDATES_CHANNEL} ♦️━╹\n\n#CloudSize")
    await del_it.delete()

async def g_clearme(client, message):

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Yes 🚫", callback_data=("fuckingdo").encode("UTF-8")),
        InlineKeyboardButton("No 🤗", callback_data=("fuckoff").encode("UTF-8"))]
    ])
    await message.reply_text(
        "Are you sure? 🚫 This will delete all your downloads locally 🚫",
        reply_markup=reply_markup,
        quote=True,
    )
