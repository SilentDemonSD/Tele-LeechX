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

import asyncio
import os
import shutil

from TeleLX import LOGGER
from TeleLX.core.exceptions import NotSupportedExtractionArchive

async def create_archive(input_directory, archive_format='zip'):
    valid_formats = ["zip", "tar", "rar", "7z"]
    if archive_format not in valid_formats:
        raise ValueError("Invalid archive format")

    return_name = None
    if os.path.exists(input_directory):
        base_dir_name = os.path.basename(input_directory)
        compressed_file_name = f"{base_dir_name}{archive_format}"
        suffix_extension_length = len(archive_format) + 1
        if len(base_dir_name) > (64 - suffix_extension_length):
            compressed_file_name = f"{base_dir_name[:64-suffix_extension_length]}{archive_format}"

        if archive_format == ".zip":
            file_generator_command = ["zip", "-r", compressed_file_name, input_directory]
        elif archive_format == ".tar":
            file_generator_command = ["tar", "-zcvf", compressed_file_name, input_directory]
        elif archive_format == ".rar":
            file_generator_command = ["rar", "a", "-r", compressed_file_name, input_directory]
        elif archive_format == ".7z":
            file_generator_command = ["7z", "a", "-r", compressed_file_name, input_directory]

        process = await asyncio.create_subprocess_exec(
            *file_generator_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        LOGGER.error(stderr.decode().strip())
        if os.path.exists(compressed_file_name):
            try:
                shutil.rmtree(input_directory)
            except:
                pass
            return_name = compressed_file_name
    return return_name


async def extract_archive(input_directory):
    return_name = None
    if os.path.exists(input_directory):
        base_dir_name = os.path.basename(input_directory)
        uncompressed_file_name = get_base_name(base_dir_name)
        LOGGER.info(f"Compressed FileName : {uncompressed_file_name}")
        cmd = ["./extract", f"{input_directory}"]
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        LOGGER.info(f"{stdout}") #More Good
        if os.path.exists(uncompressed_file_name):
            try:
                os.remove(input_directory)
            except:
                pass
            return_name = uncompressed_file_name
    return return_name


def get_base_name(orig_path: str):
    supported_extensions = [".tar.bz2", ".tar.gz", ".bz2", ".gz", ".tar", ".tbz2", ".tgz", ".zip", ".7z", ".Z", ".rar", ".iso", ".wim", ".cab", ".apm", ".arj", ".chm", ".cpio", ".cramfs", ".deb", ".dmg", ".fat", ".hfs", ".lzh", ".lzma", ".lzma2", ".mbr", ".msi", ".mslz", ".nsis", ".ntfs", ".rpm", ".squashfs", ".udf", ".vhd", ".xar"]

    base_name, ext = os.path.splitext(orig_path)
    if ext.lower() not in supported_extensions:
        raise NotSupportedExtractionArchive("File format not supported for extraction")

    return base_name
