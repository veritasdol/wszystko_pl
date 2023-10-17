import requests
from . import config



def send_request(method: str, path: str, params: dict = None) -> dict:
    params = params
    url = config.API_URL + path
    try:
        response = requests.request(method=method,
                                    url=url,
                                    params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    