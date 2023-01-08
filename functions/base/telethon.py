# https://github.com/json1c
# Copyright (C) 2023  json1c

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

from functions.base.base import BaseFunction
from modules.storages.sessions_storage import SessionsStorage
from modules.settings import Settings

from typing import List
from telethon.sync import TelegramClient

from modules.types.json_session import JsonSession


class TelethonFunction(BaseFunction):
    def __init__(self, storage: SessionsStorage, settings: Settings):
        self.storage = storage
        self.settings = settings
        
        self.sessions: List[TelegramClient] = storage.sessions
