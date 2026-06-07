from typing import Dict, List, Optional
from pydantic import Field
import uuid
from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    language: Optional[str] = None
    chats: Optional[List[Dict[str, str]]] = Field(default_factory=list)


class UserCreate(schemas.BaseUserCreate):
    language: Optional[str] = None
    chats: Optional[List[Dict[str, str]]] = Field(default_factory=list)


class UserUpdate(schemas.BaseUserUpdate):
    language: Optional[str] = None
    chats: Optional[List[Dict[str, str]]] = Field(default_factory=list)