# https://github.com/json1c
# Copyright (C) 2023  json1c

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.


import os
import sys
import toml
from rich.console import Console
from typing import List, Tuple

console = Console()


class Settings:
    def __init__(self):
        if not os.path.exists("config.toml"):
            self.initial_setup()
            sys.exit()

        with open("config.toml") as file:
            config = toml.load(file)

        self.api_id: int = config["sessions"]["api_id"]
        self.api_hash: str = config["sessions"]["api_hash"]
        self.messages: List[str] = config["flood"]["messages"]
        self.messages_count: int = config["flood"]["messages_count"]
        self.trigger: str = config["flood"]["trigger"]
        self.delay: List[int] = config["flood"]["delay"]

    def save(
        self,
        api_id: int,
        api_hash: str,
        messages: List[str],
        delay: List[int],
        messages_count: int,
        trigger: str
    ):
        config = dict(
            sessions=dict(
                api_hash=api_hash,
                api_id=api_id
            ),
            flood=dict(
                messages=messages,
                delay=delay,
                messages_count=messages_count,
                trigger=trigger
            )
        )

        with open("config.toml", "w") as file:
            toml.dump(config, file)

    def initial_setup(self):
        console.print(
            "[bold yellow]Initial setup[/]",
            justify="center"
        )

        print()

        console.print(
            "[bold blue]Sessions[/]",
            justify="center"
        )

        print()
        api_id, api_hash = self.setup_sessions()

        console.print(
            "[bold blue]Flood[/]",
            justify="center"
        )

        print()
        messages, delay, trigger = self.setup_flood()

        self.save(
            api_id,
            api_hash,
            messages,
            delay,
            0,
            trigger
        )

    def setup_sessions(self) -> Tuple[int, str]:
        api_id = console.input("[bold white]Enter API ID: [/]")
        api_hash = console.input("[bold white]Enter API hash: [/]")

        return int(api_id), api_hash

    def setup_flood(self) -> Tuple[List[str], List[int], str]:
        console.print("[bold white]Enter messages[/]")

        messages = []

        while message := console.input("[bold white]>> [/]"):
            messages.append(message)

        print()

        delay = console.input("[bold white]Flooding delay (e.g. 1-3): [/]")
        delay = delay.split("-")
        delay = [int(x) for x in delay]

        trigger = console.input("[bold white]Enter the text after which bots will start flooding: [/]")

        return messages, delay, trigger


