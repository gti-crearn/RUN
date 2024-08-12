import os
import random
import datetime
from dotenv import load_dotenv
from app.art import schemas
from database import models
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List



load_dotenv()

tokenAcesso = os.getenv('KEY_CONFEA')

class ArtServices:
    def __init__(self, db: Session):
        self.db = db

    # Outros métodos...

    #Gerar numero da Art
    def gerar_numero_art(self, cod_crea_regional: str) -> str:
        ano_atual = datetime.datetime.now().year
        codigo_aleatorio = f"{random.randint(0, 99999):05d}"
        return f"{cod_crea_regional}{ano_atual}{codigo_aleatorio}"



    def criar_art(self, art_data: schemas.ARTBase):
        try:
            crea_codigo = self.db.query(models.CodCrea).filter(
                models.CodCrea.codigo == art_data.codigo_crea_fk
            ).first()
            # Gerar número da ART
            numero_art = self.gerar_numero_art(crea_codigo.crea_nome)
            
            
            # Criar o objeto ART
            art = models.ART(
                modelo=art_data.modelo,
                numero=numero_art,
                rnp=art_data.rnp,
                forma_registro=art_data.forma_registro,
                codigo_crea_fk=art_data.codigo_crea_fk,
                tipo_participacao=art_data.tipo_participacao,
                finalidade=art_data.finalidade,
                observacao=art_data.observacao,
                acao_institucional=art_data.acao_institucional,
                nome_contratante=art_data.nome_contratante,
                nome_proprietario=art_data.nome_proprietario,
                numero_contrato=art_data.numero_contrato,
                codigo_obra_publica=art_data.codigo_obra_publica,
                data_celebracao_contrato=art_data.data_celebracao_contrato,
                data_inicio_obra=art_data.data_inicio_obra,
                data_previsao_termino=art_data.data_previsao_termino,
                valor_obra=art_data.valor_obra,
                endereco_contratante=art_data.endereco_contratante,
                endereco_proprietario=art_data.endereco_proprietario,
                endereco_obra=art_data.endereco_obra,
                concorda_acessibilidade=art_data.concorda_acessibilidade,
                clausula_compromissoria=art_data.clausula_compromissoria,
                atividades_responsabilidade=art_data.atividades_responsabilidade
            )            
            self.db.add(art)
            self.db.commit()
            self.db.refresh(art)

            # Adicionar atividades associadas à ART
            if art_data.atividades:
                for atividade in art_data.atividades:
                    atividade_pivot = models.AtividadePivot(
                        nivel_atividade_id=atividade.nivel_atividade_id,
                        atividade_profissional_id=atividade.atividade_profissional_id,
                        atividade_id=atividade.atividade_id,
                        art_id=art.id
                    )
                    self.db.add(atividade_pivot)
            
            self.db.commit()

            # Retornar uma resposta de sucesso
            return {"id": art.id}

        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Erro ao criar ART: {str(e)}")

    #Editar Art
    def editar_art(self, art_id: int, art_data: schemas.ARTBase):
        try:
            # Buscar a ART existente
            art = self.db.query(models.ART).filter(models.ART.id == art_id).first()
            if not art:
                raise HTTPException(status_code=404, detail="ART não encontrada")

            # Atualizar os campos da ART
            art.modelo = art_data.modelo
            art.rnp = art_data.rnp
            art.forma_registro = art_data.forma_registro
            art.codigo_crea_fk = art_data.codigo_crea_fk
            art.tipo_participacao = art_data.tipo_participacao
            art.finalidade = art_data.finalidade
            art.observacao = art_data.observacao
            art.acao_institucional = art_data.acao_institucional
            art.nome_contratante = art_data.nome_contratante
            art.nome_proprietario = art_data.nome_proprietario
            art.numero_contrato = art_data.numero_contrato
            art.codigo_obra_publica = art_data.codigo_obra_publica
            art.data_celebracao_contrato = art_data.data_celebracao_contrato
            art.data_inicio_obra = art_data.data_inicio_obra
            art.data_previsao_termino = art_data.data_previsao_termino
            art.valor_obra = art_data.valor_obra
            art.endereco_contratante = art_data.endereco_contratante
            art.endereco_proprietario = art_data.endereco_proprietario
            art.endereco_obra = art_data.endereco_obra
            art.concorda_acessibilidade = art_data.concorda_acessibilidade
            art.clausula_compromissoria = art_data.clausula_compromissoria
            art.atividades_responsabilidade = art_data.atividades_responsabilidade

            self.db.commit()
            self.db.refresh(art)

            # Atualizar atividades associadas à ART
            if art_data.atividades:
                # Remover atividades antigas
                self.db.query(models.AtividadePivot).filter(models.AtividadePivot.art_id == art_id).delete()

                # Adicionar atividades atualizadas
                for atividade in art_data.atividades:
                    atividade_pivot = models.AtividadePivot(
                        nivel_atividade_id=atividade.nivel_atividade_id,
                        atividade_profissional_id=atividade.atividade_profissional_id,
                        atividade_id=atividade.atividade_id,
                        art_id=art.id
                    )
                    self.db.add(atividade_pivot)
            
            self.db.commit()

            # Retornar o ID da ART editada
            return {"id": art.id}

        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Erro ao editar ART: {str(e)}")


        
    #listar arts passando registro do profissional como parametro
    def listar_arts(self, rnp: str = None, numero: str = None) -> List[schemas.ARTResponse]:
        try:
            query = self.db.query(models.ART)
            
            if rnp:
                query = query.filter(models.ART.rnp == rnp)
                
            if numero:
                query = query.filter(models.ART.numero == numero)
                
            arts = query.all()

            art_responses = []
            for art in arts:
                atividades = self.db.query(models.AtividadePivot).filter(models.AtividadePivot.art_id == art.id).all()
                atividade_pivot_responses = []

                for ap in atividades:
                    nivel_atividade = self.db.query(models.NivelAtividade).filter(models.NivelAtividade.id == ap.nivel_atividade_id).first()
                    atividade_profissional = self.db.query(models.AtividadeProfissional).filter(models.AtividadeProfissional.id == ap.atividade_profissional_id).first()
                    atividade = self.db.query(models.Atividade).filter(models.Atividade.id == ap.atividade_id).first()

                    atividade_pivot_response = schemas.AtividadePivotResponse.from_orm(ap)
                    #atividade_pivot_response.nivel_atividade_codigo = nivel_atividade.codigo if nivel_atividade else None
                    atividade_pivot_response.nivel_atividade_descricao = nivel_atividade.descricao if nivel_atividade else None
                    #atividade_pivot_response.atividade_profissional_codigo = atividade_profissional.codigo if atividade_profissional else None
                    atividade_pivot_response.atividade_profissional_descricao = atividade_profissional.descricao if atividade_profissional else None
                    #atividade_pivot_response.atividade_codigo = atividade.codigo if atividade else None
                    atividade_pivot_response.atividade_descricao = atividade.descricao if atividade else None

                    atividade_pivot_responses.append(atividade_pivot_response)

                art_response = schemas.ARTResponse.from_orm(art)
                art_response.atividades = atividade_pivot_responses
                art_responses.append(art_response)

            return art_responses
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao listar ARTs: {e}")
    
        
    def listar_art_por_id(self, art_id: int) -> schemas.ARTResponse:
        try:
            art = self.db.query(models.ART).filter(models.ART.id == art_id).first()
            if not art:
                raise HTTPException(status_code=404, detail="ART não encontrada")

            atividades = self.db.query(models.AtividadePivot).filter(models.AtividadePivot.art_id == art.id).all()
            atividade_pivot_responses = []

            for ap in atividades:
                nivel_atividade = self.db.query(models.NivelAtividade).filter(models.NivelAtividade.id == ap.nivel_atividade_id).first()
                atividade_profissional = self.db.query(models.AtividadeProfissional).filter(models.AtividadeProfissional.id == ap.atividade_profissional_id).first()
                atividade = self.db.query(models.Atividade).filter(models.Atividade.id == ap.atividade_id).first()

                atividade_pivot_response = schemas.AtividadePivotResponse.from_orm(ap)
                atividade_pivot_response.nivel_atividade_descricao = nivel_atividade.descricao if nivel_atividade else None
                atividade_pivot_response.atividade_profissional_descricao = atividade_profissional.descricao if atividade_profissional else None
                atividade_pivot_response.atividade_descricao = atividade.descricao if atividade else None

                atividade_pivot_responses.append(atividade_pivot_response)

            art_response = schemas.ARTResponse.from_orm(art)
            art_response.atividades = atividade_pivot_responses

            return art_response
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Erro ao listar ART por ID: {e}")

    def excluir_art(self, art_id: int):
        try:
            art = self.db.query(models.ART).filter(models.ART.id == art_id).first()
            if not art:
                raise HTTPException(status_code=404, detail="ART não encontrada")

            # Remover atividades associadas à ART
            self.db.query(models.AtividadePivot).filter(models.AtividadePivot.art_id == art_id).delete()

            # Remover a ART
            self.db.delete(art)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Erro ao excluir ART: {str(e)}")