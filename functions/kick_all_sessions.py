import asyncio

from rich.progress import track
from rich.console import Console

from telethon.tl.functions.account import GetAuthorizationsRequest, ResetAuthorizationRequest
from telethon import TelegramClient

from functions.base import TelethonFunction

console = Console()


class KickAllSessionsFunc(TelethonFunction):
    """Kick all users from sessions"""
    
    async def kick_all_sessions(self, session: TelegramClient):
        async with self.storage.ainitialize_session(session):
            try:
                authorizations = await session(GetAuthorizationsRequest())
            except Exception as error:
                console.print(f"Error while getting authorizations : {error}")
                return
            
            for authorization in authorizations.authorizations:
                if authorization.hash != 0:
                    try:
                        await session(ResetAuthorizationRequest(hash=authorization.hash))
                    except Exception as error:
                        console.print(f"Error : {error}")
                    else:
                        console.print(f"Resetted authorization {authorization.ip} ({authorization.device_model}, {authorization.platform})")

    async def execute(self):
        await asyncio.gather(*[
            self.kick_all_sessions(session)
            for session in track(self.sessions, "Kicking...")
        ])
