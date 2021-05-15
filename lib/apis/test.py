import requests
import json

URLS = json.load(open('./URLS.json', 'r'))
headers = {"accept": "application/json",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Brave Chrome/90.0.4430.93 Safari/537.36",
           "Accept-Language": "en_us"}


def list_states() -> list:
    resp = requests.get(URLS.get('GET_STATES'), headers=headers)
    if resp.status_code == 200:
        states_string = json.loads(resp.text)
        return states_string.get('states')
    else:
        return []


def list_dist(state: str) -> list:
    url = URLS.get("GET_DIST").replace("{state_id}", state)
    resp = session.get(url=url, headers=headers)
    if resp.status == 200:
        dist_string = json.loads( resp.text())
        return dist_string.get('districts')
    else:
        return []

print(list_states())