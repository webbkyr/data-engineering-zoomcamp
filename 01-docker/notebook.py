#!/usr/bin/env python
# coding: utf-8

# In[26]:


import pandas as pd


# In[27]:


url_prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
filename = 'yellow_tripdata_2021-01.csv.gz'


# In[28]:


df = pd.read_csv(url_prefix + filename)


# In[29]:


# pandas can't figure out the types consistently (DTypeWarning)
df.head()


# In[30]:


df.dtypes


# In[31]:


# data shape: row count, columns
df.shape


# In[32]:


len(df)


# In[33]:


# investigate the mixed data types from warning
col = df.columns[6]
df[col].apply(type).value_counts()


# In[40]:


# Explicitly define dtype mappings
dtype_mapping = {
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

df = pd.read_csv(url_prefix + filename, dtype=dtype_mapping, parse_dates=dtype_dates)


# In[41]:


df.head()


# In[36]:


from sqlalchemy import create_engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')


# In[37]:


print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))


# In[38]:


df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')


# In[46]:


# create an iterator to load data in batches
from tqdm.auto import tqdm

table_name = 'yellow_taxi_data'
df_iterator = pd.read_csv(
    url_prefix + filename,
    dtype=dtype_mapping,
    parse_dates=dtype_dates,
    iterator=True,
    chunksize=100000
)
counter = 0
first_chunk = True

for chunk in tqdm(df_iterator):
    if first_chunk:
        # create the table schema
        chunk.head(0).to_sql(
            name=table_name,
            con=engine,
            if_exists='replace'
        )
        first_chunk = False
        print('Table created')
    chunk.to_sql(
        name=table_name,
        con=engine,
        if_exists='append'
    )
    counter += len(chunk)
    print(f"Inserted: {len(chunk)}")
print(f"Total rows inserted: {counter}")


# In[ ]:




