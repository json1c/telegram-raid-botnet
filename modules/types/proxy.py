from dataclasses import dataclass


@dataclass
class Proxy:
    socks: int
    proxy_ip: str
    port: int
    proxy_login: str
    proxy_pass: str
