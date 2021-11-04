# https://github.com/json1c
# Copyright (C) 2021  json1c

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

import os
import asyncio
from contextlib import contextmanager, asynccontextmanager
from typing import List, Dict
from telethon.sync import TelegramClient
from telethon.sessions import StringSession


class SessionsStorage:
    def __init__(self, directory, api_id, api_hash):
        self.full_sessions: Dict[str, TelegramClient] = {}

        self.initialize = (
            True if input("Initialize sessions? (y/n) ") == "y"
            else False
        )

        for file in os.listdir(directory):
            if file.endswith(".session"):
                session_path = os.path.join(directory, file)

                with open(session_path) as fileobj:
                    auth_key = fileobj.read()

                session = TelegramClient(
                    StringSession(auth_key),
                    api_id,
                    api_hash,
                    lang_code="en",
                    system_lang_code="en"
                )

                self.full_sessions[session_path] = session

        if self.initialize:
            asyncio.get_event_loop().run_until_complete(
                asyncio.wait([
                    self.check_session(session, path)
                    for path, session in self.full_sessions.items()
                ])
            )

    async def check_session(self, session, path):
        print(f"initializing session {path}")

        try:
            await session.connect()
        except Exception as err:
            print(f"session {path} returned error. {err}. removing.")
            os.remove(os.path.join(directory, file))
            return

        if not await session.is_user_authorized():
            print(f"session {path} is dead. removing it")
            os.remove(os.path.join(directory, file))
            return
        
        print(f"initialized {path}")

    def get_session_path(self, session: TelegramClient) -> str:
        for path, client in self.full_sessions.items():
            if client == session:
                return path

    @property
    def sessions(self) -> List[TelegramClient]:
        return list(self.full_sessions.values())

    @contextmanager
    def initialize_session(self, session):
        if not self.initialize:
            session.connect()

        yield

        if not self.initialize:
            session.disconnect()

    @asynccontextmanager
    async def ainitialize_session(self, session):
        if not self.initialize:
            await session.connect()

        yield

        if not self.initialize:
            await session.disconnect()

    def __len__(self):
        return len(self.sessions)
