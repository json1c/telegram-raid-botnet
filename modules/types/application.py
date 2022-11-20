from dataclasses import dataclass


@dataclass
class Application:
    api_id: int
    api_hash: str
    
    device_name: str
    app_version: str | int
    sdk: str
    lang_pack: str
    system_lang_code: str
