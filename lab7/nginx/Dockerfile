FROM nginx:1.27.5-alpine

# Установка зависимостей
RUN apk add --no-cache python3 wget unzip

# Создаем директории
RUN mkdir -p /etc/nginx/geoip && chown -R nginx:nginx /etc/nginx/geoip

# Скачивание и распаковка базы
ARG DATABASE_CODE="DB1-LITE"
ARG TOKEN="ваш_токен"
RUN wget -O /tmp/IP2LOCATION-LITE.zip \
    "https://www.ip2location.com/download/?token=${TOKEN}&file=${DATABASE_CODE}" && \
    unzip -j -o /tmp/IP2LOCATION-LITE.zip "IP2LOCATION-LITE-DB1*.CSV" -d /tmp/ && \
    mv /tmp/IP2LOCATION-LITE-DB1*.CSV /tmp/IP2LOCATION-LITE-DB1.CSV && \
    rm -f /tmp/IP2LOCATION-LITE.zip

# Копирование и запуск скрипта
COPY ip2location-cidr-generator.py /tmp/
RUN chmod +x /tmp/ip2location-cidr-generator.py && \
    python3 /tmp/ip2location-cidr-generator.py && \
    [ -s /etc/nginx/geoip/ru-cidr.txt ] || { echo "CIDR file empty!"; exit 1; }

# Копирование конфигов
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY blocked.html /usr/share/nginx/html/blocked.html

# Фикс прав
RUN chown -R nginx:nginx /etc/nginx/geoip /usr/share/nginx/html