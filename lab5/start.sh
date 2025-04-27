#!/bin/bash

set -a 
source .env
set +a

echo "Starting app with DB user: $DB_USER"

# create network
docker network create app-net || true

# launch PostgreSQL
docker run -d --name db \
  --network app-net \
  -e POSTGRES_USER=$DB_USER \
  -e POSTGRES_PASSWORD=$DB_PASSWORD \
  -e POSTGRES_DB=$DB_NAME \
  -v pgdata:/var/lib/postgresql/data \
  postgres:13

echo "Waiting for PostgreSQL to start..."
until docker exec db pg_isready -U $DB_USER -d $DB_NAME > /dev/null 2>&1
do
  sleep 1
done

# building image
docker build -t flask-app .

# run app
docker run -d --name web \
  --network app-net \
  -p 5000:5000 \
  -e SECRET_KEY=$SECRET_KEY \
  -e DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME \
  flask-app

echo "Waiting for web container to start..."
sleep 5

# run migrations
echo "Running database migrations..."
docker exec web flask db upgrade

echo "Application is running on http://localhost:5000"