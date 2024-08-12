# schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from datetime import datetime

from pydantic import BaseModel

 #art
    # Schema para Nível Atividade
class NivelAtividadeBase(BaseModel):
    codigo: str
    descricao: str

class NivelAtividadeCreate(NivelAtividadeBase):
    pass

class NivelAtividadeResponse(NivelAtividadeBase):
    id: int

    class Config:
        orm_mode = True

# Schema para Atividade Profissional
class AtividadeProfissionalBase(BaseModel):
    codigo: str
    descricao: str

class AtividadeProfissionalCreate(AtividadeProfissionalBase):
    pass

class AtividadeProfissionalResponse(AtividadeProfissionalBase):
    id: int

    class Config:
        orm_mode = True

# Schema para Atividade
class AtividadeBase(BaseModel):
    codigo: str
    descricao: str

class AtividadeCreate(AtividadeBase):
    pass

class AtividadeResponse(AtividadeBase):
    id: int

    class Config:
        orm_mode = True

# Schema para Atividade Pivot
class AtividadePivotBase(BaseModel):
    nivel_atividade_id: int
    atividade_profissional_id: int
    atividade_id: int
    art_id: int

class AtividadePivotCreate(BaseModel):
    nivel_atividade_id: int
    atividade_profissional_id: int
    atividade_id: int    


class AtividadePivotResponse(BaseModel):
    id: int
    nivel_atividade_descricao: Optional[str] = None  
    atividade_profissional_descricao: Optional[str] = None  
    atividade_descricao: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True
        
class AtividadePivotListResponse(BaseModel):
    pivots: List[AtividadePivotResponse]
    
    

# Schema para ART
class ARTBase(BaseModel):
    modelo: str
    forma_registro: str   
    rnp:str
    codigo_crea_fk: str
    tipo_participacao: str
    finalidade: str
    observacao: Optional[str]
    acao_institucional: str
    nome_contratante: str
    nome_proprietario: str
    numero_contrato: Optional[str] = ""
    codigo_obra_publica:Optional[str] = ""
    data_celebracao_contrato: date
    data_inicio_obra: date
    data_previsao_termino: date
    valor_obra: float
    endereco_contratante: str
    endereco_proprietario: str
    endereco_obra: str
    concorda_acessibilidade: Optional[bool] = False
    clausula_compromissoria: Optional[bool] = False
    atividades_responsabilidade: Optional[bool] = False
    atividades: List[AtividadePivotCreate]
    
    class Config:
        orm_mode = True
        from_attributes = True


class ARTResponse(ARTBase):
    id: int
    rnp:str
    data_cadastro: Optional[datetime]
    atividades: List[AtividadePivotResponse] = []

    class Config:
        orm_mode = True
        from_attributes = True

class ARTCreateResponse(ARTBase):
    id: int
    numero:str
    codigo_crea_fk:str
    data_cadastro: Optional[datetime]
    atividades: List[AtividadePivotBase]

    class Config:
        orm_mode = True
        from_attributes = True
