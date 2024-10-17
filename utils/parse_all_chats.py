import logging
from pyrogram import Client
from pyrogram.enums import ChatType

logger = logging.getLogger(__name__)

async def parse_all_chats(client: Client):
    session_name = client.name
    all_chats = []
    try:
        async for dialog in client.get_dialogs():
            chat = dialog.chat
            if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL]:
                if chat.username:
                    chat_link = f"https://t.me/{chat.username}"
                elif getattr(chat, 'invite_link', None):
                    chat_link = chat.invite_link
                else:
                    continue

                all_chats.append(chat_link)

        with open(f'{session_name}_chats.py', 'w', encoding='utf-8') as f:
            f.write("CHANNELS_TO_JOIN = [\n")
            for chat in all_chats:
                f.write(f"    \"{chat}\",\n")
            f.write("]\n\n")
            f.write("def get_channels():\n")
            f.write("    return CHANNELS_TO_JOIN\n")

        logger.info(f"{session_name} | Successfully saved all available groups, channels, and chats to the fil <green>{session_name}_chats.py<green>")
    except Exception as e:
        logger.error(f"{session_name} | Error while parsing chats: {str(e)}")