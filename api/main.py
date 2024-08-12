from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.profissional.routes import router as usuario_router
from app.sic.routes import router as sic_router
from app.crea.routes import router as crea_router
from app.art.routes import router as art_router
from app.atividade.routes import router as atividade_router



app = FastAPI()

# Configurando o CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas as origens
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE"],  # Métodos permitidos
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)

app.include_router(usuario_router)
app.include_router(sic_router)
app.include_router(crea_router)
app.include_router(art_router)
app.include_router(atividade_router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)