# routes.py
from fastapi import APIRouter, Depends, HTTPException, Request,Query
from sqlalchemy.orm import Session
from app.profissional import schemas, services
from database.utils import get_db
from typing import List, Optional
from fastapi.responses import RedirectResponse
import os
from dotenv import load_dotenv
import base64
import hashlib
import secrets
import urllib.parse
from fastapi.security import OAuth2PasswordBearer


router = APIRouter(
    prefix="/profissional",
    tags=["PROFISSIONAL"],    
    responses={404: {"description": "Not found"}},
)

# def get_current_user(request: Request):
#     user = request.state.user
#     if user is None:
#         raise HTTPException(status_code=401, detail="Usuário não autenticado")
#     return user

# def generate_code_challenge(code_verifier: str) -> str:
#     code_challenge = base64.urlsafe_b64encode(
#         hashlib.sha256(code_verifier.encode('ascii')).digest()
#     ).rstrip(b'=').decode('ascii')
#     return code_challenge

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Configurações da sua aplicação
# client_id = os.getenv("GOVBR_CLIENT_ID")
# redirect_uri = os.getenv("GOVBR_REDIRECT_URI")
# gov_auth_url = os.getenv("GOVBR_AUTH_URL")

# if not redirect_uri or not client_id or not gov_auth_url:
#     raise HTTPException(status_code=500, detail="Configurações de autenticação não definidas")

# @router.get("/login")
# async def login():
#     redirect_uri = os.getenv("GOVBR_REDIRECT_URI")  # Verifique se essa variável está corretamente configurada no seu ambiente
#     client_id = os.getenv("GOVBR_CLIENT_ID")
#     gov_auth_url = os.getenv("GOVBR_AUTH_URL")
    
#     nonce = secrets.token_urlsafe(16)
#     state = secrets.token_urlsafe(16)
#     code_verifier = secrets.token_urlsafe(32)
#     code_challenge = generate_code_challenge(code_verifier)
    
#     full_redirect_uri = (
#         f"{gov_auth_url}?response_type=code"
#         f"&client_id={client_id}"
#         f"&scope=openid+email+profile+govbr_confiabilidades"
#         f"&redirect_uri={urllib.parse.quote(redirect_uri, safe='')}"
#         f"&nonce={nonce}"
#         f"&state={state}"
#         f"&code_challenge={code_challenge}"
#         f"&code_challenge_method=S256"
#     )
    
#     return RedirectResponse(full_redirect_uri)

# @router.get("/callback")
# async def callback(request: Request):
#     code = request.query_params.get("code")
#     if not code:
#         raise HTTPException(status_code=400, detail="Code not found in callback request")

#     client_id = os.getenv("GOVBR_CLIENT_ID")
#     client_secret = os.getenv("GOVBR_CLIENT_SECRET")
#     redirect_uri = os.getenv("GOVBR_REDIRECT_URI")

#     token_response = request.post(os.getenv("GOVBR_TOKEN_URL"), data={
#         'grant_type': 'authorization_code',
#         'code': code,
#         'redirect_uri': redirect_uri,
#         'client_id': client_id,
#         'client_secret': client_secret
#     })

#     token_response_data = token_response.json()
#     if "error" in token_response_data:
#         raise HTTPException(status_code=400, detail=token_response_data["error_description"])

#     access_token = token_response_data["access_token"]
#     return {"access_token": access_token}


# cria profissional
@router.post("/criar_profissional")
def criar_profissional(profissional: schemas.CriarProfissional, db: Session = Depends(get_db)):
    service = services.ProfissionalServices(db)
    return service.criar_profissional(profissional)

@router.get("/{prfCadCodRnp}")
def get_profissional(prfCadCodRnp: str, db: Session = Depends(get_db)):
    service = services.ProfissionalServices(db)
    return service.listar_profissional(prfCadCodRnp)

@router.post("/vistos/")
def criar_visto(visto: schemas.VistoCreate,db: Session = Depends(get_db)):
    # Verificar se o código do visto já existe
    service = services.ProfissionalServices(db)
    # Criar e retornar o novo visto
    return service.criar_visto(visto)





    

