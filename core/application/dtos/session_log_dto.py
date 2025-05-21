from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

@dataclass
class CreateSessionLogDTO:
    user_id:      int
    session_key:  str
    login_time:   datetime
    logout_time:  Optional[datetime] = None
    duration:     Optional[timedelta] = None
    ip:           Optional[str] = None

@dataclass
class SessionLogDTO:
    id:           int
    user_id:      int
    session_key:  str
    login_time:   str   # ISO datetime
    logout_time:  Optional[str]
    duration:     Optional[float]  # segundos
    ip:           Optional[str]
