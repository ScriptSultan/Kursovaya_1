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

TOKEN = ''
vk_id = ''
yandex_token = ''


class DlYandex:

    URL_BASE = 'https://api.vk.com/method/'

    def __init__(self, token, user_id, token_ya):
        self.token = token
        self.user_id = user_id
        self.token_ya = token_ya

    def get_common_paramas(self):
        return {
            'album_id': 'profile',
            'extended': '1',
            'access_token': self.token,
            'v': '5.131'
        }

    def get_json_photos_vk(self):
        response = (requests.get(f'{self.URL_BASE}photos.get?{urlencode(self.get_common_paramas())}')).json()
        return response