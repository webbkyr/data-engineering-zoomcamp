# Module 3 Homework Responses

## Create external table from GCS

```sql
CREATE OR REPLACE EXTERNAL TABLE `daring-pier-447713-j0.zoomcamp.yellow_taxi_tripdata_2024_ext`
  OPTIONS (
    format = "parquet",
    uris = ['gs://daring-pier-dezoomcamp-hw3-2026/*.parquet']
);
```
## Create table from external table
```sql
CREATE OR REPLACE TABLE `daring-pier-447713-j0.zoomcamp.yellow_taxi_tripdata_2024` AS
  SELECT * FROM `daring-pier-447713-j0.zoomcamp.yellow_taxi_tripdata_2024_ext`;
```

## Question 1. Counting records
What is count of records for the 2024 Yellow Taxi Data?

```sql
SELECT count(*) FROM `daring-pier-447713-j0.zoomcamp.yellow_taxi_tripdata_2024`;
```

* 20,332,093

## Question 2. Data read estimation
Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.

What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

```sql
-- external table
SELECT count(distinct PULocationID) FROM `daring-pier-447713-j0.zoomcamp.yellow_taxi_tripdata_2024_ext`;
```

```sql
-- materialized table
SELECT count(distinct PULocationID) FROM `daring-pier-447713-j0.zoomcamp.yellow_taxi_tripdata_2024`;
```
* 0 MB for the External Table and 155.12 MB for the Materialized Table

## Question 3. Understanding columnar storage
Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery.

```sql
SELECT "PULocationID" from `daring-pier-447713-j0.zoomcamp.yellow_taxi_tripdata_2024`
```
* 155.12MB

Now write a query to retrieve the PULocationID and DOLocationID on the same table.
```sql
SELECT "PULocationID", "DOLocationID" from `daring-pier-447713-j0.zoomcamp.yellow_taxi_tripdata_2024`
```
* 310.24 MB

Why are the estimated number of Bytes different?

* BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.

## Question 4. Counting zero fare trips
How many records have a fare_amount of 0?

```sql
SELECT count(*) from `daring-pier-447713-j0.zoomcamp.yellow_taxi_tripdata_2024_ext` where fare_amount=0;
```
* 8,333

## Question 5. Partitioning and clustering
What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID (Create a new table with this strategy)

```sql
CREATE OR REPLACE TABLE daring-pier-447713-j0.zoomcamp.yellow_taxi_tripdata_2024_partitioned
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM daring-pier-447713-j0.zoomcamp.yellow_taxi_tripdata_2024_ext;

```
* Partition by tpep_dropoff_datetime and Cluster on VendorID

## Question 6. Partition benefits
Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive)

```sql
SELECT count(distinct VendorID)
FROM daring-pier-447713-j0.zoomcamp.yellow_taxi_tripdata_2024
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15'; 

```
310.24 MB

Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values?

```sql
SELECT count(distinct VendorID)
FROM daring-pier-447713-j0.zoomcamp.yellow_taxi_tripdata_2024_partitioned
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15'; 

```
26.84 MB

* 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table

## Question 7. External table storage
Where is the data stored in the External Table you created?

* GCP Bucket

## Question 8. Clustering best practices
It is best practice in Big Query to always cluster your data:

* False

## Question 9. Understanding table scans
No Points: Write a SELECT count(*) query FROM the materialized table you created. How many bytes does it estimate will be read? Why?

```sql
SELECT count(*)
FROM daring-pier-447713-j0.zoomcamp.yellow_taxi_tripdata_2024
```

This results in 0 bytes processed because BigQuery maintains metadata about each table, including the total row count. Therefore, no table data is scanned to return the results of this query. On the other hand, if any columns are specified in the count, BQ would need to scan data (check for NULLs in that column) to return the appropriate results.
