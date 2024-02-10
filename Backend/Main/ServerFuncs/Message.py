"""
Message Module for BaseModels
-----------------------------
"""
from pydantic import BaseModel


class MessageFromClient(BaseModel):
    """
    Basemodel for Messages from the Client\n
    """
    username: str
    message: str
    language: str
    timestamp: str


class MessageToClient(BaseModel):
    """
    Basemodel for Messages to the Client\n
    """
    username: str
    message: str
    language: str
    timestamp: str
    sentiment: float
    orgmessage: str | None = None
    detectedlang: str | None = None
