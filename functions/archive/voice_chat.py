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
from pytgcalls import idle
from pytgcalls.types import AudioPiped
from pytgcalls import PyTgCalls
from telethon import utils
from rich.console import Console
from youtube_dl import YoutubeDL

from functions.function import Function

console = Console()


class VoicePlayFunc(Function):
    """Join voice chat and play audio"""

    async def join_and_play(self, session):
        await session.start()

        app = PyTgCalls(session)
        await app.start()
        entity = await session.get_entity(self.chat)

        await app.join_group_call(
            utils.get_peer_id(entity),
            AudioPiped(self.media_url)
        )

        await idle()


    async def execute(self):
        self.ask_accounts_count()

        self.chat = console.input("[bold red]chat link> [/]")
        
        console.print(
            "\n[bold white][1] From Youtube\n"
            "[2] From direct link to file[/]\n"
        )

        choice = console.input("[bold white]>> [/]")

        if choice == "1":
            url = console.input("[bold red]video url> [/]")
            ydl = YoutubeDL()

            r = ydl.extract_info(url, download=False)
            self.media_url = r['formats'][-1]['url']
        
        elif choice == "2":
            url = console.input("[bold red]url> [/]")
            self.media_url = url

        await asyncio.wait([
            self.join_and_play(session)
            for session in self.sessions
        ])
