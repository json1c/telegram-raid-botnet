# This programm protected by GNU General Public License.
# If you bought this program, then you were deceived.
# https://github.com/json1c/telegram-raid-botnet

import asyncio
import importlib.util
import inspect
import os


class FunctionsStorage:
    def __init__(self, directory: str, sessions_storage):
        self.sessions = sessions_storage
        self.functions = []

        for file in os.listdir(directory):
            if file.endswith(".py"):
                self.load_function(
                    file[:-3], os.path.join(directory, file)
                )

    def load_function(self, name: str, path: str):
        spec = importlib.util.spec_from_file_location(name, path)
        function = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(function)

        self.register_function(function)

    def register_function(self, module):
        for classname, classobj in inspect.getmembers(module, inspect.isclass):
            if classname.endswith("Func"):
                self.functions.append((
                    classobj(self.sessions),
                    classobj.__doc__
                ))

    def execute(self, index: int):
        function_instance = self.functions[index][0]
        function = function_instance.execute()

        if inspect.isawaitable(function):
            asyncio.get_event_loop().run_until_complete(function)
