!#/bin/bash

echo "ingesting ny taxi data"
docker run -it --rm \
  --network=pg-network \
  ny_taxi:1.0.0 \
    --pg-user=root \
    --pg-password=root \
    --pg-host=pgdatabase \
    --pg-port=5432 \
    --pg-db=ny_taxi \
    --target-table=yellow_taxi_trips_2021_2 \
    --year=2021 \
    --month=2 \
    --chunksize=100000

    echo "done"
    