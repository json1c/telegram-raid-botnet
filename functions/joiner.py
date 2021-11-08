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

from functions.function import Function

console = Console()


class JoinerFunc(Function):
    """Join chat"""

    async def join(self, session, invite, index):
        try:
            if "@" in invite:
                await session(JoinChannelRequest(invite))
            else:
                await session(ImportChatInviteRequest(invite))
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


    async def execute(self):
        accounts_count = int(Prompt.ask(
            "[bold magenta]how many accounts to use? [/]",
            default=str(len(self.sessions))
        ))

        self.sessions = self.sessions[:accounts_count]

        link = Prompt.ask("[bold red]link[/]")
       
        mode = Prompt.ask(
            "[bold red]mode>[/]",
            choices=["normal", "fast"]
        )

        if "t.me" in link:
            if "joinchat" in link:
                invite = link.split("/")[-1]
            else:
                invite = "@" + link.split("/")[-1]
        elif link.startswith("@"):
            invite = link

        joined = 0

        if mode == "normal":
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

                is_joined = await self.join(session, invite, index)

                if is_joined:
                    joined += 1

                await asyncio.sleep(int(delay))

        if mode == "fast":
            if not self.storage.initialize:
                for session in track(
                    self.sessions,
                    "[yellow]Initializing sessions[/]",
                    total=len(self.sessions)
                ):
                    await session.connect()

            with console.status("Joining"):
                start = perf_counter()

                tasks = await asyncio.wait([
                    self.join(session, invite, index)
                    for index, session in enumerate(self.sessions)
                ])

            for task in tasks[0]:
                if task.result():
                    joined += 1
            
        joined_time = round(perf_counter() - start, 2)
        console.print(f"[+] {joined} bots joined in [yellow]{joined_time}[/]s")

