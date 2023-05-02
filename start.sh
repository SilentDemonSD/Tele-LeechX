#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# This file is part of Tele-LeechX: https://github.com/SilentDemonSD/Tele-LeechX
# Copyright (c) 2022-2023 SilentDemonSD.
# All rights reserved.

# Generate a random string to use as a file name prefix
ran=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 12 | head -n 1)

# Download the config.env file if the CONFIG_ENV_URL environment variable is set
if [[ -n $CONFIG_ENV_URL ]]; then
    echo "Downloading config.env file 📁📁"
    wget -q "$CONFIG_ENV_URL" -O "/app/config.env"
fi

# Load environment variables from the .env file, if it exists
if [ -f .env ]; then
    echo "Loading environment variables from .env file"
    set -o allexport
    source .env
    set +o allexport
fi

echo "Starting Tele-LeechX... ♻️♻️"
python3 update.py && python3 -m tobrot

