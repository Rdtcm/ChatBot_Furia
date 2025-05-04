# 🐺 Chatbot FURIA Fans — Experiência Conversacional

Este projeto foi desenvolvido como parte do desafio técnico para a FURIA, com o objetivo de criar uma experiência conversacional para os fãs do time de CS\:GO. O sistema consiste em um chatbot interativo que permite ao usuário acompanhar informações do time, interagir com comandos específicos e conversar com um agente inteligente. Estou aberto a sugestões e melhorias no projeto.

---

## 🚀 Funcionalidades

### 📋 Comandos do Chat

* `/elenco`

  * Retorna a formação atual do time de CS\:GO da FURIA.
  * Dados atualizados via integração com a API da PandaScore.

* `/torneios`

  * Lista os torneios de CS\:GO em que a FURIA está participando em 2025.
  * Também utiliza dados em tempo real da PandaScore.

### 💬 Agente Inteligente

* O bot responde perguntas e curiosidades sobre o time e o universo do CS.
* Integrado com a API da [OpenRouter](https://openrouter.ai/), utilizando modelos de linguagem (LLMs) para respostas mais naturais.

---

## 🛠️ Tecnologias Utilizadas

* **Backend**: [Django](https://www.djangoproject.com/)
* **Frontend**: HTML, CSS, JavaScript puro (sem frameworks)
* **APIs Externas**:

  * [PandaScore](https://developers.pandascore.co/) (dados de eSports)
  * [OpenRouter](https://openrouter.ai/) (agente conversacional via LLM)

---

## 📂 Como Rodar Localmente

# Obs: 

1. Clone este repositório:

```bash
git clone https://github.com/seu-usuario/chatbot-furia.git
cd chatbot-furia
```

2. Crie um ambiente virtual e instale as dependências:

```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
```

3. Configure variáveis de ambiente:

Crie um arquivo `.env` com suas chaves da PandaScore e OpenRouter:

```
PANDASCORE_TOKEN=seu_token_aqui
OPENROUTER_API_KEY=sua_api_key_aqui
```
---

4. Execute o servidor:

```bash
python manage.py runserver
```

5. Acesse via navegador:

```
http://127.0.0.1:8000/chat/
```

---

## ⚠️ Nota sobre os Dados de Torneios

Os torneios listados no comando `/torneios` foram obtidos via API da **PandaScore**, utilizando o **ID oficial da FURIA** como filtro. No entanto, essa API retorna todas as ligas e qualificatórias **associadas à equipe**, mesmo que **a FURIA não tenha participado efetivamente em 2025**.

Por limitação de tempo e acesso aos endpoints mais específicos, **não foi possível filtrar apenas os torneios com participação confirmada**. A solução ideal seria utilizar os endpoints de partidas, agrupando os torneios apenas a partir de confrontos reais — estrutura essa que já está prevista e pode ser aplicada facilmente no futuro.

Esse ponto foi documentado para manter total transparência.

## 🧠 Considerações

Este chatbot é uma iniciativa voltada à comunidade de fãs da FURIA, oferecendo uma experiência interativa, informativa e inteligente. O projeto se mantém modular, com potencial para novos comandos, integração de histórico de partidas e muito mais.

---

## 📸 Demonstração
Index
![Screenshot from 2025-05-02 17-25-28](https://github.com/user-attachments/assets/e0dab788-3ec4-460c-8000-27f73bd2ff49)  
Login
![Screenshot from 2025-05-02 17-25-34](https://github.com/user-attachments/assets/1f2bd7b9-03c5-49b8-8dcc-aaed0996a1dd)  
Criar Conta
![Screenshot from 2025-05-02 17-25-39](https://github.com/user-attachments/assets/a7a6651b-37c5-49dd-b6a0-c502f5688735)  
Pagina de Chat
![Screenshot from 2025-05-02 19-25-34](https://github.com/user-attachments/assets/47d8c540-af5b-4998-adef-ac211b6ec2c3)  

---

## 📄 Licença

MIT © 2025 – \Ryan Ledo
