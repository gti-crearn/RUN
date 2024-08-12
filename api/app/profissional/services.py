import os
import random
import datetime
from dotenv import load_dotenv
from app.profissional import schemas
from database import models
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

load_dotenv()

class ProfissionalServices:    
    def __init__(self, db: Session):
        self.db = db
    
    def gerar_rnp_aleatorio(self, cod_crea_regional: str) -> str:
        ano_atual = datetime.datetime.now().year
        codigo_aleatorio = f"{random.randint(0, 99999):05d}"
        return f"{cod_crea_regional}{ano_atual}{codigo_aleatorio}"

    def criar_profissional(self, profissional: schemas.CriarProfissional):
        try:
            crea_codigo = self.db.query(models.CodCrea).filter(
                models.CodCrea.codigo == profissional.codigo_crea_fk
            ).first()
            # Se o RNP não for fornecido, gerar um novo
            if not profissional.rnp:
                profissional.rnp = self.gerar_rnp_aleatorio(crea_codigo.crea_nome)

            # Verificar se já existe um profissional com o mesmo rnp
            db_profissional_rnp = self.db.query(models.Profissional).filter(
                models.Profissional.rnp == profissional.rnp
            ).first()
            if db_profissional_rnp:
                raise HTTPException(status_code=409, detail="Profissional já existe com o mesmo RNP")

            # Verificar se já existe um profissional com o mesmo cpf
            db_profissional_cpf = self.db.query(models.Profissional).filter(
                models.Profissional.cpf == profissional.cpf
            ).first()
            if db_profissional_cpf:
                raise HTTPException(status_code=409, detail="Profissional já existe com o mesmo CPF")

            # Verificar se já existe um profissional com o mesmo email
            db_profissional_email = self.db.query(models.Profissional).filter(
                models.Profissional.email == profissional.email
            ).first()
            if db_profissional_email:
                raise HTTPException(status_code=409, detail="Profissional já existe com o mesmo email")

            # Criar o objeto Profissional
            db_profissional = models.Profissional(
                rnp=profissional.rnp,
                cpf=profissional.cpf,
                tipo_registro=profissional.tipo_registro,
                nome_profissional=profissional.nome_profissional,
                data_nascimento=profissional.data_nascimento,
                sexo=profissional.sexo,
                estado_civil=profissional.estado_civil,
                nacionalidade=profissional.nacionalidade,
                naturalidade=profissional.naturalidade,
                email=profissional.email,
                rg=profissional.rg,
                orgao_expedidor=profissional.orgao_expedidor,
                data_expedicao=profissional.data_expedicao,
                codigo_crea_fk=profissional.codigo_crea_fk,
                data_ativacao=profissional.data_ativacao,
                num_registro_regional=profissional.num_registro_regional,
                nome_mae=profissional.nome_mae,
                nome_pai=profissional.nome_pai,
                data_falecimento=profissional.data_falecimento,
                nome_social=profissional.nome_social,
                situacao_anuidade=profissional.situacao_anuidade,
                foto=profissional.foto,
                assinatura=profissional.assinatura,
                situacao_anuidade_fk=profissional.situacao_anuidade_fk
            )
            
            # Adicionar o profissional ao banco de dados
            self.db.add(db_profissional)
            self.db.commit()
            self.db.refresh(db_profissional)
            
            # Verificar se há endereços para adicionar
            if profissional.enderecos:
                for endereco in profissional.enderecos:
                    db_endereco = models.Endereco(
                        rnp=profissional.rnp,
                        tipo_endereco=endereco.tipo_endereco, 
                        logradouro=endereco.logradouro,
                        complemento=endereco.complemento,
                        numero=endereco.numero,
                        bairro=endereco.bairro,
                        cidade=endereco.cidade,
                        uf=endereco.uf,
                        cep=endereco.cep
                    )
                    self.db.add(db_endereco)
            
            # Verificar se há títulos para adicionar
            if profissional.titulos:
                for titulo in profissional.titulos:
                    db_titulo = models.Titulo(
                        rnp=profissional.rnp,
                        nome_titulo=titulo.nome_titulo,
                        tipo_graduacao=titulo.tipo_graduacao,
                        principal=titulo.principal
                    )
                    self.db.add(db_titulo)
            
            # Finalizar transação
            self.db.commit()
            return db_profissional
        
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro ao criar profissional: {e}")
        
    def listar_profissional(self, rnp: str):
        try:
            # Buscar o profissional e os relacionados
            db_profissional = self.db.query(models.Profissional).filter(models.Profissional.rnp == rnp).first()
            if not db_profissional:
                raise HTTPException(status_code=404, detail="Profissional não encontrado")

            titulos = self.db.query(models.Titulo).filter(models.Titulo.rnp == rnp).all()
            enderecos = self.db.query(models.Endereco).filter(models.Endereco.rnp == rnp).all()
            # titulos_pos_graduacao = self.db.query(models.TitulosPosGraduacao).filter(models.TitulosPosGraduacao.rnp == rnp).all()
            arts = self.db.query(models.ART).filter(models.ART.rnp == rnp).all()
            vistos = self.db.query(models.Visto).filter(models.Visto.rnp_profissional_fk == rnp).all()
            art_responses = []
            for art in arts:
                atividades = self.db.query(models.AtividadePivot).filter(models.AtividadePivot.art_id == art.id).all()
                atividade_pivot_responses = []

                for ap in atividades:
                    nivel_atividade = self.db.query(models.NivelAtividade).filter(models.NivelAtividade.id == ap.nivel_atividade_id).first()
                    atividade_profissional = self.db.query(models.AtividadeProfissional).filter(models.AtividadeProfissional.id == ap.atividade_profissional_id).first()
                    atividade = self.db.query(models.Atividade).filter(models.Atividade.id == ap.atividade_id).first()

                    atividade_pivot_detail = schemas.AtividadePivotDetail(
                        nivel_atividade_descricao=nivel_atividade.descricao if nivel_atividade else None,
                        atividade_profissional_descricao=atividade_profissional.descricao if atividade_profissional else None,
                        atividade_descricao=atividade.descricao if atividade else None
                    )

                    atividade_pivot_responses.append(atividade_pivot_detail)

                art_response = schemas.ARTResponse.from_orm(art)
                art_response.atividades = atividade_pivot_responses
                art_responses.append(art_response)

            # Conversão manual para dicionário
            def obj_to_dict(obj):
                return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

            return {
                "profissional": obj_to_dict(db_profissional),
                "titulos": [obj_to_dict(titulo) for titulo in titulos],
                "enderecos": [obj_to_dict(endereco) for endereco in enderecos],
                # "titulosPosGraduacao": [obj_to_dict(titulo_pos_graduacao) for titulo_pos_graduacao in titulos_pos_graduacao],
                "arts": art_responses,  # Inclui as ARTs com atividades relacionadas
                "vistos": vistos  # Inclui as ARTs com atividades relacionadas
            }
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Erro ao listar profissional: {e}")

    #Gerar numero da Art
    def gerar_codigo(self, cod_crea_regional: str) -> str:
        ano_atual = datetime.datetime.now().year
        codigo_aleatorio = f"{random.randint(0, 99999):05d}"
        return f"{cod_crea_regional}{ano_atual}{codigo_aleatorio}"
    #Visto
    def criar_visto(self, visto:schemas.VistoCreate):
        try:
            profissional = self.db.query(models.Profissional).filter(models.Profissional.rnp == visto.rnp_profissional_fk).first()
            if not profissional:
                return {"detail": f"Profissional com RNP {visto.rnp_profissional_fk} não encontrado."}

            crea_codigo = self.db.query(models.CodCrea).filter(
                models.CodCrea.codigo == visto.codigo_crea_fk
            ).first()

            numero_visto = self.gerar_codigo(crea_codigo.crea_nome)
            
            novo_visto = models.Visto(
                codigo_visto=numero_visto,
                codigo_crea_fk=visto.codigo_crea_fk,
                rnp_profissional_fk=visto.rnp_profissional_fk
            )

            self.db.add(novo_visto)
            self.db.commit()
            self.db.refresh(novo_visto)

            return novo_visto

        except SQLAlchemyError as e:
            self.db.rollback()
            return {"detail": f"Erro ao criar visto: {str(e)}"}
                    
        
        
    