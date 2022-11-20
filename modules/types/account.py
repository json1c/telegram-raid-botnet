from dataclasses import dataclass
from datetime import datetime


@dataclass
class Account:
    first_name: str
    last_name: str
    user_id: int
    added_at: datetime
    phone_number: str

