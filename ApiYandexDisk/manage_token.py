import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

def check_token_validity(token):
    url = 'https://cloud-api.yandex.net/v1/disk'
    headers = {
        'Authorization': f'OAuth {token}',
        'Accept': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при проверке токена: {e}")
        return False

def check_and_set_token():
    token = os.getenv('YANDEX_OAUTH_TOKEN')
    if not token:
        print("Токен для доступа к Яндекс.Диску не найден.")
        token = input("Пожалуйста, введите ваш токен: ")
        if token:
            if check_token_validity(token):
                with open('.env', 'a') as env_file:
                    env_file.write(f'\nYANDEX_OAUTH_TOKEN={token}\n')
                print("Токен успешно сохранен в .env файле.")
            else:
                print("Токен недействителен. Попробуйте еще раз!.")
                check_and_set_token()

        else:
            print("Токен недействителен. Попробуйте еще раз!.")
            check_and_set_token()

if __name__ == '__main__':
    check_and_set_token()