# routes.py
from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crea import services, schemas
from database.utils import get_db

router = APIRouter(
    prefix="/creas",
    tags=["CREA"],
    responses={404: {"description": "Not found"}},
)

def get_current_user(request: Request):
    user = request.state.user
    if user is None:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    return user

    
    
@router.get("/codigos", response_model=List[schemas.CodCrea])
def listar_cod_crea(db: Session = Depends(get_db)):
    try:
        service = services.CreaServices(db)
        return service.listar_cod_crea()
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar CodCrea: {e}")
