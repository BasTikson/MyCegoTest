import requests
import os
import aiohttp
import asyncio

class YandexDisk:
    """
    Класс для работы с Yandex.Disk API.

    :param public_key: Публичный ключ для доступа к ресурсам на Yandex.Disk.
    :param save_dir: Директория для сохранения скачанных файлов (по умолчанию 'downloads').
    """
    BASE_URL = 'https://cloud-api.yandex.net/v1/disk/public/resources'

    def __init__(self, public_key: str, save_dir: str = 'downloads'):
        self.public_key = public_key
        self.save_dir = save_dir

        # Создаем директорию для сохранения файлов, если она не существует
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def _make_request(self, params=None) -> dict:
        """
        Выполняет HTTP GET-запрос к Yandex.Disk API.

        :param params: Параметры запроса.
        :return: JSON-ответ от сервера.
        :raises requests.exceptions.RequestException: В случае ошибки запроса.
        """
        url = self.BASE_URL
        params = params or {}
        params['public_key'] = self.public_key

        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_resource_info(self, path=None, sort=None, limit=None, preview_size=None, preview_crop=None, offset=None) -> dict:
        """
        Получает информацию о ресурсе на Yandex.Disk.

        :param path: Путь к ресурсу.
        :param sort: Параметр сортировки.
        :param limit: Ограничение на количество элементов.
        :param preview_size: Размер превью.
        :param preview_crop: Обрезка превью.
        :param offset: Смещение.
        :return: JSON-ответ с информацией о ресурсе.
        """
        params = {
            'path': path,
            'sort': sort,
            'limit': limit,
            'preview_size': preview_size,
            'preview_crop': preview_crop,
            'offset': offset
        }
        return self._make_request(params)

    def check_file_access(self) -> dict:
        """
        Проверяет наличие файла и доступ по указанной ссылке.
        Возвращает ответ с информацией о файле или ошибкой.

        :return: Словарь с результатом проверки.
        """
        try:
            resource_info = self.get_resource_info()
            if 'error' in resource_info:
                return {'status': 'error'}
            return {'status': 'success'}
        except requests.exceptions.RequestException as e:
            return {'status': 'error', 'message': str(e)}

    def get_all_files(self, path=None, sort=None, limit=None, preview_size=None, preview_crop=None, offset=None) -> list:
        """
        Получает список всех файлов на Yandex.Disk.

        :param path: Путь к ресурсу.
        :param sort: Параметр сортировки.
        :param limit: Ограничение на количество элементов.
        :param preview_size: Размер превью.
        :param preview_crop: Обрезка превью.
        :param offset: Смещение.
        :return: Список файлов.
        """
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

    async def download_file(self, file_path: str, save_name: str = None) -> str:
        """
        Асинхронно скачивает файл с Yandex.Disk.

        :param file_path: Путь к файлу на Yandex.Disk.
        :param save_name: Имя файла для сохранения (по умолчанию используется имя файла на Yandex.Disk).
        :return: Имя сохраненного файла.
        """
        url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download'
        params = {
            'public_key': self.public_key,
            'path': file_path
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                download_url = (await response.json())['href']

            async with session.get(download_url) as file_response:
                file_response.raise_for_status()

                # Определяем имя файла для сохранения
                if save_name:
                    save_path = os.path.join(self.save_dir, save_name)
                else:
                    save_path = os.path.join(self.save_dir, os.path.basename(file_path))

                with open(save_path, 'wb') as f:
                    f.write(await file_response.read())

                return os.path.basename(save_path)

    async def download_files(self, file_paths: list) -> list:
        """
        Асинхронно скачивает несколько файлов с Yandex.Disk.

        :param file_paths: Список путей к файлам на Yandex.Disk.
        :return: Список имен сохраненных файлов.
        """
        tasks = [self.download_file(file_path) for file_path in file_paths]
        return await asyncio.gather(*tasks)