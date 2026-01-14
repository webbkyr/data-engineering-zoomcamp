#!/usr/bin/env python
import click
import pandas as pd
from sqlalchemy import create_engine

# Module 1: Homework Ingest.
def ingest_homework_data(engine):
    # Load taxi trips data
    source_file = 'data/green_tripdata_2025-11.parquet'
    destination_table = 'taxi_trips_2025_11'
    print("reading source data file")
    df = pd.read_parquet(source_file)
    print("loading data")
    df.to_sql(name=destination_table, con=engine, if_exists='replace')

    # Load look up table data
    taxi_zones_lkp_file = 'data/taxi_zone_lookup.csv'
    lkp_destination_table = 'taxi_zones_lkp'
    zone_dtypes = {
        'LocationID': 'Int64',
        'Borough': 'string',
        'Zone': 'string',
        'service_zone': 'string'
    }
    print("reading taxi zones lkp file")
    df_zones = pd.read_csv(taxi_zones_lkp_file, dtype=zone_dtypes)
    print("loading lkp data")
    df_zones.to_sql(name=lkp_destination_table, con=engine, if_exists='replace')

@click.command
@click.option('--pg-user',      default='root',             help='Postgres username')
@click.option('--pg-password',  default='root',             help='Postgres password')
@click.option('--pg-host',      default='localhost',        help='Postgres hostname')
@click.option('--pg-port',      default='5432',             help='Postgres port')
@click.option('--pg-db',        default='ny_taxi',          help='Postgres database name')
def main(pg_user, pg_password, pg_host, pg_port, pg_db):
    engine = create_engine(f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}')
    print("ingesting homework data")
    ingest_homework_data(engine)

if __name__ == "__main__":
    main()