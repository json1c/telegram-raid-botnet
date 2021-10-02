# This programm protected by GNU General Public License.
# If you bought this program, then you were deceived.
# https://github.com/json1c/telegram-raid-botnet

from telethon.tl.functions.account import UpdateProfileRequest
from rich.console import Console

console = Console()


class ChangeBioFunc:
    """Change bio"""

    def __init__(self, storage):
        self.storage = storage
        self.sessions = storage.sessions

    async def execute(self):
        bio = console.input("[bold red]bio> [/]")

        for session in self.sessions:
            await session.connect()

            await session(
                UpdateProfileRequest(about=bio)
            )
