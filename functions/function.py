import asyncio
import random

from modules.sessions_storage import SessionsStorage
from modules.settings import Settings

from typing import List
from telethon.sync import TelegramClient
from rich.prompt import Prompt

class Function:
    def __init__(self, storage: SessionsStorage, settings: Settings):
        self.storage = storage
        self.sessions: List[TelegramClient] = storage.sessions
        self.settings = settings

    def parse_delay(self, string: str):
        delay = string.split("-")
        return [int(x) for x in delay]

    def ask_accounts_count(self):
        accounts_count = int(Prompt.ask(
            "[bold magenta]how many accounts to use? [/]",
            default=str(len(self.sessions))
        ))

        self.sessions = self.sessions[:accounts_count]

    async def delay(self):
        if len(self.settings.delay) == 1:
            await asyncio.sleep(self.settings.delay[0])
        else:
            await asyncio.sleep(
                random.randint(*self.settings.delay)
            )

