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

## Question 6: Largest tip

## Question 7: Terraform Workflow