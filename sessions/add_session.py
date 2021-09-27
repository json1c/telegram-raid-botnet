import sys
import toml
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

name = sys.argv[1]
with open("../config.toml") as file:
    config = toml.load(file)["sessions"]

api_id = config["api_id"]
api_hash = config["api_hash"]

with TelegramClient(StringSession(), api_id, api_hash) as client:
    with open(f"{name}.session", "w") as file:
        file.write(client.session.save())
