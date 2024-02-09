"""
Message Module for BaseModels
-----------------------------
"""
from pydantic import BaseModel


class MessageFromClient(BaseModel):
    """
    Basemodel for Messages from the Client
    """
    username: str
    message: str
    language: str
    timestamp: str


class MessageToClient(BaseModel):
    """
    Basemodel for Messages to the Client
    """
    username: str
    message: str
    language: str
    timestamp: str
    sentiment: float