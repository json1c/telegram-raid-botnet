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
import phonenumbers

from phonenumbers import geocoder
from collections import Counter

from rich.table import Table
from rich.console import Console

from functions.base import TelethonFunction

console = Console()


class PhoneNumbersStatsFunc(TelethonFunction):
    """Statistics (phone numbers)"""

    async def get_phone_number(self, session):
        try:
            await session.connect()
        except Exception:
            return
        else:
            me = await session.get_me()
            return me.phone

    async def execute(self):
        with console.status("Wait..."):
            phones = await asyncio.gather(*[
                self.get_phone_number(session)
                for session in self.sessions
            ])

        countries = []
        countries_by_country_code = {}
        
        table = Table()

        table.add_column("Phone country code", justify="left", style="white")
        table.add_column("Country", style="white")
        table.add_column("Count", justify="center", style="white")

        for phone in phones:
            if phone is not None:
                try:
                    parsed_phone = phonenumbers.parse(f"+{phone}", None)
                except Exception:
                    continue

                country = geocoder.description_for_number(parsed_phone, "en")

                if not countries_by_country_code.get(parsed_phone.country_code):
                    countries_by_country_code[parsed_phone.country_code] = country
                
                countries.append(parsed_phone.country_code)

        countries = Counter(countries)

        for country_code, count in countries.items():
            country_name = countries_by_country_code[country_code]

            if not country_name:
                country_name = "N/A"

            table.add_row(
                str(country_code), country_name, str(count)
            )
        
        console.print(table)
