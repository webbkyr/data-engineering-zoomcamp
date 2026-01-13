#!/usr/bin/env python
import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

schema_mapping = {
    'VendorID': 'Int64',
    'passenger_count': 'Int64',
    'trip_distance': 'float64',
    'RatecodeID': 'Int64',
    'store_and_fwd_flag': 'string',
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"

}
dtype_dates = ['tpep_pickup_datetime', 'tpep_dropoff_datetime']

def ingest_data(url: str, engine, target_table: str, chunksize: int = 100000):
    # create an iterator to load data in batches
    df_iterator = pd.read_csv(
        url,
        dtype=schema_mapping,
        parse_dates=dtype_dates,
        iterator=True,
        chunksize=chunksize
    )
    counter = 0
    first_chunk = True

    for chunk in tqdm(df_iterator):
        if first_chunk:
            # create the table schema
            chunk.head(0).to_sql(
                name=target_table,
                con=engine,
                if_exists='replace'
            )
            first_chunk = False
            print('Table created')
        chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists='append'
        )
        counter += len(chunk)
        print(f"Inserted: {len(chunk)}\n")
    print(f"Total rows inserted: {counter}")

@click.command
@click.option('--pg-user',      default='root',             help='Postgres username')
@click.option('--pg-password',  default='root',             help='Postgres password')
@click.option('--pg-host',      default='localhost',        help='Postgres hostname')
@click.option('--pg-port',      default='5432',             help='Postgres port')
@click.option('--pg-db',        default='ny_taxi',          help='Postgres database name')
@click.option('--year',         default=2021,   type=int,   help='Year of the source data')
@click.option('--month',        default=1,      type=int,   help='Month of the source data')
@click.option('--chunksize',    default=100000, type=int,   help='Month of the source data')
@click.option('--target-table', default='yellow_taxi_data', help='Target table name')
def main(pg_user, pg_password, pg_host, pg_port, pg_db, year, month, chunksize, target_table):
    engine = create_engine(f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}')
    url_prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    url = f"{url_prefix}/yellow_tripdata_{year:04d}-{month:02d}.csv.gz"

    ingest_data(
        url,
        engine,
        target_table,
        chunksize
    )

if __name__ == "__main__":
    main()



