import base64 
import json
import cloudscraper

from urllib.parse import quote as q
from asyncio import sleep as asleep
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tobrot import LOGGER, UPDATES_CHANNEL
from tobrot.helper_funcs.display_progress import humanbytes_int
from tobrot.plugins import getUserOrChaDetails
from tobrot.plugins.mediainfo import post_to_telegraph
from tobrot.bot_theme.themes import BotTheme

nexPage = False
nexPageToken = "" 

def authorization_token(username, password):
    user_pass = f"{username}:{password}"
    return f"Basic {base64.b64encode(user_pass.encode()).decode()}"
	 	 
async def scrapeURL(payload_input, url, username, password): 
    global nexPage
    global nexPageToken
    url = f"{url}/" if url[-1] != '/' else url

    try: 
        headers = {"authorization":authorization_token(username,password)}
    except Exception as e: 
        LOGGER.info(f"[INDEX SCRAPE] Error : {e}")
        return f"Error : {e}", True

    session = cloudscraper.create_scraper(allow_brotli=False)
    enResp = session.post(url, data=payload_input, headers=headers)
    if enResp.status_code == 401: 
        return "Could not Acess your Entered URL!, Check your Username / Password", True

    try: 
        deResp = json.loads(base64.b64decode(enResp.text[::-1][24:-20]).decode('utf-8'))
    except Exception as err: 
        LOGGER.info(f"[INDEX SCRAPE] Error : {err}")
        return "Something Went Wrong. Check Index Link / Username / Password Valid or Not", True

    pagToken = deResp["nextPageToken"]
    if pagToken is None: 
        nexPage = False
    else: 
        nexPage = True 
        nexPageToken = pagToken 

    if list(deResp.get("data").keys())[0] == "error":
        return "Nothing Found in Your Entered URL", True
    file_length = len(deResp["data"]["files"])
    scpText = ""

    scpText += f"🗄 <i><b> Total Files : </b></i> {file_length} <br><br>"
    LOGGER.info(file_length)
    for i, _ in enumerate(range(file_length)):

        files_type = deResp["data"]["files"][i]["mimeType"]
        files_name = deResp["data"]["files"][i]["name"]
        direct_download_link = url + q(files_name)
        no = i + 1
        LOGGER.info(direct_download_link)
        if files_type == "application/vnd.google-apps.folder":
            url_link = f'{direct_download_link}/'
            scpText += f"📄 <strong>{no}. {files_name}</strong> : <br><br><pre>🔖 Directory Index Link :<a href='{url_link}'> Index Link </a> <br>"
            #await asleep(10)
            #scpInText, error = await scrapeURL(payload_input, url, username, password)
            #if not error:
            #    title = "Directory Link Scrapper"
            #    tgh_link = post_to_telegraph(title, scpInText)
            #    LOGGER.info(tgh_link)
            #    scpText += f"<br>📂 Telegraph Link : <a href='{tgh_link}'> Click Here </a> | 📋 Type : {files_type} "
            scpText += f"<br>📂 Size : - | 📋 Type : {files_type} "
        else:
            scpText += f"📄 <strong>{no}. {files_name}</strong> : <br><br><pre>🔖 Index Link :<a href='{direct_download_link}'> Index Link </a> <br>"
            try:
                files_size = deResp["data"]["files"][i]["size"]
                scpText += f"<br>📂 Size : {humanbytes_int(files_size)} | 📋 Type : {files_type} "
            except:
                pass
        try:
            files_time = deResp["data"]["files"][i]["modifiedTime"]
            scpText += f"| ⏰ Modified Time : {files_time}<br><br>"
        except:
            pass
        scpText += "</pre>"
    LOGGER.info(scpText)
    return scpText, False
	        
	
async def index_scrape(client, message):
    '''  /indexscape <link>\n username\n password uscommand '''
    lm = await message.reply_text(
        text="`Scrapping Down ...`",
    )
    username = ""
    password = ""
    user_id_, u_men = getUserOrChaDetails(message)
    _send = message.text.split(" ", maxsplit=1)
    reply_to = message.reply_to_message
    if len(_send) > 1:
        txt = _send[1]
    elif reply_to is not None:
        txt = reply_to.text
    else:
        txt = ""
    url = ""
    if txt != "":
        _lin = txt.split("\n")
        url = _lin[0]
        try:
            username = _lin[1]
            password = _lin[2]
        except:
            username="none"
            password="none"
    else:
        await lm.edit_text("`Not Provided URL to Scrape`")
        return
    x = 0
    global body_text
    if url:
        body_text = f"<i>🔗 Raw Index Link :</i> <a href='{url}'> Click Here </a> <br>"
    if username != "none" and password != "none":
        cpass = "".join("*" for _ in range(len(password)))
        cname = "".join("*" for _ in range(len(username)))
        body_text += f"<i>👤 Username :</i> {cname} <br><i>📟 Password :</i> {cpass} <br><hr><br>"
    payload = {"page_token":nexPageToken, "page_index": x}
    LOGGER.info(f"Index Scrape Link: {url}")
    body_txt, error = await scrapeURL(payload, url, username, password)

    body_text += str(body_txt)

    if error:
        await lm.delete()
        await message.reply_text(body_txt)
        return

    while nexPage == True: #Not to be Executed 
        payload = {"page_index":nexPageToken, "page_index": x}
        print(await scrapeURL(payload, url, username, password))
        x += 1

    title = "Index Link Scrapper"
    tgh_link = post_to_telegraph(title, body_text)

    markup_ = InlineKeyboardMarkup([[InlineKeyboardButton(text="Iɴᴅᴇx Sᴄʀᴀᴘᴇ Lɪɴᴋ", url=tgh_link)]])

    await lm.delete()
    await message.reply_text(text=((BotTheme(user_id_)).INDEX_SCRAPE_MSG).format(
            u_men = u_men,
            uid = user_id_,
            url = url,
            UPDATES_CHANNEL = UPDATES_CHANNEL
        ),
        reply_markup=markup_
    )

#┣ 📰 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲 : {cname}
#┣ 📟 𝗣𝗮𝘀𝘀𝘄𝗼𝗿𝗱 : {cpass}
