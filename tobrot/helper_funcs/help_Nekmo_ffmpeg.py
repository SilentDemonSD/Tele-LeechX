#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Shrimadhav U K
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved

from re import search as rsearch
from asyncio import subprocess, create_subprocess_exec
from os import path as opath
from time import time
from shutil import copyfile

MAGNETIC_LINK_REGEX = r"magnet\:\?xt\=urn\:btih\:([A-F\d]+)"

def extract_info_hash_from_ml(magnetic_link):
    ml_re_match = rsearch(MAGNETIC_LINK_REGEX, magnetic_link)
    if ml_re_match is not None:
        return ml_re_match.group(1)

async def copy_file(input_file, output_dir): #Ref :https://stackoverflow.com/a/123212/4723940
    output_file = opath.join(output_dir, str(time()) + ".jpg")
    copyfile(input_file, output_file)
    return output_file

async def take_screen_shot(video_file, output_directory, ttl):
    out_put_file_name = opath.join(output_directory, str(time()) + ".jpg")
    VIDEO_SUFFIXES = ("MKV", "MP4", "MOV", "WMV", "3GP", "MPG", "WEBM", "AVI", "FLV", "M4V", "GIF")
    if video_file.upper().endswith(VIDEO_SUFFIXES):
        file_genertor_command = ["opera", "-ss", str(ttl), "-i", video_file, "-vframes", "1", out_put_file_name]
        # Width = "90"
        process = await create_subprocess_exec(
            *file_genertor_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        e_response = stderr.decode().strip()
        t_response = stdout.decode().strip()
    if opath.lexists(out_put_file_name):
        return out_put_file_name
    else:
        return None
