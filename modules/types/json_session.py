# https://github.com/json1c
# Copyright (C) 2023  json1c

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

import dataclasses
import json
import random
from datetime import datetime
from typing import Any

from telethon import TelegramClient
from telethon.sessions import StringSession

from modules.generators.application import Application
from modules.generators.linux import LinuxAPI
from modules.generators.telegram_android import TelegramAppAPI
from modules.types.account import Account
from modules.types.account_settings import AccountSettings
from modules.types.application import Application
from modules.types.proxy import Proxy


class JsonSession:    
    def __init__(self, *, account_settings=None, dict_settings=None):
        if account_settings is not None:
            self.account: AccountSettings = account_settings

        elif dict_settings is not None:
            self.account: AccountSettings = AccountSettings.from_dict(dict_settings)

    def save(self, filename):
        with open(filename, 'w') as file:
            json.dump(file, dataclasses.as_json(self.account), indent=4)

    @staticmethod
    async def create_application_session(
        generator: Application | Any = None,
        proxy: Proxy | Any = None,
        api_hash: str | Any = None,
        api_id: str | Any = None,
        device_name: str | Any = None,
        app_version: str | Any = None,
        sdk: str | Any = None,
    ):
        if not generator:
            generator = random.choice([LinuxAPI, TelegramAppAPI])

        api_hash = api_hash or generator.api_hash
        api_id = api_id or generator.api_id
        app_version = app_version or generator.app_version()
        device_name = device_name or generator.device()
        sdk = sdk or generator.sdk()
        lang_pack = generator.lang_pack
        system_lang_code = generator.system_lang_code()

        async with TelegramClient(
            session=StringSession(),
            api_id=api_id,
            api_hash=api_hash,
            device_model=device_name,
            app_version=app_version,
            system_version=sdk,
            lang_code=system_lang_code,
            system_lang_code=system_lang_code,
            proxy=proxy.as_telethon() if proxy else None
        ) as client:
            account = await client.get_me()

            account_settings = AccountSettings(
                auth_key=client.session.save(),
                account=Account(
                    first_name=account.first_name,
                    last_name=account.last_name,
                    user_id=account.id,
                    added_at=datetime.now().timestamp(),
                    phone_number=account.phone,
                ),
                application=Application(
                    api_id=api_id,
                    api_hash=api_hash,
                    device_name=device_name,
                    app_version=app_version,
                    sdk=sdk,
                    lang_pack=lang_pack,
                    system_lang_code=system_lang_code,
                ),
                proxy=proxy
            )

            with open(f"{account.phone}.jsession", "w") as file:
                json.dump(
                    dataclasses.asdict(account_settings),
                    file,
                    ensure_ascii=True,
                    indent=4
                )

    @staticmethod
    async def build_session_from_telegram_client(
        client: TelegramClient,
        api_hash: str | Any = None,
        api_id: str | Any = None,
        device_name: str | Any = None,
        app_version: str | Any = None,
        sdk: str | Any = None,
        lang_pack: str | Any = None,
        system_lang_code: str | Any = None,
    ) -> "JsonSession":
        account = await client.get_me()

        if not generator:
            generator = random.choice([LinuxAPI, TelegramAppAPI])

        api_hash = api_hash or generator.api_hash
        api_id = api_id or generator.api_id
        app_version = app_version or generator.app_version()
        device_name = device_name or generator.device()
        sdk = sdk or generator.sdk()
        lang_pack = generator.lang_pack
        system_lang_code = system_lang_code or generator.system_lang_code()

        return JsonSession(
            account_settings=AccountSettings(
                auth_key=client.session.auth_key.key,
                fiest_name=account.first_name,
                last_name=account.last_name,
                user_id=account.user_id,
                added_at=datetime.now().timestamp(),
                phone_number=account.phone,
                application=Application(
                    api_id=api_id,
                    api_hash=api_hash,
                    device_name=device_name,
                    app_version=app_version,
                    sdk=sdk,
                    lang_pack=lang_pack,
                    system_lang_pack=system_lang_code,
                )
            )
        )
