#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52 | SilentDemonSD
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/SilentDemonSD/Tele-LeechX >
# All Right Reserved

import asyncio
import os
import shutil

from tobrot import LOGGER


async def create_archive(input_directory):
    return_name = None
    if os.path.exists(input_directory):
        base_dir_name = os.path.basename(input_directory)
        compressed_file_name = f"{base_dir_name}.tar.gz"
        suffix_extention_length = 1 + 3 + 1 + 2
        if len(base_dir_name) > (64 - suffix_extention_length):
            compressed_file_name = base_dir_name[:64 - suffix_extention_length]
            compressed_file_name += ".tar.gz"
        file_genertor_command = [
            "tar",
            "-zcvf",
            compressed_file_name,
            f"{input_directory}",
        ]
        process = await asyncio.create_subprocess_exec(
            *file_genertor_command,
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


async def unzip_me(input_directory):
    return_name = None
    if os.path.exists(input_directory):
        base_dir_name = os.path.basename(input_directory)
        # uncompressed_file_name = os.path.splitext(base_dir_name)[0]
        uncompressed_file_name = get_base_name(base_dir_name)
        LOGGER.info(uncompressed_file_name)
        g_cmd = ["./extract", f"{input_directory}"]
        ga_utam = await asyncio.create_subprocess_exec(
            *g_cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        gau, tam = await ga_utam.communicate()
        LOGGER.info(gau.decode().strip())
        LOGGER.info(tam.decode().strip())
        if os.path.exists(uncompressed_file_name):
            try:
                os.remove(input_directory)
            except:
                pass
            return_name = uncompressed_file_name
    return return_name


async def untar_me(input_directory):
    return_name = None
    if os.path.exists(input_directory):
        print(input_directory)
        base_dir_name = os.path.basename(input_directory)
        uncompressed_file_name = os.path.splitext(base_dir_name)[0]
        m_k_gaut = ["mkdir", f"{uncompressed_file_name}"]
        await asyncio.create_subprocess_exec(
            *m_k_gaut, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        g_cmd_t = [
            "tar",
            "-xvf",
            f"/app/{base_dir_name}",
            "-C",
            f"{uncompressed_file_name}",
        ]
        bc_kanger = await asyncio.create_subprocess_exec(
            *g_cmd_t, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        mc, kanger = await bc_kanger.communicate()
        LOGGER.info(mc)
        LOGGER.info(kanger)
        # e_response = stderr.decode().strip()
        # t_response = stdout.decode().strip()
        if os.path.exists(uncompressed_file_name):
            try:
                os.remove(input_directory)
            except:
                pass
            return_name = uncompressed_file_name
            LOGGER.info(return_name)
    return return_name


async def unrar_me(input_directory):
    return_name = None
    if os.path.exists(input_directory):
        base_dir_name = os.path.basename(input_directory)
        uncompressed_file_name = os.path.splitext(base_dir_name)[0]
        m_k_gau = ["mkdir", f"{uncompressed_file_name}"]
        await asyncio.create_subprocess_exec(
            *m_k_gau, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        print(base_dir_name)
        gau_tam_r = ["unrar", "x", f"{base_dir_name}", f"{uncompressed_file_name}"]
        jai_hind = await asyncio.create_subprocess_exec(
            *gau_tam_r, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        jai, hind = await jai_hind.communicate()
        LOGGER.info(jai)
        LOGGER.info(hind)
        # e_response = stderr.decode().strip()
        # t_response = stdout.decode().strip()
        if os.path.exists(uncompressed_file_name):
            try:
                os.remove(input_directory)
            except:
                pass
            return_name = uncompressed_file_name
            LOGGER.info(return_name)
    return return_name


def get_base_name(orig_path: str):
    if orig_path.endswith(".tar.bz2"):
        return orig_path.replace(".tar.bz2", "")
    if orig_path.endswith(".tar.gz"):
        return orig_path.replace(".tar.gz", "")
    if orig_path.endswith(".bz2"):
        return orig_path.replace(".bz2", "")
    if orig_path.endswith(".gz"):
        return orig_path.replace(".gz", "")
    if orig_path.endswith(".tar"):
        return orig_path.replace(".tar", "")
    if orig_path.endswith(".tbz2"):
        return orig_path.replace("tbz2", "")
    if orig_path.endswith(".tgz"):
        return orig_path.replace(".tgz", "")
    if orig_path.endswith(".zip"):
        return orig_path.replace(".zip", "")
    if orig_path.endswith(".7z"):
        return orig_path.replace(".7z", "")
    if orig_path.endswith(".Z"):
        return orig_path.replace(".Z", "")
    if orig_path.endswith(".rar"):
        return orig_path.replace(".rar", "")
    if orig_path.endswith(".iso"):
        return orig_path.replace(".iso", "")
    if orig_path.endswith(".wim"):
        return orig_path.replace(".wim", "")
    if orig_path.endswith(".cab"):
        return orig_path.replace(".cab", "")
    if orig_path.endswith(".apm"):
        return orig_path.replace(".apm", "")
    if orig_path.endswith(".arj"):
        return orig_path.replace(".arj", "")
    if orig_path.endswith(".chm"):
        return orig_path.replace(".chm", "")
    if orig_path.endswith(".cpio"):
        return orig_path.replace(".cpio", "")
    if orig_path.endswith(".cramfs"):
        return orig_path.replace(".cramfs", "")
    if orig_path.endswith(".deb"):
        return orig_path.replace(".deb", "")
    if orig_path.endswith(".dmg"):
        return orig_path.replace(".dmg", "")
    if orig_path.endswith(".fat"):
        return orig_path.replace(".fat", "")
    if orig_path.endswith(".hfs"):
        return orig_path.replace(".hfs", "")
    if orig_path.endswith(".lzh"):
        return orig_path.replace(".lzh", "")
    if orig_path.endswith(".lzma"):
        return orig_path.replace(".lzma", "")
    if orig_path.endswith(".lzma2"):
        return orig_path.replace(".lzma2", "")
    if orig_path.endswith(".mbr"):
        return orig_path.replace(".mbr", "")
    if orig_path.endswith(".msi"):
        return orig_path.replace(".msi", "")
    if orig_path.endswith(".mslz"):
        return orig_path.replace(".mslz", "")
    if orig_path.endswith(".nsis"):
        return orig_path.replace(".nsis", "")
    if orig_path.endswith(".ntfs"):
        return orig_path.replace(".ntfs", "")
    if orig_path.endswith(".rpm"):
        return orig_path.replace(".rpm", "")
    if orig_path.endswith(".squashfs"):
        return orig_path.replace(".squashfs", "")
    if orig_path.endswith(".udf"):
        return orig_path.replace(".udf", "")
    if orig_path.endswith(".vhd"):
        return orig_path.replace(".vhd", "")
    if orig_path.endswith(".xar"):
        return orig_path.replace(".xar", "")
    raise Exception("File format not supported for extraction")
