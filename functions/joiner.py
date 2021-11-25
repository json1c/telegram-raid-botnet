# https://github.com/json1c
# Copyright (C) 2021  json1c

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

import random
import asyncio

from rich.progress import track
from rich.console import Console
from rich.prompt import Prompt, Confirm

from time import perf_counter

from telethon import events, types
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.sync import TelegramClient

from functions.function import Function

console = Console()


class JoinerFunc(Function):
    """Join chat"""

    async def join(self, session, link, index, mode):
        if mode == "1":
            try:
                if "joinchat" in link:
                    invite = link.split("/")[-1]
                    await session(ImportChatInviteRequest(invite))
                elif "+" in link:
                    invite = link.split("+")[1]
                    await session(ImportChatInviteRequest(invite))
                else:
                    await session(JoinChannelRequest(link))
            except Exception as error:
                print(f"[-] [acc {index + 1}] {error}")
            else:
                return True

        elif mode == "2":
            try:
                channel = await session(GetFullChannelRequest(link))
                chat = channel.chats[1]
                await session(JoinChannelRequest(chat))
            except Exception as error:
                print(f"[-] [acc {index + 1}] {error}")
            else:
                return True

    async def solve_captcha(self, session: TelegramClient):
        session.add_event_handler(
            self.on_message,
            events.NewMessage
        )

        await session.run_until_disconnected()

    async def on_message(self, msg: types.Message):
        if msg.mentioned:
            if msg.reply_markup:
                captcha = msg.reply_markup.rows[0] \
                    .buttons[0].data.decode("utf-8")

                await msg.click(data=captcha)

    async def flood(self, session, peer):
        count = 0
        errors = 0
        me = await session.get_me()

        if self.mention_all:
            users = await session.get_participants(peer)

            users_links = [
                f"<a href=\"tg://user?id={user.id}\">\u206c\u206f</a>"
                for user in users
            ]


        while count < self.settings.messages_count \
                or self.settings.messages_count == 0:
            if not self.mention_all:
                text = random.choice(self.settings.messages)
            else:
                text = random.choice(self.settings.messages) + \
                    "\u206c\u206f".join(
                        random.sample(users_links, 5) if self.mention_mode == "users"
                        else random.sample(admin_links, len(admins) // 2)
                    )

            try:
                await session.send_message(
                    peer,
                    text,
                    parse_mode="html"
                )
            except Exception as err:
                console.print(
                    "[{name}] [bold red]not sended.[/] [bold white]{err}[/]"
                    .format(name=me.first_name, err=err)
                )

                errors += 1

                if errors >= 5:
                    break
            else:
                count += 1
                console.print(
                    "[{name}] [bold green]sended.[/] COUNT: [yellow]{count}[/]"
                    .format(name=me.first_name, count=count)
                )
            finally:
                await self.delay()

    async def execute(self):
        self.ask_accounts_count()

        print()

        console.print(
            "[1] Just join chat/channel",
            "[2] Join linked to channel chat",
            sep="\n",
            style="bold white"
        )

        print()

        mode = console.input("[bold red]mode> [/]")
        link = console.input("[bold red]link> [/]")

        speed = Prompt.ask(
            "[bold red]speed>[/]",
            choices=["normal", "fast"]
        )

        flood = Confirm.ask("[bold red]flood instantly?[/]")

        if flood:
            self.mention_all = Confirm.ask(
                "[bold red]mention all?[/]",
                default=True
            )

        joined = 0

        if speed == "normal":
            delay = Prompt.ask("[bold red]delay[/]", default="0")
            captcha = Confirm.ask("[bold red]captcha[/]")

            start = perf_counter()

            for index, session in track(
                enumerate(self.sessions),
                "[yellow]Joining[/]",
                total=len(self.sessions)
            ):
                await session.start()

                if captcha:
                    asyncio.create_task(
                        self.solve_captcha(session)
                    )

                is_joined = await self.join(session, link, index, mode)

                if is_joined:
                    joined += 1

                await asyncio.sleep(int(delay))

        if speed == "fast":
            if not self.storage.initialize:
                for session in track(
                    self.sessions,
                    "[yellow]Initializing sessions[/]",
                    total=len(self.sessions)
                ):
                    await session.connect()

            with console.status("Joining"):
                start = perf_counter()

                tasks = await asyncio.gather(*[
                    self.join(session, link, index, mode)
                    for index, session in enumerate(self.sessions)

                ])

            for result in tasks:
                if result:
                    joined += 1
        if flood:
            await asyncio.wait([
                self.flood(session, link)
                for session in self.sessions
            ])

        joined_time = round(perf_counter() - start, 2)
        console.print(f"[+] {joined} bots joined in [yellow]{joined_time}[/]s")

