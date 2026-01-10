# base image
FROM python:3.13.11-slim 
# install dependencies
RUN pip install pandas pyarrow
# setup working directory in the container
WORKDIR /app
# source file => destination file
COPY pipeline/pipeline.py pipeline.py

# what to do when the container starts => run the pipeline
ENTRYPOINT ["python", "pipeline.py"]