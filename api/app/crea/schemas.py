# schemas.py
from pydantic import BaseModel

class CodCrea(BaseModel):
    id: int
    codigo: str
    crea_nome: str

    class Config:
        orm_mode = True

