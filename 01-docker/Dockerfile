# base image
FROM python:3.13.11-slim
# use from arg to copy something from a different docker image and put it in our container (/bin) 
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin

# specify the current working directory and copy dependencies
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"
COPY pyproject.toml .python-version uv.lock ./

COPY homework/data data

# install deps from lock file
RUN uv sync --locked

# finally copy our code that could change frequently
# COPY pipeline/pipeline.py pipeline.py
# COPY ingest.py ingest.py
COPY homework/ingest.py ingest.py

# what to do when the container starts => run the pipeline
ENTRYPOINT [ "python", "ingest.py"]
