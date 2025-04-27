# URL Storage Application

Веб-приложение для хранения ссылок с использованием Flask и PostgreSQL, развертываемое в Docker-контейнерах.

## Требования

- Docker 20.10+
- Git 2.25+

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo/lab5
```

### 2. Установка Docker

[Официальная инструкция по установке Docker](https://docs.docker.com/get-docker/)

### 3. Настройка окружения

Создайте файл `.env` в корне проекта:

```bash
touch .env
```

Заполните его по образцу:

```env
# PostgreSQL
DB_USER=storage_user
DB_PASSWORD=secure_password123
DB_NAME=url_storage
DB_HOST=db
DB_PORT=5432

# Flask
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
```

### 4. Запуск приложения

Выполните команду:

```bash
./start.sh
```

Приложение будет доступно по адресу: [http://localhost:5000](http://localhost:5000)

## Остановка приложения

```bash
./stop.sh
```

## Структура проекта

```
lab5/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   └── templates/
├── migrations/
├── Dockerfile
├── start.sh
├── stop.sh
├── requirements.txt
└── .env.example
```

## Особенности реализации

- 🐳 Два Docker-контейнера: 
  - `web` - Flask-приложение (порт 5000)
  - `db` - PostgreSQL 13
- 🌐 Пользовательская сеть `app-net` для взаимодействия контейнеров
- 📦 Автоматическое создание БД при первом запуске
- 🔒 Безопасное хранение конфиденциальных данных в `.env`

## Возможные проблемы

### Ошибки прав доступа
```bash
# Для Linux/MacOS
sudo chmod +x *.sh
```

### Занятый порт 5000
Измените порт в:
1. `.env` (FLASK_RUN_PORT)
2. `docker-compose.yml` (ports)

### Миграции базы данных
При необходимости выполните вручную:
```bash
docker exec -it web flask db upgrade
```

## Лицензия
MIT License. Подробнее см. в файле [LICENSE](LICENSE).
```
