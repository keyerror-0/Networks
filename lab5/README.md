# URL Storage Application

Веб-приложение для хранения ссылок с использованием Flask и PostgreSQL, развертываемое в Docker-контейнерах.

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
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
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

### Проблема с форматом конца строки (CRLF → LF)
```bash
# Установите dos2unix (если не установлен)
sudo apt-get install dos2unix

# Конвертируйте файл
dos2unix start.sh
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
