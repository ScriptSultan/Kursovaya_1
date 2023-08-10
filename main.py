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

    def dict_info_photo(self):
        files_photos = self.get_json_photos_vk()['response']['items']

        url_p = []
        likes_p = []
        date_p = []

        for tex_l in files_photos:
            like = tex_l['likes']['count']
            likes_p.append(f'{like}.jpg')
        for tex_u in files_photos:
            for url in tex_u['sizes']:
                if url['type'] == 'w':
                    url_p.append(url['url'])
        for tex_d in files_photos:
            date = tex_d['date']
            date_p.append(date)

        seen_elements = set()
        for i in range(len(likes_p) - 1, -1, 1):
            if likes_p[i] in seen_elements:
                y_index = int(likes_p[i]) - 1
                likes_p[i] = date_p[y_index]
            else:
                seen_elements.add(likes_p[i])
        file_for = dict(zip(likes_p, url_p))
        return file_for

    def download_to_yandexdisk(self):
        global url_s
        url = 'https://cloud-api.yandex.net:443/v1/disk/resources'
        headers = {'Authorization': 'OAuth ' + self.token_ya}
        params = {'path': 'VK_photos'}
        response = requests.put(url, headers=headers, params=params)
        url_up = 'https://cloud-api.yandex.net:443/v1/disk/resources/upload'
        for url_s in self.dict_info_photo().items():
            params = {'path': '/VK_photos/' + url_s[0], 'url': url_s[1]}
            resp = requests.post(url_up, headers=headers, params=params)
        return resp

    def info_json(self):
        files_photos = self.get_json_photos_vk()['response']['items']

        size = []
        file_name = []

        for names in files_photos:
            name = names['likes']['count']
            file_name.append(f'{name}.jpg')

        seen_elements = set()
        for i in range(len(file_name) - 1, -1, 1):
            if file_name[i] in seen_elements:
                y_index = int(file_name[i]) - 1
                file_name[i] = file_name[y_index]
            else:
                seen_elements.add(file_name[i])

        for tex_u in files_photos:
            list_type = []
            for url in tex_u['sizes']:
                list_type.append(url['height'])
            sort_type = sorted(list_type, reverse=True)[0]
            for url in tex_u['sizes']:
                if sort_type == url['height']:
                    size.append(url['type'])

        pairs = [{'name': name, 'count': count} for name, count in zip(file_name, size)]
        return pairs