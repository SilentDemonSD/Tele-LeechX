#bin #!bash
# -*- coding: utf-8 -*-
# Shrimadhav U K | gautamajay52 | MaxxRider | SilentDemonSD | Other Contributors 
#
# Copyright 2022-present ~ Team[Tele-LeechX]
# 
# This is Part of < https://github.com/SilentDemonSD/Tele-LeechX >
# All Right Reserved

## Adding Files ++++
ran=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 12 | head -n 1)
## Adding Files ----

if [[ -n $CONFIG_ENV_URL ]]; then
  echo " Found config.env File 📁📁 "
	wget -q $CONFIG_ENV_URL -O /app/config.env
fi

if [ -f .env ] ; then  set -o allexport; source .env; set +o allexport ; fi


echo "Starting Your Tele-LeechX... ♻️♻️"
python3 update.py && python3 -m tobrot

