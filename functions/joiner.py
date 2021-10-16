# https://github.com/json1c
# Copyright (C) 2021  json1c

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

import asyncio

from rich.progress import track
from rich.console import Console
from rich.prompt import Prompt, Confirm

from multiprocessing import Process
from time import perf_counter

from telethon import events, types
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.sync import TelegramClient

console = Console()


class JoinerFunc:
    """Join chat"""

    def __init__(self, storage):
        self.storage = storage
        self.sessions = storage.sessions

    def solve_captcha(self, session: TelegramClient):
        self.solved = False

        @session.on(events.NewMessage)
        async def handler(msg: types.Message):
            me = await session.get_me()

            username = "" if me.username is None else me.username

            if not self.solved:
                if me.first_name in msg.text or username in msg.text:
                    if msg.reply_markup:
                        captcha = msg.reply_markup.rows[0] \
                            .buttons[0].data.decode("utf-8")

                        await msg.click(data=captcha)
                        self.solved = True

        if not self.storage.initialize:
            session.start()

        session.run_until_disconnected()

    async def execute(self):
        link = Prompt.ask("[bold red]link[/]")
        delay = Prompt.ask("[bold red]delay[/]", default=0)
        captcha = Confirm.ask("[bold red]captcha?", default="n")

        if "t.me" in link:
            if "joinchat" in link:
                invite = link.split("/")[-1]
            elif link.startswith("@"):
                invite = link
            else:
                invite = "@" + link.split("/")[-1]

        start = perf_counter()
        joined = 0

        for index, session in track(
            enumerate(self.sessions),
            "[yellow]Bots joining[/]",
            total=len(self.sessions)
        ):
            async with self.storage.ainitialize_session(session):
                try:
                    if captcha == "y":
                        Process(
                            target=self.solve_captcha,
                            args=[session]
                        ).start()

                    if "@" in invite:
                        await session(JoinChannelRequest(invite))
                    else:
                        await session(ImportChatInviteRequest(invite))
                except Exception as error:
                    print(f"[-] [acc {index + 1}] {error}")
                else:
                    joined += 1
                finally:
                    await asyncio.sleep(
                        int(delay)
                    )

        joined_time = round(perf_counter() - start, 2)

        console.print(f"[+] {joined} bots joined in [yellow]{joined_time}[/]s")
