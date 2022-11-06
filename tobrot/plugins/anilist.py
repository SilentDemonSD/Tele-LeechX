#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) 5MysterySD Made from Scratch !!
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved

from requests import post as rpost
from random import choice
from datetime import datetime
from calendar import month_name
from pycountry import countries as conn
from urllib.parse import quote as q
from pyrogram import enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from tobrot import LOGGER, ANILIST_TEMPLATE, DEF_ANILIST_TEMPLATE
from tobrot.helper_funcs.display_progress import TimeFormatter
GENRES_EMOJI = {"Action": "👊", "Adventure": choice(['🪂', '🧗‍♀']), "Comedy": "🤣", "Drama": " 🎭", "Ecchi": choice(['💋', '🥵']), "Fantasy": choice(['🧞', '🧞‍♂', '🧞‍♀','🌗']), "Hentai": "🔞", "Horror": "☠", "Mahou Shoujo": "☯", "Mecha": "🤖", "Music": "🎸", "Mystery": "🔮", "Psychological": "♟", "Romance": "💞", "Sci-Fi": "🛸", "Slice of Life": choice(['☘','🍁']), "Sports": "⚽️", "Supernatural": "🫧", "Thriller": choice(['🥶', '🔪','🤯'])}

ANIME_GRAPHQL_QUERY = """
query ($id: Int, $idMal: Int, $search: String) {
  Media(id: $id, idMal: $idMal, type: ANIME, search: $search) {
    id
    idMal
    title {
      romaji
      english
      native
    }
    type
    format
    status(version: 2)
    description(asHtml: true)
    startDate {
      year
      month
      day
    }
    endDate {
      year
      month
      day
    }
    season
    seasonYear
    episodes
    duration
    chapters
    volumes
    countryOfOrigin
    source
    hashtag
    trailer {
      id
      site
      thumbnail
    }
    updatedAt
    coverImage {
      large
    }
    bannerImage
    genres
    synonyms
    averageScore
    meanScore
    popularity
    trending
    favourites
    tags {
      name
      description
      rank
    }
    relations {
      edges {
        node {
          id
          title {
            romaji
            english
            native
          }
          format
          status
          source
          averageScore
          siteUrl
        }
        relationType
      }
    }
    characters {
      edges {
        role
        node {
          name {
            full
            native
          }
          siteUrl
        }
      }
    }
    studios {
      nodes {
         name
         siteUrl
      }
    }
    isAdult
    nextAiringEpisode {
      airingAt
      timeUntilAiring
      episode
    }
    airingSchedule {
      edges {
        node {
          airingAt
          timeUntilAiring
          episode
        }
      }
    }
    externalLinks {
      url
      site
    }
    rankings {
      rank
      year
      context
    }
    reviews {
      nodes {
        summary
        rating
        score
        siteUrl
        user {
          name
        }
      }
    }
    siteUrl
  }
}
"""
ani_url = 'https://graphql.anilist.co'

def get_anime_query(client, message, aniid=None):
    if not aniid:
        squery = message.text.split(' ', 1)
        if len(squery) == 1:
            message.reply_text("__Provide AniList ID / Anime Name / MyAnimeList ID__")
            return
        vars = {'search' : squery[1]}
    else:
        vars = {'id' : aniid}
    animeResp = rpost(ani_url, json={'query': ANIME_GRAPHQL_QUERY, 'variables': vars}).json()['data'].get('Media', None)
    if animeResp:
        ro_title = animeResp['title']['romaji']
        na_title = animeResp['title']['native']
        en_title = animeResp['title']['english']
        format = animeResp['format'] 
        if format: format = format.capitalize()
        status = animeResp['status']
        if status: status = status.capitalize()
        year = animeResp['seasonYear'] or 'N/A'
        try:
            sd = animeResp['startDate']
            if sd['day'] and sd['year']: startdate = f"{month_name[sd['month']]} {sd['day']}, {sd['year']}"
        except: startdate = ""
        try:
            ed = animeResp['endDate']
            if ed['day'] and ed['year']: enddate = f"{month_name[ed['month']]} {ed['day']}, {ed['year']}"
        except: enddate = ""
        season = f"{animeResp['season'].capitalize()} {animeResp['seasonYear']}"
        conname = (conn.get(alpha_2=animeResp['countryOfOrigin'])).name
        try:
            flagg = (conn.get(alpha_2=animeResp['countryOfOrigin'])).flag
            country = f"{flagg} #{conname}"
        except AttributeError:
            country = f"#{conname}"
        episodes = animeResp.get('episodes', 'N/A')
        try:
            duration = f"{TimeFormatter(animeResp['duration']*60*1000)}"
        except: duration = "N/A"
        avgscore = f"{animeResp['averageScore']}%" or ''
        genres = ", ".join(f"{GENRES_EMOJI[x]} #{x.replace(' ', '_').replace('-', '_')}" for x in animeResp['genres'])
        studios = ", ".join(f"""<a href="{x['siteUrl']}">{x['name']}</a>""" for x in animeResp['studios']['nodes'])
        source = animeResp['source'] or '-'
        hashtag = animeResp['hashtag'] or 'N/A'
        synonyms = ", ".join(x for x in animeResp['synonyms']) or ''
        siteurl = animeResp.get('siteUrl')
        trailer = animeResp.get('trailer', None)
        if trailer and trailer.get('site') == "youtube":
            trailer = f"https://youtu.be/{trailer.get('id')}"
        postup = datetime.fromtimestamp(animeResp['updatedAt']).strftime('%d %B, %Y')
        description = animeResp.get('description', 'N/A')
        if len(description) > 500:  
            description = f"{description[:500]}...."
        popularity = animeResp['popularity'] or ''
        trending = animeResp['trending'] or ''
        favourites = animeResp['favourites'] or ''
        siteid = animeResp.get('id')
        bannerimg = animeResp['bannerImage'] or ''
        coverimg = animeResp['coverImage']['large'] or ''
        title_img = f"https://img.anili.st/media/{siteid}"
        buttons = [
            [InlineKeyboardButton("AniList Info 🎬", url=siteurl)],
            [InlineKeyboardButton("Reviews 📑", callback_data=f"reviews {siteid}"),
            InlineKeyboardButton("Tags 🎯", callback_data=f"tags {siteid}"),
            InlineKeyboardButton("Relations 🧬", callback_data=f"relations {siteid}")],
            [InlineKeyboardButton("Streaming Sites 📊", callback_data=f"stream {siteid}"),
            InlineKeyboardButton("Characters 👥️️", callback_data=f"characters {siteid}")]
        ]
        if trailer:
            buttons[0].insert(1, InlineKeyboardButton("Trailer 🎞", url=trailer))
        aniListTemp = ANILIST_TEMPLATE.get(int(message.from_user.id), "")
        if not aniListTemp:
            aniListTemp = DEF_ANILIST_TEMPLATE
        try:
            template = aniListTemp.format(**locals())
        except Exception as e:
            template = ""
            LOGGER.error(e)
        if aniid:
            return template, buttons
        else: message.reply_photo(photo = (title_img or 'https://te.legra.ph/file/8a5155c0fc61cc2b9728c.jpg'), caption = template, parse_mode=enums.ParseMode.HTML, reply_markup=InlineKeyboardMarkup(buttons))

async def anilist_callbackquery(client, query: CallbackQuery):
    qdata = query.data
    if qdata.startswith("tags"):
        qdic = qdata.split(" ")
        siteid = qdic[1]
        aniTag = rpost(ani_url, json={'query': ANIME_GRAPHQL_QUERY, 'variables': {'id' : siteid}}).json()['data'].get('Media', None)
        msg = "<b>Tags :</b>\n\n"
        msg += "\n".join(f"""<a href="https://anilist.co/search/anime?genres={q(x['name'])}">{x['name']}</a> {x['rank']}%""" for x in aniTag['tags'])
        btn = [
            [InlineKeyboardButton("⌫ Back", callback_data = f"home {siteid}")]
        ]
        await query.edit_message_caption(caption=msg, reply_markup=InlineKeyboardMarkup(btn))
    elif qdata.startswith("stream"):
        qdic = qdata.split(" ")
        siteid = qdic[1]
        links = rpost(ani_url, json={'query': ANIME_GRAPHQL_QUERY, 'variables': {'id' : siteid}}).json()['data'].get('Media', None)
        msg = "<b>External & Streaming Links :</b>\n\n"
        msg += "\n".join(f"""<a href="{x['url']}">{x['site']}</a>""" for x in links['externalLinks'])
        btn = [
            [InlineKeyboardButton("⌫ Back", callback_data = f"home {siteid}")]
        ]
        await query.edit_message_caption(caption=msg, reply_markup=InlineKeyboardMarkup(btn))
    elif qdata.startswith("reviews"):
        qdic = qdata.split(" ")
        siteid = qdic[1]
        animeResp = rpost(ani_url, json={'query': ANIME_GRAPHQL_QUERY, 'variables': {'id' : siteid}}).json()['data'].get('Media', None)
        msg = "<b>Reviews :</b>\n\n"
        reList = animeResp['reviews']['nodes']
        msg += "\n\n".join(f"""<a href="{x['siteUrl']}">{x['summary']}</a>\n<b>Score :</b> <code>{x['score']} / 100</code>\n<i>By {x['user']['name']}</i>""" for x in reList[:8])
        btn = [
            [InlineKeyboardButton("⌫ Back", callback_data = f"home {siteid}")]
        ]
        await query.edit_message_caption(caption=msg, reply_markup=InlineKeyboardMarkup(btn))
    elif qdata.startswith("relations"):
        qdic = qdata.split(" ")
        siteid = qdic[1]
        animeResp = rpost(ani_url, json={'query': ANIME_GRAPHQL_QUERY, 'variables': {'id' : siteid}}).json()['data'].get('Media', None)
        msg = "<b>Relations :</b>\n\n"
        msg += "\n\n".join(f"""<a href="{x['node']['siteUrl']}">{x['node']['title']['english']}</a> ({x['node']['title']['romaji']})\n<b>Format</b>: <code>{x['node']['format'].capitalize()}</code>\n<b>Status</b>: <code>{x['node']['status'].capitalize()}</code>\n<b>Average Score</b>: <code>{x['node']['averageScore']}%</code>\n<b>Source</b>: <code>{x['node']['source'].capitalize()}</code>\n<b>Relation Type</b>: <code>{x['relationType'].capitalize()}</code>""" for x in animeResp['relations']['edges'])
        btn = [
            [InlineKeyboardButton("⌫ Back", callback_data = f"home {siteid}")]
        ]
        await query.edit_message_caption(caption=msg, reply_markup=InlineKeyboardMarkup(btn))
    elif qdata.startswith("characters"):
        qdic = qdata.split(" ")
        siteid = qdic[1]
        animeResp = rpost(ani_url, json={'query': ANIME_GRAPHQL_QUERY, 'variables': {'id' : siteid}}).json()['data'].get('Media', None)
        msg = "<b>List of Characters :</b>\n\n"
        msg += "\n\n".join(f"""• <a href="{x['node']['siteUrl']}">{x['node']['name']['full']}</a> ({x['node']['name']['native']})\n<b>Role :</b> {x['role'].capitalize()}""" for x in (animeResp['characters']['edges'])[:8])
        btn = [
            [InlineKeyboardButton("⌫ Back", callback_data = f"home {siteid}")]
        ]
        await query.edit_message_caption(caption=msg, reply_markup=InlineKeyboardMarkup(btn))
    elif qdata.startswith("home"):
        qdic = qdata.split(" ")
        siteid = qdic[1]
        msg, btn = get_anime_query(client, query, siteid)
        await query.edit_message_caption(caption=msg, reply_markup=InlineKeyboardMarkup(btn))
    await query.answer()
