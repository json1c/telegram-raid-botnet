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
import importlib.util
import inspect
import os

from typing import List, Callable, Awaitable, Union

from .sessions_storage import SessionsStorage
from .settings import Settings

class FunctionsStorage:
    def __init__(
        self,
        directory: str,
        sessions_storage: SessionsStorage,
        settings: Settings
    ):
        self.storage = sessions_storage
        self.settings = settings

        self.functions: List[Union[Callable, Awaitable]] = []

        for file in os.listdir(directory):
            if file.endswith(".py"):
                self.load_function(
                    file[:-3], os.path.join(directory, file)
                )

        self.functions.sort(key=lambda item: item[1].lower())

    def load_function(self, name: str, path: str):
        spec = importlib.util.spec_from_file_location(name, path)
        function = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(function)

        self.register_function(function)

    def register_function(self, module):
        for classname, classobj in inspect.getmembers(module, inspect.isclass):
            if classname.endswith("Func"):
                self.functions.append((
                    classobj(self.storage, self.settings),
                    classobj.__doc__
                ))

    def execute(self, index: int):
        try:
            function_instance = self.functions[index][0]
        except Exception:
            return

        function = function_instance.execute()

        if inspect.isawaitable(function):
            asyncio.get_event_loop().run_until_complete(function)
