with open('token.txt', 'r') as file_object:
    token_vk = file_object.read().strip()

import requests
from pprint import pprint
from tqdm import tqdm
from time import sleep
for i in tqdm(range(200)):
    sleep(.01)

class VK:

    def get_url_photo_vk(owner_id):
        URL = 'https://api.vk.com/method/photos.get'
        params = {owner_id: owner_id, 'album_id': 'profile', 'extended': '1', 'access_token': token_vk, 'v': '5.131'}
        res = requests.get(URL, params=params)
        file_url = res.json()['response']['items'][0]['sizes']
        for i in file_url:
            if i.get('type') == 'z':
                url = i.get('url')
        return url


    def get_photo_name_vk(owner_id):
        URL = 'https://api.vk.com/method/photos.get'
        params = {owner_id: owner_id, 'album_id': 'profile', 'extended': '1', 'access_token': token_vk, 'v': '5.131'}
        res = requests.get(URL, params=params)
        file_name = f"{res.json()['response']['items'][0]['likes']['count']}.png"
        return file_name

class YandexDisk:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload_file_to_disk(self, disk_file_path, filename):
        href = self._get_upload_link(disk_file_path=disk_file_path).get("href", "")
        response = requests.put(href, data=open(filename, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print("Success")

    def upload_url_to_disk(self, disk_path, file_url):
        params = {'path': disk_path, 'url': file_url}
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        response = requests.post(url=upload_url, params=params, headers=headers)
        response.raise_for_status()
        if response.status_code == 201:
            print("Success")

if __name__ ==  '__main__':
    #print(VK.get_url_photo_vk('353981485'))
    #print(VK.get_photo_name_vk('353981485'))

    TOKEN = ''
    ya = YandexDisk(token=TOKEN)
    ya.upload_url_to_disk(f"/netology/{VK.get_photo_name_vk('353981485')}", VK.get_url_photo_vk('353981485'))