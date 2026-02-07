# Data Warehouses

Lecure times: 
  * 2/6 1.5hr

## OLAP vs OLTP
An [analogy](https://www.reddit.com/r/dataengineering/comments/1ilpzw1/comment/mbz4uax/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button) from Reddit:

>Keeping an eye on the score displayed on the big screen at a cricket stadium (OLAP) is much better than running onto the field to ask the umpire (OLTP) about the score after every ball. 
>
>The umpire’s primary role is to make crucial decisions during the game (process transactions), and while they can provide the score, interrupting them is ofcourse not ideal LOL. The scoreboard (OLAP), which is regularly updated after each ball or over, is a more efficient and non-disruptive way to stay informed.


Another [analogy](https://www.reddit.com/r/dataengineering/comments/1ilpzw1/comment/mbwsdqr/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button):

>A weird analogy might be: looking at the arrivals/departures board at the airport (OLAP) instead of calling the Air Traffic Control tower (OLTP) to get flight statuses.
>
>ATC just needs to be left alone to do their job of conducting traffic (processing transactions), calling ATC (OLTP) WILL get you the answer you need, but it will make things slower for both of you than just looking at the board (OLAP) and it’s unnecessary compared to just waiting a few minutes (or whatever the refresh frequency is for your case) for the next refresh.


### Online transaction processing
* Row optimized
* Backend services grouping sql together and rollback in case one of them fails
* Short, fast updates to the data
* DB design is normalized
* Users are customer facing

### Online analytical processing
* Column optimized
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
* Clustering is best used for high-cardinality columns, filter-heavy queries, or along with partitioning, as it allows BigQuery to skip scanning irrelevant data. 

### Takeaway
* Use a time unit column for partitioning
* In BQ, tables that are less than 1GB in size don't see significant improvement with partioning and clustering

How do you want to query the data for your use case? Partitioning and clustering will improve performance and optimize costs (if using cloud storage/compute) if you choose the right keys for each.

BigQuery separates storage (Colossus) from compute (Dremel) so it is cost effective.

## What's the purpose of using external tables?

* Cost savings: You're not paying for BigQuery storage since the data stays where it is. You only pay for queries.
* Real-time data access: Great when your data is frequently updated elsewhere and you want to query the latest version without constantly reloading it into BigQuery.
* ETL simplification: You can skip the "load" step in your pipeline - just point BigQuery at your data and query it directly. Useful for exploratory analysis before deciding what to actually import.
* Federation: Query data across multiple systems. For example, you could join data in BigQuery tables with data sitting in Cloud Storage CSV files in a single query.

The *tradeoff* is performance - querying external data is typically slower than querying native BigQuery tables since the data isn't optimized in BigQuery's columnar format, and you don't get benefits like partitioning and clustering in the same way.

Common use cases include querying data lakes in Cloud Storage, accessing live data from Google Sheets for quick analysis, or setting up staging areas where raw data lands before being processed into optimized tables.

When running queries, sBigQuery's "bytes processed" metric only counts data read from BigQuery's native storage.

## Links on BG Infrastructure
* https://luminousmen.com/post/bigquery-explained-what-really-happens-when-you-hit-run/
* https://panoply.io/data-warehouse-guide/bigquery-architecture/
* https://research.google/pubs/dremel-interactive-analysis-of-web-scale-datasets-2/

