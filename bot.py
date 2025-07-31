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
from telethon import TelegramClient, events
from telethon.tl.functions.channels import GetParticipantRequest, GetFullChannelRequest
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator
import os
import asyncio

api_id = 12210813
api_hash = 'e42eeae11a2f96bcfc5ec3b46a30adad'
bot_token = "7756181021:AAH8mPBjMb0SRB9LUAdZDdJxt5ZZaY6Oa4k"

# Userbotun ID və ya username-i (məsələn, 123456789 və ya "myuserbot")
userbot_username = "PersionalMusic"  # istifadəçi adı varsa @siz yazmadan
# userbot_id = 123456789

ASSISTANT_ID = 5871660730  # Asistant userbotun ID-si
ASİSSTANT_TAG = "@PersionalMusic"  # Asisstantın ve ya userbotun Tağ adı


client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)




O_MSG = "⚠️ Bu əmri yalnız qruplarda istifadə edə bilər və ya asistanta daxil olaraq .music yazılmalıdır."

P_MSG = "👤 Asistant bu qrupda deyil. Zəhmət olmasa onu qrupa əlavə edin."


P_BAN = "🔇 Asistant bu qrupda səsizə alınıb. Zəhmət olmasa /unmute əmri ilə səsin açın.\n🆔 `5871660730`\n🌐 @sesizKOLGE"

buttons = [[Button.url("🎧 Asistant Hesabı »", f"https://t.me/{userbot_username}")]]

#button = [[Button.url("🎧 Asistant Hesabı »", f"https://t.me/{userbot_username}")]]                


@client.on(events.NewMessage(pattern='[.!/]music'))
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
        await client.send_message(userbot_username, f"[.!/]music {chat_id}")
        
    except Exception as e:
        await event.reply(f"⚠️ Xəta baş verdi: {e}")



@client.on(events.NewMessage(pattern='[./!]stopvc'))
async def stop_vc(event):
    if not (event.is_group or event.is_channel):
        await event.reply("❌ Bu əmr yalnız qruplarda istifadə oluna bilər.")
        return

    chat = await event.get_chat()

    try:
        participant = await bot(GetParticipantRequest(chat, ASSISTANT_ID))
        part = participant.participant

        # Admin olub-olmadığını yoxlayırıq
        if not isinstance(part, (ChannelParticipantAdmin, ChannelParticipantCreator)):
            await event.reply(f"⚠️ Asisstant bu qrupda səssizə alınıb və ya səsli söhbət üçün yetkisi yoxdur. Asisstanta ✓ Canlı (Görüntülü) yayını idarə yetkisi verin\n\nID: `{ASİSSTANT_ID}`\nTağ: {ASİSSTANT_TAG}")
            return

        # Səssiz edilibmi?
        if hasattr(part, "banned_rights") and part.banned_rights and part.banned_rights.send_messages:
            await event.reply(f"⚠️ Asisstant bu qrupda səssizə alındığı üçün səsli söhbəti idarə edə bilmir.\n\n ID:- `{ASİSSTANT_ID}`\nTağ:- {ASİSSTANT_TAG}")
            return

        # Səsli söhbət aktivdirmi?
        full_chat = await bot(GetFullChannelRequest(chat.id))
        if not full_chat.full_chat.call:
            await event.reply("🔇 Hal hazırda səsli söhbət aktiv deyil")
            return

    except Exception as e:
        await event.reply(f"❌ Asisstant bu qrupda deyil və ya Səsli söhbət idarə yetkisi yoxdur\n\n")
        return
        print("xəta {e}")

    with open("command.txt", "w") as f:
        f.write(f"stop|{event.chat_id}")
    msg = await event.reply("✅ Səsli söhbət sonlandırılır.....")
    await asyncio.sleep(3)
    await msg.edit("✅ Səsli söhbət uğurla sonlandırıldı.")
    await asyncio.sleep(3)
    await msg.delete()




  
client.run_until_disconnected()  
