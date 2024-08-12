from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

database_url = os.getenv("DATABASE_URL")

# Crie o mecanismo (engine)
engine = create_engine(database_url)

# Crie uma instância de sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crie uma instância de Base para declaração de modelos
Base = declarative_base()

