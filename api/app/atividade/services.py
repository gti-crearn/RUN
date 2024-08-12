
# services.py
import os
from sqlalchemy.orm import Session
from fastapi import HTTPException
from dotenv import load_dotenv
from database import models


# load_dotenv()

# tokenAcesso = os.getenv('KEY_CONFEA')

class ProfissionalAtividade:
    def __init__(self, db: Session):
        self.db = db

    # Outros métodos...

    def listar_atividades(self):
        try:
            return self.db.query(models.Atividade).all()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao listar CodCrea: {e}")
    
    def listar_atividade_profissional(self):
        try:
            return self.db.query(models.AtividadeProfissional).all()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao listar CodCrea: {e}")
        
    def listar_nivel_atividade(self):
        try:
            return self.db.query(models.NivelAtividade).all()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao listar CodCrea: {e}")