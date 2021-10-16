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
from rich.console import Console

console = Console()


class PmFloodFunc:
    """Flood to PM"""

    def __init__(self, storage):
        self.storage = storage
        self.sessions = storage.sessions

    async def flood(self, session, peer, text, delay):
        count = 0

        async with self.storage.ainitialize_session(session):
            me = await session.get_me()

            while True:
                try:
                    await session.send_message(peer, text)
                except Exception as err:
                    console.print(
                        "[{name}] [bold red]not sended.[/] {err}"
                        .format(name=me.first_name, err=err)
                    )
                else:
                    count += 1
                    console.print(
                        "[{name}] [bold green]sended.[/] COUNT: [yellow]{count}[/]"
                        .format(name=me.first_name, count=count)
                    )
                finally:
                    await asyncio.sleep(delay)

    async def execute(self):
        peer = console.input("[bold red]enter uid or username> [/]")
        text = console.input("[bold red]text> [/]")

        delay = float(
            console.input("[bold red]delay> [/]")
        )

        await asyncio.wait([
            self.flood(session, peer, text, delay)
            for session in self.sessions
        ])
