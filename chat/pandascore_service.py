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
from datetime import datetime


load_dotenv()
PANDASCORE_API_KEY = os.getenv('PANDASCORE_API_KEY')
ID_TIME_FURIA = 124530
DATA_ATUAL = datetime.now()


def buscar_elenco_furia() -> list:
    url = 'https://api.pandascore.co/csgo/tournaments?search=furia'
    headers = {
        'Authorization': f'Bearer {PANDASCORE_API_KEY}'
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return [f"Erro ao buscar torneios: {resp.status_code}"]

    try:
        torneios = resp.json()
    except ValueError:
        return ["Resposta da API não é um JSON válido."]

    TARGET_SLUG = 'furia'

    for torneio in torneios:
        roster = torneio.get('expected_roster', [])
        if not roster:
            continue

        for entry in roster:
            team = entry.get('team') or {}
            if team.get('slug', '').lower() == TARGET_SLUG:
                players = entry.get('players', [])
                # Filtra só os ativos e retorna os nomes
                elenco = [p['name'] for p in players if p.get('active')]
                if elenco:
                    return elenco

    return ["Time da FURIA não encontrado em nenhum roster."]


def buscar_torneios_furia() -> list:
    url = f'https://api.pandascore.co/teams/{ID_TIME_FURIA}/leagues'
    headers = {
        'Authorization': f'Bearer {PANDASCORE_API_KEY}'
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return [f"Erro ao buscar torneios: {resp.status_code}"]

    try:
        torneios = resp.json()
    except ValueError:
        return ["Resposta da API não é um JSON válido."]

    torneios_2025 = []

    for torneio in torneios:
        for serie in torneio.get("series", []):
            begin_at = serie.get("begin_at")
            if begin_at:
                data_inicio = datetime.fromisoformat(
                    begin_at.replace("Z", "+00:00"))
                if data_inicio.year == 2025:
                    torneios_2025.append({
                        "torneio": torneio.get("name"),
                        "inicio": data_inicio.strftime("%d/%m/%Y"),
                        "season": serie.get("season"),
                        "serie_nome": serie.get("full_name")
                    })

    if not torneios_2025:
        return ["Não há torneios da FURIA em 2025 nesse momento."]

    return [
        f"{t['torneio']} ({t['serie_nome'] or t['season']}) - Início: {t['inicio']}"
        for t in torneios_2025
    ]


if __name__ == '__main__':
    # testando se a API responde corretamente
    # endpoint que fornece os torneios que a furia participou: https://api.pandascore.co/teams/124530/leagues
    agenda_furia = buscar_torneios_furia()
    print(agenda_furia)

    elenco_furia = buscar_elenco_furia()
    print(elenco_furia)
