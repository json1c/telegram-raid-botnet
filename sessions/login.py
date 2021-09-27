import sys
import toml
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon import events

name = sys.argv[1]
with open("../config.toml") as file:
    config = toml.load(file)["sessions"]

api_id = config["api_id"]
api_hash = config["api_hash"]

with open(name) as file:
    auth_key = file.read()

client = TelegramClient(StringSession(auth_key), api_id, api_hash)

with client:
    print("Mobile phone:", client.get_me().phone)


@client.on(events.NewMessage)
async def handler(msg):
    if msg.from_id.user_id == 777000:
        print(msg.text)

client.start()
client.run_until_disconnected()
