from pydantic import BaseModel


class Message(BaseModel):
    greeting: str = "Добро пожаловать, {name}!"


msg = Message()
