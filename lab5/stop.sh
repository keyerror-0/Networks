#!/bin/bash

# stop and delete containers
docker stop web db
docker rm web db

# delete network
docker network rm app-net

# delete tome (optional) if you want to delete your postgres volume
# docker volume rm pgdata

echo "Cleanup complete"