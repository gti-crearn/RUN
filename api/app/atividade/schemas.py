# schemas.py
from pydantic import BaseModel

class AtividadeResponse(BaseModel):
    id: int
    codigo: str
    descricao: str

    class Config:
        orm_mode = True

class AtividadeProfisionalResponse(BaseModel):
    id: int
    codigo: str
    descricao: str

    class Config:
        orm_mode = True

