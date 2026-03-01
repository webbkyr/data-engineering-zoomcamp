# Data Platforms Notes

## Materialization Strategy

Materialization strategies are really about answering one core question: how should new data relate to what's already in the table? The right choice depends on your data's nature and how it changes over time.

* Full Replacement (create+replace)
    Use this when your query always produces the complete, correct dataset and history doesn't matter. A good example is a simple lookup/reference table (e.g., a list of product categories). Every run just rebuilds the whole thing from scratch.
* Truncate + Insert
    Similar to create+replace in outcome, but instead of dropping and recreating the table (which would lose permissions, metadata, etc.), it empties the table and refills it. Useful when you want a full refresh but need to preserve the table's schema or access controls.
* Delete + Insert (Incremental)
    Instead of refreshing everything, you only touch a specific partition — say, "yesterday's data." This is common for large event tables where reprocessing all historical data every day would be expensive. You identify rows by an incremental_key (like a date column) and only replace that slice.
* Append
    New rows only — nothing is ever updated or deleted. Good for immutable event streams (logs, audit trails, clickstream data) where you know records won't change after they're written.
* Merge
    You have a primary key and records can change. Instead of deleting and reinserting, you match on the key and update existing rows or insert new ones. Classic use case: syncing a source-of-truth CRM or transactional database into your warehouse.
* Time Interval
    A more structured form of incremental loading where the pipeline itself manages the time windows. Useful for backfilling historical data or when you want Bruin to handle "give me data between X and Y" logic automatically.
* SCD2 (Slowly Changing Dimensions)
    This is for when you need to track history of changes, not just the current state. For example, if a user changes their country, SCD2 keeps both the old and new record with validity timestamps. The two variants are:

    * scd2_by_column — triggers a new version when specific column values change
    * scd2_by_time — uses a time-based key to detect new versions

* DDL
    You're not running a SELECT at all — you're defining the table structure explicitly. Useful for creating empty staging tables or tables with very specific configurations that a SELECT can't express.

A good mental model: think about how often data changes, how much of it changes at once, and whether history matters. 

### Real World Examples of Each
* create+replace
    A `dim_countries` table that maps country codes to country names. The source data rarely changes, the dataset is tiny, and you always want the full current list. Just rebuild it every time.

* truncate+insert
    A `daily_exchange_rates` table that your BI tool reads from. You want a full refresh daily, but the table has carefully configured row-level access policies you don't want to lose — so you truncate and refill rather than drop and recreate.

* delete+insert
    A `fct_orders` table partitioned by order_date. Every night you only reprocess yesterday's partition because late-arriving orders might have updated — but you don't want to reprocess 3 years of history. You set incremental_key: order_date and only that partition gets refreshed.

* append
    A `user_clickstream_events` table where every page view or button click is an immutable event. Once a click happened, it happened — there's nothing to update. You just keep adding new events as they come in.

* merge
    A `customers` table synced nightly from your Salesforce CRM. Customers can update their email, phone, or address at any time. You match on customer_id and update the row if anything changed, or insert if it's a new customer.

* time_interval
    A `fct_ad_impressions` table where you need to backfill 2 years of historical ad data from an external API that only lets you query 7 days at a time. Bruin manages the time windows for you, stepping through the range automatically.

* scd2_by_column
    A `dim_employee` table where you need to know what department an employee was in at any point in time for compliance reporting. When someone transfers from Engineering to Marketing, you close the old record and open a new one — so you can always answer "what department was Alice in during Q3 2023?"

* scd2_by_time
    A `dim_product_pricing` table fed by a daily snapshot from your pricing system. You don't explicitly know what changed, but you use the snapshot timestamp as the incremental key — if a new snapshot arrives with different values, a new version of that record is created automatically.

* DDL
    You're setting up a new data pipeline and need an empty `stg_raw_events` staging table with a very specific schema — particular column types, clustering keys, and partitioning — before any data flows into it. You define it once with DDL and other assets write into it downstream.


* Consider: how often data changes, how much of it changes at once, and whether history matters

