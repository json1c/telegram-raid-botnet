# This programm protected by GNU General Public License.
# If you bought this program, then you were deceived.
# https://github.com/json1c/telegram-raid-botnet

import random
from telethon.tl.functions.account import UpdateProfileRequest
from rich.console import Console

console = Console()


class ChangeNameFunc:
    """Change names"""

    def __init__(self, storage):
        self.storage = storage
        self.sessions = storage.sessions

    async def execute(self):
        from_file = console.input("[bold red]from file? (y/n)> ")

        for session in self.sessions:
            if from_file == "y":
                with open("assets/names.txt") as file:
                    names = file.read().strip().splitlines()

                name = random.choice(names).split()
            else:
                name = console.input("[bold red]name> [/]").split()

            first_name = name[0]

            if len(name) == 2:
                last_name = name[1]
            else:
                last_name = ""

            async with self.storage.ainitialize_session(session):
                await session(
                    UpdateProfileRequest(
                        first_name=first_name,
                        last_name=last_name
                    )
                )
