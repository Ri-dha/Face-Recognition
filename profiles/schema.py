from ninja import Schema



class ProfileIn(Schema):
    id_number: int = None
    name: str = None



class ProfileOut(Schema):
    id: int
    name: str = None
    id_number: int = None

