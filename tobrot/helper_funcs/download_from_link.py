#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | MaxxRider
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved

import asyncio
import os
import time

from tobrot import DOWNLOAD_LOCATION


async def request_download(url, file_name, r_user_id):
    directory_path = os.path.join(DOWNLOAD_LOCATION, str(r_user_id), str(time.time()))

    if not os.path.isdir(directory_path):
        os.makedirs(directory_path)
    local_file_path = os.path.join(directory_path, file_name)
    command_to_exec = ["wget", "-O", local_file_path, url]
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    final_m_r = e_response + "\n\n\n" + t_response

    if os.path.exists(local_file_path):
        return True, local_file_path
    else:
        return False, final_m_r
