from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime


class UserRole(str, Enum):
    FOUNDER = "FOUNDER"
    INVESTOR = "INVESTOR"


class StatusEnum(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class IncomingConnectionRequest(BaseModel):
    id: int
    sender_id: int
    sender_role: str
    message: Optional[str]
    status: str
    created_at: datetime


class ConnectionRequestCreate(BaseModel):
    sender_id: int
    sender_role: UserRole
    receiver_id: int
    receiver_role: UserRole
    message: Optional[str] = None


class Connection(BaseModel):
    id: int
    user_a_id: int
    user_a_role: UserRole
    user_b_id: int
    user_b_role: UserRole
    connection_request_id: Optional[int]
    created_at: datetime
