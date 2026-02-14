WITH source AS (
    SELECT * FROM {{ source('raw', 'fhv_tripdata') }}
),
renamed AS (
    SELECT
    -- identifiers
    cast(dispatching_base_num as varchar) as dispatching_base_num,
    cast(Affiliated_base_number as varchar) as affiliated_base_num,
    cast(PUlocationID as integer) as pickup_location_id,
    cast(DOlocationID as integer) as dropoff_location_id,

    -- timestamps
    cast(pickup_datetime as timestamp) as pickup_datetime,
    cast(dropOff_datetime as timestamp) as dropoff_datetime,

    -- trip info
    cast(SR_Flag as integer) as sr_flag

    from source
    where dispatching_base_num is not null
)

SELECT count(*) FROM renamed

-- {% if target.name == 'dev' %}
-- where pickup_datetime >= '2019-01-01' and pickup_datetime < '2019-02-01'
-- {% endif %}