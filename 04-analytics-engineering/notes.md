# Analytics Engineering

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


dimension 
- attributes of an entity
- customers, vendors, locations