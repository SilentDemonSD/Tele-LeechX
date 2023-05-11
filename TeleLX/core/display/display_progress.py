#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52 | MaxxRider | Other Contributors 
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/SilentDemonSD/Tele-LeechX >
# All Right Reserved

from math import floor
from time import time, sleep as tsleep

from pyrogram.errors.exceptions import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from TeleLX import (
    EDIT_SLEEP_TIME_OUT,
    FINISHED_PROGRESS_STR,
    UN_FINISHED_PROGRESS_STR,
    gDict,
    LOGGER,
    UPDATES_CHANNEL,
    HALF_FINISHED
)
from TeleLX.core.bot_themes import BotTheme


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
                f"⛔ **Cancelled / Error** ⛔ \n\n `{ud_type}` ({format_bytes(total)})"
            )
            await self._client.stop_transmission()

        if round(diff % float(EDIT_SLEEP_TIME_OUT)) == 0 or current == total:
            # if round(current / total * 100, 0) % 5 == 0:
            percentage = current * 100 / total
            digits = [int(x) for x in str(("{}").format("%.2d" % percentage))]
            speed = current / diff
            elapsed_time = format_time(round(diff) * 1000)
            estimated_total_time = format_time(round((total - current) / speed) * 1000)

            tmp = ((BotTheme(self._from_user)).PROG_MSG).format(
                ''.join([FINISHED_PROGRESS_STR for _ in range(floor(percentage / 5))]),
                HALF_FINISHED if floor(digits[1]) > 5 else UN_FINISHED_PROGRESS_STR,
                ''.join([UN_FINISHED_PROGRESS_STR for _ in range(19 - floor(percentage / 5))]),
                round(percentage, 2),
            )

            tmp += ((BotTheme(self._from_user)).DOWN_PROG_MSG).format(
                d = format_bytes(current),
                t = format_bytes(total),
                s = format_bytes(speed),
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


def progressBar(percentage):
    p_used, p_total = '▰', '▱'
    try: percentage=int(percentage)
    except: percentage = 0
    return ''.join(p_used if i <= percentage // 10 else p_total for i in range(10))
