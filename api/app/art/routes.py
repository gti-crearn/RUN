# routes.py
from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.art import services, schemas
from database.utils import get_db

router = APIRouter(
    prefix="/art",
    tags=["ART"],
    responses={404: {"description": "Not found"}},
)

@router.post("/criar")
def criar_art(art_data: schemas.ARTBase, db: Session = Depends(get_db)):
    try:
        service = services.ArtServices(db)
        result = service.criar_art(art_data)
        return {"status": "ok", "id": result["id"]}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar ART: {str(e)}")


@router.put("/editar/{art_id}")
def editar_art(
    art_id: int,
    art_data: schemas.ARTBase,
    db: Session = Depends(get_db)
):
    try:
        service = services.ArtServices(db)
        result = service.editar_art(art_id, art_data)
        return {"status": "ok", "id": result["id"]}  # Retorna o ID da ART editada
    except HTTPException as e:  
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar ART: {str(e)}")

@router.get("/arts/{art_id}", response_model=schemas.ARTResponse)
def listar_art_por_id(art_id: int, db: Session = Depends(get_db)):
    service = services.ArtServices(db)
    return service.listar_art_por_id(art_id)

   
@router.get("/list", response_model=List[schemas.ARTResponse])
def listar_arts(rnp: str = None, numero: str = None, db: Session = Depends(get_db)):
    service = services.ArtServices(db)
    return service.listar_arts(rnp=rnp, numero=numero)

@router.delete("/art/{art_id}")
def excluir_art(
    art_id: int,
    db: Session = Depends(get_db)
):
    try:
        service = services.ArtServices(db)
        service.excluir_art(art_id)
        return {"status": "ok", "message": "ART excluída com sucesso"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao excluir ART: {str(e)}")

