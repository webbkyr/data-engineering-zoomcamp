# Data Warehouses

Lecure times: 
  * 2/6 @ 2pm

## OLAP vs OLTP

### Online transaction processing
* Backend services grouping sql together and rollback in case one of them fails
* Short, fast updates to the data
* DB design is normalized
* Users are customer facing

### Online analytical processing
* Writing A LOT of data and driving insights for them (i.e. analytics and data science)
* Data is perioditcally refreshed or appended with scheduled, long running batch jobs
* DB design is denormalized for analysis
* Users are data scientists, business analysts, and executives

## What is a Data Warehouse?
It's an OLAP solution. It's used for reporting. It consists of raw data, metadata, and summary.
* BigQuery (GCP), Redshift (AWS)
* Source data is typically written to a staging area before being written to the data warehouse.
* Consumers from the data warehouse can include other data marts
  * For an e-commerce business there can be data marts for purchasing, sales, inventory to gather further insights


## Partitioning vs Clustering
We can partition a large table by a column that will divide the dataset into smaller segements for manageability and data skipping. In BigQuery, if I write a queries like:

```sql
-- Impact of partition
-- Scanning 1.6GB of data
SELECT DISTINCT(VendorID)
FROM taxi-rides-ny.nytaxi.yellow_tripdata_non_partitioned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';

-- Scanning ~106 MB of DATA
-- Paritioned by tpep_pickup_datetime
SELECT DISTINCT(VendorID)
FROM taxi-rides-ny.nytaxi.yellow_tripdata_partitioned #
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';
```
Note the difference in the amount of data scanned in the queries. 

Clustering, on the other hand, organizes data within a partition by sorting the rows based on one or more clustering keys (i.e. tags, user_id). It will group all of those items together, which speeds up reads.

### Criteria for choose one, the other or both
* Partition => cost known up front; filter on aggregation on a single column

* Clustering => better if you need more granularity; if your queries use a lot of filtereing or aggregations against multiple columns; cardinality can be large

### Takeaway
* Use a time unit column for partitioning
* In BQ, tables that are less than 1GB in size don't see significant improvement with partioning and clustering

How do you want to query the data for your use case? Partitioning and clustering will improve performance and optimize costs (if using cloud storage/compute) if you choose the right keys for each.

BigQuery separates storage (Colossus) from compute (Dremel) so it is cost effective.