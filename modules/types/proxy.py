from dataclasses import dataclass, field


@dataclass
class Proxy:
    proxy_type: str  # socks4, socks5, http
    ip: str
    port: int
    user: str
    password: str

    def __init__(
        self,
        proxy_type: str,
        ip: str,
        port: int,
        user: str = None,
        password: str = None,
    ):
        self.proxy_type = proxy_type
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password

    def as_telethon(self) -> tuple:
        if self.user and self.password:
            return (
                self.proxy_type,
                self.ip,
                self.port,
                False,
                self.user,
                self.password,
            )

        return (self.proxy_type, self.ip, self.port)
