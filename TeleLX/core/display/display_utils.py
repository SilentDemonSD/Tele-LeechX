#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of Tele-LeechX: https://github.com/SilentDemonSD/Tele-LeechX
# Copyright (c) 2022-2023 SilentDemonSD.
# All rights reserved.

"""
This script is a part of the Tele-LeechX project, a Telegram bot based on Pyrogram Framework and 
extra leeching utilities. Its purpose is to allow users to easily download and save media files 
in Telegram chats and channels.
"""

def format_time(milliseconds: int) -> str:
    """
    Formats the given number of milliseconds into a human-readable time string.

    Args:
        milliseconds: An integer representing the number of milliseconds to format.

    Returns:
        A string representing the formatted time in the format "Dd, Hh, Mm, Ss, Ms".
    """
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return f"{days}d, " * bool(days) + f"{hours}h, " * bool(hours) + f"{minutes}m, " * bool(minutes) \
           + f"{seconds}s, " * bool(seconds) + f"{milliseconds}ms, " * bool(milliseconds)[:-2]

def format_bytes(size: int) -> str:
    """
    Convert a file size in bytes to a human-readable format.
    
    Args:
        size (int): The size of the file in bytes.

    Returns:
        str: A string representing the size of the file in a human-readable format.
             For example, if the size is 1024 bytes, the function will return "1.00 KB".
    """
    if not size:
        return ""
    power = 2 ** 10
    ind = 0
    size_in_units = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    while size > power:
        size /= power
        ind += 1
    try:
        return f"{size:.2f} {size_in_units[ind]}"
    except IndexError:
        return "File too large"