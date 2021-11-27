# https://github.com/json1c
# Copyright (C) 2021  json1c

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

import asyncio
from rich.console import Console
from functions.function import Function

console = Console()

class SetPasswordFunc(Function):
    """Set two-step verification password to accounts"""

    async def execute(self):
        password = console.input("[bold red]new password> [/]")

        with console.status("Setting password..."):
            await asyncio.wait([
                session.edit_2fa(new_password=password)
                for session in self.sessions
            ])

