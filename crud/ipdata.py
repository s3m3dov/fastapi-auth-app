import aiohttp
import requests

from core import settings
from core.utils import prettify_json
from db.models import IPData as model_IPData


def get_by_ip_address(ip_address: str):
    return model_IPData.filter(model_IPData.ip_address == ip_address).first()


def get_user_ip_data(client_ip):
    ip_data_url = f"https://api.ipdata.co/{client_ip}?api-key={settings.IPDATA_API_KEY}"
    response = requests.get(ip_data_url)
    return prettify_json(response.json())


async def get_user_ip_data_async(client_ip):
    ip_data_url = f"https://api.ipdata.co/{client_ip}?api-key={settings.IPDATA_API_KEY}"
    async with aiohttp.ClientSession() as session:
        async with session.get(ip_data_url) as response:
            json_dict = await response.json()

    return prettify_json(json_dict)



