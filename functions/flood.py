# https://github.com/json1c
# Copyright (C) 2022  json1c

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

import asyncio
import os
import random
from rich.prompt import Prompt, Confirm
from rich.console import Console
from multiprocessing import Process
from telethon import events, types
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import InputStickerSetShortName

from functions.base import TelethonFunction
console = Console()

class Flood(TelethonFunction):
    def __init__(self, storage, settings):
        super().__init__(storage, settings)

        self.choice = None
        self.function = None

        self.modes = (
            ("Raid with text", self.text_flood),
            ("Single bot raid", self.text_flood),
            ("Raid with media", self.gif_flood),
            ("Raid with reply", self.reply_flood),
            ("Raid with stickers", self.stickers_flood)
        )

        self.reply_msg_id = 0
    
    async def stickers_flood(self, session, peer, text):
        stickers = await session(
            GetStickerSetRequest(
                stickerset=InputStickerSetShortName(
                    short_name=self.sticker_set
                )
            )
        )

        await session.send_file(peer, random.choice(stickers.documents))

        await session.send_message(
            peer,
            text,
            parse_mode="html"
        )

    async def text_flood(self, session, peer, text):
        await session.send_message(
            peer,
            text,
            parse_mode="html"
        )

    async def reply_flood(self, session, peer, text):
        await session.send_message(
            peer,
            text,
            reply_to=self.reply_msg_id,
            parse_mode="html"
        )

    async def gif_flood(self, session, peer, text):
        file = random.choice(os.listdir("media"))

        await session.send_file(
            peer,
            os.path.join("media", file),
            caption=text,
            parse_mode="html"
        )

    async def flood(self, session, peer, function):
        if not self.storage.initialize:
            await session.connect()

        users = []
        admins = []

        admin_links = []

        count = 0
        errors = 0
        me = await session.get_me()

        if self.mention_all:
            admins = await session.get_participants(
                peer,
                filter=types.ChannelParticipantsAdmins
            )

            if self.mention_mode == "users":
                users = [
                    user for user in await session.get_participants(peer)
                    if user not in admins
                ]

                users_links = [
                    f"<a href=\"tg://user?id={user.id}\">\u206c\u206f</a>"
                    for user in users
                ]

            admin_links = [
                f"<a href=\"tg://user?id={user.id}\">\u206c\u206f</a>"
                for user in admins
            ]


        while count < self.settings.messages_count \
                or self.settings.messages_count == 0:
            if not self.mention_all:
                text = random.choice(self.settings.messages)
            else:
                if function is not self.gif_flood:
                    text = random.choice(self.settings.messages) + \
                        "\u206c\u206f".join(
                            random.sample(users_links, 15) if self.mention_mode == "users"
                            else random.sample(admin_links, len(admins) // 2)
                        )
                else:
                    text = random.choice(self.settings.messages) + \
                        "\u206c\u206f".join(
                            random.sample(users_links, 5) if self.mention_mode == "users"
                            else random.sample(admin_links, len(admins) // 2)
                        )

            try:
                await function(session, peer, text)
            except Exception as err:
                console.print(
                    "[{name}] [bold red]not sended.[/] [bold white]{err}[/]"
                    .format(name=me.first_name, err=err)
                )

                errors += 1

                if errors >= 3:
                    await session.delete_dialog(peer)
                    break

            else:
                count += 1
                console.print(
                    "[{name}] [bold green]sended.[/] COUNT: [yellow]{count}[/]"
                    .format(name=me.first_name, count=count)
                )
            finally:
                await self.delay()

    def handle(self, session, function):
        @session.on(events.NewMessage)
        async def handler(message: types.Message):
            if message.raw_text == self.settings.trigger:
                await self.flood(
                    session,
                    message.chat_id,
                    function,
                )

                if message.reply_to:
                    self.reply_msg_id = message.reply_to.reply_to_msg_id

        if not self.storage.initialize:
            session.start()

        session.run_until_disconnected()

    def ask(self):
        for index, mode in enumerate(self.modes):
            console.print(
                "[bold white][{index}] {description}[/]"
                .format(index=index + 1, description=mode[0]),
            )

        choice = console.input(
            "[bold white]>> [/]"
        )

        while not choice.isdigit():
            choice = console.input(
                "[bold white]>> [/]"
            )

        else:
            self.choice = int(choice) - 1

        self.function = self.modes[self.choice][1]
        self.ask_accounts_count()

        if self.choice == 4:
            self.sticker_set = console.input("[bold red]enter link to sticker set (e.g https://t.me/addstickers/AlbinoEmoji)> [/]")
            self.sticker_set = self.sticker_set.replace("https://t.me/addstickers/", "")

        delay = Prompt.ask(
            "[bold red]delay[/]",
            default="-".join(str(x) for x in self.settings.delay)
        )

        self.settings.delay = self.parse_delay(delay)
        self.mention_all = Confirm.ask("[bold red]mention all?[/]", default="y")

        if self.mention_all:
            self.mention_mode = Prompt.ask(
                "[bold red]mention mode[/]",
                choices=["admins", "users"]
            )
        
        return self.choice
    
    async def start_single_raid(self, sessions, link):
        for session in sessions:
            await session.connect()

            await self.flood(
                session,
                link,
                self.function,
            )

    def start_processes(self):
        if self.choice == 1:
            link = Prompt.ask("[bold red]link to chat[/]")

            asyncio.get_event_loop().run_until_complete(self.start_single_raid(self.sessions, link))

        processes = []

        for session in self.sessions:
            if self.choice != 1:
                process = Process(
                    target=self.handle, args=[session, self.function]
                )

                process.start()
                processes.append(process)


        if self.choice != 1:
            console.print(
                "[bold white][*] Send «[green]{trigger}[/]» to chat[/]"
                .format(trigger=self.settings.trigger)
            )

            for process in processes:
                process.join()

