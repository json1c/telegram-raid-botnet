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
import toml
import asyncio
from rich.prompt import Prompt
from rich.console import Console

from functions.function import Function

console = Console()


class CommentsFloodFunc(Function):
    """Flood to a channel comments"""

    async def flood(self, session, channel, post_id):
        await session.connect()
        me = await session.get_me()
        count = 0
        errors = 0

        while count < self.settings.messages_count \
                or self.settings.messages_count == 0:        
            text = random.choice(self.settings.messages)

            try:
                await session.send_message(
                    channel,
                    text,
                    comment_to=int(post_id),
                    parse_mode="html"
                )
            except Exception as err:
                console.print(
                    "[{name}] [bold red]not sended.[/] {err}"
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

        link = console.input("[bold red]link to post> [/]")

        delay = Prompt.ask(
            "[bold red]delay[/]",
            default="-".join(str(x) for x in self.settings.delay)
        )

        self.settings.delay = self.parse_delay(delay)

        channel = "/" .join(link.split("/")[:-1])
        post_id = link.split("/")[-1]

        await asyncio.wait([
            self.flood(session, channel, post_id)
            for session in self.sessions
        ])
