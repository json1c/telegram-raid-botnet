# This programm protected by GNU General Public License.
# If you bought this program, then you were deceived.
# https://github.com/json1c/telegram-raid-botnet

import random
import toml
import asyncio
from rich.console import Console

console = Console()


class CommentsFloodFunc:
    """Flood to a channel comments"""

    def __init__(self, storage):
        self.storage = storage
        self.sessions = storage.sessions

        with open("config.toml") as f:
            self.config = toml.load(f)["flood"]

    def get_delay(self):
        if len(self.config["delay"]) == 1:
            return self.config["delay"][0]
        else:
            return random.randint(*self.config["delay"])

    async def flood(self, session, channel, post_id):
        if self.config["messages_count"] == 0:
            self.config["messages_count"] = 900000000

        await session.connect()
        me = await session.get_me()
        count = 0

        for _ in range(self.config["messages_count"]):
            text = random.choice(self.config["messages"])

            while True:
                try:
                    await session.send_message(
                        channel,
                        text,
                        comment_to=int(post_id),
                        parse_mode="html"
                    )
                except Exception as err:
                    console.print(
                        "[{name}] [bold red]not sended.[/] {err}"
                        .format(name=me.first_name, err=err)
                    )
                else:
                    count += 1
                    console.print(
                        "[{name}] [bold green]sended.[/] COUNT: [yellow]{count}[/]"
                        .format(name=me.first_name, count=count)
                    )
                finally:
                    await asyncio.sleep(
                        self.get_delay()
                    )

    async def execute(self):
        link = console.input("[bold red]link to post> [/]")

        channel = "/" .join(link.split("/")[:-1])
        post_id = link.split("/")[-1]

        await asyncio.wait([
            self.flood(session, channel, post_id)
            for session in self.sessions
        ])
