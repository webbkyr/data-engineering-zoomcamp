# Analytics Engineering

## dbt
dbt (data build tool) is a *transformation* framework for analytics engineering. It's the control plane for your entire analytics development lifecycle. 

It is a powerful tool that lets us transform data that is already inside of our data warehouse using SQL. On top of that, it supports best practices like version control, testing, documentation, and CI/CD.

It:
- Runs SQL models
- Transforms raw data into analytics-ready tables
- Manages dependencies between models
- Tests data quality
- Builds documentation

It does not:
- Extract data from APIs
- Load files into S3
- Trigger pipelines on schedules
- Handle retries across systems

## Kimball Modeling
### Fact Tables (Verbs - What Happened)
* Maps processes
* Definition: Store quantitative data (measures) and foreign keys to dimensions.
* Verb Examples: Purchased, Sold, Shipped, Claimed, Logged, trips
* One row per trip, sale, campaign contribution, application

Key Contents:
Measurements/Metrics: Quantity sold, dollar amount, duration, cost.
Foreign Keys: customer_id, product_id, date_id.
Degenerate Dimensions: Transaction IDs or invoice numbers directly in the table. 
 
### Dimension Tables (Nouns - Who, What, Where, When, Why) 
* Represents attributes of an entity
* Definition: Provide descriptive, textual context to the facts.
* Noun Examples: Customer, Product, Store, Employee, Date, Time, Location, Vendor
Key Contents:
Descriptive Attributes: Customer Name, Product Category, Store City, Product Color.
Primary Key: Unique identifier to link to the fact table. 

## Accomplished in this module
- Setup DuckDB with dev and prod schemas for ny taxi trip data
- Create dbt project for yellow, green, fhv trip data
- Load data into duckdb via python script
- Run model transformation logic on duckdb warehouse
- Ran tests on trip data models
- Setup and gathered insights from final data marts with trip data