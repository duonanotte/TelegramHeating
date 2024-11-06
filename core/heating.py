import os
import asyncio
import random
import json
import aiohttp
import emoji
import re

from datetime import datetime, timedelta
from pyrogram import Client
from pyrogram.types import ChatPreview, ChatReactions, Chat
from pyrogram.errors import Unauthorized, UserDeactivated, AuthKeyUnregistered, BadRequest
from pyrogram.errors import UsernameInvalid, UsernameNotOccupied, PeerIdInvalid, UserNotParticipant, InviteHashExpired, InviteHashInvalid, FloodWait, ChannelPrivate
from pyrogram.raw.functions.account import UpdateProfile, UpdateNotifySettings, UpdateStatus
from pyrogram.raw.functions.messages import GetAvailableReactions, SendReaction
from pyrogram.enums import ChatType
from pyrogram.raw.types import InputNotifyPeer, InputPeerNotifySettings
from pyrogram.raw.types import InputPeerUser, InputPeerChannel, ChatReactionsAll, ChatReactionsSome, ChatReactionsNone
from utils import logger
from utils.channels import get_channels
from utils.bio import BioGenerator
from utils.parse_all_chats import parse_all_chats
from config.config import settings
from exceptions import InvalidSession

import logging
logging.getLogger("pyrogram").setLevel(logging.ERROR)

def proxy_dict_to_url(proxy_dict):
    if not proxy_dict:
        return None
    scheme = proxy_dict.get('scheme', 'http')
    hostname = proxy_dict.get('hostname')
    port = proxy_dict.get('port')
    username = proxy_dict.get('username')
    password = proxy_dict.get('password')

    if not hostname or not port:
        return None

    auth = f"{username}:{password}@" if username and password else ""
    return f"{scheme}://{auth}{hostname}:{port}"

class UserBehaviorSimulator:
    @staticmethod
    async def simulate_typing(client, chat):
        if chat.type in [ChatType.PRIVATE, ChatType.GROUP, ChatType.SUPERGROUP]:
            typing_duration = random.uniform(5, 30)
            logger.info(f"{client.name} | <light-yellow>Simulated typing in {chat.title} for {typing_duration:.0f} seconds</light-yellow>")
            await client.send_chat_action(chat.id, "typing")
            await asyncio.sleep(typing_duration)

    @staticmethod
    async def simulate_reading(client, message_count):
        reading_time = random.uniform(3, 10) * message_count
        logger.info(f"{client.name} | <light-yellow>Simulated reading {message_count} messages for {reading_time:.0f} seconds</light-yellow>")
        await asyncio.sleep(reading_time)

    @staticmethod
    async def simulate_online_status(client):
        online_duration = random.uniform(60, 300)
        logger.info(f"{client.name} | <light-yellow>Simulated online status for {online_duration:.0f} seconds</light-yellow>")
        await client.invoke(UpdateStatus(offline=False))
        await asyncio.sleep(online_duration)
        await client.invoke(UpdateStatus(offline=True))

    @staticmethod
    async def simulate_pause_between_actions(client):
        pause_duration = random.uniform(10, 30)
        logger.info(f"{client.name} | <light-yellow>Pausing between actions for {pause_duration:.0f} seconds</light-yellow>")
        await asyncio.sleep(pause_duration)


class ChannelInteractions:
    @staticmethod
    async def react_to_message(client, chat):
        try:
            chat_full = await client.get_chat(chat.id)
            available_reactions = chat_full.available_reactions

            emoji_reactions = []
            if isinstance(available_reactions, ChatReactions):
                emoji_reactions = [reaction.emoji for reaction in available_reactions.reactions]
            elif isinstance(available_reactions, dict) and 'reactions' in available_reactions:
                emoji_reactions = [reaction['emoji'] for reaction in available_reactions['reactions']
                                   if isinstance(reaction, dict) and 'emoji' in reaction]

            if not emoji_reactions:
                logger.info(f"{client.name} | No available reactions in <cyan>{chat.title}</cyan>. Skipping reaction.")
                return

            reaction = random.choice(emoji_reactions[:5])

            messages = []
            async for message in client.get_chat_history(chat.id, limit=10):
                messages.append(message)

            if messages:
                message = random.choice(messages)
                reaction_unicode = emoji.emojize(reaction, language='alias')

                max_attempts = 3
                for attempt in range(max_attempts):
                    try:
                        await asyncio.sleep(random.uniform(2, 5))

                        await client.send_reaction(
                            chat_id=chat.id,
                            message_id=message.id,
                            emoji=reaction_unicode
                        )
                        logger.info(f"{client.name} | <light-yellow>Reacted with {reaction} to a message in</light-yellow> <cyan>{chat.title}</cyan>")
                        break
                    except FloodWait as e:
                        logger.warning(f"{client.name} | FloodWait: sleeping for {e.x} seconds")
                        await asyncio.sleep(e.x + random.randint(600, 1900))
                    except BadRequest as e:
                        logger.error(f"{client.name} | BadRequest when reacting to message in {chat.title}: {str(e)}")
                        if "REACTIONS_TOO_MANY" in str(e):
                            logger.info(f"{client.name} | Waiting before next attempt...")
                            await asyncio.sleep(random.uniform(60, 120))
                        else:
                            break
                    except Exception as e:
                        logger.error(f"{client.name} | Unexpected error reacting to message in {chat.title}: {str(e)}")
                        break
                else:
                    logger.warning(f"{client.name} | Failed to react after {max_attempts} attempts in {chat.title}")

        except Exception as e:
            logger.error(f"{client.name} | Error reacting to message in {chat.title}: {str(e)}")

    async def scroll_feed(self, client, chat):
        scroll_time = random.uniform(10, 60)
        logger.info(f"{client.name} | <light-yellow>Scrolling feed in {chat.title} for {scroll_time:.0f} seconds</light-yellow>")
        await asyncio.sleep(scroll_time)

    async def view_media(self, client, chat):
        view_time = random.uniform(5, 20)
        logger.info(f"{client.name} | <light-yellow>Viewing media in {chat.title} for {view_time:.0f} seconds</light-yellow>")
        await asyncio.sleep(view_time)


class TelegramJoiner:
    def __init__(self, tg_client: Client, proxy: str):
        self.tg_client = tg_client
        self.session_name = tg_client.name
        self.proxy = self.parse_proxy(proxy) if proxy else None
        self.user_behavior = UserBehaviorSimulator()
        self.channel_interactions = ChannelInteractions()
        self.channels_to_join = get_channels()
        self.joined_channels = set()
        self.avatar_set = False
        self.bio_set = False
        self.avatar_time = None
        self.bio_time = None
        self.bio_generator = BioGenerator()

    def parse_proxy(self, proxy_str: str) -> dict:
        parts = proxy_str.split('@')
        auth, address = parts[0], parts[1]
        protocol, credentials = auth.split('://')
        username, password = credentials.rsplit(':', 1)
        host, port = address.split(':')
        return {
            "scheme": protocol,
            "hostname": host,
            "port": int(port),
            "username": username,
            "password": password
        }

    async def start(self):
        if self.proxy:
            self.tg_client.proxy = self.proxy
        try:
            await self.tg_client.start()
        except Exception as e:
            logger.error(f"{self.session_name} | Failed to start session: {str(e)}")
            return False
        return True

    async def stop(self):
        await self.tg_client.stop()
        logger.info(f"{self.session_name} | Stopped session")

    async def check_tg_proxy(self):
        try:
            me = await self.tg_client.get_me()
            async with aiohttp.ClientSession() as session:
                async with session.get('https://ipinfo.io/json', proxy=f"{self.proxy['scheme']}://{self.proxy['hostname']}:{self.proxy['port']}", proxy_auth=aiohttp.BasicAuth(self.proxy['username'], self.proxy['password'])) as response:
                    if response.status != 200:
                        raise Exception(f"HTTP status: {response.status}")
                    data = await response.json()

            ip = data.get('ip')
            city = data.get('city')
            country = data.get('country')

            logger.info(
                f"{self.session_name} | "
                f"User ID: <cyan>{me.id}</cyan> | Country: <cyan>{country}</cyan> | "
                f"City: <light-yellow>{city}</light-yellow> | "
                f"Proxy IP: <light-white>{ip}</light-white>"
            )
            return True
        except Exception as error:
            logger.error(f"{self.session_name} | Telegram proxy check failed. Error: {error}")
            return False

    async def join_and_mute_channel(self, link):
        try:
            chat = await self.get_chat_safely(link)
            if not chat:
                logger.error(f"{self.session_name} | Invalid or non-existent channel: {link}")
                return

            try:
                await self.tg_client.get_chat_member(chat.id, "me")
                logger.info(f"{self.session_name} | Already a member of <cyan>{chat.title}</cyan>")
                return
            except UserNotParticipant:
                await asyncio.sleep(random.uniform(10, 20))

                if isinstance(chat, ChatPreview):
                    await self.tg_client.join_chat(link)
                else:
                    await self.tg_client.join_chat(chat.id)

                logger.info(f"{self.session_name} | Joined channel <cyan>{chat.title}</cyan>")

                await asyncio.sleep(random.uniform(25, 95))

                await self.tg_client.invoke(UpdateNotifySettings(
                    peer=InputNotifyPeer(peer=await self.tg_client.resolve_peer(chat.id)),
                    settings=InputPeerNotifySettings(mute_until=2147483647)
                ))
                logger.info(f"{self.session_name} | Muted notifications for <cyan>{chat.title}</cyan>")

                self.joined_channels.add(link)

        except FloodWait as e:
            logger.warning(f"{self.session_name} | FloodWait: sleeping for {e.x} seconds")
            await asyncio.sleep(e.x + random.randint(600, 1900))
        except Exception as e:
            logger.error(f"{self.session_name} | Error joining channel {link}: {str(e)}")

    async def set_avatar(self):
        if self.avatar_set:
            return

        img_dir = "img"
        avatar_files = [f for f in os.listdir(img_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]

        if not avatar_files:
            logger.warning(f"{self.session_name} | No avatar images found in the img directory")
            return

        avatar_path = os.path.join(img_dir, random.choice(avatar_files))

        try:
            await self.tg_client.set_profile_photo(photo=avatar_path)
            logger.info(f"{self.session_name} | <green>Set new profile picture</green>")
            self.avatar_set = True
            await asyncio.sleep(15)

            os.remove(avatar_path)
            logger.info(f"{self.session_name} | Removed used avatar image: {avatar_path}")
        except Exception as e:
            logger.error(f"{self.session_name} | Error setting avatar: {str(e)}")

    def generate_bio(self):
        return self.bio_generator.generate_bio()

    async def set_bio(self):
        if self.bio_set:
            return

        bio = self.generate_bio()

        try:
            await self.tg_client.update_profile(bio=bio)
            logger.info(f"{self.session_name} | <green>Set new bio successfully:</green> {bio}")
            self.bio_set = True
            self.bio_time = datetime.now()
        except Exception as e:
            logger.error(f"{self.session_name} | Error setting bio: {str(e)}")

    async def check_avatar_and_bio(self):
        me = await self.tg_client.get_me()
        if me.photo:
            self.avatar_set = True
            logger.info(f"{self.session_name} | Avatar is <yellow>already set</yellow> in your profile!")

        full_me = await self.tg_client.get_chat(me.id)
        if full_me.bio:
            self.bio_set = True
            logger.info(f"{self.session_name} | Bio is <yellow>already set</yellow> in your profile!")

    async def get_chat_safely(self, chat_id):
        try:
            if chat_id.startswith('https://t.me/'):
                chat_id = chat_id.split('/')[-1]
            elif chat_id.startswith('@'):
                chat_id = chat_id[1:]

            chat = await self.tg_client.get_chat(chat_id)
            return chat
        except (UsernameInvalid, UsernameNotOccupied, PeerIdInvalid) as e:
            logger.error(f"{self.session_name} | Failed to get chat info for {chat_id}: {str(e)}")
            async for dialog in self.tg_client.get_dialogs():
                if dialog.chat.username == chat_id or str(dialog.chat.id) == chat_id:
                    return dialog.chat
            return None
        except ValueError as e:
            logger.error(f"{self.session_name} | ValueError for chat {chat_id}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"{self.session_name} | Unexpected error getting chat {chat_id}: {str(e)}")
            return None

    async def perform_random_actions(self, chat_id):
        try:
            chat = await self.get_chat_safely(chat_id)
            if not chat:
                logger.warning(f"{self.session_name} | Skipping random actions for invalid chat: {chat_id}")
                return

            actions = [
                (self.user_behavior.simulate_typing, (self.tg_client, chat)),
                (self.user_behavior.simulate_reading, (self.tg_client, random.randint(5, 20),)),
                (self.user_behavior.simulate_online_status, (self.tg_client,)),
                (ChannelInteractions.react_to_message, (self.tg_client, chat)),
                (self.channel_interactions.scroll_feed, (self.tg_client, chat)),
                (self.channel_interactions.view_media, (self.tg_client, chat)),
            ]

            num_actions = random.randint(1, len(actions))
            selected_actions = random.sample(actions, num_actions)
            performed_actions = 0

            for action, args in selected_actions:
                if random.random() < 0.7:
                    try:
                        await action(*args)
                    except FloodWait as e:
                        logger.warning(f"{self.session_name} | FloodWait: sleeping for {e.value} seconds")
                        await asyncio.sleep(e.value + random.randint(600, 1900))
                    except Exception as e:
                        logger.error(f"{self.session_name} | Error during {action.__name__}: {str(e)}")
                    await asyncio.sleep(random.uniform(5, 15))

            if random.random() < 0.1:
                logger.info(f"{self.session_name} | <light-yellow>Simulating forgetting to go offline</light-yellow>")
            else:
                logger.info(f"{self.session_name} | <light-yellow>Setting status to offline</light-yellow>")
                await self.tg_client.invoke(UpdateStatus(offline=True))

        except Exception as e:
            logger.error(f"{self.session_name} | Unexpected error performing random actions: {str(e)}")
            logger.error(f"Traceback: ", exc_info=True)

    async def add_emoji_if_missing(self):
        if not settings.SET_EMOJI or not settings.EMOJI_TO_SET:
            return

        emoji_to_add = settings.EMOJI_TO_SET

        try:
            me = await self.tg_client.get_me()
            first_name = me.first_name or ""
            last_name = me.last_name or ""

            if emoji_to_add not in first_name and emoji_to_add not in last_name:
                new_last_name = last_name + emoji_to_add if last_name else emoji_to_add

                try:
                    await self.tg_client.update_profile(last_name=new_last_name)
                    logger.info(f"{self.session_name} | Added emoji {emoji_to_add} to last name: {new_last_name}")
                except FloodWait as e:
                    logger.warning(
                        f"{self.session_name} | FloodWait error when updating profile. Sleeping for {e.value} seconds.")
                    await asyncio.sleep(e.value)
                except Exception as e:
                    logger.error(f"{self.session_name} | Error updating profile: {e}")
            else:
                logger.info(f"{self.session_name} | Emoji {emoji_to_add} already present in name or last name")

        except Exception as e:
            logger.error(f"{self.session_name} | Error checking/updating profile: {e}")

    async def delete_all_emoji(self):
        try:
            me = await self.tg_client.get_me()
            first_name = me.first_name or ""
            last_name = me.last_name or ""

            emoji_pattern = re.compile("["
                                       u"\U0001F600-\U0001F64F"
                                       u"\U0001F300-\U0001F5FF"
                                       u"\U0001F680-\U0001F6FF"
                                       u"\U0001F1E0-\U0001F1FF"
                                       u"\U00002702-\U000027B0"
                                       u"\U000024C2-\U0001F251"
                                       "]+", flags=re.UNICODE)

            clean_first_name = emoji_pattern.sub(r'', first_name).strip()
            clean_last_name = emoji_pattern.sub(r'', last_name).strip()

            if clean_first_name != first_name or clean_last_name != last_name:
                try:
                    await self.tg_client.update_profile(
                        first_name=clean_first_name if clean_first_name else "User",
                        last_name=clean_last_name
                    )
                    logger.info(
                        f"{self.session_name} | Successfully removed emoji from profile | "
                        f"New name: <ly>{clean_first_name} {clean_last_name}</ly>"
                    )
                except FloodWait as e:
                    logger.warning(
                        f"{self.session_name} | FloodWait on profile update. "
                        f"Sleep {e.value} seconds"
                    )
                    await asyncio.sleep(e.value)
            else:
                logger.info(f"{self.session_name} | No emoji found in profile")

        except Exception as e:
            logger.error(f"{self.session_name} | Error when deleting an emoji: {e}")
            logger.error(f"Traceback: ", exc_info=True)

    async def run(self):
        if settings.USE_RANDOM_DELAY_IN_RUN:
            random_delay = random.randint(settings.RANDOM_DELAY_IN_RUN[0], settings.RANDOM_DELAY_IN_RUN[1])
            logger.info(
                f"{self.session_name} | The bot will start the heating process in <y>{random_delay}s</y>")
            await asyncio.sleep(random_delay)

        while True:
            try:
                if not await self.start():
                    raise Exception("Failed to start session")

                if settings.USE_PROXY and not await self.check_tg_proxy():
                    raise Exception("Proxy check failed")
                break

            except Exception as e:
                retry_delay = random.randint(60 * 60, 180 * 60)
                retry_time = timedelta(seconds=retry_delay)
                logger.error(f"{self.session_name} | {str(e)}. Retrying in <light-red>{retry_time}</light-red>")
                await asyncio.sleep(retry_delay)

        if settings.DELETE_ALL_EMOJI:
            await self.delete_all_emoji()
            logger.info(f"{self.session_name} | Shutdown after deleting an emoji")
            await self.stop()
            return

        start_time = datetime.now()

        me = await self.tg_client.get_me()
        full_name = f"{me.first_name} {me.last_name}" if me.last_name else me.first_name
        logger.info(f"{self.session_name} | User: {full_name} | Open telegram successfully!")

        if settings.PARSE_ALL_CHATS and self.session_name == settings.PARSE_ALL_CHATS_SESSION:
            logger.info(f"{self.session_name} | Starting to parse all chats...")
            await parse_all_chats(self.tg_client)
            logger.info(f"{self.session_name} | Finished parsing all chats.")
            await self.stop()
            return

        if settings.SET_AVATAR:
            if not self.avatar_set:
                try:
                    random_hours = random.uniform(settings.AVATAR_DELAY_RANGE[0], settings.AVATAR_DELAY_RANGE[1])
                    avatar_delay = timedelta(hours=random_hours)

                    self.avatar_time = start_time + avatar_delay

                    formatted_time = self.avatar_time.strftime('%d.%m.%Y at %H:%M')
                    logger.info(
                        f"{self.session_name} | Avatar will be set on <ly>{formatted_time}</ly>")
                except Exception as e:
                    logger.error(f"{self.session_name} | Error in avatar time calculation and logging: {str(e)}")
                    logger.error(f"Traceback: ", exc_info=True)
            else:
                logger.info(f"{self.session_name} | Avatar is already set")

        if settings.SET_BIO:
            if not self.bio_set:
                try:
                    bio_delay = timedelta(
                        hours=random.uniform(settings.BIO_DELAY_RANGE[0], settings.BIO_DELAY_RANGE[1]))
                    self.bio_time = start_time + bio_delay
                    formatted_bio_time = self.bio_time.strftime('%d.%m.%Y at %H:%M')
                    logger.info(f"{self.session_name} | Bio will be set on <ly>{formatted_bio_time}</ly>")
                except Exception as e:
                    logger.error(f"{self.session_name} | Error in bio time calculation: {str(e)}")
                    logger.error(f"Traceback: ", exc_info=True)
            else:
                logger.info(f"{self.session_name} | Bio is already set")

        if settings.SET_EMOJI:
            await self.add_emoji_if_missing()

        while self.channels_to_join:
            if settings.SET_AVATAR and self.avatar_time and datetime.now() >= self.avatar_time and not self.avatar_set:
                await self.set_avatar()

            if settings.SET_BIO and self.bio_time and datetime.now() >= self.bio_time and not self.bio_set:
                await self.set_bio()

            num_channels = min(random.randint(1, 3), len(self.channels_to_join))
            channels_to_join_now = random.sample(self.channels_to_join, num_channels)

            for channel in channels_to_join_now:
                await self.join_and_mute_channel(channel)
                await self.perform_random_actions(channel)

                tasks_delay = random.uniform(30, 160)
                logger.info(
                    f"{self.session_name} | Delay between surfing <yellow>{tasks_delay:.0f} seconds</yellow> ...")
                await asyncio.sleep(tasks_delay)

            if self.joined_channels:
                random_channel = random.choice(list(self.joined_channels))
                await self.perform_random_actions(random_channel)

            sleep_duration = random.uniform(12 * 3600, 30 * 3600)
            hours = int(sleep_duration // 3600)
            minutes = (int(sleep_duration % 3600)) // 60
            logger.info(
                f"{self.session_name} | Sleeping before next heating <yellow>{hours} hours</yellow> and <yellow>{minutes} minutes</yellow>.")
            await asyncio.sleep(sleep_duration)

        logger.info(f"{self.session_name} | Finished joining all channels")
        await self.stop()


async def run_heating(tg_client: Client, proxy: str | None):
    session_name = tg_client.name
    if settings.USE_PROXY and not proxy:
        logger.error(f"{session_name} | No proxy found for this session")
        return
    try:
        await TelegramJoiner(tg_client=tg_client, proxy=proxy).run()
    except InvalidSession:
        logger.error(f"{session_name} | Invalid Session")
