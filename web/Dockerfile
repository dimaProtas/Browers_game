FROM python:3.10


RUN apt-get update && apt-get install -y netcat-openbsd && apt-get install -y locales

# Устанавливаем зависимости
RUN pip install --upgrade pip

RUN locale-gen en_US.UTF-8 ru_RU.UTF-8


# Указываем рабочую директорию внутри контейнера
WORKDIR /web

# Копируем файлы приложения в контейнер
COPY . /web

# Устанавливаем зависимости из requirements.txt
RUN pip install -r requirements.txt

# Установка сервера Daphne
CMD ["daphne", "-b", "0.0.0.0", "web.asgi:application", "--port", "8001"]

