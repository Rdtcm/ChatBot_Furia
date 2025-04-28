# flake8: noqa
'''
    Arquivo destinado a integrar com a api do DeepSeek

    O arquivo se comunicara com a view send_message para responder 
    as perguntas feita no chat
'''

import requests
import os
from dotenv import load_dotenv


load_dotenv()
DEEPSEEK_API_KEY = 'sk-b6a0c4a5aaee452aa70715c13a73f11b'

DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions'


def enviar_para_deepseek(mensagem_usuario):

    contexto = "Você é um bot especializado em fornecer informações sobre o time FURIA e-Sports"

    headers = {
        'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
        'Content-Type': 'application/json',
    }
    payload = {
        'model': 'deepseek-chat',  # modelo de chat
        'messages': [
            {'role': 'system', 'content': contexto},
            {'role': 'user', 'content': mensagem_usuario}
        ],
        'temperature': 0.7
    }
    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        resposta = response.json()
        return resposta['choices'][0]['message']['content']
    else:
        return "Erro ao conectar com o DeepSeek."


if __name__ == '__main__':
    # testando a api do deep seek
    print(DEEPSEEK_API_KEY)

    resposta = enviar_para_deepseek('Ola')

    print(resposta)
