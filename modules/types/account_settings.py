# https://github.com/json1c
# Copyright (C) 2023  json1c

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

from dataclasses import dataclass
from datetime import datetime

from modules.types.account import Account
from modules.types.application import Application


@dataclass
class AccountSettings:
    auth_key: str

    account: Account
    application: Application

    @staticmethod
    def from_dict(session_dict: dict) -> "AccountSettings":
        return AccountSettings(
            auth_key=session_dict["auth_key"],
            account=Account(
                first_name=session_dict["account"]["first_name"],
                last_name=session_dict["account"]["last_name"],
                user_id=session_dict["account"]["user_id"],
                added_at=datetime.fromtimestamp(session_dict["account"]["added_at"]),
                phone_number=session_dict["account"]["phone_number"],
            ),
            application=Application(
                api_id=session_dict["application"]["api_id"],
                api_hash=session_dict["application"]["api_hash"],
                device_name=session_dict["application"]["device_name"],
                app_version=session_dict["application"]["app_version"],
                sdk=session_dict["application"]["sdk"],
                lang_pack=session_dict["application"]["lang_pack"],
                system_lang_code=session_dict["application"]["system_lang_code"],
            )
        )
