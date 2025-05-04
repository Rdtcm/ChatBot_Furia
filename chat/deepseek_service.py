# flake8: noqa
'''
Integração com a API do OpenRouter (modelo deepseek-v3-base:free).
'''

from dotenv import load_dotenv
import os
import requests
import re


load_dotenv()
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"


def enviar_para_openrouter(mensagem_usuario: str, historico: list[dict]) -> str:
    """
    Envia a mensagem e o histórico de conversa para o OpenRouter
    e retorna a resposta do bot.
    """
    if not OPENROUTER_API_KEY:
        raise RuntimeError("Chave OPENROUTER_API_KEY não encontrada em .env")

    # Prompt do sistema como string única
    system_prompt = (
        "Você é o FURIABot, bot oficial da FURIA e-Sports. "
        "Responda apenas perguntas sobre curiosidades"
    )

    # Montagem das mensagens: system + histórico + user
    mensagens = [{"role": "system", "content": system_prompt}]
    mensagens += historico
    mensagens.append({"role": "user", "content": mensagem_usuario})

    payload = {
        "model": "deepseek/deepseek-v3-base:free",
        "messages": mensagens,
        "temperature": 0.7,
        "max_tokens": 500,
        "stop": ["\n#"],
    }

    try:
        response = requests.post(
            OPENROUTER_API_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=10
        )
    except requests.RequestException as e:
        return f"Erro de conexão com a API: {e}"

    # Log para depuração
    # print(f"[OpenRouter] status: {response.status_code}")
    # print(f"[OpenRouter] body: {response.text}")

    # Tenta converter para JSON
    try:
        data = response.json()
    except ValueError:
        return f"Resposta inválida da API: {response.text}"

    # Se não vier 'choices', trata como erro
    if response.status_code != 200 or "choices" not in data:
        err = data.get("error", {}).get("message", response.text)
        return f"Erro da API ({response.status_code}): {err}"

    # Retorna o conteúdo da primeira escolha
    raw = data["choices"][0]["message"]["content"].strip()

    return limpar_resposta(raw)


def limpar_resposta(resposta: str) -> str:
    padroes = [
        r"Você é o FURIABot[^.]*\.",     # remove "Você é o FURIABot ... ."
        # remove "Responda apenas perguntas ..."
        r"Responda apenas perguntas[^.]*\.",
        r"ChatGPT",                      # remove menções ao ChatGPT
        r"(?i)bot oficial da FURIA e-?Sports",
        r"^o,\s*[:：]?\s*",
    ]

    for padrao in padroes:
        resposta = re.sub(padrao, '', resposta, flags=re.IGNORECASE)

    # removendo espacos e linhas vazias
    resposta = re.sub(r'\s+', ' ', resposta).strip()
    return resposta


# if __name__ == '__main__':
    # Teste com histórico vazio
    # resposta = enviar_para_openrouter("Olá bot!", [])
    # print(resposta)
