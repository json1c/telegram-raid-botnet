# https://github.com/json1c
# Copyright (C) 2022  json1c

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

import struct
import base64
from telethon import TelegramClient

from functions.base.base import BaseFunction
from modules.sessions_storage import SessionsStorage
from modules.settings import Settings

from typing import List
from pyrogram import Client


class PyrogramFunction(BaseFunction):
    PYROGRAM_STRING_SESSION_FORMAT = ">BI?256sQ?"

    def __init__(self, storage: SessionsStorage, settings: Settings):
        self.storage = storage
        self.settings = settings

        self.telethon_sessions: List[TelegramClient] = storage.sessions
        self.sessions: List[Client] = []
        
        for session in self.telethon_sessions:
            packed = struct.pack(
                self.PYROGRAM_STRING_SESSION_FORMAT,
                session.session.dc_id,
                settings.api_id,
                False,
                session.session.auth_key.key,
                111,
                False      
            )
            
            pyrogram_string_session = base64.urlsafe_b64encode(packed).decode().rstrip("=")

            self.sessions.append(
                Client(
                    name=self.storage.get_session_path(session),
                    api_id=settings.api_id,
                    api_hash=settings.api_hash,
                    session_string=pyrogram_string_session,
                    app_version="5.2",
                    device_model="Redmi Note 10",
                    lang_code="en",
                    in_memory=True
                )
            )
