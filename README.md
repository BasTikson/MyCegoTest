Запуск проекта
Выполните git clone https://github.com/BasTikson/MyCegoTest.git
Установка необходимых инструментов.
Убедитесь, что у вас установлены Python и python3-venv. Если они не установлены, вы можете установить их с помощью следующих команд:

Для Ubuntu/Debian:
sudo apt update
sudo apt install python3 python3-venv

Для macOS (с использованием Homebrew):
brew install python3

Создание виртуального окружения
python3 -m venv venv

 Активация виртуального окружения
Активируйте созданное виртуальное окружение:

Для Linux/macOS:
source venv/bin/activate

Для Windows:
venv\Scripts\activate

Установите все зависимости, перечисленные в файле requirements.txt
cd ApiYandexDisk/
pip install -r requirements.txt

Применение миграций
Примените все миграции базы данных:
python manage.py migrate

Запуск сервера Django
python manage.py runserver
