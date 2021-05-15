import aiohttp
import json
from log import LOGGER

URLS = json.load(open('./lib/apis/URLS.json', 'r'))
headers = {"accept": "application/json",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Brave Chrome/90.0.4430.93 Safari/537.36",
           "Accept-Language": "en_us"}
session = aiohttp.ClientSession()


async def check_pin(pincode: str, date: str) -> list:
    url = URLS.get("CHECK_PIN").replace("{pincode}", pincode).replace("{date}", date)
    resp = await session.get(url=url, headers=headers)
    if resp.status == 200:
        print(await resp.text())
        pin_string = json.loads(await resp.text())
        return pin_string.get('centers')
    else:
        LOGGER.debug(f"{resp.status}:  {await resp.text()}")
        return []


async def check_dist(dist_id: str, date: str) -> list:
    url = URLS.get("CHECK_DISTRICT").replace("{dist_id}", dist_id).replace("{date}", date)
    resp = await session.get(url=url, headers=headers)
    if resp.status == 200:
        print(await resp.text())
        dist_string = json.loads(await resp.text())
        return dist_string.get('centers')
    else:
        LOGGER.debug(f"{resp.status}:  {await resp.text()}")
        return []
