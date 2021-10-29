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
import os
import random
import re

from typing import Dict, List

from rich.prompt import Confirm
from rich.console import Console

from telethon import events
from telethon.sync import TelegramClient

console = Console()


class SpamBlockFunc:
    """Check accounts status"""

    def __init__(self, storage):
        self.storage = storage
        self.sessions = storage.sessions

    async def execute(self):
        blocks: Dict[str, List[TelegramClient]] = {}
        for session in self.sessions:
            async with self.storage.ainitialize_session(session):
                me = await session.get_me()
                console.print(f"[bold white][*] Checking {me.first_name}")

                try:
                    await session.send_message("SpamBot", "/start")
                except Exception as err:
                    console.print(f"[bold red][!] {err}[/]")
                    continue

                messages = await session.get_messages("SpamBot", limit=1)
                text = messages[0].message
                print(text)
                
                if text != "Good news, no limits are currently applied to your account. You’re free as a bird!":
                    if "sending spam" in text:
                        console.print(f"[bold red][-] This is an eternal limitation[/]")

                        if not blocks.get("permanent"):
                            blocks["permanent"] = []

                        blocks["permanent"].append(session)
                    else:
                        date = re.findall(r"\d+\s\w+\s\d{4}", text)[0]
                        console.print(f"[bold red][-] {date}[/]")

                        if not blocks.get(date):
                            blocks[date] = []

                        blocks[date].append(session)
                else:
                    console.print("[bold green][+] Account without spam block[/]")

        move_sessions = Confirm.ask("[bold magenta]Move restricted sessions to other folders?[/]")

        if move_sessions:
            if not os.path.exists("sessions/spamblock"):
                os.mkdir("sessions/spamblock")
            
            for date, sessions in blocks.items():
                for session in sessions:
                    path = os.path.join("sessions", "spamblock", date)

                    if not os.path.exists(path):
                        os.mkdir(path)

                    session_path = self.storage.get_session_path(session)
                    session_name = os.path.basename(session_path)

                    os.rename(
                        session_path,
                        os.path.join(path, session_name)
                    )

