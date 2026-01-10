import sys
import pandas as pd

if len(sys.argv) > 1:
    month = int(sys.argv[1])
    print(f"Processing pipeline for date {month}")

    df = pd.DataFrame({"day": [1,2], "num_passengers": [3,4]})
    df['month'] = month
    print(df.head())

    df.to_parquet(f"output_{month}.parquet")
else:
    print(f"Month required.")
    sys.exit(1)


