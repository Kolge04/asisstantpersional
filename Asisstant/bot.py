# bot.py
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.messages import GetFullChatRequest, GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, PeerUser, PeerChat, PeerChannel, ChannelParticipantsSearch
import asyncio
from telethon.tl.custom import Button  # Əlavə et

from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantBanned, ChatBannedRights
from telethon.tl.functions.channels import GetParticipantRequest


api_id = 12210813
api_hash = 'e42eeae11a2f96bcfc5ec3b46a30adad'
bot_token = "7756181021:AAH8mPBjMb0SRB9LUAdZDdJxt5ZZaY6Oa4k"

# Userbotun ID və ya username-i (məsələn, 123456789 və ya "myuserbot")
userbot_username = "PersionalMusic"  # istifadəçi adı varsa @siz yazmadan
# userbot_id = 123456789

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)




O_MSG = "⚠️ Bu əmri yalnız qruplarda istifadə edə bilər və ya asistanta daxil olaraq .music yazılmalıdır."

P_MSG = "👤 Asistant bu qrupda deyil. Zəhmət olmasa onu qrupa əlavə edin."


P_BAN = "🔇 Asistant bu qrupda səsizə alınıb. Zəhmət olmasa /unmute əmri ilə səsin açın.\n🆔 `5871660730`\n🌐 @sesizKOLGE"

buttons = [[Button.url("🎧 Asistant Hesabı »", f"https://t.me/{userbot_username}")]]

#button = [[Button.url("🎧 Asistant Hesabı »", f"https://t.me/{userbot_username}")]]                


@client.on(events.NewMessage(pattern='[.!/]as'))
async def bot_as_command(event):
    if event.is_private:
        await event.reply(O_MSG, buttons=buttons)
        return

    try:
        chat = await event.get_chat()
        chat_id = event.chat_id

        try:
            participant = await client(GetParticipantRequest(chat_id, userbot_username))
            part = participant.participant

            # BAN olub olmadığını yoxla
            if hasattr(part, 'banned_rights') and part.banned_rights:
                await event.reply(P_BAN, buttons=buttons)
                return

            # SƏSİZƏ alınıbsa
            if hasattr(part, 'restrictions') and part.restrictions:
                await event.reply(P_BAN, buttons=buttons)
                return

        except UserNotParticipantError:
            await event.reply(P_MSG, buttons=buttons)
            return

        # Əgər hər şey qaydasındadırsa, userbota mesaj göndər
        await client.send_message(userbot_username, f"[.!/]as {chat_id}")
        
    except Exception as e:
        await event.reply(f"⚠️ Xəta baş verdi: {e}")
  
client.run_until_disconnected()  
