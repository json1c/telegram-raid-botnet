# https://github.com/json1c
# Copyright (C) 2022  json1c

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

import asyncio

from rich.console import Console
from rich.markup import escape

from telethon import TelegramClient
from functions.base import TelethonFunction

console = Console()

class SetPasswordFunc(TelethonFunction):
    """Set two-step verification password to accounts"""
    
    async def edit_2fa(self, session: TelegramClient, password: str):
        async with self.storage.ainitialize_session(session):
            me = await session.get_me()

            try:
                await session.edit_2fa(new_password=password)
            except Exception as err:
                console.print(
                    "[{name}] : [bold red]Password not changed[/]. Error: {error}"
                    .format(name=escape(me.first_name), error=err)
                )
            else:
                console.print(
                    "[{name}] : [bold green]Successfully updated password"
                    .format(name=escape(me.first_name))
                )

    async def execute(self):
        password = console.input("[bold red]new password> [/]")

        with console.status("Setting password..."):
            await asyncio.wait([
                self.edit_2fa(session=session, password=password)
                for session in self.sessions
            ])

