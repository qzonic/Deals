# Стек
<img src="https://img.shields.io/badge/Python-4169E1?style=for-the-badge"/> <img src="https://img.shields.io/badge/Django-008000?style=for-the-badge"/> <img src="https://img.shields.io/badge/DRF-800000?style=for-the-badge"/> <img src="https://img.shields.io/badge/Docker-00BFFF?style=for-the-badge"/> <img src="https://img.shields.io/badge/PostgreSQL-87CEEB?style=for-the-badge"/> <img src="https://img.shields.io/badge/Redis-910112?style=for-the-badge"/>

# Описание проекта:

**Проект Deals**

Данный REST API сервис позволяет загружать с помощью POST запроса .csv файл 
с данными о покупках драгоценных камней. Дальше можно просмотреть топ 5 пользователей, 
которые потратили больше всего денег. Данные кэшируются в Redis.

Каждый клиент описывается следующими полями:
* username - логин клиента;
* spent_money - сумма потраченных средств за весь период;
* gems - список из названий камней, которые купили как минимум двое из списка "5 клиентов, потративших наибольшую сумму за весь период", и данный клиент является одним из этих покупателей.

# Как запустить проект:

*Клонировать репозиторий и перейти в него в командной строке:*
```
https://github.com/qzonic/Deals.git
```
```
cd Deals/
```

В директории Deals нужно создать .env файл, в котором указывается следующее:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

REDIS_HOST = redis
REDIS_PORT = 6379
```

*Теперь необходимо собрать Docker-контейнеры:*
```
docker-compose up -d
```

*После сборки контейнеров, нужно прописать следующую команду:*
```
docker-compose exec web python manage.py migrate
```

*Теперь проект доступен по адресу:*
```
http://127.0.0.1/
```

# Примеры запросов к API:
В примерах для запроса к API используется библиотека requests.

### Загрузка данных:
```python
import requests


with open('deals.csv', 'rb') as file:
    data = {
        'deals': file
    }
    response = requests.post('http://127.0.0.1', files=data)
```
*Ответ от сервиса*
```json
{
  "status": "Success"
}
```

### Получение пользователей:
```python
import requests


response = requests.get('http://127.0.0.1')
```
*Ответ от сервиса*
```json
{
  "response": [
    {
      "username": "resplendent", 
      "spent_money": "451731.00", 
      "gems": []
    }, 
    {
      "username": "bellwether", 
      "spent_money": "217794.00", 
      "gems": []
    }, 
    {
      "username": "uvulaperfly117", 
      "spent_money": "120419.00", 
      "gems": []
    }, 
    {
      "username": "braggadocio", 
      "spent_money": "108957.00", 
      "gems": [{"name": "Изумруд"}]
    }, 
    {
      "username": "turophile", 
      "spent_money": "100132.00", 
      "gems": [{"name": "Изумруд"}]
    }
  ]
}
```

### Автор
[![telegram](https://img.shields.io/badge/Telegram-Join-blue)](https://t.me/qzonic)