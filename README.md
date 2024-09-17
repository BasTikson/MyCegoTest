Запуск проекта
1.Выполните git clone https://github.com/BasTikson/MyCegoTest.git
2.Установка необходимых инструментов.
  Убедитесь, что у вас установлены Python и python3-venv. Если они не установлены, вы можете установить их с помощью следующих команд:

  Для Ubuntu/Debian:
  sudo apt update
  sudo apt install python3 python3-venv
  
  Для macOS (с использованием Homebrew):
  brew install python3

3. Создание виртуального окружения
   python3 -m venv venv

4. Активация виртуального окружения
   Активируйте созданное виртуальное окружение:
   
   Для Linux/macOS:
   source venv/bin/activate
   
   Для Windows:
   venv\Scripts\activate

5. Установите все зависимости, перечисленные в файле requirements.txt
   cd ApiYandexDisk/
   pip install -r requirements.txt

6. Применение миграций
   Примените все миграции базы данных:
   python manage.py migrate

7. Запуск сервера Django
   python manage.py runserver
