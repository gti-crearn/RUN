from sqlalchemy import Column, Integer, String,DateTime, Boolean, ForeignKey, Date,Float
from sqlalchemy.orm import relationship
from .config import Base
from datetime import datetime, timezone, timedelta
import random
import string
import pytz


# Define o fuso horário de Brasília
brazil_tz = pytz.timezone('America/Recife')
# Tabela principal ART
def now_in_brazil():
    return datetime.now(brazil_tz)

class Profissional(Base):
    __tablename__ = 'tb_profissional'

    rnp = Column(String, primary_key=True, index=True)   
    cpf = Column(String, nullable=False, unique=True)
    tipo_registro = Column(String, nullable=False)
    data_registro = Column(DateTime(timezone=True), default=now_in_brazil)
    nome_profissional = Column(String, nullable=False)
    nome_mae = Column(String, nullable=True)
    nome_pai = Column(String, nullable=True)
    data_nascimento = Column(String, nullable=False)
    data_falecimento = Column(String, nullable=True)
    sexo = Column(String(1), nullable=False)
    estado_civil = Column(String(1), nullable=False)
    nacionalidade = Column(String, nullable=False)
    naturalidade = Column(String, nullable=False)   
    email = Column(String, nullable=False)
    rg = Column(String, nullable=False)
    orgao_expedidor = Column(String, nullable=False)
    data_expedicao = Column(String, nullable=False)
    # codigo_crea = Column(String(2), nullable=False)
    data_ativacao = Column(String, nullable=False) 
    num_registro_regional = Column(String, nullable=False)
    nome_social = Column(String, nullable=True)
    situacao_anuidade = Column(String, nullable=True)
    foto = Column(String, nullable=True)
    assinatura = Column(String, nullable=True)
    situacao_anuidade_fk = Column(Integer, ForeignKey('tb_situacao_registro.num'))
    codigo_crea_fk = Column(String(2), ForeignKey('tb_cod_crea.codigo'))
        
    titulos = relationship("Titulo", back_populates="profissional", cascade="all, delete-orphan")
    enderecos = relationship("Endereco", back_populates="profissional", cascade="all, delete-orphan")  
    arts = relationship("ART", back_populates="profissional", cascade="all, delete-orphan")
    vistos = relationship("Visto", back_populates="profissional", cascade="all, delete-orphan")
    # titulosPosGraduacao = relationship("TitulosPosGraduacao", back_populates="profissional", cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not hasattr(self, 'titulos'):
            self.titulos = []
        if not hasattr(self, 'enderecos'):
            self.enderecos = []
        if not hasattr(self, 'ART'):
            self.arts = []
        if not hasattr(self, 'Visto'):
            self.vistos = []
            
                        
class Titulo(Base):
    __tablename__ = 'tb_titulo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rnp = Column(String, ForeignKey('tb_profissional.rnp'), nullable=False)
    nome_titulo = Column(String, nullable=False)
    tipo_graduacao = Column(String, nullable=False)
    principal = Column(Boolean, default=False)
    # Relacionamento
    profissional = relationship("Profissional", back_populates="titulos")
    
    
class SiticaoRegistro(Base):
    __tablename__ = "tb_situacao_registro"

    num = Column(Integer, primary_key=True, index=True)   
    descricao = Column(String, index=True, unique=True)    

    # profissional = relationship("Profissional", back_populates="titulosPosGraduacao")


class Endereco(Base):
    __tablename__ = 'tb_endereco'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rnp = Column(String, ForeignKey('tb_profissional.rnp'))
    tipo_endereco = Column(String(1), nullable=False)
    logradouro = Column(String)   
    complemento = Column(String, nullable=True)
    numero = Column(String, nullable=False)
    bairro = Column(String, nullable=False)
    cidade = Column(String, nullable=False)
    uf = Column(String, nullable=False)
    cep = Column(String, nullable=False)
    # Relacionamento
    profissional = relationship("Profissional", back_populates="enderecos")
   

    
#Tabela para codigos Crea
class CodCrea(Base):
    __tablename__ = 'tb_cod_crea'

    codigo = Column(String, primary_key=True)
    crea_nome = Column(String(),  nullable=False)     

#Tabela vistos
class Visto(Base):
    __tablename__ = 'tb_profissional_visto'
    codigo_visto = Column(String, primary_key=True, index=True) 
    
    codigo_crea_fk = Column(String(2), ForeignKey('tb_cod_crea.codigo'))
    data_inicio =Column(DateTime(timezone=True), default=now_in_brazil) 

    rnp_profissional_fk = Column(String, ForeignKey('tb_profissional.rnp'))  
    profissional = relationship("Profissional", back_populates="vistos")


class NivelAtividade(Base):
    __tablename__ = "nivel_atividade"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, index=True, unique=True)
    descricao = Column(String, index=True, unique=True)
    # Relacionamentos
    atividades_pivot = relationship("AtividadePivot", back_populates="nivel_atividade")
    
class AtividadeProfissional(Base):
    __tablename__ = "atividade_profissional"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, index=True, unique=True)
    descricao = Column(String, index=True, unique=True)
    # Relacionamentos
    atividades_pivot = relationship("AtividadePivot", back_populates="atividade_profissional")

class Atividade(Base):
    __tablename__ = "atividade"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, index=True, unique=True)
    descricao = Column(String, index=True, unique=True)

    # Relacionamentos
    atividades_pivot = relationship("AtividadePivot", back_populates="atividade")


class AtividadePivot(Base):
    __tablename__ = "atividade_pivot"

    id = Column(Integer, primary_key=True, index=True)
    nivel_atividade_id = Column(Integer, ForeignKey("nivel_atividade.id"))
    atividade_profissional_id = Column(Integer, ForeignKey("atividade_profissional.id"))
    atividade_id = Column(Integer, ForeignKey("atividade.id"))
    art_id = Column(Integer)

    # Relacionamentos
    nivel_atividade = relationship("NivelAtividade", back_populates="atividades_pivot")
    atividade_profissional = relationship("AtividadeProfissional", back_populates="atividades_pivot")
    atividade = relationship("Atividade", back_populates="atividades_pivot")
    


class ART(Base):
    __tablename__ = "arts"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String(20), nullable=False)
    data_cadastro= Column(DateTime(timezone=True), default=now_in_brazil)
    codigo_crea_fk = Column(String(2), ForeignKey('tb_cod_crea.codigo'))
    rnp = Column(String, ForeignKey('tb_profissional.rnp'), nullable=False)
    modelo = Column(String, index=True)
    forma_registro = Column(String, index=True)
    tipo_participacao = Column(String, index=True)
    finalidade = Column(String, index=True)
    observacao = Column(String)
    acao_institucional = Column(String, index=True)
    nome_contratante = Column(String, index=True)
    nome_proprietario = Column(String, index=True)
    numero_contrato = Column(String, index=True,  nullable=True, default=None)
    codigo_obra_publica = Column(String, index=True, nullable=True, default=None)
    data_celebracao_contrato = Column(Date)
    data_inicio_obra = Column(Date)
    data_previsao_termino = Column(Date)
    valor_obra = Column(Float)
    endereco_contratante = Column(String)
    endereco_proprietario = Column(String)
    endereco_obra = Column(String)
    concorda_acessibilidade =Column(Boolean, default=False)
    clausula_compromissoria = Column(Boolean, default=False)
    atividades_responsabilidade = Column(Boolean, default=False)
    
    profissional = relationship('Profissional', back_populates='arts')
   
 