from sqlmodel import SQLModel


class Token(SQLModel): ...


class AccessToken(Token):
    access: str


class RefreshToken(Token):
    refresh: str


class TokenPair(AccessToken, RefreshToken): ...
