import json
import sys

sys.path.append("..")

from telethon import events
from telethon.sessions.string import StringSession
from telethon.sync import TelegramClient

from modules.types.json_session import JsonSession

if len(sys.argv) != 2:
    print("Usage: python login.py <session_file>")
    sys.exit(1)

name = sys.argv[1]

with open(name) as fileobj:
    session_settings = json.load(fileobj)

session = JsonSession(dict_settings=session_settings)

client = TelegramClient(
    session=StringSession(session.account.auth_key),
    api_id=session.account.application.api_id,
    api_hash=session.account.application.api_hash,
    device_model=session.account.application.device_name,
    app_version=session.account.application.app_version,
    system_version=session.account.application.sdk,
    lang_code=session.account.application.system_lang_code,
    system_lang_code=session.account.application.system_lang_code,
    proxy=session.account.proxy.as_telethon()
    if session.account.proxy else None,
)

with client:
    print("Mobile phone:", client.get_me().phone)


@client.on(events.NewMessage)
async def handler(msg):
    if msg.from_id.user_id == 777000:
        print(msg.text)

client.start()
client.run_until_disconnected()
