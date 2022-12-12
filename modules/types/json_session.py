from __future__ import annotations

import random
import json
import dataclasses

from telethon import TelegramClient
from telethon.sessions import StringSession
from typing import Any
from datetime import datetime

from modules.generators.application import Application
from modules.generators.linux import LinuxAPI
from modules.generators.telegram_android import TelegramAppAPI
from modules.types.account import Account
from modules.types.application import Application
from modules.types.account_settings import AccountSettings
from modules.generators.proxy import IP
from modules.types.proxy import Proxy


class JsonSession:
    def __init__(self, *, account_settings=None, dict_settings=None, ):

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

        if input("Would you like to use proxy? y/n ") == 'y':
            random_IP_iter = random.randrange(len(IP))
            proxy_ip = IP[random_IP_iter][0]
            port = IP[random_IP_iter][1]
            ip_socks = IP[random_IP_iter][2]

            try:
                proxy_login = IP[random_IP_iter][3]
                proxy_pass = IP[random_IP_iter][4]
            except:
                proxy_login = None
                proxy_pass = None

            if input("Would you like to custom connection to proxy? y/n ") == 'y':
                input_proxy_number = 0
                input_proxy_number = int(input(f"Please input number of a PROXY from [0:{len(IP) - 1}]: "))
                proxy_ip = IP[input_proxy_number][0]
                port = IP[input_proxy_number][1]
                ip_socks = IP[input_proxy_number][2]
                try:
                    proxy_login = IP[input_proxy_number][3]
                    proxy_pass = IP[input_proxy_number][4]
                except:
                    proxy_login = None
                    proxy_pass = None

            proxy = (ip_socks, proxy_ip, port, True, proxy_login, proxy_pass)

            async with TelegramClient(
                    session=StringSession(),
                    api_id=api_id,
                    api_hash=api_hash,
                    proxy=proxy,
                    device_model=device_name,
                    app_version=app_version,
                    system_version=sdk,
                    lang_code=system_lang_code,
                    system_lang_code=system_lang_code
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
                    proxy=Proxy(
                        socks=ip_socks,
                        proxy_ip=proxy_ip,
                        port=port,
                        proxy_login=proxy_login,
                        proxy_pass=proxy_pass
                    )
                )

                with open(f"{account.phone}.jsession", "w") as file:
                    json.dump(
                        dataclasses.asdict(account_settings),
                        file,
                        ensure_ascii=True,
                        indent=4
                    )

        else:
            async with TelegramClient(
                    session=StringSession(),
                    api_id=api_id,
                    api_hash=api_hash,
                    device_model=device_name,
                    app_version=app_version,
                    system_version=sdk,
                    lang_code=system_lang_code,
                    system_lang_code=system_lang_code
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
                    )
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
