class TXStyle:
    TOGGLEDOC_MSG = '''╭ <b>Usᴇʀ :</b> {u_men}
│ <b>Iᴅ :</b> #ID{u_id}
│
╰ <b>Tᴏɢɢʟᴇ : 📂 Dᴏᴄᴜᴍᴇɴᴛ 📂</b>'''
    TOGGLEVID_MSG = '''╭ <b>Usᴇʀ :</b> {u_men}
│ <b>Iᴅ :</b> #ID{u_id}
│
╰ <b>Tᴏɢɢʟᴇ : 🎞 Vɪᴅᴇᴏ 🎞</b>'''
    THUMB_REPLY = "Pʀᴏᴄᴇssɪɴɢ ..."
    SAVE_THUMB_MSG = '''╭ <b>⚡Cᴜsᴛᴏᴍ Tʜᴜᴍʙɴᴀɪʟ Sᴀᴠᴇᴅ ⚡</b>
│
╰ <b>🔭 Nᴏᴡ Tʀʏ Uᴘʟᴏᴀᴅɪɴɢ Sᴏᴍᴇᴛʜɪɴɢ . . .</b>.'''
    SAVE_THUMB_FAIL_MSG = "<b><i>⛔Sorry⛔</i></b>\n\n<b>❌ Reply with Image to Save Your Custom Thumbnail.❌</b>"
    CLEAR_THUMB_SUCC_MSG = "<b><i>✅Success✅</i></b>\n\n <b>🖼Custom Thumbnail Cleared Successfully As Per Your Request.</b>"
    CLEAR_THUMB_FAIL_MSG = "<b><i>⛔Sorry⛔</i></b>\n\n <b>❌Nothing to Clear For You❌</b>"
    PREFIX_MSG = "⚡️<i><b>Custom Prefix Set Successfully</b></i> ⚡️ \n\n👤 <b>User :</b> {u_men}\n🆔 <b>User ID :</b> <code>{uid}</code>\n🗃 <b>Prefix :</b> <code>{t}</code>"
    CAPTION_MSG = "⚡️<i><b>Custom Caption Set Successfully</b></i> ⚡️ \n\n👤 <b>User :</b> {u_men}\n🆔 <b>User ID :</b> <code>{uid}</code>\n🗃 <b>Caption :</b>\n<code>{t}</code>"
    IMDB_MSG = "⚡️<i><b>Custom Template Set Successfully</b></i> ⚡️ \n\n👤 <b>User :</b> {u_men}\n🆔 <b>User ID :</b> <code>{uid}</code>\n🗃 <b>IMDB Template :</b> \n<code>{t}</code>"
    THEME_MSG = "⚡️ <i><b>Available Custom Themes</b></i> ⚡️\n\n👤 <b>User :</b> {u_men}\n🆔 <b>User ID :</b> <code>{uid}</code>\n\n🗄 <b>Choose Available Theme from Below:</b>"
    STATS_MSG_1 = '╭──── 📊 𝗕𝗼𝘁 𝗦𝘁𝗮𝘁𝘀 📊 ─────╮\n│\n'
    STATS_MSG_2 = '├ 📝 <b>Commit Date:</b> {lc}\n│\n'
    STATS_MSG_3 = '''├ 🤖 <b>Bot Uptime:</b> {currentTime}
├ 📶 <b>OS Uptime:</b> {osUptime}
│
├ 🚦<b>ᴄᴘᴜ:</b>
│  ┗ <code>{cpu_prog} {cpuUsage}%</code>
│
├ 🧬 <b>ʀᴀᴍ:</b>
│  ┗ <code>{mem_prog} {mem_p}%</code>
├  • <i><b>Total:</b> {mem_t}</i> │ • <i><b>Used:</b> {mem_u}</i>
│                • <i><b>Free:</b> {mem_a}</i>
│
├ 🗃 <b>ᴅɪsᴋ:</b>
│  ┗ <code>{disk_prog} {disk}%</code>
├  • <i><b>Total:</b> {total}</i> │ • <i><b>Used:</b> {used}</i>
│                • <i><b>Free:</b> {free}</i>
│
├ 🔁 <b>sᴡᴀᴘ:</b>
│  ┗ <code>{swap_prog} {swap_p}%</code>
├  • <i><b>Total:</b> {swap_t}</i> │ • <i><b>Used:</b> {swap_u}</i>
│                • <i><b>Free:</b> {swap_f}</i>
│
├ 🗄 <b>ᴄᴏʀᴇs:</b>
│  ┗ <code>{core_prog} {core_per}%</code>
├ 📄 <i><b>Physical Cores:</b> {p_core}</i> │ 📑 <i><b>Total Cores:</b> {t_core}</i>
│
├ 📤 <b>Total Upload Data :</b> {sent}
╰ 📥 <b>Total Download Data :</b> {recv}'''
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
    STATUS_MSG_1 = '''╭🗄 Nᴀᴍᴇ: <a href='{mess_link}'>{file_name}</a>
├📈 Sᴛᴀᴛᴜs: <i>Downloading...📥</i>
│<code>{progress}</code>
├⚡️ Dᴏᴡɴʟᴏᴀᴅᴇᴅ: <code>{prog_string}</code> <b>of</b> <code>{total_string}</code>
├📡 Sᴘᴇᴇᴅ: <code>{speed_string}</code>, ⏳️ ᴇᴛᴀ: <code>{eta_string}</code>'''
    STATUS_MSG_2 = "\n├⏰️ Eʟᴀᴘsᴇᴅ: <code>{etime}</code>"
    STATUS_MSG_3 = '''
├👤 Usᴇʀ: {u_men} ( #ID{uid} )'''
    STATUS_MSG_4 = "\n├📊 Cᴏɴɴᴇᴄᴛɪᴏɴs: <code>{connections}</code>"
    STATUS_MSG_5 = "\n├🍇 Sᴇᴇᴅᴇʀs: <code>{num_seeders}</code> ┃🍒 Lᴇᴇᴄʜᴇʀs: <code>{connections}</code>"
    STATUS_MSG_6 = '''
╰🚫 Tᴏ Sᴛᴏᴘ: /cancel_{gid}
'''
    TOP_STATUS_MSG = '''
❣ 𝘽𝙮 : {umen} (<code>{uid}</code>)
━━━━━━━✦✗✦━━━━━━━━
'''
    BOTTOM_STATUS_MSG = "━━━━━━━✦✗✦━━━━━━━━"
    DEF_STATUS_MSG = '''
 ⚠️ <b>No Active, Queued or Paused 
 Torrents / Direct Links ⚠️</b>

'''
    WRONG_COMMAND = "<i> Hey {u_men}, \n\n ⚠️ Check and Send a Valid Download Source to Start Me Up !! ⚠️</i>"
    WRONG_DEF_COMMAND = " <b><i>⊠ Reply with Direct/Torrent Link or File⁉️</i></b>"
    DOWNLOAD_ADDED_MSG = "╭👤 Usᴇʀ : {u_men}({u_id}) \n│\n│ <code>⚡️ Your Request Has Been Added To The Status List ⚡️</code> \n│\n╰ <b>Sᴇɴᴅ /{status_cmd} Tᴏ Cʜᴇᴄᴋ Yᴏᴜʀ Pʀᴏɢʀᴇss</b>"
    EXCEP_DEF_MSG = "<b> 🏖Maybe You Didn't Know I am Being Used !!</b> \n\n<b>🌐 API Error</b>: {cf_name}"
    WRONG_RENAME_MSG = "⚡Provide Name with extension.\n\n➩<b>Example</b>: <code> /rename Sample.mkv</code>"
    TOP_LIST_FILES_MSG = '''╭ ᒪᗴᗴᑕᕼ ᑕOᗰᑭᒪᗴTᗴ !!
│
├ 👤 Usᴇʀ : {u_men} ( #ID{user_id} )
├ ⏰️ Eʟᴀᴘsᴇᴅ : {timeuti}
│
'''
    BOTTOM_LIST_FILES_MSG = '''│
╰ #Uploaded'''
    SINGLE_LIST_FILES_MSG = "├ ▷ <a href='{private_link}'>{local_file_name}</a>\n"
    EXTRACT_MSG = "🛠 <i>Exᴛʀᴀᴄᴛɪɴɢ : <code>{no_of_con}</code> Fɪʟᴇ(s)</i>"
    START_UPLOAD_MSG = '''╭🗄 Nᴀᴍᴇ: <code>{filename}</code>
│
╰📈 Sᴛᴀᴛᴜs: <b><i>Uploading...📤</i></b>'''
    START_DOWM_MSG = '''╭⚡️ <i>Telegram Download Initiated</i> ⚡️
│
╰📈 Sᴛᴀᴛᴜs: <b><i>Downloading...📥</i></b>'''

    DOWN_COM_MSG = '''╭🗄 Nᴀᴍᴇ: `{filename}`
│
├📈 Sᴛᴀᴛᴜs: <b><i>Downloaded 📥</i></b>
├📦 Sɪᴢᴇ: `{size}`
│
╰ #Downloaded'''
    DOWN_RE_COM_MSG = '''╭🗄 Nᴀᴍᴇ: `{base_file_name}`
│
├📈 Sᴛᴀᴛᴜs: <b><i>Downloaded 📥</i></b>
├📦 Sɪᴢᴇ: `{file_size}`
├⏰️ Tɪᴍᴇ Tᴀᴋᴇɴ: `{tt}`
│
╰ #Downloaded'''
    TOP_PROG_MSG = '''╭🗄 Nᴀᴍᴇ : `{base_file_name}`'''
    PROG_MSG = '''│
│<code>[{0}{1}{2}] {3}%</code>
│
'''
    DOWN_PROG_MSG = '''├📦 Tᴏᴛᴀʟ : `〚{t}〛`
├⚡️ Dᴏᴡɴʟᴏᴀᴅᴇᴅ  :`〚{d}〛`
├📡 Sᴘᴇᴇᴅ : ` 〚{s}〛`
╰⏳️ ᴇᴛᴀ : `〚{eta}〛`'''

    CANCEL_PROG_BT = "⛔ Cᴀɴᴄᴇʟ ⛔"
