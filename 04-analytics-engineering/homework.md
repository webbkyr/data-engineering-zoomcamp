# Module 4 Homework Responses

## Question 1. dbt Lineage and Execution
* int_trips_unioned only

## Question 2. dbt Tests
* dbt will fail the test, returning a non-zero exit code

## Question 3. Counting Records in fct_monthly_zone_revenue
What is the count of records in the fct_monthly_zone_revenue model?

* `12184`

## Question 4. Best Performing Zone for Green Taxis (2020)
Using the fct_monthly_zone_revenue table, find the pickup zone with the highest total revenue (revenue_monthly_total_amount) for Green taxi trips in 2020.
* `East Harlem North`

```sql
SELECT pickup_zone, revenue_monthly_total_amount
FROM prod.fct_monthly_zone_revenue
WHERE service_type = 'Green' AND revenue_month BETWEEN '2020-01-01' and '2020-12-31'
ORDER BY revenue_monthly_total_amount desc
LIMIT 1;
```

## Question 5. Green Taxi Trip Counts (October 2019)
Using the fct_monthly_zone_revenue table, what is the total number of trips (total_monthly_trips) for Green taxis in October 2019?
* `384,624`

```sql
SELECT sum(total_monthly_trips) 
FROM prod.fct_monthly_zone_revenue 
WHERE service_type = 'Green' and revenue_month = '2019-10-01'
```

## Question 6. Build a Staging Model for FHV Data
1. Load FHV trip data for 2019
2. Create a staging model `stg_fhv_tripdata` 
  * Filter out records where dispatching_base_num is null
  * Rename fields to match your project's naming conventions (i.e., `PULocationID` => `pickup_location_id`)

What is the count of records in stg_fhv_tripdata?
* 43,244,693

Ran `dbt -t prod build --select +stg_fhv_tripdata+` and executed query in VSCode.