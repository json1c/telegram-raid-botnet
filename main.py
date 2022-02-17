# https://github.com/json1c
# Copyright (C) 2021  json1c

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

import sys
from rich.console import Console
from modules.settings import Settings
from modules.sessions_storage import SessionsStorage
from modules.functions_storage import FunctionsStorage

console = Console()

console.print("""
[bold magenta]Copyright (C) 2021  https://github.com/json1c/telegeram-raid-botnet
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it under certain conditions.[/]
""")

console.print("Author's channel: https://t.me/huis_bn")

if sys.version_info < (3, 8, 0):
    console.print("\n[red]Error: you using an outdated Python version. Install Python 3.8.0 at least.")
else:
    if sys.platform == "win32":
        console.print("[yellow]Warning: you using an untested platform. Some features may not work properly\n")

    settings = Settings()

    sessions_storage = SessionsStorage(
        "sessions",
        settings.api_id,
        settings.api_hash
    )

    functions_storage = FunctionsStorage(
        "functions",
        sessions_storage,
        settings
    )

    console.print("[bold white]accounts count> %d[/]" % len(sessions_storage))

    for index, module in enumerate(functions_storage.functions):
        instance, doc = module

        console.print(
            "[bold white][{index}] {doc}[/]"
            .format(index=index + 1, doc=doc)
        )

    while True:
        console.print()

        try:
            choice = console.input(
                "[bold white]>> [/]"
            )

            while not choice.isdigit():
                choice = console.input(
                    "[bold white]>> [/]"
                )
        except KeyboardInterrupt:
            console.print("[bold white]Bye![/]")
            break

        else:
            choice = int(choice) - 1

        try:
            functions_storage.execute(choice)
        except KeyboardInterrupt:
            pass

