# routes.py
from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.atividade import services, schemas
from database.utils import get_db

router = APIRouter(
    prefix="/atividade",
    tags=["ATIVIDADE"],
    responses={404: {"description": "Not found"}},
)

def get_current_user(request: Request):
    user = request.state.user
    if user is None:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    return user

    
@router.get("/nivel_atividade", response_model=List[schemas.AtividadeProfisionalResponse])
def listar_atividades(db: Session = Depends(get_db)):
    try:
        service = services.ProfissionalAtividade(db)
        return service.listar_atividade_profissional()
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar CodCrea: {e}")
    
    
@router.get("/listar", response_model=List[schemas.AtividadeResponse])
def listar_atividades(db: Session = Depends(get_db)):
    try:
        service = services.ProfissionalAtividade(db)
        return service.listar_atividades()
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar CodCrea: {e}")

@router.get("/atividade_profissional", response_model=List[schemas.AtividadeProfisionalResponse])
def listar_atividades(db: Session = Depends(get_db)):
    try:
        service = services.ProfissionalAtividade(db)
        return service.listar_atividade_profissional()
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar CodCrea: {e}")
