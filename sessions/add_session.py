import string
import random
import toml
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

with open("../config.toml") as file:
    config = toml.load(file)["sessions"]

api_id = config["api_id"]
api_hash = config["api_hash"]

name = "".join(random.choices(string.ascii_letters, k=10))

with TelegramClient(
    StringSession(),
    api_id,
    api_hash,
    device_model="Redmi Note 10",
    lang_code="en",
    system_lang_code="en"
) as client:
    with open(f"{name}.session", "w") as file:
        file.write(client.session.save())
