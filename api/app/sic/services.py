
# services.py
import os
import requests
from sqlalchemy.orm import Session
from dotenv import load_dotenv


load_dotenv()

tokenAcesso = os.getenv('KEY_CONFEA')

class SicServices:
    def __init__(self, db: Session):
        self.db = db
                
        
    def get_profissional_sic(self, prfCadCodRnp: str):
        url = f'https://api.teste.confea.org.br/Profissionais/{prfCadCodRnp}'
        headers = {
            'tokenAcesso': tokenAcesso,
            'Content-Type': 'application/json'
        }

        try:
            response = requests.get(url, headers=headers)
            dados = response.json()
         
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception('Erro na requisição: {}'.format(response.status_code))
        except Exception as error:
            print(f'Erro: {error}')
            return None
        
        