
# services.py
import os
from sqlalchemy.orm import Session
from fastapi import HTTPException
from dotenv import load_dotenv
from database import models


load_dotenv()

tokenAcesso = os.getenv('KEY_CONFEA')

class CreaServices:
    def __init__(self, db: Session):
        self.db = db

    # Outros métodos...

    def listar_cod_crea(self):
        try:
            return self.db.query(models.CodCrea).all()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao listar CodCrea: {e}")
        