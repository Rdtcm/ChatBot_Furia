# flake8: noqa
'''
    Arquivo destinado a integrar com a api do DeepSeek

    O arquivo se comunicara com a view send_message para responder 
    as perguntas feita no chat
'''

import requests
import json


DEEPSEEK_API_KEY = 'sk-ea1c6e401d9c4e469ab60863346ee22f'

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"


def enviar_para_deepseek(mensagem):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Você é um assistente inteligente."},
            {"role": "user", "content": mensagem}
        ],
        "temperature": 0.7,
        "max_tokens": 200
    }

    try:
        response = requests.post(
            DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        # Debug: Mostra a resposta completa da API
        print("Resposta bruta da API:", response.text)

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            error_msg = response.json().get('error', {}).get('message', 'Erro desconhecido')
            raise Exception(f"Erro {response.status_code}: {error_msg}")

    except requests.exceptions.RequestException as e:
        print("Erro de conexão:", str(e))
    except json.JSONDecodeError:
        print("Erro ao decodificar resposta JSON")
    except Exception as e:
        print("Erro inesperado:", str(e))

    return None


if __name__ == '__main__':
    # testando a api do deep seek
    resposta = enviar_para_deepseek('Hello')

    # print(resposta)
