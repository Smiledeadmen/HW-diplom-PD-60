with open('token.txt', 'r') as file_object:
    token = file_object.read().strip()

import time
import requests
from tqdm import tqdm
from pprint import pprint
import os

class VK_Photo:
    url = 'https://api.vk.com/method/'
    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }


    def photos_get(self, id, al_id='profile'):
        '''
        wall — фотографии со стены;
        profile — фотографии профиля;
        saved — сохраненные фотографии. Возвращается только с ключом доступа пользователя.
        '''
        photo_params = {
            'owner_id': id,
            'album_id': al_id,
            'extended': 1,
            'count': 10,
            'rev': 1
        }
        req = requests.get(self.url + 'photos.get', params={**self.params, **photo_params}).json()
        req = req['response']['items']
        return req


    def create_folder(self):
      BASE_PATH = os.getcwd()
      folder = 'VK-photo'
      path_repl = os.path.join(BASE_PATH, folder)
      if os.path.exists(path_repl) != True:
        os.mkdir(path_repl)
      return str(path_repl) + '/'


    def get_largest(self, size_dict):
      if size_dict['width'] >= size_dict['height']:
        return size_dict['width']
      else:
        return size_dict['height']


    def download_photo(self, url, filename):
      res = requests.get(url)
      path = self.create_folder()
      with open(path + filename + '.jpg', 'bw') as file:
        file.write(res.content)


    def save_photo(self, id, al_id='profile'):
      filename_lib = []
      res = self.photos_get(id, al_id)
      for photo in tqdm(res):
        sizes = photo['sizes']
        max_sizes_url = max(sizes, key=self.get_largest)['url']
        filename = str(photo['likes']['count'])
        filename_lib.append(filename)
        if filename_lib.count(filename) > 1:
            filename += ' likes ' + str(time.ctime())
            self.download_photo(max_sizes_url,filename)
        else:
            self.download_photo(max_sizes_url,filename)


if __name__ == '__main__':
  vk_client = VK_Photo(token,'5.131')
  vk_client.save_photo(10538884)

# import os
# import requests
# from pprint import pprint
#
# with open('token-YD.txt', 'r') as file_object:
#     tokenYD = file_object.read().strip()
#
# FILE_NAME = '20.jpg'
# PHOTO_DIR = 'VK-photo'
# BASE_PATH = os.getcwd()
# path_repl = os.path.join(PHOTO_DIR, FILE_NAME)
#
#
# class YaUploader:
#     def __init__(self, token: str):
#         self.token = token
#         self.url = 'https://cloud-api.yandex.net/v1/disk/resources'
#         self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
#                         'Authorization': f'OAuth {self.token}'}
#
#     def upload(self, file_path: str):
#         self.create_folder(PHOTO_DIR)
#         res = requests.get(f'{self.url}/upload?path={file_path}', headers=self.headers).json()
#         with open(path_repl, 'rb') as f:
#             try:
#                 requests.put(res['href'], files={'file': f})
#             except KeyError:
#                 print(res)
#
#     def create_folder(self, name_folder):
#         self.check_folder(name_folder)
#         requests.put(f'{self.url}?path={name_folder}', headers=self.headers).json()
#
#     def check_folder(self, name_folder):
#         res = requests.get(f'{self.url}?path={name_folder}', headers=self.headers).json()
#         pprint(res.response.status_code)
#         if res['error'] == "'DiskNotFoundError'":
#             print(f'Папка {name_folder} есть на Я.Диске')
#             self.create_folder(name_folder)
#         else:
#             print(f'Папки {name_folder} нет на Я.Диске. Создаём')
#
#
# if __name__ == '__main__':
#     path_to_file = path_repl
#     uploader = YaUploader(tokenYD)
#     result = uploader.upload(path_to_file)