#!/bin/sh

set -e

if [ ! -d "migrations" ]; then
  flask db init
fi

flask db migrate -m "Auto migration"

flask db upgrade

exec "$@"