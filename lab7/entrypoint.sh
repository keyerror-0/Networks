#!/bin/sh

# Wait for DB
until pg_isready -h db -U ${DB_USER} -d ${DB_NAME} > /dev/null 2>&1; do
  echo "Waiting for database connection..."
  sleep 2
done

# Initialize migrations if env.py is missing
if [ ! -f "migrations/env.py" ]; then
  echo "Initializing database migrations..."
  flask db init
fi

# Generate and apply migrations
echo "Generating migrations..."
flask db migrate -m "Auto-generated migration"

echo "Applying migrations..."
flask db upgrade

exec "$@"