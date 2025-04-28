FROM python:3.12-alpine

# Устанавливаем системные зависимости
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    postgresql-client \
    && rm -rf /var/cache/apk/*

# Создаем пользователя и рабочую директорию
RUN adduser -D appuser && \
    mkdir -p /project && \
    chown -R appuser:appuser /project

WORKDIR /project
USER appuser

# Копируем зависимости
COPY --chown=appuser:appuser requirements.txt .

# Устанавливаем Python-зависимости в домашнюю директорию пользователя
ENV PATH="/home/appuser/.local/bin:${PATH}"
RUN pip install --user --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY --chown=appuser:appuser . .

RUN chmod +x entrypoint.sh

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

EXPOSE 5000

ENTRYPOINT ["/project/entrypoint.sh"]
CMD ["flask", "run"]