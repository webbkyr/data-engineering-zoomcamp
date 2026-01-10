# Course Notes

## Module 1: Docker, SQL

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
  * Use sys.argv to access command line arguments to our py scripts.
  * Using `pandas` and `pyarrow`, it's better to use a virtual environment for the project rather than `pip` installing packages globally on the host machine.
  * Using `uv` package manager
    * The system version of Python (host machine) is 3.12.1 but we want to create a virtual env for the project. 
    * `pip install uv` (global) Then we can init a virtual env in our project 
    * init the python version we want in our project: `uv unit --python 3.13`
    * Check the version is correct for the project: `uv run python -V` vs the host machine's version (`python -V`).
    * Update interpreter location: select interpreter -> browse for `.venv/bin/python`
    * Run our script using the virtual env: `uv run python pipeline/pipeline.py 12`
  * To Dockerize the pipeline
    * add a dockerfile that builds the image (See Dockerfile and notes)
    * Build the image: `docker build -t test:pandas` the `-t` flag tags the image. The name of the image is `test` and the tag is `pandas`. The default tag is `latest` if not provided.
    * Run the pipeline: `docker run -it --rm test:pandas 12` 
