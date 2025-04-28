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

    # ID ou slug da FURIA para comparar
    TARGET_SLUG = 'furia'

    # Percorre todos os torneios retornados
    for torneio in torneios:
        # Dentro de cada torneio, há uma lista "expected_roster"
        roster = torneio.get('expected_roster', [])
        if not roster:
            continue

        # Para cada entrada de roster, checa se o time é a FURIA
        for entry in roster:
            team = entry.get('team') or {}
            if team.get('slug', '').lower() == TARGET_SLUG:
                players = entry.get('players', [])
                # Filtra só os ativos e retorna os nomes
                elenco = [p['name'] for p in players if p.get('active')]
                if elenco:
                    return elenco

    # Se chegar aqui, não encontrou nenhum roster válido da FURIA
    return ["Time da FURIA não encontrado em nenhum roster."]


def buscar_agenda_furia():
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
    agenda = []

    for torneio in torneios:
        # só processa torneios onde a FURIA está no roster esperado
        roster = torneio.get('expected_roster', [])
        if not any((entry.get('team') or {}).get('slug', '').lower() == TARGET_SLUG for entry in roster):
            continue

        # extrai todas as partidas agendadas desse torneio
        for m in torneio.get('matches', []):
            agenda.append({
                'id':           m.get('id'),
                'name':         m.get('name'),
                'scheduled_at': m.get('scheduled_at') or m.get('begin_at'),
                'slug':         m.get('slug'),
                'tournament':   torneio.get('name'),
                # se quiser incluir league (nome da liga), pode usar:
                'league':      (torneio.get('league') or {}).get('name'),
            })

    if not agenda:
        return [f"Nenhum jogo da FURIA encontrado nos torneios."]

    return agenda


if __name__ == '__main__':
    # testando se a API responde corretamente
    agenda_furia = buscar_agenda_furia()
    print(agenda_furia)

    elenco_furia = buscar_elenco_furia()
    print(elenco_furia)

    '''
        lEMBRETE***

        Elenco furia funcionando!

        exemplo de retorno da funcao agenda:

        {
            "agenda": [
                {
                "id": 1170665,
                "name": "Quarterfinal 1: ghoulsW vs FURIA",
                "scheduled_at": "2025-05-02T10:00:00Z",
                "slug": "ghoulsw-2025-05-02",
                "tournament": "Playoffs",
                "league": "Paramigo Cup"
                },
                {
                "id": 1170700,
                "name": "Semifinal: FURIA vs TBD",
                "scheduled_at": "2025-05-03T16:00:00Z",
                "slug": "furia-2025-05-03",
                "tournament": "Playoffs",
                "league": "Paramigo Cup"
                }
                // ...
            ]
        }

    '''
