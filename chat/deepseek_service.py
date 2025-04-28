# flake8: noqa
'''
    Arquivo destinado a integrar com a api do DeepSeek

    O arquivo se comunicara com a view send_message para responder 
    as perguntas feita no chat

    A api do deepseek nao e gratuita como imaginei, por isso, irei usar
    o OpenRouter a partir de agora - usando o modelo deepseek v3 (free)
'''

from dotenv import load_dotenv
import os
import requests
import json


load_dotenv()
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"


def enviar_para_openrouter(mensagem_usuario: str) -> str:
    """
    Envia a mensagem para o OpenRouter (modelo deepseek-v3-base:free)
    e retorna o conteúdo da resposta do bot.
    """
    if not OPENROUTER_API_KEY:
        raise RuntimeError("Chave OPENROUTER_API_KEY não encontrada em .env")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "deepseek/deepseek-v3-base:free",
        "messages": [
            {"role": "system", "content": "Você é um bot da FURIA e-Sports que responde curiosidades sobre o time."},
            {"role": "user",   "content": mensagem_usuario},
        ],
        "temperature": 0.7,
        # opcional: "max_tokens": 200
    }

    response = requests.post(
        OPENROUTER_API_URL, headers=headers, json=payload, timeout=10)

    # Log para depuração
    # print(f"[OpenRouter] status: {response.status_code}")
    # print(f"[OpenRouter] body: {response.text}")

    if response.status_code == 200:
        data = response.json()
        # Ajuste aqui caso o path seja diferente
        return data["choices"][0]["message"]["content"]
    else:
        # em produção você pode lançar exceção ou retornar uma mensagem de erro
        return f"Erro {response.status_code}: {response.text}"


if __name__ == '__main__':
    # testando a api do deep seek
    resposta = enviar_para_openrouter(
        "Ola, me conte por que a furia e tao boa no que faz"
    )

    print(resposta)

    '''
     payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Você é um assistente inteligente."},
            {"role": "user", "content": mensagem}
        ],
        "temperature": 0.7,
        "max_tokens": 200
    }
    '''
