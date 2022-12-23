import unittest

from main import YaUploader

with open('token-YD.txt', 'r') as file_object:
    tokenYD = file_object.read().strip()

class TestYandexAPI(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        uploader = YaUploader(tokenYD)
        uploader.del_folder('test_folder')

    def test_check_and_create_folder(self):
        uploader = YaUploader(tokenYD)
        result = uploader.check_and_create_folder('test_folder')
        assert result == 'Папки test_folder нет на Я.Диске. Создаём.'

    def test_check_and_create_folder2(self):
        uploader = YaUploader(tokenYD)
        result = uploader.check_and_create_folder('test_folder')
        assert result == 'Папка test_folder есть на Я.Диске.'


