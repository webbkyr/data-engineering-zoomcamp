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
