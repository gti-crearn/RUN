from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from app.art.schemas import ARTResponse

class TituloBase(BaseModel):
    #rnp: str
    nome_titulo: str
    tipo_graduacao: str
    principal: Optional[bool] = False

class EnderecoBase(BaseModel):
    #rnp: str
    tipo_endereco: str
    logradouro: str
    complemento: Optional[str] = None
    numero: str
    bairro: str
    cidade: str
    uf: str
    cep: str



class AtividadePivotDetail(BaseModel):
    nivel_atividade_descricao: Optional[str] = None
    atividade_profissional_descricao: Optional[str] = None
    atividade_descricao: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True

class AtividadePivotDetail(BaseModel):
    nivel_atividade_descricao: Optional[str] = None
    atividade_profissional_descricao: Optional[str] = None
    atividade_descricao: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True

    
class VistoBase(BaseModel):
    #codigo_visto: str = Field(..., title="Código do Visto", description="Código único do visto.")
    codigo_crea_fk: str = Field(..., title="Código Regional", description="Código regional do visto.")
    rnp_profissional_fk: str = Field(..., title="RNP do Profissional", description="RNP do profissional associado ao visto.")

class VistoResponse(VistoBase):
    codigo_visto: str = Field(..., title="Código do Visto", description="Código único do visto.")
    data_inicio: date
    pass

class VistoCreate(VistoBase):

    pass
class CriarProfissional(BaseModel):
    rnp: Optional[str] = None
    cpf: str
    tipo_registro: str
    nome_profissional: str
    data_nascimento: str
    sexo: str
    estado_civil: str
    nacionalidade: str
    naturalidade: str
    email: str
    rg: str
    orgao_expedidor: str
    data_expedicao: str
    codigo_crea_fk: str
    data_ativacao: str
    num_registro_regional: str
    nome_mae: Optional[str] = None
    nome_pai: Optional[str] = None
    data_falecimento: Optional[str] = None
    nome_social: Optional[str] = None
    situacao_anuidade: Optional[str] = None
    foto: Optional[str] = None
    assinatura: Optional[str] = None
    situacao_anuidade_fk: Optional[int] = None
    titulos: Optional[List[TituloBase]] = Field(None, description="Lista de títulos")
    enderecos: Optional[List[EnderecoBase]] = Field(None, description="Lista de endereços")
    # arts: Optional[List[ARTResponse]] = Field(None, description="Lista de arts")
 
 
class ProfissionalResponse(BaseModel):
    id: int
    rnp: str
    arts: List[ARTResponse]
    vistos: List[VistoResponse]



    