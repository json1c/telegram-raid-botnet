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
import random
import os
from rich.prompt import Prompt, Confirm
from rich.console import Console

console = Console()


class PmFloodFunc:
    """Flood to PM"""

    def __init__(self, storage):
        self.storage = storage
        self.sessions = storage.sessions

    async def flood(self, session, peer, text, delay, media):
        count = 0
        errors = 0

        async with self.storage.ainitialize_session(session):
            me = await session.get_me()

            while True:
                try:
                    if not media:
                        await session.send_message(peer, text)
                    else:
                        file = random.choice(os.listdir("media"))

                        await session.send_file(
                            peer,
                            os.path.join("media", file),
                            caption=text,
                            parse_mode="html"
                        )
                except Exception as err:
                    console.print(
                        "[{name}] [bold red]not sended.[/] {err}"
                        .format(name=me.first_name, err=err)
                    )

                    if errors > 3:
                        break
                    
                    errors += 1
                else:
                    count += 1
                    console.print(
                        "[{name}] [bold green]sended.[/] COUNT: [yellow]{count}[/]"
                        .format(name=me.first_name, count=count)
                    )
                finally:
                    await self.sleep()

    async def sleep(self):
        if isinstance(self.delay, list):
            delay = random.randint(*self.delay)
        else:
            delay = self.delay

        await asyncio.sleep(delay)

    async def execute(self):
        accounts_count = int(Prompt.ask(
            "[bold magenta]how many accounts to use? [/]",
            default=str(len(self.sessions))
        ))

        self.sessions = self.sessions[:accounts_count]

        peer = console.input("[bold red]enter uid or username> [/]")
        media = Confirm.ask("[bold red]media")
        text = console.input("[bold red]text> [/]")

        delay = Prompt.ask(
            "[bold red]delay[/]",
            default="1-3"
        ).split("-")

        if len(delay) == 1:
            self.delay = int(delay[0])
        elif len(delay) == 2:
            self.delay = [int(i) for i in delay]

        await asyncio.wait([
            self.flood(session, peer, text, delay, media)
            for session in self.sessions
        ])
