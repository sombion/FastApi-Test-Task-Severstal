# FastApi-Test-Task-Severstal

## Описание  
Этот проект представляет собой REST API для управления рулонами металла (`Roll`).  
API позволяет добавлять, удалять, фильтровать и получать статистику по рулонам.  

## Технологии  
- **Python 3.12+**  
- **FastAPI** – фреймворк для разработки API  
- **SQLAlchemy** – ORM для работы с базой данных  
- **PostgreSQL** – в качестве базы данных  
- **Alembic** – инструмент для миграций  
- **Pytest** – для тестирования  
- **Docker, Docker Compose** – для контейнеризации  

## Установка и запуск  

### Клонирование репозитория  
```
git clone https://github.com/your-repo/FastApi-Test-Task-Severstal.git
cd FastApi-Test-Task-Severstal
```

### Настройка переменных окружения
Создайте .env и .env-non-dev файлы в корне проекта и добавить в них:
```
MODE=

DB_HOST=
DB_PORT=
DB_USER=
DB_PASS=
DB_NAME=

POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=

TEST_DB_HOST=
TEST_DB_PORT=
TEST_DB_USER=
TEST_DB_PASS=
TEST_DB_NAME=
```

Для запуска всех сервисов (БД, FastAPI) через docker-compose необходимо использовать файл docker-compose.yml и команды:
```
docker compose build
docker compose up
```
Документация в формате Swagger доступна по адресу:
```
http://127.0.0.1:8000/docs
```

## API Эндпоинты

| Метод    | Эндпоинт            | Описание                           |
|----------|---------------------|------------------------------------|
| `POST`   | `/roll/add`         | Добавить рулон                    |
| `DELETE` | `/roll/delete/{id}` | Удалить рулон по ID               |
| `GET`    | `/roll/all`         | Получить все рулоны               |
| `GET`    | `/roll/filter`      | Фильтрация рулонов по параметрам  |
| `GET`    | `/rolls/stats/`     | Получить статистику за период     |



Запуск тестов
```
pytest
```