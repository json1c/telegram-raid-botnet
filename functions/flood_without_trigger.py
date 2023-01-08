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
from functions.base import TelethonFunction
from functions.flood import Flood
from rich.console import Console

console = Console()


class FloodWithoutTriggerFunc(TelethonFunction):
    """Flood without trigger (asyncio)"""

    async def execute(self):
        link = console.input("[bold red]link> [/]")
        flood = Flood(self.storage, self.settings)
        flood.ask()

        await asyncio.wait([
            flood.flood(session, link, flood.function)
            for session in self.sessions
        ])
        