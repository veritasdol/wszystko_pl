from os import environ, path
import requests
import json
from datetime import datetime, timedelta


API_URL = 'https://wszystko.pl/api'
DEVICE_CODE_VAR_NAME = 'WSZYSTKO_PL_DEVICE_CODE'  # type your variable name
TOKEN_JSON_FILE = 'tokens.json'  # type path to your tokens file


def get_device_code(is_registered: bool = True) -> str:
    '''
    Return device code
    '''
    if is_registered and environ.get(DEVICE_CODE_VAR_NAME):
        device_code = environ.get(DEVICE_CODE_VAR_NAME)
        return device_code
    else:
        response = send_request(method='GET', path='/integration/register')
        device_code = response['deviceCode']
        input(f'Open this URL in your browser and complete authorization: {response["verificationUriPrettyComplete"]} \n Then press Enter')
        print(
            f'Add your "Device Code" to a System variables and reboot your system: {device_code}')
        return device_code


def send_request(method:str, path: str, device_code: str = None, refresh_token: str = None) -> dict:
    params = {'deviceCode': device_code, 'refreshToken': refresh_token}
    url = API_URL + path
    try:
        response = requests.request(method=method,
                                    url=url,
                                    params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    

def get_token(device_code: str = None, refresh_token: str = None) -> str:
    '''
    Send request to API for new token or token extension
    '''
    match device_code:
        case None: response = send_request(
            method='POST',
            path='/integration/token',
            refresh_token=refresh_token
        )
        case _: response = send_request(
            method='GET',
            path='/integration/token',
            device_code=device_code
        )
    with open(TOKEN_JSON_FILE, 'w') as file:
        response['date'] = str(datetime.now())
        file.write(json.dumps(response))
    return response['accessToken']


def check_file(path_to_file: str) -> bool:
    '''
    Return True if file exist and it is not empty, False otherwise.
    '''

    if path.isfile(path_to_file):
        with open(path_to_file, 'r') as file:
            return bool(file.read())
    return False


def check_token(data: dict) -> bool:
    '''
    Return True if token still valid, False otherwise.
    '''
    
    date = datetime.fromisoformat(data['date'])
    token_exp_time = data['expiresIn']
    return date + timedelta(seconds=token_exp_time) > datetime.now()
    
def token() -> str:
    '''
    Return token
    '''
    if check_file(TOKEN_JSON_FILE):
        with open(TOKEN_JSON_FILE, 'r') as file:
            data = json.loads(file.read())
            if check_token(data):
                return data['accessToken']
            return get_token(refresh_token=data['refreshToken'])
    device_code = get_device_code(is_registered=False)
    return get_token(device_code=device_code)


if __name__ == '__main__':
    print(token())
