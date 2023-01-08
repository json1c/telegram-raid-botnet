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
import random
from rich.prompt import Prompt


class BaseFunction:
    def parse_delay(self, string: str):
        return list(
            map(int, string.split("-"))
        )

    def ask_accounts_count(self):
        accounts_count = int(Prompt.ask(
            "[bold magenta]how many accounts to use? [/]",
            default=str(len(self.sessions))
        ))

        self.sessions = self.sessions[:accounts_count]

    async def delay(self):
        if len(self.settings.delay) == 1:
            await asyncio.sleep(self.settings.delay[0])
        else:
            await asyncio.sleep(
                random.randint(*self.settings.delay)
            )
