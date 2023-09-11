# Используйте базовый образ Python
FROM python:3.8

# Создайте рабочую директорию
WORKDIR /app

# Скопируйте файлы вашего приложения в контейнер
COPY . /app

# Установка Pygbag и его зависимости
RUN pip install git+https://github.com/pygame-web/pygbag
RUN pip install pygbag --upgrade

# Определите команду для запуска игры
CMD ["python", "pygbag doom_bygbag"]
