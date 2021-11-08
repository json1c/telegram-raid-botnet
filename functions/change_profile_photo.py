# https://github.com/json1c
# Copyright (C) 2021  json1c

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

import random
import os

from telethon import functions, types

from rich.progress import track
from rich.console import Console

from functions.function import Function

console = Console()


class ChangeProfilePhotoFunc(Function):
    """Change profile photo"""

    async def execute(self):
        path = os.path.join(os.getcwd(), "assets", "photos")
        console.input(
            f"\n[bold white]will be used photos from folder {path}"
            "\nPress [Enter] to continue[/]"
        )
        
        photos = os.listdir(path)

        for index, session in track(
            enumerate(self.sessions),
            "[yellow]Setting photos...[/]",
            total=len(self.sessions)
        ):
            photo = os.path.join(
                path, random.choice(photos)
            )

            async with self.storage.ainitialize_session(session):
                me = await session.get_me()
                try:
                    await session(functions.photos.UploadProfilePhotoRequest(
                        file=await session.upload_file(photo),
                    ))
                except Exception as err:
                    console.print(
                        "[{name}] [bold red]error.[/] {err}"
                        .format(name=me.first_name, error=err)
                    )

