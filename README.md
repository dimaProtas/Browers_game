# GB_dev_agile_web
Pet project 
###  Цель данного проекта создать web интерфейс, через который осуществляется трансляция игрового процесса pygame игры через веб браузер. ##
## Структура проекта  
    web  
        главная страница
        личный кабинет
        страница авторизации
        страница игры
    game
        микросервис

## Окружение
    Используется virtualenv
    переменные среды хранятся в .env

## Локальный запуск проекта
Запускаем так же как здесь указоно, докер контейнер работает с MySQL, так как я не смог свою систему подружить
с PostgreSQL.
если у вас работает на Postgres, сразу выполняйте миграции.
убедитесь что все настройки django-chenels есть в setings.py и в asgi.py (нужно для работычата)

У меня работает на бд MySQL, образ собираеться в контейнере docker-compose.yaml.
собрать контейнер команда \
```docker-compose up --build```

если контейнер с бд запустился то выполняем миграции\
``` python .\manage.py makemigrations ```
```python .\manage.py migrate  ```

выполните установку зависимостей\
```pip install -r requirements.txt```

если миграции выполнились запускаете django приложение\
```python .\manage.py runserver 127.0.0.1:8888```

настройки для бд в файле .env:
фаил .env должен быть в той же директори где и docker-compose.yaml :
#Настройки Django
DEBUG=True

#Настройки базы
MYSQL_DATABASE=gb_dev_db
MYSQL_USER=user
MYSQL_PASSWORD=password
MYSQL_ROOT_PASSWORD=rootpassword
PGPORT=3306
DBHOST=192.168.99.104
