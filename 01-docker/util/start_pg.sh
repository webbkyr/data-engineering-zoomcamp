#!/bin/bash

echo "starting postgres in docker"
# the -d flag runs the container in the background
docker run -dit --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18
echo "postgres container started"