# From APIs to Warehouses: AI-Assisted Data Ingestion with dlt

## What is dlt?
* dlt hub (data loading tool) is an open-source Python library that automates schema evolution, normalization, and data loading.
* Config-driven
* We can split the process in 3 steps:
    * Define our source (i.e. external rest API) 
    * Build the pipeline; it's an object that facilitates extraction, transformation, loading
    * Run the pipeline (pipeline.run(source))

** Define the source, define the pipeline, run the pipeline. **

## The Traditional Way (no dlt)
OpenLibraryAPI: https://openlibrary.org/dev/docs/api/search

Things to consider when obtaining from an API source:
* what parameters to use for an API
* pagination
* rate limiting
* retries

After receiving the payload
* Transform it in a way to make it compatible with the destination (i.e. nested array values and getting them into a relational database)

## dlt way
* `pipeline.run(source)` which is the equivalent of:
  * `pipeline.extract(source)`
  * `pipeline.normalize()`
  * `pipeline.load()`