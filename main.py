from pprint import pprint
from urllib.parse import urlencode
import requests
import json

ID_VK = ''
authorization_vk = 'https://oauth.vk.com/authorize'
params = {
    'client_id': ID_VK,
    'redirect_uri': 'https://oauth.vk.com/blank.html',
    'display': 'page',
    'scope': 'photos',
    'response_type': 'token',

}
oauth_url = f'{authorization_vk}?{urlencode(params)}'
print(oauth_url)