import os
from contextlib import contextmanager, asynccontextmanager
from typing import List
from telethon.sync import TelegramClient
from telethon.sessions import StringSession


class SessionsStorage:
    def __init__(self, directory, api_id, api_hash):
        self.sessions: List[TelegramClient] = []

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
                    api_hash
                )

                if self.initialize:
                    print(f"initializing session {file}")

                    try:
                        session.connect()
                    except Exception as err:
                        print(f"session {file} returned error. {err}. removing.")
                        os.remove(os.path.join(directory, file))
                        continue

                    if not session.is_user_authorized():
                        print(f"session {file} is dead. removing it")
                        os.remove(os.path.join(directory, file))
                        continue

                self.sessions.append(session)

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
