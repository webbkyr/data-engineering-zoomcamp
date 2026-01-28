Docker runs Airflow — local venv is just for editing.

```
docker compose up airflow-init
docker compose up

```
This does not conflict with Docker.

VS Code → local .venv → docs only

Docker → actual runtime → real execution

This is exactly how most Airflow teams work.


Local venv + Docker runtime is the sweet spot.