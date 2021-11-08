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
import asyncio

from telethon import functions, types
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest, InviteToChannelRequest
from telethon.errors import PeerFloodError, UserPrivacyRestrictedError

from rich.prompt import Prompt
from rich.console import Console

from functions.function import Function

console = Console()


class InvitingFunc(Function):
    """Invite users from supergroup"""

    @staticmethod
    def transform_to_valid_invite(link):
        if "t.me" in link:
            if "joinchat" in link:
                invite = link.split("/")[-1]
            else:
                invite = "@" + link.split("/")[-1]
        elif link.startswith("@"):
            invite = link

        return invite

    @staticmethod
    def chunkify(lst, n):  # split list
        return [lst[i::n] for i in range(n)]
   
    async def invite(self, users, channel, session):
        users_for_invite = []

        async with self.storage.ainitialize_session(session):
            channel = await session.get_entity(channel)
            for user in users: 
                if user.username:
                    user = await session.get_entity(user.username)
                    users_for_invite.append(user)

            for user in users_for_invite:
                try:
                    await session(InviteToChannelRequest(
                        channel=channel,
                        users=[user]
                    ))
                except PeerFloodError as err:
                    console.print(f"[bold red]{err}[/]")
                    return
                except UserPrivacyRestrictedError:
                    pass

    async def execute(self):
        accounts_count = int(Prompt.ask(
            "[bold magenta]how many accounts to use?[/]",
            default=str(len(self.sessions))
        ))

        self.sessions = self.sessions[:accounts_count]

        link = console.input("[bold red]link to chat> [/]")
        invite = self.transform_to_valid_invite(link)

        session = None

        with console.status("Parsing users...", spinner="dots"):
            for session in self.sessions:
                await session.connect()

                try:
                    if "@" in invite:
                        await session(JoinChannelRequest(invite))
                    else:
                        await session(ImportChatInviteRequest(invite))
                except Exception as err:
                    console.print(err)
                    await session.disconnect()
                    continue
                else:
                    break

            users = await session.get_participants(link, aggressive=True)

        console.print(
            "[bold green][*] Parsed {} users[/]"
            .format(len(users))
        )

        users = self.chunkify(users, len(self.sessions))

        link = console.input("[bold red]where to invite users> [/]")

        with console.status("Inviting...", spinner="dots"):
            await asyncio.wait([
                self.invite(users_chunk, link, session)
                for session, users_chunk in zip(self.sessions, users)
            ])

