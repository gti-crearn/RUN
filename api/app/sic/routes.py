# routes.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.sic import schemas, services
from database.utils import get_db

router = APIRouter(
    prefix="/sic",
    tags=["SIC"],
    responses={404: {"description": "Not found"}},
)

def get_current_user(request: Request):
    user = request.state.user
    if user is None:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    return user

    
    
@router.post("/profissional/")
def buscar_profissional_sic(request: schemas.Request, db: Session = Depends(get_db)):
    service = services.SicServices(db)
    response = service.get_profissional_sic(request.prfCadCodRnp)
    if response is None:
        raise HTTPException(status_code=500, detail="Erro ao obter os dados do sic")
    return response
