import requests
import os

class YandexDisk:
    BASE_URL = 'https://cloud-api.yandex.net/v1/disk/public/resources'

    def __init__(self, public_key: str, save_dir: str = 'downloads'):
        self.public_key = public_key
        self.save_dir = save_dir

        # Создаем директорию для сохранения файлов, если она не существует
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def _make_request(self, params=None):
        url = self.BASE_URL
        params = params or {}
        params['public_key'] = self.public_key

        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_resource_info(self, path=None, sort=None, limit=None, preview_size=None, preview_crop=None, offset=None):
        params = {
            'path': path,
            'sort': sort,
            'limit': limit,
            'preview_size': preview_size,
            'preview_crop': preview_crop,
            'offset': offset
        }
        return self._make_request(params)

    def check_file_access(self):
        """
        Проверяет наличие файла и доступ по указанной ссылке.
        Возвращает ответ с информацией о файле или ошибкой.
        """
        try:
            resource_info = self.get_resource_info()
            if 'error' in resource_info:
                return {'status': 'error'}
            return {'status': 'success'}
        except requests.exceptions.RequestException as e:
            return {'status': 'error', 'message': str(e)}

    def get_all_files(self, path=None, sort=None, limit=None, preview_size=None, preview_crop=None, offset=None):
        resource_info = self.get_resource_info(path, sort, limit, preview_size, preview_crop, offset)
        files = []

        if '_embedded' in resource_info and 'items' in resource_info['_embedded']:
            files.extend(resource_info['_embedded']['items'])

        while '_embedded' in resource_info and 'next_href' in resource_info['_embedded']:
            next_href = resource_info['_embedded']['next_href']
            response = requests.get(next_href)
            response.raise_for_status()
            resource_info = response.json()
            files.extend(resource_info['_embedded']['items'])

        return files

    def download_file(self, file_path, save_name=None):
        url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download'
        params = {
            'public_key': self.public_key,
            'path': file_path
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        download_url = response.json()['href']

        file_response = requests.get(download_url)
        file_response.raise_for_status()

        # Определяем имя файла для сохранения
        if save_name:
            save_path = os.path.join(self.save_dir, save_name)
        else:
            save_path = os.path.join(self.save_dir, os.path.basename(file_path))

        with open(save_path, 'wb') as f:
            f.write(file_response.content)

        return save_path