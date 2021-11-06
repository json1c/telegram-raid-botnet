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
import toml
import os
import random
from rich.prompt import Prompt, Confirm
from rich.console import Console
from multiprocessing import Process
from telethon import events, functions, types

console = Console()


class FloodFunc:
    """Flood to chat"""

    def __init__(self, storage):
        self.storage = storage
        self.sessions = storage.sessions

        self.modes = (
            ("Raid with text", self.text_flood),
            ("Raid with media", self.gif_flood),
            ("Raid with reply", self.reply_flood)
        )

        with open("config.toml") as f:
            self.config = toml.load(f)["flood"]

    async def text_flood(self, session, msg, text):
        await session.send_message(
            msg.chat_id,
            text,
            parse_mode="html"
        )

    async def reply_flood(self, session, msg, text):
        await session.send_message(
            msg.chat_id,
            text,
            reply_to=msg.reply_to.reply_to_msg_id,
            parse_mode="html"
        )

    async def gif_flood(self, session, msg, text):
        file = random.choice(os.listdir("media"))

        await session.send_file(
            msg.chat_id,
            os.path.join("media", file),
            caption=text,
            parse_mode="html"
        )

    async def flood(self, session, msg, function):
        if self.config["messages_count"] == 0:
            self.config["messages_count"] = 900000000

        users = []
        admins = []

        user_links = []
        admin_links = []

        count = 0
        me = await session.get_me()

        if self.mention_all:
            admins = await session.get_participants(
                msg.chat_id,
                filter=types.ChannelParticipantsAdmins
            )

            async for user in session.iter_participants(msg.chat_id):
                if user not in admins:
                    users.append(user)

            users_links = [
                f"<a href=\"tg://user?id={user.id}\">\u206c\u206f</a>"
                for user in users
            ]

            admin_links = [
                f"<a href=\"tg://user?id={user.id}\">\u206c\u206f</a>"
                for user in admins
            ]


        for _ in range(self.config["messages_count"]):
            if not self.mention_all:
                text = random.choice(self.config["messages"])
            else:
                if function is not self.gif_flood:
                    text = random.choice(self.config["messages"]) + \
                        "\u206c\u206f".join(
                            random.sample(users_links, 15) if self.mention_mode == "users"
                            else random.sample(admin_links, len(admins) // 2)
                        )
                else:
                    text = random.choice(self.config["messages"]) + \
                        "\u206c\u206f".join(
                            random.sample(users_links, 5) if self.mention_mode == "users"
                            else random.sample(admin_links, len(admins) // 2)
                        )
 

            try:
                await function(session, msg, text)
            except Exception as err:
                console.print(
                    "[{name}] [bold red]not sended.[/] [bold white]{err}[/]"
                    .format(name=me.first_name, err=err)
                )
            else:
                count += 1
                console.print(
                    "[{name}] [bold green]sended.[/] COUNT: [yellow]{count}[/]"
                    .format(name=me.first_name, count=count)
                )
            finally:
                await asyncio.sleep(self.get_delay())

    def get_delay(self):
        if len(self.config["delay"]) == 1:
            return self.config["delay"][0]
        else:
            return random.randint(*self.config["delay"])

    def handle(self, session, function):
        @session.on(events.NewMessage)
        async def handler(msg):
            if msg.raw_text == self.config["trigger"]:
                await self.flood(session, msg, function)
                return

        if not self.storage.initialize:
            session.start()

        session.run_until_disconnected()

    def execute(self):
        for index, mode in enumerate(self.modes):
            console.print(
                "[bold white][{index}] {description}[/]"
                .format(index=index + 1, description=mode[0]),
            )

        choice = console.input(
            "[bold white]>> [/]"
        )

        while not choice.isdigit():
            choice = console.input(
                "[bold white]>> [/]"
            )

        else:
            choice = int(choice) - 1

        function = self.modes[choice][1]

        accounts_count = int(Prompt.ask(
            "[bold magenta]how many accounts to use? [/]",
            default=str(len(self.sessions))
        ))

        self.sessions = self.sessions[:accounts_count]

        self.mention_all = Confirm.ask("[bold red]mention all?[/]", default="y")

        if self.mention_all:
            self.mention_mode = Prompt.ask(
                "[bold red]mention mode[/]",
                choices=["admins", "users"]
            )

        processes = []

        for session in self.sessions:
            process = Process(
                target=self.handle, args=[session, function]
            )

            process.start()
            processes.append(process)

        console.print(
            "[bold white][*] Send «[green]{trigger}[/]» to chat[/]"
            .format(trigger=self.config["trigger"])
        )

        for process in processes:
            process.join()
