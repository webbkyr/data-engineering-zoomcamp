#!/bin/bash

echo "ingesting Nov. 2025 taxi data and taxi zone lookup"
docker run -it --rm \
  --network=01-docker_default \
  ny_taxi:1.0.0 \
    --pg-user=root \
    --pg-password=root \
    --pg-host=pgdatabase \
    --pg-port=5432 \
    --pg-db=ny_taxi

echo "done"
    