import aiohttp
import json
from log import LOGGER


URLS = json.load(open('./lib/apis/URLS.json', 'r'))
headers = {"accept": "application/json",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Brave Chrome/90.0.4430.93 Safari/537.36",
           "Accept-Language": "en_us"}
session = aiohttp.ClientSession()


async def list_states() -> list:
    resp = await session.get(URLS.get('GET_STATES'), headers=headers)
    if resp.status == 200:
        states_string = json.loads(await resp.text())
        return states_string.get('states')
    else:
        LOGGER.debug(f"{resp.status}:  {await resp.text()}")
        return []


async def list_dist(state: str) -> list:
    url = URLS.get("GET_DIST").replace("{state_id}", state)
    resp = await session.get(url=url, headers=headers)
    if resp.status == 200:
        dist_string = json.loads(await resp.text())
        return dist_string.get('districts')
    else:
        LOGGER.debug(f"{resp.status}:  {await resp.text()}")
        return []
