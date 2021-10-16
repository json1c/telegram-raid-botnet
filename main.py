# https://github.com/json1c
# Copyright (C) 2021  json1c

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

import toml
from rich.console import Console
from modules.sessions_storage import SessionsStorage
from modules.functions_storage import FunctionsStorage

console = Console()

with open("config.toml") as file:
    config = toml.load(file)["sessions"]

api_id = config["api_id"]
api_hash = config["api_hash"]

sessions_storage = SessionsStorage("sessions", api_id, api_hash)
functions_storage = FunctionsStorage("functions", sessions_storage)

console.print("""
[bold magenta]This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it under certain conditions.[/]
""")

console.print("[bold white]accounts count> %d[/]" % len(sessions_storage))

for index, module in enumerate(functions_storage.functions):
    instance, doc = module

    console.print(
        "[bold white][{index}] {doc}[/]"
        .format(index=index + 1, doc=doc)
    )

else:
    console.print()

    choice = console.input(
        "[bold white]>> [/]"
    )

    while not choice.isdigit():
        choice = console.input(
            "[bold white]>> [/]"
        )

    else:
        choice = int(choice) - 1

    functions_storage.execute(choice)
