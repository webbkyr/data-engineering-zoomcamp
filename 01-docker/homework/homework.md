# Module 1 Homework Responses

## Question 1: Understanding Docker images
* 25.3

## Question 2: Docker networking and compose
Two answers are correct:
* postgres:5432 => defined container_name
* db:5432 => defined service name

## Question 3: Counting short trips
```
SELECT count(*) 
FROM taxi_trips_2025_11 
WHERE (lpep_pickup_datetime between '2025-11-01' and '2025-12-01')
AND trip_distance <= 1

```
* 8007

## Question 4: Longest trip for each day
```
SELECT lpep_pickup_datetime, trip_distance 
FROM taxi_trips_2025_11 
WHERE trip_distance < 100 
ORDER BY trip_distance desc 
LIMIT 1
```
* 2025-11-14

## Question 5: Biggest pickup zone

```
SELECT sum(total_amount),
    zpu."Zone"
FROM taxi_trips_2025_11 t
	JOIN taxi_zones_lkp zpu ON t."PULocationID" = zpu."LocationID"
WHERE DATE(lpep_pickup_datetime) = DATE '2025-11-18'
GROUP BY zpu."Zone"
ORDER BY sum(total_amount) desc
LIMIT 1
```

* East Harlem North


Other option to limit to the 18th
```
lpep_pickup_datetime >= '2025-11-18'
AND lpep_pickup_datetime <  '2025-11-19'
```

Or cast the timestamp to a date
```
lpep_pickup_datetime::date = DATE '2025-11-18'
```

## Question 6: Largest tip
```
SELECT max(tip_amount), zdo."Zone" as dropoff_zone
FROM taxi_trips_2025_11 t
JOIN taxi_zones_lkp zpu ON t."PULocationID" = zpu."LocationID"
JOIN taxi_zones_lkp zdo ON t."DOLocationID" = zdo."LocationID"
WHERE zpu."LocationID" = 74 -- Eastern Harlem North
AND lpep_pickup_datetime >= '2025-11-01'
AND lpep_pickup_datetime <  '2025-12-01'
GROUP BY zdo."Zone"
ORDER BY max(tip_amount) desc
LIMIT 1
```
* Yorkville West

## Question 7: Terraform Workflow