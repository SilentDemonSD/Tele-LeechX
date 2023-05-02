class TXStyle:
    TOGGLEDOC_MSG = '''┏━━ 🛠  𝗧𝗼𝗴𝗴𝗹𝗲 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀 :
┃
┣ 👤 𝐔𝐬𝐞𝐫 : {u_men} ( #ID{u_id} )
┃
┣🏷 𝐓𝐨𝐠𝐠𝐥𝐞 : 📁<code>Document 📂</code>
┃
┗━♦️ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 {UPDATES_CHANNEL}♦️━╹'''
    TOGGLEVID_MSG = '''┏━━ 🛠  𝗧𝗼𝗴𝗴𝗹𝗲 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀 :
┃
┣ 👤 𝐔𝐬𝐞𝐫 : {u_men} ( #ID{u_id}
┃
┣🏷𝐓𝐨𝐠𝐠𝐥𝐞 : <code>🎞 Video 🎞</code>
┃
┗━♦️ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 {UPDATES_CHANNEL}♦️━╹'''
    THUMB_REPLY = "<code>Processing . . . 🔄</code>"
    SAVE_THUMB_MSG = "<b>⚡<i>Custom Thumbnail 🖼 Saved for Next Uploads</i>⚡</b>\n\n <b><i>✅Your Photo is Set, Ready to Go ...👨‍🦯</i></b>."
    SAVE_THUMB_FAIL_MSG = "<b><i>⛔Sorry⛔</i></b>\n\n<b>❌ Reply with Image to Save Your Custom Thumbnail.❌</b>"
    CLEAR_THUMB_SUCC_MSG = "<b><i>✅Success✅</i></b>\n\n <b>🖼Custom Thumbnail Cleared Successfully As Per Your Request.</b>"
    CLEAR_THUMB_FAIL_MSG = "<b><i>⛔Sorry⛔</i></b>\n\n <b>❌Nothing to Clear For You❌</b>"
    PREFIX_MSG = "⚡️<i><b>Custom Prefix Set Successfully</b></i> ⚡️ \n\n👤 <b>User :</b> {u_men}\n🆔 <b>User ID :</b> <code>{uid}</code>\n🗃 <b>Prefix :</b> <code>{t}</code>"
    CAPTION_MSG = "⚡️<i><b>Custom Caption Set Successfully</b></i> ⚡️ \n\n👤 <b>User :</b> {u_men}\n🆔 <b>User ID :</b> <code>{uid}</code>\n🗃 <b>Caption :</b>\n<code>{t}</code>"
    IMDB_MSG = "⚡️<i><b>Custom Template Set Successfully</b></i> ⚡️ \n\n👤 <b>User :</b> {u_men}\n🆔 <b>User ID :</b> <code>{uid}</code>\n🗃 <b>IMDB Template :</b> \n<code>{t}</code>"
    THEME_MSG = "⚡️ <i><b>Available Custom Themes</b></i> ⚡️\n\n👤 <b>User :</b> {u_men}\n🆔 <b>User ID :</b> <code>{uid}</code>\n\n🗄 <b>Choose Available Theme from Below:</b>"
    STATS_MSG_1 = '┏━━━━ 📊 𝗕𝗼𝘁 𝗦𝘁𝗮𝘁𝘀 📊 ━━━━━╻\n┃\n'
    STATS_MSG_2 = '┣ 📝 <b>Commit Date:</b> {lc}\n┃\n'
    STATS_MSG_3 = '''┣ 🤖 <b>Bot Uptime:</b> {currentTime}
┣ 📶 <b>OS Uptime:</b> {osUptime}
┃
┣ 🚦<b>CPU:</b>
┃  ┗ <code>{cpu_prog} {cpuUsage}%</code>
┃
┣ 🧬 <b>RAM:</b>
┃  ┗ <code>{mem_prog} {mem_p}%</code>
┣  • <i><b>Total:</b> {mem_t}</i> ┃ • <i><b>Used:</b> {mem_u}</i>
┃                • <i><b>Free:</b> {mem_a}</i>
┃
┣ 🗃 <b>DISK:</b>
┃  ┗ <code>{disk_prog} {disk}%</code>
┣  • <i><b>Total:</b> {total}</i> ┃ • <i><b>Used:</b> {used}</i>
┃                • <i><b>Free:</b> {free}</i>
┃
┣ 🔁 <b>SWAP:</b>
┃  ┗ <code>{swap_prog} {swap_p}%</code>
┣  • <i><b>Total:</b> {swap_t}</i> ┃ • <i><b>Used:</b> {swap_u}</i>
┃                • <i><b>Free:</b> {swap_f}</i>
┃
┣ 🗄 <b>CORES:</b>
┃  ┗ <code>{core_prog} {core_per}%</code>
┣ 📄 <i><b>Physical Cores:</b> {p_core}</i> ┃ 📑 <i><b>Total Cores:</b> {t_core}</i>
┃
┣ 📤 <b>Total Upload Data :</b> {sent}
┣ 📥 <b>Total Download Data :</b> {recv}
┃
┗━♦️ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 {UP_CHANNEL}♦️━╹'''
    HELP_MSG = '''┏━ 🆘 <b>HELP MODULE</b> 🆘 ━━━╻
┃
┃• <i>Open Help to Get Tips and Help</i>
┃• <i>Use the Bot Like a Pro User</i>
┃• <i>Access Every Feature That Bot Offers in Better Way </i>
┃• <i>Go through Commands to Get Help</i>
┃
┗━♦️ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 {UPDATES_CHANNEL}♦️━╹'''
    INDEX_SCRAPE_MSG = """
┏━📮  𝗜𝗻𝗱𝗲𝘅 𝗦𝗰𝗿𝗮𝗽𝗲 𝗥𝗲𝘀𝘂𝗹𝘁 :
┃
┣👤 𝐔𝐬𝐞𝐫 : {u_men} ( #ID{uid} )
┃
┣🔗 𝗨𝗥𝗟 : <code> {url} </code>
┃
┗━♦️ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 {UPDATES_CHANNEL}♦️━╹
"""
    MEDIAINFO_MEDIA_MSG = '''
ℹ️ <code>MEDIA INFO</code> ℹ
┃
┃• <b>File Name :</b> <code>{filename}</code>
┃• <b>Mime Type :</b> <code>{mimetype}</code>
┃• <b>File Size :</b> <code>{filesize}</code>
┃• <b>Date :</b> <code>{date}</code>
┃• <b>File ID :</b> <code>{fileid}</code>
┃• <b>Media Type :</b> <code>{txt}</code>
┃
┗━♦️ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 {UPDATES_CHANNEL}♦️━╹
'''
    MEDIAINFO_DIRECT_MSG = """
ℹ️ <code>DIRECT LINK INFO</code> ℹ
┃
┃• <b>File Name :</b> <code>{tit}</code>
┃• <b>Direct Link :</b> <code>{link}</code>
┃
┗━♦️ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 {UPDATES_CHANNEL}♦️━╹
"""
    SPEEDTEST_MSG = '''
┏━━━━━━━━━━━━━━━━━━╻
┣━━🚀 𝐒𝐩𝐞𝐞𝐝𝐭𝐞𝐬𝐭 𝐈𝐧𝐟𝐨:
┣ <b>Upload:</b> <code>{upload}/s</code>
┣ <b>Download:</b>  <code>{download}/s</code>
┣ <b>Ping:</b> <code>{ping} ms</code>
┣ <b>Time:</b> <code>{timestamp}</code>
┣ <b>Data Sent:</b> <code>{bytes_sent}</code>
┣ <b>Data Received:</b> <code>{bytes_received}</code>
┃
┣━━🌐 𝐒𝐩𝐞𝐞𝐝𝐭𝐞𝐬𝐭 𝐒𝐞𝐫𝐯𝐞𝐫:
┣ <b>Name:</b> <code>{name}</code>
┣ <b>Country:</b> <code>{country}, {cc}</code>
┣ <b>Sponsor:</b> <code>{sponsor}</code>
┣ <b>Latency:</b> <code>{latency}</code>
┣ <b>Latitude:</b> <code>{serverlat}</code>
┣ <b>Longitude:</b> <code>{serverlon}</code>
┃
┣━━👤 𝐂𝐥𝐢𝐞𝐧𝐭 𝐃𝐞𝐭𝐚𝐢𝐥𝐬:
┣ <b>IP Address:</b> <code>{ip}</code>
┣ <b>Latitude:</b> <code>{clientlat}</code>
┣ <b>Longitude:</b> <code>{clientlon}</code>
┣ <b>Country:</b> <code>{clicountry}</code>
┣ <b>ISP:</b> <code>{isp}</code>
┣ <b>ISP Rating:</b> <code>{isprating}</code>
┃
┗━━━━━━━━━━━━━━━━━━╹
'''
    TSHELP_MSG = '''
┏━ 𝗧𝗼𝗿𝗿𝗲𝗻𝘁 𝗦𝗲𝗮𝗿𝗰𝗵 𝗠𝗼𝗱𝘂𝗹𝗲 ━━╻
┃
┃• /nyaasi <i>[search query]</i>
┃• /sukebei <i>[search query]</i>
┃• /1337x <i>[search query]</i>
┃• /piratebay <i>[search query]</i>
┃• /tgx <i>[search query]</i>
┃• /yts <i>[search query]</i>
┃• /eztv <i>[search query]</i>
┃• /torlock <i>[search query]</i>
┃• /rarbg <i>[search query]</i>
┃• /ts <i>[search query]</i>
┃
┗━♦️ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 {UPDATES_CHANNEL}♦️━╹
'''
    STATUS_MSG_1 = '''
┏━━━━━━━━━━━━━━━━━━╻
┣🗄 𝐍𝐚𝐦𝐞: <a href='{mess_link}'>{file_name}</a>
┣📈 𝐒𝐭𝐚𝐭𝐮𝐬: <i>Downloading...📥</i>
┃<code>{progress}</code>
┣⚡️ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐞𝐝: <code>{prog_string}</code> <b>of</b> <code>{total_string}</code>
┣📡 𝐒𝐩𝐞𝐞𝐝: <code>{speed_string}</code>, ⏳️ 𝐄𝐓𝐀: <code>{eta_string}</code>'''
    STATUS_MSG_2 = "\n┣⏰️ 𝐄𝐥𝐚𝐩𝐬𝐞𝐝: <code>{etime}</code>"
    STATUS_MSG_3 = '''
┣<b>👤 𝐔𝐬𝐞𝐫:</b> {u_men} ( #ID{uid} )
┣<b>⚠️ 𝐖𝐚𝐫𝐧:</b> <code>/warn {uid}</code>'''
    STATUS_MSG_4 = "\n┣📊 𝐂𝐨𝐧𝐧𝐞𝐜𝐭𝐢𝐨𝐧𝐬: <code>{connections}</code>"
    STATUS_MSG_5 = "\n┣🍇 𝐒𝐞𝐞𝐝𝐞𝐫𝐬: <code>{num_seeders}</code> ┃🍒 𝐋𝐞𝐞𝐜𝐡𝐞𝐫𝐬: <code>{connections}</code>"
    STATUS_MSG_6 = '''
┣🚫 𝐓𝐨 𝐂𝐚𝐧𝐜𝐞𝐥: /cancel_{gid}
┗━━━━━━━━━━━━━━━━━━╹
'''
    TOP_STATUS_MSG = '''
❣ 𝘽𝙮 : {umen} (<code>{uid}</code>)
◆━━━━━━━◆ ❃ ◆━━━━━━━◆'''
    BOTTOM_STATUS_MSG = "◆━━━━━━━◆ ❃ ◆━━━━━━━◆"
    DEF_STATUS_MSG = '''
┏━━━━━━━━━━━━━━━━━━╻
┃
┃ ⚠️ <b>No Active, Queued or Paused 
┃ Torrents / Direct Links ⚠️</b>
┃
┗━━━━━━━━━━━━━━━━━━╹
'''
    WRONG_COMMAND = "<i> Hey {u_men}, \n\n ⚠️ Check and Send a Valid Download Source to Start Me Up !! ⚠️</i>"
    WRONG_DEF_COMMAND = "<b>⚠️ Opps ⚠️</b>\n\n <b><i>⊠ Reply with Direct/Torrent Link or File⁉️</i></b>"
    DOWNLOAD_ADDED_MSG = "┏━━━━━━━━━━━━━━━━╻\n┣👤 𝐔𝐬𝐞𝐫 : {u_men}({u_id}) \n┃\n┃ <code>⚡️ Your Request Has Been Added To The Status List ⚡️</code> \n┃\n┣ <b><u>Send</u> /{status_cmd} <u>To Check Your Progress</u></b>\n┃\n┗━♦️ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 {UPDATES_CHANNEL}♦️━╹"
    EXCEP_DEF_MSG = "<b> 🏖Maybe You Didn't Know I am Being Used !!</b> \n\n<b>🌐 API Error</b>: {cf_name}"
    WRONG_RENAME_MSG = "<b>⚠️ Oops ⚠️</b>\n\n⚡Provide Name with extension.\n\n➩<b>Example</b>: <code> /rename Sample.mkv</code>"
    TOP_LIST_FILES_MSG = '''┏ 🗃 𝙇𝙚𝙚𝙘𝙝 𝘾𝙤𝙢𝙥𝙡𝙚𝙩𝙚 !! 🗃
┃
┣ 👤 𝐔𝐬𝐞𝐫 : {u_men} ( #ID{user_id} )
┣ ⏰️ 𝐄𝐥𝐚𝐩𝐬𝐞𝐝 : {timeuti}
┃
'''
    BOTTOM_LIST_FILES_MSG = '''┃
┃ #Uploads
┃
┗━♦️ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 {UPDATES_CHANNEL}♦️'''
    SINGLE_LIST_FILES_MSG = "┣ ⇒ <a href='{private_link}'>{local_file_name}</a>\n"
    EXTRACT_MSG = "<b><i>🛠 Extracting : </i></b> <code>{no_of_con}</code> <b>File(s)</b>"
    START_UPLOAD_MSG = '''┏🗄 𝐍𝐚𝐦𝐞: <code>{filename}</code>
┃
┗📈 𝐒𝐭𝐚𝐭𝐮𝐬: <b><i>Uploading...📤</i></b>'''
    START_DOWM_MSG = '''┏⚡️ <i>Telegram Download Initiated</i> ⚡️
┃
┗📈 𝐒𝐭𝐚𝐭𝐮𝐬: <b><i>Downloading...📥</i></b>'''

    DOWN_COM_MSG = '''┏🗄 𝐍𝐚𝐦𝐞: `{filename}`
┃
┣📈 𝐒𝐭𝐚𝐭𝐮𝐬: <b><i>Downloaded 📥</i></b>
┣📦 𝐒𝐢𝐳𝐞: `{size}`
┃
┗ #Downloaded'''
    DOWN_RE_COM_MSG = '''┏🗄 𝐍𝐚𝐦𝐞: `{base_file_name}`
┃
┣📈 𝐒𝐭𝐚𝐭𝐮𝐬: <b><i>Downloaded 📥</i></b>
┣📦 𝐒𝐢𝐳𝐞: `{file_size}`
┣⏰️ 𝐓𝐢𝐦𝐞 𝐓𝐚𝐤𝐞𝐧: `{tt}`
┃
┗ #Downloaded'''
    TOP_PROG_MSG = '''◆━━━━━━◆ ❃ ◆━━━━━━◆

┏━━━━━━━━━━━━━━━━╻
┣🗄 𝐍𝐚𝐦𝐞: `{base_file_name}`'''
    PROG_MSG = '''┃
┃<code>[{0}{1}{2}] {3}%</code>
┃
'''
    DOWN_PROG_MSG = '''┣📦 𝐓𝐨𝐭𝐚𝐥 : `〚{t}〛`
┣⚡️ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐞𝐝  :`〚{d}〛`
┣📡 𝐒𝐩𝐞𝐞𝐝 : ` 〚{s}〛`
┣⏳️ 𝐄𝐓𝐀 : `〚{eta}〛`
┗━♦️ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 {UPDATES_CHANNEL}♦️━╹

◆━━━━━━◆ ❃ ◆━━━━━━◆'''

    CANCEL_PROG_BT = "⛔ 𝗖𝗔𝗡𝗖𝗘𝗟 ⛔"
