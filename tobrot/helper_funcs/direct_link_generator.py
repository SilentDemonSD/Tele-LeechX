#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52 | MaxxRider | 5MysterySD | Other Contributors | Scripts | Anasty [MLTB]
#
# Copyright 2022 - TeamTele-LeechX | Copyright (C) 2019 The Raphielscape Company LLC.
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved


import json
import hashlib
import re
import urllib.parse
import lk21
import requests
import cfscrape
import cloudscraper
import time
import base64

from os import popen
from random import choice
from urllib.parse import urlparse, unquote, parse_qs
from lxml import etree
from js2py import EvalJs
from bs4 import BeautifulSoup
from base64 import standard_b64encode

from tobrot import UPTOBOX_TOKEN, LOGGER, EMAIL, PWSSD, CRYPT, GDRIVE_FOLDER_ID, HUB_CRYPT, DRIVEFIRE_CRYPT, KATDRIVE_CRYPT, KOLOP_CRYPT, DRIVEBUZZ_CRYPT, GADRIVE_CRYPT, LARAVEL_SESSION, XSRF_TOKEN
from tobrot.helper_funcs.exceptions import DirectDownloadLinkException
from tobrot.plugins import is_appdrive_link, is_gdtot_link 

drive_list = ['driveapp.in', 'gdflix.pro', 'drivelinks.in', 'drivesharer.in', 'driveflix.in', 'drivebit.in', 'drivehub.in', 'driveace.in']
bypass_vip_list = ['exe.io', 'exey.io', 'sub2unlock.net', 'sub2unlock.com', 'rekonise.com', 'letsboost.net', 'ph.apps2app.com', 'mboost.me', 'shortconnect.com', 'sub4unlock.com', 'ytsubme.com', 'bit.ly', 'social-unlock.com', 'boost.ink', 'goo.gl', 'shrto.ml', 't.co', 'tinyurl.com']

def url_link_generate(text_url: str):
    ### Direct Links Generator ++++
    if not text_url:
        raise DirectDownloadLinkException("`No Links Found!, Try Again` !!")
    elif 'zippyshare.com' in text_url:
        return zippy_share(text_url)
    elif 'yadi.sk' in text_url:
        return yandex_disk(text_url)
    elif 'cloud.mail.ru' in text_url:
        return cm_ru(text_url)
    elif 'mediafire.com' in text_url:
        return mediafire(text_url)
    elif 'uptobox.com' in text_url:
        return uptobox(text_url)
    elif 'osdn.net' in text_url:
        return osdn(text_url)
    elif 'github.com' in text_url:
        return github(text_url)
    elif 'hxfile.co' in text_url:
        return hxfile(text_url)
    elif 'anonfiles.com' in text_url:
        return anonfiles(text_url)
    elif 'letsupload.io' in text_url:
        return letsupload(text_url)
    elif 'fembed.net' in text_url:
        return fembed(text_url)
    elif 'fembed.com' in text_url:
        return fembed(text_url)
    elif 'femax20.com' in text_url:
        return fembed(text_url)
    elif 'fcdn.stream' in text_url:
        return fembed(text_url)
    elif 'feurl.com' in text_url:
        return fembed(text_url)
    elif 'naniplay.nanime.in' in text_url:
        return fembed(text_url)
    elif 'naniplay.nanime.biz' in text_url:
        return fembed(text_url)
    elif 'naniplay.com' in text_url:
        return fembed(text_url)
    elif 'layarkacaxxi.icu' in text_url:
        return fembed(text_url)
    elif 'sbembed.com' in text_url:
        return sbembed(text_url)
    elif 'streamsb.net' in text_url:
        return sbembed(text_url)
    elif 'sbplay.org' in text_url:
        return sbembed(text_url)
    elif 'racaty.net' in text_url:
        return racaty(text_url)
    elif '1drv.ms' in text_url:
        return onedrive(text_url)
    elif 'pixeldrain.com' in text_url:
        return pixeldrain(text_url)
    elif 'antfiles.com' in text_url:
        return antfiles(text_url)
    elif 'streamtape.com' in text_url:
        return streamtape(text_url)
    elif 'bayfiles.com' in text_url:
        return anonfiles(text_url)
    elif '1fichier.com' in text_url:
        return fichier(text_url)
    elif 'solidfiles.com' in text_url:
        return solidfiles(text_url)
    elif 'krakenfiles.com' in text_url:
        return krakenfiles(text_url)
    elif is_gdtot_link(text_url):
        return gdtot(text_url)
    elif 'gplinks.co' in text_url:
        return gplink(text_url)
    elif is_appdrive_link(text_url) or any(x in text_url for x in drive_list):
        is_direct = True
        return appdrive_dl(text_url, is_direct)
    elif 'linkvertise.com' in text_url:
        return linkvertise(text_url)
    elif 'droplink.co' in text_url:
        return droplink(text_url)
    elif 'gofile.io' in text_url:
        return gofile(text_url)
    elif 'ouo.io' in text_url or 'ouo.press' in text_url:
        return ouo(text_url)
    elif 'upindia.mobi' in text_url:
        return upindia(text_url)
    elif 'uploadfile.cc' in text_url:
        return upindia(text_url)
    elif 'hubdrive.cc' in text_url:
        return hubdrive(text_url)
    elif "mdisk.me" in text_url:
        return mdisk(text_url)
    elif "drivefire.co" in text_url:
        return drivefire_dl(text_url)
    elif "kolop.icu" in text_url:
        return kolop_dl(text_url)
    elif "katdrive.net" in text_url:
        return katdrive_dl(text_url)
    elif "drivebuzz.icu" in text_url:
        return drivebuzz_dl(text_url)
    elif "gadrive.vip" in text_url:
        return gadrive_dl(text_url)
    elif 'adf.ly' in text_url:
        return adfly(text_url)
    elif 'https://sourceforge.net' in text_url:
        return sourceforge(text_url)
    elif 'https://master.dl.sourceforge.net' in text_url:
        return sourceforge2(text_url)
    elif "androiddatahost.com" in text_url:
        return androidatahost(text_url)
    elif "androidfilehost.com" in text_url:
        return androidfilehost(text_url)
    elif "sfile.mobi" in text_url:
        return sfile(text_url)
    elif "wetransfer.com" in text_url or "we.tl" in text_url:
        return wetransfer(text_url)
    elif "corneey.com" in text_url or "sh.st" in text_url:
        return shorte_st(text_url)
    elif "psa.pm" in text_url:
        return psa_bypasser(text_url)
    elif "upload.ee" in text_url:
        return uploadee(text_url)
    elif "dropbox.com" in text_url:
        return dropbox(text_url)
    elif "megaup.net" in text_url:
        return megaup(text_url)
    elif "mediafire.com" in text_url:
        return mediafire(text_url)
    elif "filecrypt.ws" in text_url:
        return filecrypt(text_url)
    elif "shareus.io" in text_url:
        return shareus(text_url)
    elif "shortlingly.in" in text_url:
        return shortlingly(text_url)
    elif "gyanilinks.com" in text_url:
        return gyanilinks(text_url)
    elif "pixl" in text_url:
        return pixl(text_url)
    elif "safeurl.sirigan.my.id" in text_url:
        return siriganbypass(text_url)
    elif "sharer.pw" in text_url:
        return sharer_pw(text_url)
    elif any(x in text_url for x in bypass_vip_list):
        return bypass_vip(text_url)
    elif "rocklinks.net" in text_url:
        return rocklinks(text_url)
    elif "olamovies.ink" in text_url:
        return olamovies(text_url)
    else:
        raise DirectDownloadLinkException(f'UnSupported URL : {text_url}')
        ### Direct Links Generator ----


def zippy_share(url: str) -> str:
    link = re.findall("https:/.(.*?).zippyshare", url)[0]
    response_content = (requests.get(url)).content
    bs_obj = BeautifulSoup(response_content, "lxml")

    try:
        js_script = bs_obj.find("div", {"class": "center",}).find_all(
            "script"
        )[1]
    except:
        js_script = bs_obj.find("div", {"class": "right",}).find_all(
            "script"
        )[0]

    js_content = re.findall(r'\.href.=."/(.*?)";', str(js_script))
    js_content = 'var x = "/' + js_content[0] + '"'

    evaljs = EvalJs()
    setattr(evaljs, "x", None)
    evaljs.execute(js_content)
    js_content = getattr(evaljs, "x")

    return f"https://{link}.zippyshare.com{js_content}"


def yandex_disk(url: str) -> str:
    """ Yandex.Disk direct links generator
    Based on https://github.com/wldhx/yadisk-direct"""
    try:
        text_url = re.findall(r'\bhttps?://.*yadi\.sk\S+', url)[0]
    except IndexError:
        reply = "`No Yandex.Disk links found`\n"
        return reply
    api = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}'
    try:
        dl_url = requests.get(api.format(text_url)).json()['href']
        return dl_url
    except KeyError:
        raise DirectDownloadLinkException("`Error: File not found / Download limit reached`\n")


def cm_ru(url: str) -> str:
    """ cloud.mail.ru direct links generator
    Using https://github.com/JrMasterModelBuilder/cmrudl.py"""
    reply = ''
    try:
        text_url = re.findall(r'\bhttps?://.*cloud\.mail\.ru\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No cloud.mail.ru links found`\n")
    command = f'vendor/cmrudl.py/cmrudl -s {text_url}'
    result = popen(command).read()
    result = result.splitlines()[-1]
    try:
        data = json.loads(result)
    except json.decoder.JSONDecodeError:
        raise DirectDownloadLinkException("`Error: Can't extract the link`\n")
    dl_url = data['download']
    return dl_url


def uptobox(url: str) -> str:
    """ Uptobox direct links generator
    based on https://github.com/jovanzers/WinTenCermin """
    try:
        link = re.findall(r'\bhttps?://.*uptobox\.com\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("No Uptobox links found\n")
    if UPTOBOX_TOKEN is None:
        LOGGER.error('UPTOBOX_TOKEN not provided!')
        dl_url = link
    else:
        try:
            link = re.findall(r'\bhttp?://.*uptobox\.com/dl\S+', url)[0]
            dl_url = link
        except:
            file_id = re.findall(r'\bhttps?://.*uptobox\.com/(\w+)', url)[0]
            file_link = f'https://uptobox.com/api/link?token={UPTOBOX_TOKEN}&file_code={file_id}'
            req = requests.get(file_link)
            result = req.json()
            if result['message'].lower() == 'success':
                dl_url = result['data']['dlLink']
            elif result['message'].lower() == 'waiting needed':
                waiting_time = result["data"]["waiting"] + 1
                waiting_token = result["data"]["waitingToken"]
                time.sleep(waiting_time)
                req2 = requests.get(f"{file_link}&waitingToken={waiting_token}")
                result2 = req2.json()
                dl_url = result2['data']['dlLink']
            elif result['message'].lower() == 'Please wait before next request':
                cooldown = divmod(result['data']['waiting'], 60)
                raise DirectDownloadLinkException(f"ERROR: Uptobox is being Cooldown Please Wait Until : {cooldown[0]}m {cooldown[1]}s")
            else:
                LOGGER.info(f"UPTOBOX_ERROR: {result}")
                raise DirectDownloadLinkException(f"ERROR: {result['message']}")
    return dl_url


def mediafire(url: str) -> str:
    """ MediaFire direct links generator """
    try:
        text_url = re.findall(r'\bhttps?://.*mediafire\.com\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No MediaFire links found`\n")
    page = BeautifulSoup(requests.get(text_url).content, 'lxml')
    info = page.find('a', {'aria-label': 'Download file'})
    dl_url = info.get('href')
    return dl_url


def osdn(url: str) -> str:
    """ OSDN direct links generator """
    osdn_link = 'https://osdn.net'
    try:
        text_url = re.findall(r'\bhttps?://.*osdn\.net\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No OSDN links found`\n")
    page = BeautifulSoup(
        requests.get(text_url, allow_redirects=True).content, 'lxml')
    info = page.find('a', {'class': 'mirror_link'})
    text_url = urllib.parse.unquote(osdn_link + info['href'])
    mirrors = page.find('form', {'id': 'mirror-select-form'}).findAll('tr')
    urls = []
    for data in mirrors[1:]:
        mirror = data.find('input')['value']
        urls.append(re.sub(r'm=(.*)&f', f'm={mirror}&f', text_url))
    return urls[0]


def github(url: str) -> str:
    """ GitHub direct links generator """
    try:
        text_url = re.findall(r'\bhttps?://.*github\.com.*releases\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No GitHub Releases links found`\n")
    download = requests.get(text_url, stream=True, allow_redirects=False)
    try:
        dl_url = download.headers["location"]
        return dl_url
    except KeyError:
        raise DirectDownloadLinkException("`Error: Can't extract the link`\n")


def onedrive(link: str) -> str:
    """ Onedrive direct link generator
    Based on https://github.com/UsergeTeam/Userge """
    link_without_query = urlparse(link)._replace(query=None).geturl()
    direct_link_encoded = str(standard_b64encode(bytes(link_without_query, "utf-8")), "utf-8")
    direct_link1 = f"https://api.onedrive.com/v1.0/shares/u!{direct_link_encoded}/root/content"
    resp = requests.head(direct_link1)
    if resp.status_code != 302:
        return "ERROR: Unauthorized link, the link may be private"
    dl_link = resp.next.url
    file_name = dl_link.rsplit("/", 1)[1]
    resp2 = requests.head(dl_link)
    return dl_link


def hxfile(url: str) -> str:
    """ Hxfile direct link generator
    Based on https://github.com/zevtyardt/lk21
             https://github.com/SlamDevs/slam-mirrorbot """
    bypasser = lk21.Bypass()
    dl_url=bypasser.bypass_filesIm(url)
    return dl_url


def anonfiles(url: str) -> str:
    """ Anonfiles direct link generator
    Based on https://github.com/zevtyardt/lk21
             https://github.com/SlamDevs/slam-mirrorbot """
    bypasser = lk21.Bypass()
    dl_url=bypasser.bypass_anonfiles(url)
    return dl_url


def letsupload(url: str) -> str:
    """ Letsupload direct link generator
    Based on https://github.com/zevtyardt/lk21
             https://github.com/SlamDevs/slam-mirrorbot """
    dl_url = ''
    try:
        link = re.findall(r'\bhttps?://.*letsupload\.io\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("No Letsupload links found\n")
    bypasser = lk21.Bypass()
    dl_url=bypasser.bypass_url(link)
    return dl_url


def fembed(link: str) -> str:
    """ Fembed direct link generator
    Based on https://github.com/zevtyardt/lk21
             https://github.com/SlamDevs/slam-mirrorbot """
    bypasser = lk21.Bypass()
    dl_url=bypasser.bypass_fembed(link)
    lst_link = []
    count = len(dl_url)
    for i in dl_url:
        lst_link.append(dl_url[i])
    return lst_link[count-1]


def sbembed(link: str) -> str:
    """ Sbembed direct link generator
    Based on https://github.com/zevtyardt/lk21
             https://github.com/SlamDevs/slam-mirrorbot """
    bypasser = lk21.Bypass()
    dl_url=bypasser.bypass_sbembed(link)
    lst_link = []
    count = len(dl_url)
    for i in dl_url:
        lst_link.append(dl_url[i])
    return lst_link[count-1]


def pixeldrain(url: str) -> str:
    """ Based on https://github.com/yash-dk/TorToolkit-Telegram """
    url = url.strip("/ ")
    file_id = url.split("/")[-1]
    info_link = f"https://pixeldrain.com/api/file/{file_id}/info"
    dl_link = f"https://pixeldrain.com/api/file/{file_id}"
    resp = requests.get(info_link).json()
    if resp["success"]:
        return dl_link
    else:
        raise DirectDownloadLinkException("ERROR: Cant't download due {}.".format(resp.text["value"]))


def antfiles(url: str) -> str:
    """ Antfiles direct link generator
    Based on https://github.com/zevtyardt/lk21
             https://github.com/SlamDevs/slam-mirrorbot """
    bypasser = lk21.Bypass()
    dl_url=bypasser.bypass_antfiles(url)
    return dl_url


def streamtape(url: str) -> str:
    """ Streamtape direct link generator
    Based on https://github.com/zevtyardt/lk21
             https://github.com/SlamDevs/slam-mirrorbot """
    bypasser = lk21.Bypass()
    dl_url=bypasser.bypass_streamtape(url)
    return dl_url


def racaty(url: str) -> str:
    """ Racaty direct links generator
    based on https://github.com/Slam-Team/slam-mirrorbot """
    dl_url = ''
    try:
        link = re.findall(r'\bhttps?://.*racaty\.net\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("No Racaty links found\n")
    scraper = cfscrape.create_scraper()
    r = scraper.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    op = soup.find("input", {"name": "op"})["value"]
    ids = soup.find("input", {"name": "id"})["value"]
    rpost = scraper.post(url, data = {"op": op, "id": ids})
    rsoup = BeautifulSoup(rpost.text, "lxml")
    dl_url = rsoup.find("a", {"id": "uniqueExpirylink"})["href"].replace(" ", "%20")
    return dl_url


def fichier(link: str) -> str:
    """ 1Fichier direct links generator
    Based on https://github.com/Maujar
             https://github.com/Slam-Team/slam-mirrorbot """
    regex = r"^([http:\/\/|https:\/\/]+)?.*1fichier\.com\/\?.+"
    gan = re.match(regex, link)
    if not gan:
      raise DirectDownloadLinkException("ERROR: The link you entered is wrong!")
    if "::" in link:
      pswd = link.split("::")[-1]
      url = link.split("::")[-2]
    else:
      pswd = None
      url = link
    try:
      if pswd is None:
        req = requests.post(url)
      else:
        pw = {"pass": pswd}
        req = requests.post(url, data=pw)
    except:
      raise DirectDownloadLinkException("ERROR: Unable to reach 1fichier server!")
    if req.status_code == 404:
      raise DirectDownloadLinkException("ERROR: File not found/The link you entered is wrong!")
    soup = BeautifulSoup(req.content, 'lxml')
    if soup.find("a", {"class": "ok btn-general btn-orange"}) is not None:
      dl_url = soup.find("a", {"class": "ok btn-general btn-orange"})["href"]
      if dl_url is None:
        raise DirectDownloadLinkException("ERROR: Unable to generate Direct Link 1fichier!")
      else:
        return dl_url
    else:
      if len(soup.find_all("div", {"class": "ct_warn"})) == 2:
        str_2 = soup.find_all("div", {"class": "ct_warn"})[-1]
        if "you must wait" in str(str_2).lower():
          numbers = [int(word) for word in str(str_2).split() if word.isdigit()]
          if len(numbers) == 0:
            raise DirectDownloadLinkException("ERROR: 1fichier is on a limit. Please wait a few minutes/hour.")
          else:
            raise DirectDownloadLinkException(f"ERROR: 1fichier is on a limit. Please wait {numbers[0]} minute.")
        elif "protect access" in str(str_2).lower():
          raise DirectDownloadLinkException("ERROR: This link requires a password!\n\n<b>This link requires a password!</b>\n- Insert sign <b>::</b> after the link and write the password after the sign.\n\n<b>Example:</b>\n<code>/mirror https://1fichier.com/?smmtd8twfpm66awbqz04::love you</code>\n\n* No spaces between the signs <b>::</b>\n* For the password, you can use a space!")
        else:
          raise DirectDownloadLinkException("ERROR: Error trying to generate Direct Link from 1fichier!")
      elif len(soup.find_all("div", {"class": "ct_warn"})) == 3:
        str_1 = soup.find_all("div", {"class": "ct_warn"})[-2]
        str_3 = soup.find_all("div", {"class": "ct_warn"})[-1]
        if "you must wait" in str(str_1).lower():
          numbers = [int(word) for word in str(str_1).split() if word.isdigit()]
          if len(numbers) == 0:
            raise DirectDownloadLinkException("ERROR: 1fichier is on a limit. Please wait a few minutes/hour.")
          else:
            raise DirectDownloadLinkException(f"ERROR: 1fichier is on a limit. Please wait {numbers[0]} minute.")
        elif "bad password" in str(str_3).lower():
          raise DirectDownloadLinkException("ERROR: The password you entered is wrong!")
        else:
          raise DirectDownloadLinkException("ERROR: Error trying to generate Direct Link from 1fichier!")
      else:
        raise DirectDownloadLinkException("ERROR: Error trying to generate Direct Link from 1fichier!")


def solidfiles(url: str) -> str:
    """ Solidfiles direct links generator
    Based on https://github.com/Xonshiz/SolidFiles-Downloader
    By https://github.com/Jusidama18 """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'
    }
    pageSource = requests.get(url, headers = headers).text
    mainOptions = str(re.search(r'viewerOptions\'\,\ (.*?)\)\;', pageSource).group(1))
    dl_url = json.loads(mainOptions)["downloadUrl"]
    return dl_url


def krakenfiles(page_link: str) -> str:
    """ krakenfiles direct link generator
    Based on https://github.com/tha23rd/py-kraken
    By https://github.com/junedkh """
    page_resp = requests.session().get(page_link)
    soup = BeautifulSoup(page_resp.text, "lxml")
    try:
        token = soup.find("input", id="dl-token")["value"]
    except:
        raise DirectDownloadLinkException(f"Page link is wrong: {page_link}")

    hashes = [
        item["data-file-hash"]
        for item in soup.find_all("div", attrs={"data-file-hash": True})
    ]
    if not hashes:
        raise DirectDownloadLinkException(
            f"Hash not found for : {page_link}")

    dl_hash = hashes[0]

    payload = f'------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name="token"\r\n\r\n{token}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--'
    headers = {
        "content-type": "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        "cache-control": "no-cache",
        "hash": dl_hash,
    }

    dl_link_resp = requests.session().post(
        f"https://krakenfiles.com/download/{hash}", data=payload, headers=headers)

    dl_link_json = dl_link_resp.json()

    if "url" in dl_link_json:
        return dl_link_json["url"]
    else:
        raise DirectDownloadLinkException(
            f"Failed to acquire download URL from kraken for : {page_link}")


def gdtot(url: str) -> str:
    """ Gdtot google drive link generator
    By https://github.com/majnurangeela/BypassBot/blob/main/gdtot.py """

    if CRYPT is None:
        raise DirectDownloadLinkException("ERROR: CRYPT variable not provided")

    client = requests.Session()
    client.cookies.update({ 'crypt': CRYPT })
    res = client.get(url)
    title = re.findall(r">(.*?)<\/h5>", res.text)[0]
    info = re.findall(r'<td\salign="right">(.*?)<\/td>', res.text)
    info = {
        'error': True,
        'message': 'Link Invalid.',
        'title': title,
        'size': info[0],
        'date': info[1]
    }
    new_gdtot = requests.get("https://new.gdtot.org/").url

    info['src_url'] = url
    res = client.get(f"{new_gdtot}dld?id={url.split('/')[-1]}")
    try:
        url = re.findall('URL=(.*?)"', res.text)[0]
        print(url)
    except:
        info['message'] = 'The requested URL could not be retrieved.',
        return info

    params = parse_qs(urlparse(url).query)

    if 'msgx' in params:
        info['message'] = params['msgx'][0]
    if 'gd' not in params or not params['gd'] or params['gd'][0] == 'false':
        return info

    try:
        decoded_id = base64.b64decode(str(params['gd'][0])).decode('utf-8')
        gdrive_url = f'https://drive.google.com/open?id={decoded_id}'
        info['message'] = 'Success.'
    except:
        info['error'] = True
        return info

    info['gdrive_link'] = gdrive_url
    return info


def gplink(url):

    check = re.findall(r'\bhttps?://.*gplink\S+', url)
    if not check:
        raise DirectDownloadLinkException("It's Not GPLinks")

    scraper = cloudscraper.create_scraper(allow_brotli=False)
    res = scraper.get(url)
    
    h = { "referer": res.url }
    res = scraper.get(url, headers=h)
    
    bs4 = BeautifulSoup(res.content, 'lxml')
    inputs = bs4.find_all('input')
    data = { input.get('name'): input.get('value') for input in inputs }

    h = {
        'content-type': 'application/x-www-form-urlencoded',
        'x-requested-with': 'XMLHttpRequest'
    }
    
    time.sleep(10) # !important
    
    p = urlparse(url)
    final_url = f'{p.scheme}://{p.netloc}/links/go'
    res = scraper.post(final_url, data=data, headers=h).json()

    return res

def appdrive_dl(url: str, is_direct) -> str:
    """ AppDrive link generator
    By https://github.com/xcscxr , More Clean Look by https://github.com/DragonPower84 """

    if EMAIL is None or PWSSD is None:
        raise DirectDownloadLinkException("Appdrive Cred Is Not Given")
    account = {'email': EMAIL, 'passwd': PWSSD}
    client = requests.Session()
    client.headers.update({
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    })
    data = {
        'email': account['email'],
        'password': account['passwd']
    }
    client.post(f'https://{urlparse(url).netloc}/login', data=data)
    data = {
        'root_drive': '',
        'folder': GDRIVE_FOLDER_ID
    }
    client.post(f'https://{urlparse(url).netloc}/account', data=data)
    res = client.get(url)
    key = re.findall(r'"key",\s+"(.*?)"', res.text)[0]
    ddl_btn = etree.HTML(res.content).xpath("//button[@id='drc']")
    info = re.findall(r'>(.*?)<\/li>', res.text)
    info_parsed = {}
    for item in info:
        kv = [s.strip() for s in item.split(':', maxsplit = 1)]
        info_parsed[kv[0].lower()] = kv[1] 
    info_parsed = info_parsed
    info_parsed['error'] = False
    info_parsed['link_type'] = 'login' # direct/login
    headers = {
        "Content-Type": f"multipart/form-data; boundary={'-'*4}_",
    }
    data = {
        'type': 1,
        'key': key,
        'action': 'original'
    }
    if len(ddl_btn):
        info_parsed['link_type'] = 'direct'
        data['action'] = 'direct'
    while data['type'] <= 3:
        boundary=f'{"-"*6}_'
        data_string = ''
        for item in data:
             data_string += f'{boundary}\r\n'
             data_string += f'Content-Disposition: form-data; name="{item}"\r\n\r\n{data[item]}\r\n'
        data_string += f'{boundary}--\r\n'
        gen_payload = data_string
        try:
            response = client.post(url, data=gen_payload, headers=headers).json()
            break
        except: data['type'] += 1
    if 'url' in response:
        info_parsed['gdrive_link'] = response['url']
    elif 'error' in response and response['error']:
        info_parsed['error'] = True
        info_parsed['error_message'] = response['message']
    else:
        info_parsed['error'] = True
        info_parsed['error_message'] = 'Something went wrong :('
    if info_parsed['error']: return info_parsed
    if urlparse(url).netloc == 'driveapp.in' and not info_parsed['error']:
        res = client.get(info_parsed['gdrive_link'])
        drive_link = etree.HTML(res.content).xpath("//a[contains(@class,'btn')]/@href")[0]
        info_parsed['gdrive_link'] = drive_link
    if urlparse(url).netloc == 'drivesharer.in' and not info_parsed['error']:
        res = client.get(info_parsed['gdrive_link'])
        drive_link = etree.HTML(res.content).xpath("//a[contains(@class,'btn btn-primary')]/@href")[0]
        info_parsed['gdrive_link'] = drive_link
    if urlparse(url).netloc == 'drivebit.in' and not info_parsed['error']:
        res = client.get(info_parsed['gdrive_link'])
        drive_link = etree.HTML(res.content).xpath("//a[contains(@class,'btn btn-primary')]/@href")[0]
        info_parsed['gdrive_link'] = drive_link
    info_parsed['src_url'] = url
    return info_parsed


def linkvertise(url: str):
    client = requests.Session()
    headers = {
        "User-Agent": "AppleTV6,2/11.1",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    client.headers.update(headers)
    url = url.replace("%3D", " ").replace("&o=sharing", "").replace("?o=sharing", "").replace("dynamic?r=", "dynamic/?r=")
    id_name = re.search(r"\/\d+\/[^\/]+", url)
    if not id_name: return None
    paths = [
        "/captcha", 
        "/countdown_impression?trafficOrigin=network", 
        "/todo_impression?mobile=true&trafficOrigin=network"
    ]
    for path in paths:
        url = f"https://publisher.linkvertise.com/api/v1/redirect/link{id_name[0]}{path}"
        response = client.get(url).json()
        if response["success"]: break
    data = client.get(f"https://publisher.linkvertise.com/api/v1/redirect/link/static{id_name[0]}").json()
    out = {
        'timestamp':int(str(time.time_ns())[0:13]),
        'random':"6548307", 
        'link_id':data["data"]["link"]["id"]
    }
    options = {
        'serial': base64.b64encode(json.dumps(out).encode()).decode()
    }
    data = client.get("https://publisher.linkvertise.com/api/v1/account").json()
    user_token = data["user_token"] if "user_token" in data.keys() else None
    url_submit = f"https://publisher.linkvertise.com/api/v1/redirect/link{id_name[0]}/target?X-Linkvertise-UT={user_token}"
    data = client.post(url_submit, json=options).json()
    return data

    '''client = requests.Session()
    res = client.get(url)
    ref = re.findall("action[ ]{0,}=[ ]{0,}['|\"](.*?)['|\"]", res.text)[0]
    h = {'referer': ref}
    res = client.get(url, headers=h)
    bs4 = BeautifulSoup(res.content, 'lxml')
    inputs = bs4.find_all('input')
    data = { input.get('name'): input.get('value') for input in inputs }
    h = {
        'content-type': 'application/x-www-form-urlencoded',
        'x-requested-with': 'XMLHttpRequest'
    }
    p = urlparse(url)
    final_url = f'{p.scheme}://{p.netloc}/links/go'
    time.sleep(3.1)
    res = client.post(final_url, data=data, headers=h).json()
    return res'''

def droplink(url):
    api = "https://api.emilyx.in/api"
    client = cloudscraper.create_scraper(allow_brotli=False)
    resp = client.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    try:
        resp = client.post(api, json={"type": "droplink", "url": url})
        res = resp.json()
    except Exception:
        return "API UnResponsive / Invalid Link !"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]

def gofile(url: str):
    api_uri = 'https://api.gofile.io'
    client = requests.Session()
    res = client.get(api_uri+'/createAccount').json()
    data = {
        'contentId': url.split('/')[-1],
        'token': res['data']['token'],
        'websiteToken': 'websiteToken',
        'cache': 'true'
    }
    res = client.get(api_uri+'/getContent', params=data).json()
    content = []
    for item in res['data']['contents'].values():
        content.append(item)
    #return content
    return {
        'accountToken': data['token'],
        'files': content
    }


ANCHOR_URL = 'https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Lcr1ncUAAAAAH3cghg6cOTPGARa8adOf-y9zv2x&co=aHR0cHM6Ly9vdW8uaW86NDQz&hl=en&v=1B_yv3CBEV10KtI2HJ6eEXhJ&size=invisible&cb=4xnsug1vufyr'

def RecaptchaV3(ANCHOR_URL):
    url_base = 'https://www.google.com/recaptcha/'
    post_data = "v={}&reason=q&c={}&k={}&co={}"
    client = requests.Session()
    client.headers.update({
        'content-type': 'application/x-www-form-urlencoded'
    })
    matches = re.findall(r'([api2|enterprise]+)\/anchor\?(.*)', ANCHOR_URL)[0]
    url_base += matches[0]+'/'
    params = matches[1]
    res = client.get(url_base+'anchor', params=params)
    token = re.findall(r'"recaptcha-token" value="(.*?)"', res.text)[0]
    params = dict(pair.split('=') for pair in params.split('&'))
    post_data = post_data.format(params["v"], token, params["k"], params["co"])
    res = client.post(url_base+'reload', params=f'k={params["k"]}', data=post_data)
    answer = re.findall(r'"rresp","(.*?)"', res.text)[0]    
    return answer


def ouo(url: str) -> str:
    """ Ouo Bypasser generator
    By https://github.com/xcscxr """

    client = requests.Session()
    tempurl = url.replace("ouo.press", "ouo.io")
    p = urlparse(tempurl)
    id = tempurl.split('/')[-1]
    res = client.get(tempurl)
    next_url = f"{p.scheme}://{p.hostname}/go/{id}"

    for _ in range(2):
        if res.headers.get('Location'):
            break
        bs4 = BeautifulSoup(res.content, 'lxml')
        inputs = bs4.form.findAll("input", {"name": re.compile(r"token$")})
        data = { input.get('name'): input.get('value') for input in inputs }
        ans = RecaptchaV3(ANCHOR_URL)
        data['x-token'] = ans
        h = {
            'content-type': 'application/x-www-form-urlencoded'
        }
        res = client.post(next_url, data=data, headers=h, allow_redirects=False)
        next_url = f"{p.scheme}://{p.hostname}/xreallcygo/{id}"
    return {
        'original_link': url,
        'bypassed_link': res.headers.get('Location')
    }


def upindia(url: str) -> str:
  REGEX = r'(http[s]*://(?:upindia|uploadfile|upload)\.(?:cc|mobi)+/\d{6}/\S{7})'
  match = re.findall(REGEX, url)
  if not match:
    return "The Provided Link Do not Match with the Standard Format."
  
  session = requests.Session()
  url = match[0]
  LOGGER.debug(f"Matched URL: {url}")
  file_id, file_code = url.split('/')[-2:]
  LOGGER.debug(f"File Code: {file_code}, File Id: {file_id}")
  url_parts = urllib.parse.urlparse(url)
  req = session.get(url)
  page_html = req.text
  itemlink = re.findall(r'class="download_box_new[^"]*".*itemlink="([^">]+)"', page_html)
  if not itemlink:
    return "File Does Not Exist!"
  
  itemlink = itemlink[0]
  itemlink_parsed = urllib.parse.parse_qs(itemlink)
  file_key = itemlink_parsed['down_key'][0]
  LOGGER.debug(f"file_key: {file_key}")
  params = {
    'file_id':file_id,
    'file_code':file_code,
    'file_key':file_key,
    'serv':1
  }
  req_url = url_parts.scheme + '://' +  url_parts.netloc + "/download"
  r = session.head(req_url, params=params)
  dl_url = r.headers.get('location', None)
  if dl_url is None:
    return "This File cannot be Downloaded at this moment!"
  LOGGER.debug(dl_url)
  return dl_url


def hubdrive(url: str) -> str:

    if HUB_CRYPT is None:
        raise DirectDownloadLinkException("HubDrive CRYPT Is Not Given")
    client = requests.Session()
    client.cookies.update({'crypt': HUB_CRYPT})
    res = client.get(url)
    info_parsed = {}
    title = re.findall(r'>(.*?)<\/h4>', res.text)[0]
    info_chunks = re.findall(r'>(.*?)<\/td>', res.text)
    info_parsed['title'] = title
    for i in range(0, len(info_chunks), 2):
        info_parsed[info_chunks[i]] = info_chunks[i+1]
    info_parsed = info_parsed 
    info_parsed['error'] = False
    up = urlparse(url)
    req_url = f"{up.scheme}://{up.netloc}/ajax.php?ajax=download"
    file_id = url.split('/')[-1]
    data = { 'id': file_id }
    headers = {
        'x-requested-with': 'XMLHttpRequest'
    }
    try:
        res = client.post(req_url, headers=headers, data=data).json()['file']
    except: return {'error': True, 'src_url': url}
    gd_id = re.findall('gd=(.*)', res, re.DOTALL)[0]
    info_parsed['gdrive_url'] = f"https://drive.google.com/open?id={gd_id}"
    info_parsed['src_url'] = url
    if info_parsed['error']:
        raise DirectDownloadLinkException(f"Error in HubDrive Link")
    return info_parsed


def adfly(url: str) -> str:

    res = requests.get(url).text
    out = {'error': False, 'src_url': url}
    try:
        ysmm = re.findall(r"ysmm\s+=\s+['|\"](.*?)['|\"]", res)[0]
    except:
        out['error'] = True
        return out
    a, b = '', ''
    for i in range(0, len(code)):
        if i % 2 == 0: a += code[i]
        else: b = code[i] + b
    code = ysmm
    key = list(a + b)
    i = 0
    while i < len(key):
        if key[i].isdigit():
            for j in range(i+1,len(key)):
                if key[j].isdigit():
                    u = int(key[i]) ^ int(key[j])
                    if u < 10: key[i] = str(u)
                    i = j					
                    break
        i+=1
    key = ''.join(key)
    decrypted = b64decode(key)[16:-16]
    url = decrypted.decode('utf-8')
    #url = decrypt_url(ysmm)
    if re.search(r'go\.php\?u\=', url):
        url = b64decode(re.sub(r'(.*?)u=', '', url)).decode()
    elif '&dest=' in url:
        url = unquote(re.sub(r'(.*?)dest=', '', url))
    out['bypassed_url'] = url
    if out['error']:
        raise DirectDownloadLinkException(f"Error in Adfly Link")
    return out


def sourceforge(url: str) -> str:
    """ SourceForge direct links generator
    Based on https://github.com/REBEL75/REBELUSERBOT """
    try:
        link = re.findall(r"\bhttps?://sourceforge\.net\S+", url)[0]
    except IndexError:
        return "`No SourceForge links found`\n"
    file_path = re.findall(r"files(.*)/download", url)[0]
    project = re.findall(r"projects?/(.*?)/files", url)[0]
    mirrors = (
        f"https://sourceforge.net/settings/mirror_choices?"
        f"projectname={project}&filename={file_path}"
    )
    page = BeautifulSoup(requests.get(mirrors).content, "html.parser")
    info = page.find("ul", {"id": "mirrorList"}).findAll("li")
    for mirror in info[1:]:
        dl_url = f'https://{mirror["id"]}.dl.sourceforge.net/project/{project}/{file_path}?viasf=1'
    return dl_url


def sourceforge2(url: str) -> str:
    """ Sourceforge Master.dl bypass """
    return f"{url}" + "?viasf=1"


def androidatahost(url: str) -> str:
    """ Androiddatahost direct generator
        Based on https://github.com/nekaru-storage/re-cerminbot """
    try:
        link = re.findall(r"\bhttps?://androiddatahost\.com\S+", url)[0]
    except IndexError:
        return "`No Androiddatahost links found`\n"
    url3 = BeautifulSoup(requests.get(link).content, "html.parser")
    fin = url3.find("div", {'download2'})
    return fin.find('a')["href"]


def sfile(url: str) -> str:
    """ Sfile.mobi direct generator
        Based on https://github.com/nekaru-storage/re-cerminbot """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532G Build/MMB29T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.83 Mobile Safari/537.36'
    }
    url3 = BeautifulSoup(requests.get(url, headers=headers).content, "html.parser")
    return url3.find('a', 'w3-button w3-blue')['href']


def androidfilehost(url: str) -> str:

    try:
        link = re.findall(r"\bhttps?://.*androidfilehost.*fid.*\S+", url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No AFH links found`\n")
        return reply
    fid = re.findall(r"\?fid=(.*)", link)[0]
    session = requests.Session()
    user_agent = useragent()
    if user_agent == "":
        raise DirectDownloadLinkException("`Error: Can't find Mirrors for the link`\n")
        error = "Error: Can't find Mirrors for the link"
        return error
    headers = {"user-agent": user_agent}
    res = session.get(link, headers=headers, allow_redirects=True)
    headers = {
        "origin": "https://androidfilehost.com",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "user-agent": user_agent,
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "x-mod-sbb-ctype": "xhr",
        "accept": "*/*",
        "referer": f"https://androidfilehost.com/?fid={fid}",
        "authority": "androidfilehost.com",
        "x-requested-with": "XMLHttpRequest",
    }
    data = {
        "submit": "submit",
        "action": "getdownloadmirrors",
        "fid": f"{fid}"}
    mirrors = None
    reply = ""
    error = "`Error: Can't find Mirrors for the link`\n"
    try:
        req = session.post(
            "https://androidfilehost.com/libs/otf/mirrors.otf.php",
            headers=headers,
            data=data,
            cookies=res.cookies,
        )
        mirrors = req.json()["MIRRORS"]
    except (json.decoder.JSONDecodeError, TypeError):
        reply += error
    if not mirrors:
        reply += error
        return reply
    for item in mirrors:
        name = item["name"]
        dl_url = item["url"]
        #reply += f"[{name}]({dl_url}) "
    return dl_url 
 
def useragent():
    try:
        useragents = BeautifulSoup(
            requests.get(
                "https://developers.whatismybrowser.com/"
                "useragents/explore/operating_system_name/android/"
            ).content,
            "lxml",
        ).findAll("td", {"class": "useragent"})
        user_agent = choice(useragents)
        return user_agent.text
    except IndexError:
        return ""


def wetransfer(url: str):
    """ Based on https://github.com/Chason610/Flameshot1/blob/bd90f4c9d677f972a4d2435c00614d0fc1330c67/scripts/upload_services/transferwee.py
    Given a wetransfer.com download URL download return the downloadable URL.
    """
    WETRANSFER_API_URL = 'https://wetransfer.com/api/v4/transfers'
    WETRANSFER_DOWNLOAD_URL = WETRANSFER_API_URL + '/{transfer_id}/download'

    # Follow the redirect if we have a short URL
    if url.startswith('https://we.tl/'):
        r = requests.head(url, allow_redirects=True)
        url = r.url
    recipient_id = None
    params = urllib.parse.urlparse(url).path.split('/')[2:]
    if len(params) == 2:
        transfer_id, security_hash = params
    elif len(params) == 3:
        transfer_id, recipient_id, security_hash = params
    else:
        raise DirectDownloadLinkException(f"Error in wetransfer.com Link")
        return None
    j = {
        "intent": "entire_transfer",
        "security_hash": security_hash,
    }
    if recipient_id:
        j["recipient_id"] = recipient_id
    s = ression()
    r = s.get('https://wetransfer.com/')
    m = re.search('name="csrf-token" content="([^"]+)"', r.text)
    s.headers.update(
        {
            "x-csrf-token": m.group(1),
            "x-requested-with": "XMLHttpRequest",
        }
    )
    r = s.post(WETRANSFER_DOWNLOAD_URL.format(transfer_id=transfer_id),
               json=j)
    j = r.json()
    try:
        if "direct_link" in j:
            return j["direct_link"]
    except:
        raise DirectDownloadLinkException("ERROR: Error while trying to generate Direct Link from WeTransfer!") 


def shorte_st(url: str):    
    client = requests.Session()
    client.headers.update({'referer': url})
    p = urlparse(url)
    res = client.get(url)
    sess_id = re.findall(r'''sessionId(?:\s+)?:(?:\s+)?['|"](.*?)['|"]''', res.text)[0]
    final_url = f"{p.scheme}://{p.netloc}/shortest-url/end-adsession"
    params = {
        'adSessionId': sess_id,
        'callback': '_'
    }
    time.sleep(5)
    res = client.get(final_url, params=params)
    dest_url = re.findall('"(.*?)"', res.text)[1].replace(r'\/','/')
    return dest_url


def mdisk(url: str) -> str:
    """MDisk DDL link generator"""

    try:
        fxl = url.split("/")
        urlx = fxl[-1]
        scraper = cloudscraper.create_scraper(interpreter="nodejs", allow_brotli=False)
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"
        }
        apix = f"http://x.egraph.workers.dev/?param={urlx}"
        try:
            response = scraper.get(apix, headers=headers)
            query = response.json()
        except:
            raise DirectDownloadLinkException("ERROR: Error while trying to generate Direct Link from MDisk!")
        return query
    except ValueError:
        raise DirectDownloadLinkException("ERROR: The Content is Deleted from MDisk!")


def drivefire_dl(url: str):

    if DRIVEFIRE_CRYPT is None:
        raise DirectDownloadLinkException("DriveFire CRYPT Is Not Given")

    client = requests.Session()
    client.cookies.update({'crypt': DRIVEFIRE_CRYPT})
    
    res = client.get(url)

    info_parsed = {}
    title = re.findall(r'>(.*?)<\/h4>', res.text)[0]
    info_chunks = re.findall(r'>(.*?)<\/td>', res.text)
    info_parsed['title'] = title
    for i in range(0, len(info_chunks), 2):
        info_parsed[info_chunks[i]] = info_chunks[i+1]
    
    info_parsed['error'] = False
    
    up = urlparse(url)
    req_url = f"{up.scheme}://{up.netloc}/ajax.php?ajax=download"
    
    file_id = url.split('/')[-1]
    data = { 'id': file_id }
    headers = {
        'x-requested-with': 'XMLHttpRequest'
    }
    
    try:
        res = client.post(req_url, headers=headers, data=data).json()['file']
    except: return {'error': True, 'src_url': url}
    
    decoded_id = res.rsplit('/', 1)[-1]
    info_parsed = f"https://drive.google.com/file/d/{decoded_id}"

    return info_parsed


def katdrive_dl(url):

    if KATDRIVE_CRYPT is None:
        raise DirectDownloadLinkException("KatDrive CRYPT Is Not Given")

    client = requests.Session()
    client.cookies.update({'crypt': KATDRIVE_CRYPT})
    
    res = client.get(url)

    info_parsed = {}
    title = re.findall(r'>(.*?)<\/h4>', res.text)[0]
    info_chunks = re.findall(r'>(.*?)<\/td>', res.text)
    info_parsed['title'] = title
    for i in range(0, len(info_chunks), 2):
        info_parsed[info_chunks[i]] = info_chunks[i+1]
    
    info_parsed['error'] = False
    
    up = urlparse(url)
    req_url = f"{up.scheme}://{up.netloc}/ajax.php?ajax=download"
    
    file_id = url.split('/')[-1]
    data = { 'id': file_id }
    headers = {
        'x-requested-with': 'XMLHttpRequest'
    }
    
    try:
        res = client.post(req_url, headers=headers, data=data).json()['file']
    except: return {'error': True, 'src_url': url}
    
    gd_id = re.findall('gd=(.*)', res, re.DOTALL)[0]
    
    info_parsed['gdrive_url'] = f"https://drive.google.com/open?id={gd_id}"
    info_parsed['src_url'] = url

    return info_parsed


def kolop_dl(url):

    if KOLOP_CRYPT is None:
        raise DirectDownloadLinkException("Kolop CRYPT Is Not Given")

    client = requests.Session()
    client.cookies.update({'crypt': KOLOP_CRYPT})
    
    res = client.get(url)
    info_parsed = {}
    title = re.findall(r'>(.*?)<\/h4>', res.text)[0]
    info_chunks = re.findall(r'>(.*?)<\/td>', res.text)
    info_parsed['title'] = title
    for i in range(0, len(info_chunks), 2):
        info_parsed[info_chunks[i]] = info_chunks[i+1]
    info_parsed['error'] = False
    
    up = urlparse(url)
    req_url = f"{up.scheme}://{up.netloc}/ajax.php?ajax=download"
    
    file_id = url.split('/')[-1]
    data = { 'id': file_id }
    headers = {
        'x-requested-with': 'XMLHttpRequest'
    }
    
    try:
        res = client.post(req_url, headers=headers, data=data).json()['file']
    except: return {'error': True, 'src_url': url}
    
    gd_id = re.findall('gd=(.*)', res, re.DOTALL)[0]
    
    info_parsed['gdrive_url'] = f"https://drive.google.com/open?id={gd_id}"
    info_parsed['src_url'] = url

    return info_parsed


def drivebuzz_dl(url):

    if DRIVEBUZZ_CRYPT is None:
        raise DirectDownloadLinkException("DriveBuzz CRYPT Is Not Given")

    client = requests.Session()
    client.cookies.update({'crypt': DRIVEBUZZ_CRYPT})
    
    res = client.get(url)

    info_parsed = {}
    title = re.findall(r'>(.*?)<\/h4>', res.text)[0]
    info_chunks = re.findall(r'>(.*?)<\/td>', res.text)
    info_parsed['title'] = title
    for i in range(0, len(info_chunks), 2):
        info_parsed[info_chunks[i]] = info_chunks[i+1]
    
    info_parsed['error'] = False
    
    up = urlparse(url)
    req_url = f"{up.scheme}://{up.netloc}/ajax.php?ajax=download"
    
    file_id = url.split('/')[-1]
    data = { 'id': file_id }
    headers = {
        'x-requested-with': 'XMLHttpRequest'
    }
    
    try:
        res = client.post(req_url, headers=headers, data=data).json()['file']
    except: return {'error': True, 'src_url': url}
    
    gd_id = re.findall('gd=(.*)', res, re.DOTALL)[0]
    
    info_parsed['gdrive_url'] = f"https://drive.google.com/open?id={gd_id}"
    info_parsed['src_url'] = url

    return info_parsed


def gadrive_dl(url):

    if GADRIVE_CRYPT is None:
        raise DirectDownloadLinkException("GADrive CRYPT Is Not Given")

    client = requests.Session()
    client.cookies.update({'crypt': GADRIVE_CRYPT})
    
    res = client.get(url)

    info_parsed = {}
    title = re.findall(r'>(.*?)<\/h4>', res.text)[0]
    info_chunks = re.findall(r'>(.*?)<\/td>', res.text)
    info_parsed['title'] = title
    for i in range(0, len(info_chunks), 2):
        info_parsed[info_chunks[i]] = info_chunks[i+1]
    
    info_parsed['error'] = False
    
    up = urlparse(url)
    req_url = f"{up.scheme}://{up.netloc}/ajax.php?ajax=download"
    
    file_id = url.split('/')[-1]
    data = { 'id': file_id }
    headers = {
        'x-requested-with': 'XMLHttpRequest'
    }
    
    try:
        res = client.post(req_url, headers=headers, data=data).json()['file']
    except: return {'error': True, 'src_url': url}
    
    gd_id = re.findall('gd=(.*)', res, re.DOTALL)[0]
    
    info_parsed['gdrive_url'] = f"https://drive.google.com/open?id={gd_id}"
    info_parsed['src_url'] = url

    return info_parsed

def try2link_bypass(url):
	client = cloudscraper.create_scraper(allow_brotli=False)
	
	url = url[:-1] if url[-1] == '/' else url
	
	params = (('d', int(time.time()) + (60 * 4)),)
	r = client.get(url, params=params, headers= {'Referer': 'https://newforex.online/'})
	
	soup = BeautifulSoup(r.text, 'html.parser')
	inputs = soup.find(id="go-link").find_all(name="input")
	data = { input.get('name'): input.get('value') for input in inputs }	
	time.sleep(7)
	
	headers = {'Host': 'try2link.com', 'X-Requested-With': 'XMLHttpRequest', 'Origin': 'https://try2link.com', 'Referer': url}
	
	bypassed_url = client.post('https://try2link.com/links/go', headers=headers,data=data)
	return bypassed_url.json()["url"]
		

def try2link_scrape(url):
	client = cloudscraper.create_scraper(allow_brotli=False)	
	h = {
	'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
	}
	res = client.get(url, cookies={}, headers=h)
	url = 'https://try2link.com/'+re.findall('try2link\.com\/(.*?) ', res.text)[0]
	return try2link_bypass(url)
    

def psa_bypasser(psa_url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    r = client.get(psa_url)
    soup = BeautifulSoup(r.text, "html.parser").find_all(class_="dropshadowboxes-drop-shadow dropshadowboxes-rounded-corners dropshadowboxes-inside-and-outside-shadow dropshadowboxes-lifted-both dropshadowboxes-effect-default")
    links = ""
    for link in soup:
        try:
            exit_gate = link.a.get("href")
            links = links + try2link_scrape(exit_gate) + '\n'
        except: pass
    return links

def uploadee(url: str) -> str:
    """ uploadee direct link generator
    By https://github.com/iron-heart-x"""
    try:
        soup = BeautifulSoup(rget(url).content, 'lxml')
        sa = soup.find('a', attrs={'id':'d_l'})
        return sa['href']
    except:
        raise DirectDownloadLinkException(f"ERROR: Failed to acquire download URL from upload.ee for : {url}")

def dropbox(url):
    return url.replace("www.","").replace("dropbox.com","dl.dropboxusercontent.com").replace("?dl=0","")

def megaup(url):
    api = "https://api.emilyx.in/api"
    client = cloudscraper.create_scraper(allow_brotli=False)
    resp = client.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    try:
        resp = client.post(api, json={"type": "megaup", "url": url})
        res = resp.json()
    except Exception:
        return "API UnResponsive / Invalid Link !"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]

def mediafire(url: str) -> str:
    """ MediaFire direct link generator """
    try:
        link = re_findall(r'\bhttps?://.*mediafire\.com\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("No MediaFire links found")
    page = BeautifulSoup(rget(link).content, 'lxml')
    info = page.find('a', {'aria-label': 'Download file'})
    return info.get('href')

def getlinks(dlc,client):
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
    'Accept': 'application/json, text/javascript, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'http://dcrypt.it',
    'Connection': 'keep-alive',
    'Referer': 'http://dcrypt.it/',
    }

    data = {
        'content': dlc,
    }

    response = client.post('http://dcrypt.it/decrypt/paste', headers=headers, data=data).json()["success"]["links"]
    links = ""
    for link in response:
        links = links + link + "\n"
    return links[:-1]


def filecrypt(url):

    client = cloudscraper.create_scraper(allow_brotli=False)
    headers = {
    "authority": "filecrypt.co",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "content-type": "application/x-www-form-urlencoded",
    "dnt": "1",
    "origin": "https://filecrypt.co",
    "referer": url,
    "sec-ch-ua": '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36" 
    }
    

    resp = client.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, "html.parser")

    buttons = soup.find_all("button")
    for ele in buttons:
        line = ele.get("onclick")
        if line !=None and "DownloadDLC" in line:
            dlclink = "https://filecrypt.co/DLC/" + line.split("DownloadDLC('")[1].split("'")[0] + ".html"
            break

    resp = client.get(dlclink,headers=headers)
    return getlinks(resp.text,client)

def shareus(url):
    token = url.split("=")[-1]
    bypassed_url = "https://us-central1-my-apps-server.cloudfunctions.net/r?shortid="+ token
    response = requests.get(bypassed_url).text
    return response

def shortlingly(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    if 'shortingly.me' in url:
        DOMAIN = "https://go.techyjeeshan.xyz"
    else:
        return "Incorrect Link"

    url = url[:-1] if url[-1] == '/' else url

    code = url.split("/")[-1]
    
    final_url = f"{DOMAIN}/{code}"

    resp = client.get(final_url)
    soup = BeautifulSoup(resp.content, "html.parser")
    
    try: inputs = soup.find(id="go-link").find_all(name="input")
    except: return "Incorrect Link"
    
    data = { input.get('name'): input.get('value') for input in inputs }

    h = { "x-requested-with": "XMLHttpRequest" }
    
    time.sleep(5)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try:
        return r.json()['url']
    except: return "Something went wrong :("

def gyanilinks(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    if 'gtlinks.me' in url:
        DOMAIN = "https://go.bloggertheme.xyz"
    else:
        return "Incorrect Link"

    url = url[:-1] if url[-1] == '/' else url

    code = url.split("/")[-1]
    
    final_url = f"{DOMAIN}/{code}"

    resp = client.get(final_url)
    soup = BeautifulSoup(resp.content, "html.parser")
    
    try: inputs = soup.find(id="go-link").find_all(name="input")
    except: return "Incorrect Link"
    
    data = { input.get('name'): input.get('value') for input in inputs }

    h = { "x-requested-with": "XMLHttpRequest" }
    
    time.sleep(5)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try:
        return r.json()['url']
    except: return "Something went wrong :("

def pixl(url):
    count = 1
    dl_msg = ""
    currentpage = 1
    settotalimgs = True
    totalimages = ""
    client = cloudscraper.create_scraper(allow_brotli=False)
    resp = client.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    soup = BeautifulSoup(resp.content, "html.parser")
    if "album" in url and settotalimgs:
        totalimages = soup.find("span", {"data-text": "image-count"}).text
        settotalimgs = False
    thmbnailanch = soup.findAll(attrs={"class": "--media"})
    links = soup.findAll(attrs={"data-pagination": "next"})
    try:
        url = links[0].attrs["href"]
    except BaseException:
        url = None
    for ref in thmbnailanch:
        imgdata = client.get(ref.attrs["href"])
        if not imgdata.status_code == 200:
            time.sleep(5)
            continue
        imghtml = BeautifulSoup(imgdata.text, "html.parser")
        downloadanch = imghtml.find(attrs={"class": "btn-download"})
        currentimg = downloadanch.attrs["href"]
        currentimg = currentimg.replace(" ", "%20")
        dl_msg += f"{count}. {currentimg}\n"
        count += 1
    currentpage += 1
    fld_msg = f"Your provided Pixl.is link is of Folder and I've Found {count - 1} files in the folder.\n"
    fld_link = f"\nFolder Link: {url}\n"
    final_msg = fld_link + "\n" + fld_msg + "\n" + dl_msg
    return final_msg

def siriganbypass(url):
    client = requests.Session()
    res = client.get(url)
    url = res.url.split('=', maxsplit=1)[-1]

    while True:
        try: url = base64.b64decode(url).decode('utf-8')
        except: break

    return url.split('url=')[-1]

def parse_info_sharer(res):
    f = re.findall(">(.*?)<\/td>", res.text)
    info_parsed = {}
    for i in range(0, len(f), 3):
        info_parsed[f[i].lower().replace(' ', '_')] = f[i+2]
    return info_parsed

def sharer_pw(url, forced_login=False):
    client = cloudscraper.create_scraper(allow_brotli=False)
    client.cookies.update({
        "XSRF-TOKEN": XSRF_TOKEN,
        "laravel_session": LARAVEL_SESSION
    })
    res = client.get(url)
    token = re.findall("_token\s=\s'(.*?)'", res.text, re.DOTALL)[0]
    ddl_btn = etree.HTML(res.content).xpath("//button[@id='btndirect']")
    info_parsed = parse_info_sharer(res)
    info_parsed['error'] = True
    info_parsed['src_url'] = url
    info_parsed['link_type'] = 'login'
    info_parsed['forced_login'] = forced_login
    headers = {
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'x-requested-with': 'XMLHttpRequest'
    }
    data = {
        '_token': token
    }
    if len(ddl_btn):
        info_parsed['link_type'] = 'direct'
    if not forced_login:
        data['nl'] = 1
    try: 
        res = client.post(url+'/dl', headers=headers, data=data).json()
    except:
        return info_parsed
    if 'url' in res and res['url']:
        info_parsed['error'] = False
        info_parsed['gdrive_link'] = res['url']
    if len(ddl_btn) and not forced_login and not 'url' in info_parsed:
        # retry download via login
        return sharer_pw(url, forced_login=True)
    return info_parsed["gdrive_link"]

def bypass_vip(url):
    try:
        payload = {"url": url}
        url_bypass = requests.post("https://api.bypass.vip/", data=payload).json()
        bypassed = url_bypass["destination"]
        return bypassed
    except:
        return "Could not Bypass your URL :("

def rocklinks(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    if 'rocklinks.net' in url:
        DOMAIN = "https://blog.disheye.com"
    else:
        DOMAIN = "https://rocklinks.net"

    url = url[:-1] if url[-1] == '/' else url

    code = url.split("/")[-1]
    if 'rocklinks.net' in url:
        final_url = f"{DOMAIN}/{code}?quelle=" 
    else:
        final_url = f"{DOMAIN}/{code}"

    resp = client.get(final_url)
    soup = BeautifulSoup(resp.content, "html.parser")
    
    try: inputs = soup.find(id="go-link").find_all(name="input")
    except: return "Incorrect Link"
    
    data = { input.get('name'): input.get('value') for input in inputs }

    h = { "x-requested-with": "XMLHttpRequest" }
    
    time.sleep(10)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try:
        return r.json()['url']
    except: return "Something went wrong :("

def olamovies(url):
    #print("this takes time, you might want to take a break.")
    headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': url,
            'Alt-Used': 'olamovies.ink',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
        }

    client = cloudscraper.create_scraper()
    res = client.get(url)
    soup = BeautifulSoup(res.text,"html.parser")
    soup = soup.findAll("div", class_="wp-block-button")

    outlist = []
    for ele in soup:
        outlist.append(ele.find("a").get("href"))

    slist = []
    for ele in outlist:
        try:
            key = ele.split("?key=")[1].split("&id=")[0].replace("%2B","+").replace("%3D","=").replace("%2F","/")
            id = ele.split("&id=")[1]
        except:
            continue
        
        count = 3
        params = { 'key': key, 'id': id}
        soup = "None"
        # print("trying","https://olamovies.ink/download/&key="+key+"&id="+id)

        while 'rocklinks.net' not in soup and "try2link.com" not in soup:
            res = client.get("https://olamovies.ink/download/", params=params, headers=headers)
            soup = BeautifulSoup(res.text,"html.parser")
            soup = soup.findAll("a")[0].get("href")
            if soup != "":
                if "try2link.com" in soup or 'rocklinks.net' in soup:
                    # print("added", soup)
                    slist.append(soup)
                else:
                    # print(soup, "not addded")
                    pass
            else:
                if count == 0:
                    # print('moving on')
                    break
                else:
                    count -= 1
                    # print("retrying")
                
            # print("waiting 10 secs")
            time.sleep(10)

    #print(slist)
    final = []
    for ele in slist:
        if "rocklinks.net" in ele:
            final.append(rocklinks(ele))
        elif "try2link.com" in ele:
            final.append(try2link_bypass(ele))
        else:
            # print(ele)
            pass
    #print(final)
    links = ""
    for ele in final:
        links = links + ele + "\n"
    #print("Bypassed Links")
    #print(links)
    return links
