# This programm protected by GNU General Public License.
# If you bought this program, then you were deceived.
# https://github.com/json1c/telegram-raid-botnet

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
