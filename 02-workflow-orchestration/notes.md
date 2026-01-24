# Workflow Orchestration
Orchestrator (i.e. Kestra, Airflow) ensures independent pieces of our pipeline can work together: code, database, Cloud provider. Supercharges existing data pipelines.
* Provides logging information between the tools
* Can have logic to run things in parallel
* Workflows can be run on a schedule or be event-based

## Building Orchestration Workflow with Kestra
* Kestra is an orchestration platform to manage business-critical workflows. They can be built with code, no code, AI copilot
* Language-agnostic (vs. Airflow, which is Python based)

### Kestra Concepts
* Workflow has a number of tasks.
* Define how the tasks work with properties.
* Pass data between the tasks using outputs.

## Workflow / Task Best Practices (ETL)

### Why do we have a staging table at all?
It's a safe-zone between source and our production tables.

Real-world scenerios we need to consider:
* What happens if something goes wrong halfway through your data transformation or loading process. We'd be able to "restart" the process from the staging table and not the loading step, saving time and compute resources. 
  * Source data can be unpredicatable
    * What if an external API charges per request or we try fetching a file that is now changed or deleted or it's a very large table scan?

* What if you need to apply complex transformations or data quality checks? We should NOT be doing this directly on our production tables. We need to consider whether users are querying the data (complex transformations and analytics on prod tables could slow down their experience). Furthermore, data quality checks need to be done BEFORE data is available to users on production.

* Consider data arriving from external APIs or files - do you trust it implicitly, or might you want to inspect/validate it first?

Without a staging table, we risk corrupting our production data and exposing unvalidated data to downstream consumers.

### To truncate staging table or not?
In a very basic sense, truncating staging tables (i.e. full refresh) keeps things simple and predictable and mirrors the source data at that point in time. Everything, however depends on our requirements.

#### Most Common for Partitioned Data - Delete + Insert
This is typically the best choice when you're working with time-partitioned data (i.e., year/month).
```sql
-- Delete the bad January data
DELETE FROM production WHERE year = 2024 AND month = 1;
-- Insert the corrected January data from staging
INSERT INTO production SELECT * FROM staging;
```
Why this works well:

* Simple and easy to understand
* Idempotent: run it multiple times, same result
* Fast when you have partitions (databases can drop entire partitions efficiently)
* Clean slate - no risk of partial updates or orphaned records

#### What is there are record-level issues with the data that need to be fixed? - Upsert/Merge
```sql
MERGE INTO production p
USING staging s
ON p.trip_id = s.trip_id
WHEN MATCHED THEN 
    UPDATE SET p.fare = s.fare, p.distance = s.distance, ...
WHEN NOT MATCHED THEN
    INSERT VALUES (s.trip_id, s.fare, s.distance, ...);
```
Why this works:
* Updates individual records based on a unique key
* Good when only some records changed, not the whole partition
* Handles both updates and inserts in one operation

When to use it:
* You have reliable unique keys (like trip_id)
* Only some records in a partition need correction
* Deletes are expensive or you need to preserve some columns

Challenges:
* Requires a unique key
* More complex logic
* Can be slower than delete+insert for full partition reprocessing