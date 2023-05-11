#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Shrimadhav U K
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/SilentDemonSD/Tele-LeechX >
# All Right Reserved

from re import search as rsearch
from asyncio import subprocess, create_subprocess_exec
from os import path as opath, makedirs
from time import time
from shutil import copyfile

MAGNETIC_LINK_REGEX = r"magnet\:\?xt\=urn\:btih\:([A-F\d]+)"

def extract_info_hash_from_ml(magnetic_link):
    ml_re_match = rsearch(MAGNETIC_LINK_REGEX, magnetic_link)
    if ml_re_match is not None:
        return ml_re_match.group(1)

async def copy_file(input_file, output_dir):
    """
    Copies a file to the specified output directory.

    Args:
        input_file (str): Path to the input file.
        output_dir (str): Directory where the file will be copied.

    Returns:
        str: Path to the copied file in the output directory.
    """
    if not opath.exists(output_dir):
        makedirs(output_dir)
    output_file = opath.join(output_dir, f"{time()}.jpg")
    if input_file.lower().endswith(".jpg"):
        shutil.copy2(input_file, output_file)
        return output_file
    else:
        raise ValueError("Input file must have a '.jpg' extension.")

async def take_screen_shot(video_file, output_directory, ttl):
    """
    Takes a screen shot of a video file at a specified time and saves it to the output directory.

    Args:
        video_file (str): Path to the video file.
        output_directory (str): Directory where the screen shot will be saved.
        ttl (int): Time in seconds at which to take the screen shot.

    Returns:
        str: Path to the saved screen shot file, or None if the screen shot could not be taken.
    """
    out_filename = opath.join(output_directory, str(time()) + ".jpg")
    VIDEO_SUFFIXES = ("MKV", "MP4", "MOV", "WMV", "3GP", "MPG", "WEBM", "AVI", "FLV", "M4V", "GIF", "TS", "VOB", "OGV")
    if video_file.upper().endswith(VIDEO_SUFFIXES):
        file_genertor_command = ["opera", "-ss", str(ttl), "-i", video_file, "-vframes", "1", out_filename, "-hide_banner", "-loglevel", "error"]
        process = await create_subprocess_exec(
            *file_genertor_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        e_response = stderr.decode().strip()
        t_response = stdout.decode().strip()
    if opath.lexists(out_filename):
        return out_filename
    return None
