## Описание:
    Это веб-приложение, разработанное на основе Django и Django REST Framework, которое предоставляет API для социальной сети.
## Установка:
    1.Склонируйте репозиторий на локальную машину.
    2.Установите зависимости, используя команду: pip install -r requirements.txt.
    3.Настройте базу данных в файле settings.py.
    4.Выполните миграции командой: python manage.py migrate.
    5.Запустите сервер разработки с помощью команды: python manage.py runserver.
## Примеры:
http://127.0.0.1:8000/api/v1/posts/
{
  "count": 123,
  "next": "http://api.example.org/accounts/?offset=400&limit=100",
  "previous": "http://api.example.org/accounts/?offset=200&limit=100",
  "results": [
    {
      "id": 0,
      "author": "string",
      "text": "string",
      "pub_date": "2021-10-14T20:41:29.648Z",
      "image": "string",
      "group": 0 
    }
  ]
}

http://127.0.0.1:8000/api/v1/follow/
{
  "following": "string"
}
