import asyncio
from datetime import datetime, timedelta

from tobrot import FSUB_CHANNEL, LOGGER
from pyrogram import enums, Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message


async def get_invite_link(client, chat_id):
    try:
        invite_link = await client.create_chat_invite_link(chat_id=chat_id, name="Updates Invite Link", member_limit=1, expire_date=datetime.now() + timedelta(days=1))
        return invite_link
    except FloodWait as e:
        LOGGER.info(f"FloodWait : Sleeping {e.value}s")
        await asyncio.sleep(e.value)
        return await get_invite_link(client, chat_id)

async def handle_force_sub(client: Client, cmd: Message):
    if FSUB_CHANNEL and FSUB_CHANNEL.startswith("-100"):
        channel_chat_id = int(FSUB_CHANNEL)
    elif FSUB_CHANNEL and (not FSUB_CHANNEL.startswith("-100")):
        channel_chat_id = FSUB_CHANNEL
    else:
        return 200
    try:
        user = await client.get_chat_member(chat_id=channel_chat_id, user_id=cmd.from_user.id)
        if user.status in (enums.ChatMemberStatus.BANNED, enums.ChatMemberStatus.RESTRICTED):
            await client.reply_text(text="<b>Sorry, You are Banned to Use me.</b>", parse_mode=enums.ParseMode.HTML)
            return 400
        elif user.status == enums.ChatMemberStatus.LEFT:
            raise UserNotParticipant
    except UserNotParticipant:
        try:
            invite_link = await get_invite_link(client, chat_id=channel_chat_id)
        except Exception as err:
            LOGGER.info(f"Unable to Generate Invite Link of {FSUB_CHANNEL}\n\nError: {err}")
            return 200
        await cmd.reply_text(
            text=f'''<i>Dear {cmd.from_user.mention},</i>

⚠️ <b>You haven't Joined our Channel yet.</b> ⚠️

<i>Join the Channel to Start Using the Bot Without Restrictions.</i>''',
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True,
            quote=True,
            reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("⚡️ Join Channel ⚡️", url=str(invite_link.invite_link))]
                ]
            )
        )
        return 400
    except Exception as err:
        LOGGER.info(f"Force Subscribe Error: {err}")
        return 200
    return 200
