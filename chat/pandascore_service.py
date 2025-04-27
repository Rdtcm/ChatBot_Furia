# flake8: noqa
'''
    Arquivo destinado a integrar com a API que vai fornecer os dados 
    da furia e-sports

    API UTILIZADA -- > PandaScore
    senha pandaScore: -$Xs2x!qidRyC8+

    Rdtcm notes: o comando /agenda esta buscando a agenda apenas do time de csgo
'''
import requests
import os
from dotenv import load_dotenv


load_dotenv()
PANDASCORE_API_KEY = os.getenv('PANDASCORE_API_KEY')


def buscar_elenco_furia():
    url = 'https://api.pandascore.co/csgo/teams?search=furia'
    headers = {
        'Authorization': f'Bearer {PANDASCORE_API_KEY}'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()
            if data:
                elenco = [player['name'] for player in data[0]['players']]
                return elenco
            else:
                return ["Time da Furia não encontrado."]
        except ValueError:
            return ["Erro ao processar a resposta da API."]


def buscar_agenda_furia():
    url = 'https://api.pandascore.co/csgo/matches/upcoming'
    headers = {
        'Authorization': f'Bearer {PANDASCORE_API_KEY}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        matches = response.json()
        agenda = []

        for match in matches:
            opponents = [opponent['opponent']['name'].lower()
                         for opponent in match['opponents']]
            if "furia" in opponents:
                adversarios = ' vs '.join(
                    [opponent['opponent']['name'] for opponent in match['opponents']])
                agenda.append(
                    f"{adversarios} - {match['begin_at']} - {match['league']['name']}"
                )
        if agenda:
            return agenda
        else:
            return ["Nenhum jogo encontrado."]
    else:
        return [f"Erro ao buscar agenda: {response.status_code}"]
