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
import json
import os
from contextlib import asynccontextmanager, contextmanager
from typing import Dict, List, Union

from rich.console import Console
from telethon.sessions import StringSession
from telethon.sync import TelegramClient

from modules.types.json_session import JsonSession

console = Console()


class SessionsStorage:
    def __init__(self, directory: str, api_id: Union[str, int], api_hash: str):
        self.full_sessions: Dict[str, Union[TelegramClient, JsonSession]] = {}
        self.json_sessions: List[JsonSession] = []

        self.initialize = True if input("Initialize sessions? (y/n) ") == "y" else False

        for file in os.listdir(directory):
            if file.endswith(".session"):
                session_path = os.path.join(directory, file)

                with open(session_path) as fileobj:
                    auth_key = fileobj.read()

                if len(auth_key) != 353:
                    continue

                session = TelegramClient(
                    StringSession(auth_key),
                    api_id,
                    api_hash,
                    device_model="Redmi Note 10",
                    lang_code="en",
                    system_lang_code="en",
                )

                self.full_sessions[session_path] = session

            elif file.endswith(".jsession"):
                session_path = os.path.join(directory, file)

                with open(session_path) as fileobj:
                    session_settings = json.load(fileobj)

                session = JsonSession(dict_settings=session_settings)

                if old_session := self.is_user_id_exists(
                    session.account.account.user_id
                ):
                    old_session_path = self.get_session_path(old_session)
                    session_path = self.get_session_path(session)

                    console.print(
                        f"[bold yellow]WARNING:[/] Same accounts in botnet — {old_session_path} matches with {session_path}"
                    )
                    continue

                client = TelegramClient(
                    session=StringSession(session.account.auth_key),
                    api_id=session.account.application.api_id,
                    api_hash=session.account.application.api_hash,
                    device_model=session.account.application.device_name,
                    app_version=session.account.application.app_version,
                    system_version=session.account.application.sdk,
                    lang_code=session.account.application.system_lang_code,
                    system_lang_code=session.account.application.system_lang_code,
                )

                self.json_sessions.append(session)
                self.full_sessions[session_path] = client

        if self.initialize:
            if len(self.full_sessions) == 0:
                return print(
                    "In order for the botnet to work, you need to add accounts"
                )

            with console.status("Initializing..."):
                asyncio.get_event_loop().run_until_complete(
                    asyncio.gather(
                        *[
                            self.check_session(session, path)
                            for path, session in self.full_sessions.items()
                        ]
                    )
                )

    async def check_session(self, session: TelegramClient, path: str):
        console.log(f"Initializing session {path}")

        try:
            await session.connect()
        except Exception as err:
            console.log(f"Session {path} returned error. {err}. Removing.")
            del self.full_sessions[path]
            os.remove(path)
            return

        if not await session.is_user_authorized():
            console.log(f"Session {path} is dead. Removing it")
            del self.full_sessions[path]
            os.remove(path)
            return

        console.log(f"Initialized {path}")

    def get_session_path(self, session: TelegramClient | JsonSession) -> str:
        for path, client in self.full_sessions.items():
            if client == session:
                return path

    def is_user_id_exists(self, user_id: int) -> bool:
        for session in self.json_sessions:
            if session.account.account.user_id == user_id:
                return session

        return False

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
