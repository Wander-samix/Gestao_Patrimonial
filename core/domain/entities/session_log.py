from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

@dataclass
class SessionLog:
    id: Optional[int]
    user_id: int
    session_key: str
    login_time: datetime
    logout_time: Optional[datetime]
    duration: Optional[timedelta]
    ip: Optional[str]
