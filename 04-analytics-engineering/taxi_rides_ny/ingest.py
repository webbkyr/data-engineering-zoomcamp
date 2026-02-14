import click
import duckdb
import requests
from pathlib import Path

BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download"

FHV_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv"

def convert_gz_csv_to_parquet(
    con: duckdb.DuckDBPyConnection,
    csv_filename: str,
    csv_filepath: str,
    parquet_filepath: str,
    parquet_filename: str
):
    try:
        print(f"Converting {csv_filename} to Parquet...")

        con.execute(f"""
            COPY (
                SELECT *
                FROM read_csv_auto(
                    '{csv_filepath}',
                    ignore_errors=true,
                    sample_size=-1
                )
            )
            TO '{parquet_filepath}' (FORMAT PARQUET)
        """)

        print(f"Completed {parquet_filename}")

    except Exception as e:
        print(f"Failed converting {csv_filename}: {e}")

    finally:
        if csv_filepath.exists():
            csv_filepath.unlink()

def load_to_duckdb(con: duckdb.DuckDBPyConnection, taxi_type: str):
    print("Connected to db")
    con.execute("CREATE SCHEMA IF NOT EXISTS prod")

    print(f"Loading data")
    con.execute(f"""
        CREATE OR REPLACE TABLE prod.{taxi_type}_tripdata AS
        SELECT * FROM read_parquet('data/{taxi_type}/*.parquet', union_by_name=true)
    """)
    print("Complete")



def download_and_convert_fhv():
    data_dir = Path("data") / "fhv"
    data_dir.mkdir(exist_ok=True, parents=True)
    print("Creating directory at:", data_dir.resolve())
    con = duckdb.connect()

    for month in range(1, 13):
        parquet_filename = f"fhv_tripdata_2019-{month:02d}.parquet"
        parquet_filepath = data_dir / parquet_filename

        if parquet_filepath.exists():
            print(f"Skipping {parquet_filename} (already exists)")
            continue

        csv_gz_filename = f"fhv_tripdata_2019-{month:02d}.csv.gz"
        csv_gz_filepath = data_dir / csv_gz_filename

        url = f"{FHV_URL}/{csv_gz_filename}"
        print(f"Downloading {url}")

        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Write file fully before conversion
        with open(csv_gz_filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        convert_gz_csv_to_parquet(
            con,
            csv_gz_filename,
            csv_gz_filepath,
            parquet_filepath,
            parquet_filename
        )

    con.close()

def download_and_convert_files(taxi_type):
    data_dir = Path("data") / taxi_type
    data_dir.mkdir(exist_ok=True, parents=True)

    for year in [2019, 2020]:
        for month in range(1, 13):
            parquet_filename = f"{taxi_type}_tripdata_{year}-{month:02d}.parquet"
            parquet_filepath = data_dir / parquet_filename

            if parquet_filepath.exists():
                print(f"Skipping {parquet_filename} (already exists)")
                continue

            # Download CSV.gz file
            csv_gz_filename = f"{taxi_type}_tripdata_{year}-{month:02d}.csv.gz"
            csv_gz_filepath = data_dir / csv_gz_filename

            response = requests.get(f"{BASE_URL}/{taxi_type}/{csv_gz_filename}", stream=True)
            response.raise_for_status()

            with open(csv_gz_filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"Converting {csv_gz_filename} to Parquet...")
            con = duckdb.connect()
            con.execute(f"""
                COPY (SELECT * FROM read_csv_auto('{csv_gz_filepath}'))
                TO '{parquet_filepath}' (FORMAT PARQUET)
            """)
            con.close()

            # Remove the CSV.gz file to save space
            csv_gz_filepath.unlink()
            print(f"Completed {parquet_filename}")

def update_gitignore():
    gitignore_path = Path(".gitignore")

    # Read existing content or start with empty string
    content = gitignore_path.read_text() if gitignore_path.exists() else ""

    # Add data/ if not already present
    if 'data/' not in content:
        with open(gitignore_path, 'a') as f:
            f.write('\n# Data directory\ndata/\n' if content else '# Data directory\ndata/\n')

@click.command
@click.argument('taxi_type', nargs=-1, default=['yellow', 'green'])
def main(taxi_type):
    # Update .gitignore to exclude data directory
    update_gitignore()
    con = duckdb.connect("taxi_rides_ny.duckdb")

    # TODO: refactor
    if taxi_type == 'fhv':
        download_and_convert_fhv()
        load_to_duckdb(con, taxi_type)
    else:
        for t in taxi_type:
            print(t)
            download_and_convert_files(t)
            load_to_duckdb(con, t)

    con.close()

if __name__ == "__main__":
    main()