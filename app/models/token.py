from sqlmodel import SQLModel


class Token(SQLModel):
    token_type: str


class AccessToken(Token):
    access: str

    def __str__(self):
        return self.access_token


class RefreshToken(Token):
    refresh: str

    def __str__(self):
        return self.refresh_token


class TokenPair(AccessToken, RefreshToken):
    def __init__(self, access_token: str, refresh_token: str):
        self.access = access_token
        self.refresh = refresh_token
    