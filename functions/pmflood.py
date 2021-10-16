# This programm protected by GNU General Public License.
# If you bought this program, then you were deceived.
# https://github.com/json1c/telegram-raid-botnet

import asyncio
from rich.console import Console

console = Console()


class PmFloodFunc:
    """Flood to PM"""

    def __init__(self, storage):
        self.storage = storage
        self.sessions = storage.sessions

    async def flood(self, session, peer, text, delay):
        count = 0

        async with self.storage.ainitialize_session(session):
            me = await session.get_me()

            while True:
                try:
                    await session.send_message(peer, text)
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
                    await asyncio.sleep(delay)

    async def execute(self):
        peer = console.input("[bold red]enter uid or username> [/]")
        text = console.input("[bold red]text> [/]")

        delay = float(
            console.input("[bold red]delay> [/]")
        )

        await asyncio.wait([
            self.flood(session, peer, text, delay)
            for session in self.sessions
        ])
