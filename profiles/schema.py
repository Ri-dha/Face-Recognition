from ninja import Schema


class ProfileIn(Schema):
    id_number: int = None
    username: str = None
    name: str = None
    profile_password: str = None

    refresh_token: str = None
    profile_email: str = None


class ProfileOut(Schema):
    id: int
    name: str = None
    id_number: int = None
    refresh_token: str = None
    profile_password: str = None
    profile_email: str = None


class UpdateRefreshToken(Schema):
    refresh_token: str = None


class UpdatePassword(Schema):
    profile_password: str = None
