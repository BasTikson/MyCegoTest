import os
import requests
from dotenv import load_dotenv

load_dotenv()

class YandexDiskClient:
    BASE_URL = 'https://cloud-api.yandex.net/v1/disk'

    def __init__(self):
        self.oauth_token = os.getenv('YANDEX_OAUTH_TOKEN')
        if not self.oauth_token:
            raise ValueError("OAuth token is not set")

    def _make_request(self, method, url, params=None, data=None):
        headers = {
            'Authorization': f'OAuth {self.oauth_token}',
            'Accept': 'application/json'
        }

        response = requests.request(method, url, headers=headers, params=params, json=data)
        response.raise_for_status()
        return response.json()

    def get_files_list(self):
        url = f'{self.BASE_URL}/resources/files'
        return self._make_request('GET', url)

    def download_file(self, file_path):
        url = f'{self.BASE_URL}/resources/download'
        params = {'path': file_path}
        response = self._make_request('GET', url, params=params)
        download_url = response['href']
        return requests.get(download_url)

# Пример использования
# if __name__ == '__main__':
#     client = YandexDiskClient()
#
#     # Получение списка файлов
#     files = client.get_files_list()
#     print("Список файлов:", files)
#
#     # Скачивание файла
#     file_path = '/path/to/your/file.txt'
#     file_response = client.download_file(file_path)
#     with open('downloaded_file.txt', 'wb') as f:
#         f.write(file_response.content)
#     print("Файл успешно скачан")