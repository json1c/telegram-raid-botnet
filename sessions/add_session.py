import sys

sys.path.append("..")

import asyncio
import random

from telethon import TelegramClient

from modules.generators.linux import LinuxAPI
from modules.generators.telegram_android import TelegramAppAPI
from modules.types.json_session import JsonSession


print("[1] - Telegram Android")
print("[2] - Telegram Desktop (Linux)")
print("[3] - Random")

choice = input(">> ")

if choice == "1":
    generator = TelegramAppAPI

if choice == "2":
    generator = LinuxAPI

if choice == "3":
    generator = None


asyncio.run(
    JsonSession().create_application_session(generator)
)

