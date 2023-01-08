# https://github.com/json1c
# Copyright (C) 2023  json1c

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

import asyncio
import random

from pyrogram import Client
from functions.base import PyrogramFunction
from rich.console import Console

console = Console()


class ReactionsFunc(PyrogramFunction):
    """Set reactions to message/post"""

    reactions = ['👍', '❤️', '🔥', '🥰', '👏', '😁', '🎉', '🤩', '👎', '🤯', '😱', '🤬', '😢', '🤮', '💩', '🙏']

    async def set_reaction(self, session: Client, chat_username: str, message_id: int, reaction=None):
        if not reaction:
            reaction = random.choice(self.reactions)

        async with session:
            try:
                await session.send_reaction(
                    chat_id=chat_username,
                    message_id=int(message_id),
                    emoji=reaction 
                )
            except Exception as err:
                console.print(f"[bold red][ERROR][/] [bold yellow][{session.me.id}][/] : {err}")
            else:
                console.print(f"[bold green][SUCCESS] [{session.me.id}][/] : Reaction \"{reaction}\" was sent")


    async def execute(self):
        link_to_message = console.input("[bold red]link to msg/post> [/]")
        chat_username, message_id = link_to_message.split("/")[-2:]

        reaction = console.input(
            "[bold red]enter reaction ({reactions}) or skip for random> [/]"
            .format(reactions=", ".join(self.reactions))
        )

        await asyncio.gather(*[
            self.set_reaction(
                session=session,
                chat_username=chat_username,
                message_id=message_id,
                reaction=reaction
            )
            for session in self.sessions
        ])
