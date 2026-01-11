# Containterization (Docker) and Infrastructure as Code (IaC)

* Modify $PS1 to change the look of terminal prompt. i.e. `$PS1="> "` will change the prompt to `>` with the cursor. 

### Docker
  * Every time we run a container, we run it from a docker image. An instance of the image is created. The container has what is described in the image. It is stateless. When we stop the container, nothing is saved (i.e. installing python).

  * `docker run -it python:3.13.11`
  * add the `rm` argument to automatically delete the container when it exits.

  * python:3.13.11-slim => python is the image name and anything after the colon is the image tag (`3.13.11-slim`).
    * The entrypoint for this image is a python prompt. To overwrite this add `--entrypoint=` arg. So, for bash it would be `--entrypoint=bash`.
      - `docker run -it --entrypoint=bash python:3.13.11-slim`

  * `docker ps -a` to find exited docker containers
  * `docker ps -aq` displays container ids on the current system, whether exited or not
  * Use volume mapping to mount files in a docker container
    * `docker run -it --rm --entrypoint=bash -v $(pwd)/whatever:/app/whatever python:3.13.11-slim`. The left side of the volume argument is the host machine and the right is where we want to map it on the container. 

### Data Pipeline
  * Use `sys.argv` to access command line arguments to our py scripts.
  * Using `pandas` and `pyarrow`, it's better to use a virtual environment for the project rather than `pip` installing packages globally on the host machine.
  * Using `uv` package manager
    * The system version of Python (host machine) is 3.12.1 but we want to create a virtual env for the project. 
    * `pip install uv` (global) Then we can init a virtual env in our project 
    * init the python version we want in our project: `uv unit --python 3.13`
    * Check the version is correct for the project: `uv run python -V` vs the host machine's version (`python -V`).
    * Update interpreter location: select interpreter -> browse for `.venv/bin/python`
    * Run our script using the virtual env: `uv run python pipeline/pipeline.py 12`
### Dockerize the Pipeline
  * add a dockerfile that builds the image
      * See [Dockerfile](01-docker/Dockerfile)
  * Build the image: `docker build -t test:pandas` the `-t` flag tags the image. The name of the image is `test` and the tag is `pandas`. The default tag is `latest` if not provided.
  * Run the pipeline: `docker run -it --rm test:pandas 12` 
  * Using multiple `COPY` commands creates layers and improves caching functionality. 
  * Installing dependencies from `uv.lock` keeps our local and container environments identical -- avoids surprises.
  * Adding the virtual environment to the PATH in the container obviates the need to specify `uv run` on the entrypoint command.
    * `ENV PATH="/app/.venv/bin:$PATH"`: PATH is a system environment variable that tells the shell where to look for executable commands (i.e python, etc.). Here, we are prepending `app/.venv/bin` to the existing `PATH`. Putting it first we use the versions from the virtual environment by default and avoid accidently using system python.
    * If we don't prepend the .venv, our entrypoint command would need to be `ENTRYPOINT ["uv", "run", "python", "pipeline.py"]`

### Running PostgreSQL with Docker

* How to run a containerized version of postgres
```
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18
```
  * `-e` are environment variables
  * `-v` is the volume on our local machine that is managed by Docker. It allows us to persist the data we write to the database. You can inspect the volume with `docker volume inspect ny_taxi_postgres_data`
  * `-p` is port forwarding from host machine to the container, so traffic to `localhost:5432` is forwarded to the running container. 5432 is the default port for postgres. If 5432 is already in use on our host machine, we could map it to a different port: `-p 5433:5432`.
    * We can connect from the host machine `psql -h localhost -p 5432 -U root -d ny_taxi`
  * Connect to db from the project
    * add pgcli as a dev dependency: `uv add --dev pgcli`
    * connect to the db: `uv run pgcli -h localhost -p 5432 -u root -d ny_taxi`

### NY Taxi Dataset and Data Ingestion
  * Install Jupyter: `uv add --dev jupyter` to use a notebook for data analysis, iteration and documentation.
    * start the notebook: `uv run jupyter notebook` 
      * automatically adds a port mapping to the server (i.e. 8888)
      * click the browser link that contains the token to open the notebook