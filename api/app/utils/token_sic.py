import requests
from dotenv import load_dotenv
import os


load_dotenv()


tokenAcesso = os.getenv('KEY_CONFEA')

def obter_foto(prfCadCodRnp):
    url = 'https://api.teste.confea.org.br/Imagens/Listar'
    headers = {
        'tokenAcesso': tokenAcesso,
        'Content-Type': 'application/json'
    }
    body = {
        'prfCadCodRnp': prfCadCodRnp
    }

    try:
        response = requests.post(url, json=body, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception('Erro na requisição: {}'.format(response.status_code))
    except Exception as error:
        print(f'Erro: {error}')
        return None
