import random
from abc import ABC, abstractmethod


class Application(ABC):
    api_id: int
    api_hash: str
    
    lang_pack: str
    
    def system_lang_code():
        return random.choice(["zh-hans", "cn", "en", "ru", "af", "sq", "cs", "pl"])
    
    @abstractmethod
    def app_version() -> str:
        raise NotImplementedError()

    @abstractmethod
    def device() -> str:
        raise NotImplementedError()
    
    @abstractmethod
    def sdk() -> str:
        raise NotImplementedError()
