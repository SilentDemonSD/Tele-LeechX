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

from requests import get as rget
from os import path as opath, getenv, listdir
from pkg_resources import working_set
from logging import FileHandler, StreamHandler, INFO, basicConfig, getLogger
from subprocess import run as srun, call as scall
from dotenv import load_dotenv

for log in listdir():
    if log.endswith('Logs.txt'):
        with open(log, 'r+') as f:
              f.truncate(0)

basicConfig(format="[%(asctime)s] [%(levelname)s] - %(message)s [%(filename)s:%(lineno)d]",
                    datefmt="%d-%b-%y %I:%M:%S %p",
                    handlers=[FileHandler('Logs.txt'), StreamHandler()],
                    level=INFO)
LOGGER = getLogger(__name__)

CONFIG_FILE_URL = getenv('CONFIG_FILE_URL')
if len(CONFIG_FILE_URL) != 0:
    try:
        res = rget(CONFIG_FILE_URL)
        if res.status_code == 200:
            with open('config.env', 'wb+') as f:
                f.write(res.content)
        else:
            LOGGER.error(f"Failed to download config.env {res.status_code}")
    except Exception as e:
        LOGGER.error(f"CONFIG_FILE_URL: {e}")

load_dotenv('config.env', override=True)

if getenv('UPDATE_PACKAGES', '').lower() == 'true':
    packages = [dist.project_name for dist in working_set]
    scall("pip install " + ' '.join(packages), shell=True)

UPSTREAM_REPO = getenv('UPSTREAM_REPO', "https://github.com/SilentDemonSD/Tele-LeechX")
if len(UPSTREAM_REPO) == 0:
    UPSTREAM_REPO = None

UPSTREAM_BRANCH = getenv('UPSTREAM_BRANCH', "h-code")
if len(UPSTREAM_BRANCH) == 0:
    UPSTREAM_BRANCH = 'h-code'

if UPSTREAM_REPO is not None:
    if opath.exists('.git'):
        srun(["rm", "-rf", ".git"], check=True)

    update = srun([f"git init -q \
                     && git config --global user.email mysterysd.sd@gmail.com \
                     && git config --global user.name tele-leechx \
                     && git add . \
                     && git commit -sm update -q \
                     && git remote add origin {UPSTREAM_REPO} \
                     && git fetch origin -q \
                     && git reset --hard origin/{UPSTREAM_BRANCH} -q"], shell=True, check=True)

    if update.returncode == 0:
        log_info(f'Successfully Updated : {UPSTREAM_REPO} : {UPSTREAM_BRANCH}')
    else:
        log_error(f'Something went wrong while updating, check {UPSTREAM_REPO} if valid or not!')
