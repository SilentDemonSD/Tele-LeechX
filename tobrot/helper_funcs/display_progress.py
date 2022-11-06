#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52 | MaxxRider | Other Contributors 
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved

from math import floor
from time import time, sleep as tsleep

from pyrogram.errors.exceptions import FloodWait
from tobrot import (
    EDIT_SLEEP_TIME_OUT,
    FINISHED_PROGRESS_STR,
    UN_FINISHED_PROGRESS_STR,
    gDict,
    LOGGER,
    UPDATES_CHANNEL,
    HALF_FINISHED
)
from tobrot.bot_theme.themes import BotTheme
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

class Progress:
    def __init__(self, from_user, client, mess: Message):
        self._from_user = from_user
        self._client = client
        self._mess = mess
        self._cancelled = False

    @property
    def is_cancelled(self):
        chat_id = self._mess.chat.id
        mes_id = self._mess.id
        if gDict[chat_id] and mes_id in gDict[chat_id]:
            self._cancelled = True
        return self._cancelled

    async def progress_for_pyrogram(self, current, total, ud_type, start):
        chat_id = self._mess.chat.id
        mes_id = self._mess.id
        from_user = self._from_user
        now = time()
        diff = now - start
        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton((BotTheme(self._from_user)).CANCEL_PROG_BT, callback_data=f"gUPcancel/{chat_id}/{mes_id}/{from_user}".encode("UTF-8"),)]
            ]
        )
        if self.is_cancelled:
            LOGGER.info("Stopping Process !!")
            await self._mess.edit(
                f"⛔ **Cancelled / Error** ⛔ \n\n `{ud_type}` ({humanbytes(total)})"
            )
            await self._client.stop_transmission()

        if round(diff % float(EDIT_SLEEP_TIME_OUT)) == 0 or current == total:
            # if round(current / total * 100, 0) % 5 == 0:
            percentage = current * 100 / total
            digits = [int(x) for x in str(("{}").format("%.2d" % percentage))]
            speed = current / diff
            elapsed_time = TimeFormatter(round(diff) * 1000)
            estimated_total_time = TimeFormatter(round((total - current) / speed) * 1000)

            tmp = ((BotTheme(self._from_user)).PROG_MSG).format(
                ''.join([FINISHED_PROGRESS_STR for _ in range(floor(percentage / 5))]),
                HALF_FINISHED if floor(digits[1]) > 5 else UN_FINISHED_PROGRESS_STR,
                ''.join([UN_FINISHED_PROGRESS_STR for _ in range(19 - floor(percentage / 5))]),
                round(percentage, 2),
            )

            tmp += ((BotTheme(self._from_user)).DOWN_PROG_MSG).format(
                d = humanbytes(current),
                t = humanbytes(total),
                s = humanbytes(speed),
                eta = estimated_total_time if estimated_total_time != '' else "0s",
                UPDATES_CHANNEL = UPDATES_CHANNEL
            )
            try:
                if not self._mess.photo:
                    await self._mess.edit_text(
                        text=f"{ud_type}\n{tmp}", reply_markup=reply_markup
                    )

                else:
                    await self._mess.edit_caption(caption=f"{ud_type}\n{tmp}")
            except MessageNotModified:
                pass
            except FloodWait as fd:
                LOGGER.warning(f"FloodWait : Sleeping {fd.value}s")
                tsleep(fd.value)
            except Exception as err:
                LOGGER.info(err)

def humanbytes(size) -> str:
    if not size:
        return ""
    power = 2 ** 10
    ind = 0
    SIZE_UNITS = {0: "", 1: "K", 2: "M", 3: "G", 4: "T", 5: "P", 6: "E", 7: "Z", 8: "Y"}
    while size > power:
        size /= power
        ind += 1
    try:
        return f"{str(round(size, 2))} {SIZE_UNITS[ind]}B"
    except IndexError:
        return 'File too large'

def humanbytes_int(size_str) -> str:
    size = int(size_str)
    if not size:
        return ""
    power = 2 ** 10
    ind = 0
    SIZE_UNITS = {0: "", 1: "K", 2: "M", 3: "G", 4: "T", 5: "P", 6: "E", 7: "Z", 8: "Y"}
    while size > power:
        size /= power
        ind += 1
    try:
        return f"{str(round(size, 2))} {SIZE_UNITS[ind]}B"
    except IndexError:
        return 'File too large'

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        (f"{int(days)}d, " if days else "")
        + (f"{int(hours)}h, " if hours else "")
        + (f"{int(minutes)}m, " if minutes else "")
        + (f"{int(seconds)}s, " if seconds else "")
        + (f"{int(milliseconds)}ms, " if milliseconds else "")
    )
    return tmp[:-2]
